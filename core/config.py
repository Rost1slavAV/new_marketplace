from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Настройки основной БД
    DATABASE_URL: str

    # Настройки тестовой БД
    TEST_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/marketplace_test"

    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "article-images"
    MINIO_SECURE: bool = False

    model_config = {"env_file": ".env"}


settings = Settings()