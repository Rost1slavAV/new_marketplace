import pytest
from httpx import AsyncClient

async def test_register_user(client: AsyncClient):
    """Тест успешной регистрации пользователя."""
    response = await client.post("/users/", json={
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "ivan@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "ivan@example.com"
    assert "password" not in data

async def test_register_duplicate_email(client: AsyncClient, test_user: dict):
    """Тест ошибки при регистрации с существующим email."""
    response = await client.post("/users/", json={
        "name": "Test2",
        "surname": "User2",
        "email": test_user["email"],
        "password": "password123"
    })
    assert response.status_code == 400

async def test_login_success(client: AsyncClient, test_user: dict):
    """Тест успешного логина и получения cookie."""
    response = await client.post("/users/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.cookies  

async def test_get_me_unauthorized(client: AsyncClient):
    """Тест доступа к /users/me без авторизации."""
    response = await client.get("/users/me")
    assert response.status_code == 401

async def test_get_me_authorized(auth_client: AsyncClient):
    """Тест доступа к /users/me с авторизацией."""
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    assert "email" in response.json()