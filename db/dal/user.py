from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, name:str, surname:str, email:str, password:str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


    async def find_user_by_email(
            self, email:str
    ) -> User:
        result = await self.db_session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()