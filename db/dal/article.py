from uuid import UUID
from typing import Optional, List, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article, Category


class ArticleDAL:
    def __init__(self, db: AsyncSession):
        self.db_session = db

    async def create_article(
        self, title: str, text: str, category_id: UUID
    ) -> Article:
        new_article = Article(
            title=title,
            text=text,
            category_id=category_id,
        )
        self.db_session.add(new_article)
        await self.db_session.flush()
        return new_article

    async def update_article(
            self,
            article_id: UUID,
            title: Optional[str] = None,
            text: Optional[str] = None,
            category_id: Optional[UUID] = None
    ) -> Optional[Article]:

        article = await self.db_session.get(Article, article_id)
        if article is None:
            return None
        if title is not None:
            article.title = title
        if text is not None:
            article.text = text
        if category_id is not None:
            article.category_id = category_id
        await self.db_session.flush()

        await self.db_session.refresh(article)

        return article


    async def delete_article(
            self,
            article_id: UUID,
    ) -> Optional[UUID]:
        article = await self.db_session.get(Article, article_id)
        if article is None:
            return None
        article.is_deleted = True
        await self.db_session.flush()
        return article.article_id

    async def get_category_by_id(self, category_id: UUID) -> Optional[Category]:
        return await self.db_session.get(Category, category_id)

    async def get_articles(
            self,
            page_number: int = 1,
            page_size: int = 10,
            category_id: Optional[UUID] = None,
            search: Optional[str] = None,
    ) -> Tuple[List[Article], int]:

        # 1. Собираем список условий (фильтров)
        filters = [Article.is_deleted == False]

        if category_id is not None:
            filters.append(Article.category_id == category_id)

        if search is not None:
            filters.append(Article.title.ilike(f"%{search}%"))

        # 2. Считаем общее количество с учетом фильтров
        count_query = select(func.count()).select_from(Article).where(*filters)
        total_result = await self.db_session.execute(count_query)
        total_count = total_result.scalar_one()

        # 3. Собираем запрос на получение данных
        data_query = (
            select(Article)
            .where(*filters)
            .order_by(Article.created_at.desc())
        )

        # 4. Применяем пагинацию
        offset = (page_number - 1) * page_size
        data_query = data_query.offset(offset).limit(page_size)

        # 5. Выполняем запрос и возвращаем результат
        result = await self.db_session.execute(data_query)
        articles = list(result.scalars().all())

        return articles, total_count