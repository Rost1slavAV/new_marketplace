from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.user import UserCreate, UserResponse, Token, UserLogin
from core.security import create_access_token, get_current_user
from db.models import User
from db.session import get_db
from services.user import create_user, authenticate_user

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse, status_code=201)
async def create_new_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user = await create_user(body=body, session=db)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )
    return UserResponse.model_validate(user)


@user_router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    body: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    user = await authenticate_user(body, db)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800,
    )

    return Token(access_token=access_token, token_type="bearer")


@user_router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)