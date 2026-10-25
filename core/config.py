from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT настройки
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Настройки для Minio (S3)
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "article-images"
    MINIO_SECURE: bool = False
    MINIO_PUBLIC_URL: str = "/article-images"

    model_config = {"env_file": ".env"}


settings = Settings()