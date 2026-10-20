from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    text: str
    category_id: UUID


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    category_id: Optional[UUID] = None


class ArticleResponse(BaseModel):
    article_id: UUID
    title: str
    text: str
    category_id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    model_config = {"from_attributes": True}


class PaginatedArticles(BaseModel):
    items: list[ArticleResponse]
    total: int
