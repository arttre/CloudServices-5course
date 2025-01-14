from sqlalchemy.ext.asyncio import AsyncSession
from app.config import SessionLocal


class BaseRepository:
    def __init__(self):
        self.db = SessionLocal()

    async def __aenter__(self) -> AsyncSession:
        return self.db

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()
