Backend-часть для блога маркетплейса (тестовое задание). 

## 🚀 Стек
- Python 3.12, FastAPI
- PostgreSQL 15, SQLAlchemy (async), Alembic
- MinIO (S3) для хранения изображений
- JWT (cookie-based auth)
- Docker, Docker Compose
- Pytest, httpx (интеграционные тесты)

## 📦 Запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Rost1slavAV/new_marketplace.git
   cd new_marketplace
Создайте .env (пример):

env
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Запустите проект:

bash
docker compose up -d --build
Примените миграции:

bash
docker compose exec app poetry run alembic upgrade head
Откройте Swagger:
👉 http://localhost:8000/docs

✅ Функционал
Аутентификация: Регистрация, логин (JWT в httpOnly cookie), middleware, роли USER/ADMIN.

Категории: CRUD (создание — только админ).

Статьи: CRUD, мягкое удаление (is_deleted), полнотекстовый поиск (tsvector + GIN).

Изображения: Загрузка в MinIO, отдача через прокси-эндпоинт.

🧪 Тесты
bash
docker compose exec app poetry run pytest tests/ -v
(12 интеграционных тестов, покрывающих аутентификацию, роли, статьи, поиск и загрузку картинок).