from uuid import UUID

from db.models import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional


class CategoryDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    async def create_category(
            self, name: str, description: str
    ) -> Category:
        new_category = Category(
            name=name,
            description=description,
        )
        self.db_session.add(new_category)
        await self.db_session.flush()
        return new_category

    async def find_category_by_name(self, name: str) -> Optional[Category]:
        result = await self.db_session.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalar_one_or_none()  # ← для ОДНОЙ записи

    async def list_categories(self) -> list[Category]:
        result = await self.db_session.execute(select(Category))
        return list(result.scalars().all())

    async def get_category_by_id(self, category_id: UUID) -> Optional[Category]:
        return await self.db_session.get(Category, category_id)