import uuid
import boto3
import asyncio
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException
from core.config import settings

class StorageService:
    def __init__(self):
        protocol = "https://" if settings.MINIO_SECURE else "http://"
        endpoint = settings.MINIO_ENDPOINT
        if not endpoint.startswith("http"):
            endpoint = f"{protocol}{endpoint}"

        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            region_name='us-east-1'
        )
        self.bucket = settings.MINIO_BUCKET
        self._bucket_checked = False  # <-- ДОБАВЛЕНА ЭТА СТРОКА

    async def _check_bucket(self):
        if not self._bucket_checked:
            # Вызываем синхронный метод в отдельном потоке, чтобы не блокировать event loop
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._ensure_bucket_exists)
            self._bucket_checked = True

    def _ensure_bucket_exists(self):
        """Проверяет наличие бакета и создает его, если его нет."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket)
                    print(f"Бакет {self.bucket} успешно создан.")
                except ClientError as create_error:
                    print(f"Не удалось создать бакет: {create_error}")
            else:
                print(f"Ошибка при проверке бакета: {e}")

    async def upload_image(self, file: UploadFile) -> str:
        await self._check_bucket()
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Разрешены только изображения")

        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        try:
            file_content = await file.read()
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=unique_filename,
                Body=file_content,
                ContentType=file.content_type
            )
            return unique_filename
        except ClientError as e:
            print(f"Ошибка загрузки в MinIO: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")
        finally:
            await file.close()

    async def get_image(self, filename: str):
        """Получает файл из MinIO и возвращает поток для StreamingResponse."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=filename)
            return response['Body'], response['ContentType']
        except ClientError as e:
            if e.response['Error']['Code'] == "NoSuchKey":
                raise HTTPException(status_code=404, detail="Изображение не найдено")
            print(f"Ошибка получения файла из MinIO: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при получении файла")

storage_service = StorageService()