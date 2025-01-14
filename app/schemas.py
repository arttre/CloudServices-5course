from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserCreateResponse(BaseModel):
    email: EmailStr
    name: str


class ExpenseBase(BaseModel):
    category: str
    amount: float
    description: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    date: datetime
