import bcrypt
from sqlalchemy import String, Boolean, select
from sqlalchemy.orm import mapped_column, Mapped
from starlette.authentication import BaseUser

from apps.models.database import BaseModel, db


class User(BaseModel, BaseUser):
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="False")
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default="False")

    @classmethod
    async def get_user_by_username(cls, username):
        query = select(cls).where(cls.username == username)
        return (await db.execute(query)).scalar()

    async def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())
