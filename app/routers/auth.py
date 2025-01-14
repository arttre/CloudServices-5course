import os
from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions import (
    IncorrectCredentialsException,
    UserAlreadyExistsException,
)
from app.utils.auth import create_access_token
from app.services.users import UserService
from app.schemas import UserCreate, UserCreateResponse, Token


router = APIRouter(prefix="/auth", tags=["users"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    user_service = UserService()
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise IncorrectCredentialsException
    # access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserCreateResponse)
async def register_user(
    user: UserCreate
) -> dict:
    user_service = UserService()
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise UserAlreadyExistsException

    new_user = await user_service.create_user(user)

    return {
        "name": new_user.name,
        "email": new_user.email,
    }
