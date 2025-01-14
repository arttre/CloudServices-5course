from app.schemas import ExpenseCreate
from app.models import Expense
from app.repository.expenses import ExpenseRepository


class ExpenseService:
    def __init__(self):
        self.repo = ExpenseRepository()

    async def get_all_expenses(self, user_id: int):
        return await self.repo.get_all(user_id)

    async def add_expense(self, expense_data: ExpenseCreate, user_id: int):
        new_expense = Expense(
            category=expense_data.category,
            amount=expense_data.amount,
            description=expense_data.description,
            user_id=user_id,
        )
        return await self.repo.create(new_expense)

    async def get_user_expense_by_id(self, expense_id: int, user_id: int):
        return await self.repo.get_by_id(expense_id, user_id)

    async def update_expense(self, expense_id: int, data: dict, user_id: int):
        return await self.repo.update(expense_id, data, user_id)

    async def delete_expense(self, expense_id: int, user_id: int):
        return await self.repo.delete(expense_id, user_id)
