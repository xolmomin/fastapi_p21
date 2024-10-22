import bcrypt
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField
from starlette.authentication import BaseUser

from apps.models.database import BaseModel
from config import storage


class User(BaseModel, BaseUser):
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    photo: Mapped[ImageField] = mapped_column(FileType(storage=storage('users/%Y/%m/%d')), nullable=True, doc='1234')
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="False")
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default="False")
    products: Mapped[list['Product']] = relationship('Product', back_populates='owner')

    def __str__(self):
        return super().__str__() + f" - {self.username}"

    async def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())
