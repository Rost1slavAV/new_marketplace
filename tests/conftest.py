import os
import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from main import app
from core.config import settings
from db.models import Base
from db.session import get_db
from unittest.mock import patch


test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False
)


TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


@pytest.fixture(autouse=True)
def mock_rabbitmq_publisher():
    """
    Автоматически подменяет функцию отправки в RabbitMQ на заглушку.
    Это позволяет тестам проходить без запущенного брокера.
    """
    with patch("services.email_publisher.publish_welcome_email") as mock:
        yield mock


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def setup_database():
    import subprocess
    import os

    env = os.environ.copy()
    env["DATABASE_URL"] = settings.TEST_DATABASE_URL

    subprocess.run(
        ["alembic", "upgrade", "head"],
        env=env,
        check=True
    )
    yield
    
    await test_engine.dispose()




@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    await test_engine.dispose()



@pytest_asyncio.fixture(autouse=True)
async def clean_tables():
    yield
    async with test_engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE articles, categories, users CASCADE;"))
    # Закрываем соединение сразу после очистки
    await test_engine.dispose()



@pytest.fixture
async def test_user(client: AsyncClient) -> dict:
    """Создает обычного пользователя и возвращает его данные."""
    user_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com",
        "password": "password123"
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
async def auth_client(client: AsyncClient, test_user: dict) -> AsyncClient:
    """Создает НОВЫЙ клиент, логинит обычного пользователя."""
    from httpx import AsyncClient, ASGITransport
    from main import app

    # Создаем отдельный клиент, чтобы не пересекаться с admin_client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login_data = {"email": test_user["email"], "password": test_user["password"]}
        response = await ac.post("/users/login", json=login_data)
        assert response.status_code == 200
        yield ac


@pytest.fixture
async def admin_client(client: AsyncClient) -> AsyncClient:
    """Создает НОВЫЙ клиент, создает админа и логинит его."""
    from httpx import AsyncClient, ASGITransport
    from main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_data = {
            "name": "Admin",
            "surname": "Adminov",
            "email": "admin@example.com",
            "password": "adminpass"
        }
        response = await ac.post("/users/", json=user_data)
        assert response.status_code == 201

        async with TestingSessionLocal() as session:
            await session.execute(
                text("UPDATE users SET role = 'ADMIN' WHERE email = :email"),
                {"email": "admin@example.com"}
            )
            await session.commit()

        login_data = {"email": "admin@example.com", "password": "adminpass"}
        response = await ac.post("/users/login", json=login_data)
        assert response.status_code == 200
        yield ac