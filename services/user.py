from typing import Optional
from services.email_publisher import publish_welcome_email
from sqlalchemy.ext.asyncio import AsyncSession
from db.dal.user import UserDAL
from api.schemas.user import UserCreate, UserLogin
from db.models import User
from core.security import get_password_hash, verify_password

async def create_user(body: UserCreate, session: AsyncSession) -> Optional[User]:
    user_dal = UserDAL(session)
    existing_user = await user_dal.find_user_by_email(body.email)
    if existing_user is not None:
        return None


    hashed_password = get_password_hash(body.password)
    new_user = await user_dal.create_user(
        name=body.name,
        surname=body.surname,
        email=body.email,
        password=hashed_password,
    )
    await session.commit()

    try:
        await publish_welcome_email(body.email, body.name)
    except Exception as e:
        print(f'Не удалось отправить задачу в RabbitMQ: {e}')
    return new_user


async def authenticate_user(body: UserLogin, session: AsyncSession) -> Optional[User]:
    user_dal = UserDAL(session)
    user = await user_dal.find_user_by_email(body.email)
    if user is None:
        return None
    if not verify_password(body.password, user.password):
        return None
    return user




