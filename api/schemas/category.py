from uuid import UUID

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryResponse(BaseModel):
    category_id: UUID
    name: str
    description: str

    model_config = {'from_attributes': True}