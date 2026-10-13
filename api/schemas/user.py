from uuid import UUID

from pydantic import BaseModel





class UserCreate(BaseModel):
    name:str
    surname:str
    email:str
    password:str


class UserLogin(BaseModel):
    email:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    user_id: UUID
    name:str
    surname:str
    email:str
    is_active:bool

    model_config = {"from_attributes": True}