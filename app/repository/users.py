from sqlalchemy.future import select
from app.models import User
from app.repository.base import BaseRepository


class UserRepository(BaseRepository):
    async def create(self, user: User):
        async with self as db:
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    async def get_by_email(self, email: str):
        async with self as db:
            result = await db.execute(select(User).where(User.email == email))
            return result.scalars().first()

    async def get_by_id(self, id_: int):
        async with self as db:
            result = await db.execute(select(User).where(User.id == id_))
            return result.scalars().first()
