from sqlalchemy import text
import pytest
from tests.conftest import TestingSessionLocal
from httpx import AsyncClient


@pytest.fixture
async def test_category(admin_client: AsyncClient) -> dict:
    """Создает категорию для статей."""
    response = await admin_client.post("/categories/", json={
        "name": "Технологии",
        "description": "Статьи про IT"
    })
    assert response.status_code == 201
    return response.json()


async def test_create_article_as_admin(admin_client: AsyncClient, test_category: dict):
    """Тест создания статьи админом."""
    response = await admin_client.post("/articles/", json={
        "title": "Как выучить Python",
        "text": "Python - это отличный язык программирования.",
        "category_id": test_category["category_id"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Как выучить Python"
    assert data["category_id"] == test_category["category_id"]


async def test_create_article_as_user(auth_client: AsyncClient, test_category: dict):
    """Тест ошибки при создании статьи обычным пользователем (403)."""
    response = await auth_client.post("/articles/", json={
        "title": "Хакерская статья",
        "text": "Я не админ, но хочу писать.",
        "category_id": test_category["category_id"]
    })
    assert response.status_code == 403


async def test_get_articles(client: AsyncClient, admin_client: AsyncClient, test_category: dict):
    """Тест получения списка статей (доступно всем)."""
    await admin_client.post("/articles/", json={
        "title": "Статья 1",
        "text": "Текст статьи 1",
        "category_id": test_category["category_id"]
    })


    response = await client.get("/articles/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Статья 1"


async def test_article_search(client: AsyncClient, admin_client: AsyncClient, test_category: dict):

    response1 = await admin_client.post("/articles/", json={
        "title": "Купить слона",
        "text": "Огромный слон в зоопарке",
        "category_id": test_category["category_id"]
    })
    assert response1.status_code == 201

    response2 = await admin_client.post("/articles/", json={
        "title": "Продать слона",
        "text": "Слоненок ищет дом",
        "category_id": test_category["category_id"]
    })
    assert response2.status_code == 201

    # 2. Отладочный блок: проверяем, что реально лежит в БД
    async with TestingSessionLocal() as session:
        result = await session.execute(text("SELECT title, search_vector FROM articles"))
        rows = result.fetchall()
        print("\n--- ДАННЫЕ В БД ---")
        for row in rows:
            print(f"Title: {row[0]} | search_vector: {row[1]}")
        print("-------------------\n")


        assert any(row[1] is not None for row in rows), "ОШИБКА: search_vector не заполнен! Триггер не работает."


    response = await client.get("/articles/?search=слон")
    assert response.status_code == 200
    data = response.json()

    print(f"Результат поиска 'слон': {data}")


    assert data["total"] >= 1, "ОШИБКА: Поиск по слову 'слон' не нашел статей."