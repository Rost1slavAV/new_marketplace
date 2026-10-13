from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.schemas.category import CategoryCreate, CategoryResponse
from db.session import get_db
from services.category import create_category, get_all_categories


category_router = APIRouter()


@category_router.post("/", response_model=CategoryResponse, status_code=201)
async def create_new_category(
    body: CategoryCreate,
    db: AsyncSession = Depends(get_db),
) -> CategoryResponse:
    category = await create_category(body=body, session=db)
    if category is None:
        raise HTTPException(
            status_code=400,
            detail="Category already exists",
        )
    return CategoryResponse.model_validate(category)


@category_router.get("/", response_model=List[CategoryResponse])
async def get_all_categories_handler(
    db: AsyncSession = Depends(get_db),
) -> List[CategoryResponse]:
    categories = await get_all_categories(session=db)
    return [CategoryResponse.model_validate(cat) for cat in categories]