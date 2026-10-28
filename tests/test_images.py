import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


async def test_upload_image(admin_client: AsyncClient):
    """Тест загрузки изображения (с моком MinIO)."""
    with patch("services.storage.StorageService.upload_image", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = "test-uuid.jpg"

        files = {"file": ("test.jpg", b"fake image content", "image/jpeg")}
        response = await admin_client.post("/images/upload", files=files)

        assert response.status_code == 201
        data = response.json()
        assert data["image_url"] == "/images/test-uuid.jpg"

        mock_upload.assert_called_once()


async def test_upload_non_image(admin_client: AsyncClient):
    """Тест загрузки файла, который не является картинкой."""
    files = {"file": ("test.txt", b"just text", "text/plain")}
    response = await admin_client.post("/images/upload", files=files)
    assert response.status_code == 400