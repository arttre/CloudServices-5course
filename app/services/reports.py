from app.repository.expenses import ExpenseRepository


class ReportService:
    def __init__(self):
        self.repo = ExpenseRepository()

    async def generate_monthly_report(self, user_id: int):
        expenses = await self.repo.get_all(user_id)

        categories = {}
        total = 0

        for expense in expenses:
            total += expense.amount
            if expense.category not in categories:
                categories[expense.category] = 0
            categories[expense.category] += expense.amount

        return {"total": total, "categories": categories}
