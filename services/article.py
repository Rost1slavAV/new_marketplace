from typing import Optional, Tuple, List
from uuid import UUID

from psycopg.errors import ForeignKeyViolation
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.article import ArticleCreate, ArticleUpdate
from db.dal.article import ArticleDAL
from db.dal.category import CategoryDAL
from db.models import Article


async def create_article(
        body: ArticleCreate, session: AsyncSession
) -> Optional[Article]:
    category_dal = CategoryDAL(session)
    category = await category_dal.get_category_by_id(body.category_id)

    if category is None:
        return None

    article_dal = ArticleDAL(session)
    new_article = await article_dal.create_article(
        title=body.title,
        text=body.text,
        category_id=body.category_id
    )

    return new_article


async def update_article(
        article_id: UUID,
        body: ArticleUpdate,
        session: AsyncSession,
) -> Optional[Article]:

    if body.category_id is not None:
        category_dal = CategoryDAL(session)
        category = await category_dal.get_category_by_id(body.category_id)
        if category is None:
            return None


    article_dal = ArticleDAL(session)
    updated_article = await article_dal.update_article(
        article_id=article_id,
        title=body.title,
        text=body.text,
        category_id=body.category_id,
    )

    return updated_article


async def delete_article(
        article_id: UUID,
        session: AsyncSession,
) -> Optional[UUID]:
    article_dal = ArticleDAL(session)
    deleted_article_id = await article_dal.delete_article(article_id)

    return deleted_article_id


async def get_articles(
    page_number: int,
    page_size: int,
    session: AsyncSession,           # <-- Перенесли сюда
    category_id: Optional[UUID] = None,
    search: Optional[str] = None,
) -> Tuple[List[Article], int]:

    article_dal = ArticleDAL(session)
    articles = await article_dal.get_articles(
        page_number=page_number,
        page_size=page_size,
        category_id=category_id,
        search=search,
    )
    return articles