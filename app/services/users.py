from app.repository.users import UserRepository
from app.schemas import UserCreate
from app.models import User


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def create_user(self, user_data: UserCreate):
        from app.utils.auth import get_password_hash

        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            password=hashed_password,
            name=user_data.name,
        )
        return await self.repo.create(user)

    async def authenticate_user(self, email: str, password: str):
        from app.utils.auth import verify_password

        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    async def get_user_by_id(self, id_: int):
        return await self.repo.get_by_id(id_)

    async def get_user_by_email(self, email: str):
        return await self.repo.get_by_email(email)
