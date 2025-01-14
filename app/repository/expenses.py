from sqlalchemy.future import select
from app.models import Expense
from app.schemas import ExpenseUpdate
from app.repository.base import BaseRepository


class ExpenseRepository(BaseRepository):
    async def create(self, expense: Expense):
        async with self as db:
            db.add(expense)
            await db.commit()
            await db.refresh(expense)
            return expense

    async def get_all(self, user_id: int):
        async with self as db:
            result = await db.execute(
                select(Expense).where(Expense.user_id == user_id)
            )
            return result.scalars().all()

    async def get_by_id(self, expense_id: int, user_id: int):
        async with self as db:
            result = await db.execute(
                select(Expense)
                .where(
                    Expense.id == expense_id,
                    Expense.user_id == user_id,
                )
            )
            return result.scalars().first()

    async def update(self, expense_id: int, data: ExpenseUpdate, user_id: int):
        async with self as db:
            result = await db.execute(
                select(Expense).where(
                    Expense.id == expense_id,
                    Expense.user_id == user_id,
                )
            )
            expense = result.scalars().first()
            if expense:
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(expense, key, value)
                await db.commit()
                await db.refresh(expense)
                return expense
            return None

    async def delete(self, expense_id: int, user_id: int):
        async with self as db:
            result = await db.execute(
                select(Expense).where(
                    Expense.id == expense_id,
                    Expense.user_id == user_id,
                )
            )
            expense = result.scalars().first()
            if expense:
                await db.delete(expense)
                await db.commit()
                return True
            return False
