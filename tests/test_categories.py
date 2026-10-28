import pytest
from httpx import AsyncClient


async def test_get_categories_empty(client: AsyncClient):
    """
    Проверяет, что GET /categories/ возвращает пустой список,
    когда в базе нет ни одной категории.
    """
    response = await client.get("/categories/")


    assert response.status_code == 200
    assert response.json() == []