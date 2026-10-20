from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from api.schemas.article import PaginatedArticles, ArticleResponse
from db.session import get_db
from services.article import get_articles  # Импортируем сервис

article_router = APIRouter()


@article_router.get("/", response_model=PaginatedArticles)
async def get_articles_handler(  # <-- Переименовали в _handler
        page_number: int = 1,
        page_size: int = 10,
        category_id: Optional[UUID] = None,
        search: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
) -> PaginatedArticles:
    # Распаковываем кортеж (список статей и общее количество)
    articles, total_count = await get_articles(
        page_number=page_number,
        page_size=page_size,
        session=db,
        category_id=category_id,
        search=search
    )

    # Преобразуем SQLAlchemy-объекты в Pydantic-схемы
    result_items = [ArticleResponse.model_validate(article) for article in articles]

    return PaginatedArticles(items=result_items, total=total_count)