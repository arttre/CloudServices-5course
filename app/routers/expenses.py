from fastapi import APIRouter, HTTPException, Depends, status

from app.services.expences import ExpenseService
from app.utils.auth import get_current_user
from app.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=list[ExpenseResponse])
async def get_expenses(
    current_user=Depends(get_current_user)
):
    return await ExpenseService().get_all_expenses(current_user.id)


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    expense: ExpenseCreate,
    current_user=Depends(get_current_user)
):
    return await ExpenseService().add_expense(expense, current_user.id)


@router.get("/{identifier}", response_model=ExpenseResponse)
async def get_expense(
    identifier: int,
    current_user=Depends(get_current_user)
):
    expense = await ExpenseService().get_user_expense_by_id(identifier, current_user.id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.put("/{identifier}", response_model=ExpenseResponse)
async def update_expense(
    identifier: int,
    update_data: ExpenseUpdate,
    current_user=Depends(get_current_user)
):
    updated_expense = await ExpenseService().update_expense(identifier, update_data, current_user.id)
    if not updated_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return updated_expense


@router.delete("/{identifier}")
async def delete_expense(identifier: int, current_user=Depends(get_current_user)):
    success = await ExpenseService().delete_expense(identifier, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return {"message": "Expense deleted successfully"}
