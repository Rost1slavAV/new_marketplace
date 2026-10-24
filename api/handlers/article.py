from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from api.schemas.article import PaginatedArticles, ArticleResponse, ArticleCreate, ArticleUpdate
from core.security import get_current_admin
from db.models import User
from db.session import get_db
from services.article import get_articles, create_article, update_article, delete_article  # Импортируем сервис

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

@article_router.post("/", response_model=ArticleResponse, status_code=201)
async def create_article_handler(
    body: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
) -> ArticleResponse:

    article = await create_article(
        body=body,
        session=db)

    if article is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return ArticleResponse.model_validate(article)

@article_router.patch('/{article_id}', response_model=ArticleResponse, status_code=200)
async def update_article_handler(
        article_id: UUID,
        body: ArticleUpdate,
        db: AsyncSession = Depends(get_db),
        current_admin: User = Depends(get_current_admin)
) -> ArticleResponse:
    updated_article = await update_article(article_id=article_id, body=body, session=db)
    if updated_article is None:
        raise HTTPException(status_code=404, detail="Article or Category not found")
    return ArticleResponse.model_validate(updated_article)


@article_router.delete('/{article_id}', status_code=200)
async def delete_article_handler(
        article_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_admin: User = Depends(get_current_admin)
) -> dict: 

    deleted_id = await delete_article(article_id=article_id, session=db)

    if deleted_id is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return {'status': 'deleted', 'article_id': str(deleted_id)}
