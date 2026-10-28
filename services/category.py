from typing import Optional, List

from api.schemas.category import CategoryCreate
from sqlalchemy.ext.asyncio import AsyncSession

from db.dal.category import CategoryDAL
from db.models import Category



async def create_category(body: CategoryCreate, session: AsyncSession) -> Optional[Category]:
    category_dal = CategoryDAL(session)
    existing_category = await category_dal.find_category_by_name(body.name)
    if existing_category is not None:
        return None
    new_category = await category_dal.create_category(
        name=body.name,
        description=body.description,
    )
    await session.commit()
    return new_category

async def get_all_categories(session: AsyncSession) -> List[Category]:
    category_dal = CategoryDAL(session)
    all_categories = await category_dal.list_categories()
    return all_categories