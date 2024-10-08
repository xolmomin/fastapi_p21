from datetime import timedelta, timezone, datetime
from typing import Union

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from sqladmin.authentication import AuthenticationBackend
from starlette import status
from starlette.requests import Request

from apps.models import User
from config import conf

ALGORITHM = "HS256"

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, conf.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token):
    try:
        payload = jwt.decode(token, conf.SECRET_KEY, algorithms=[ALGORITHM])
        username: dict = payload.get("username")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await User.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


class AuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        user = await User.get_user_by_username(username)
        if user is not None and user.is_superuser and user.is_active and (await user.check_password(password)):
            user_data = {
                "id": user.id,
                "username": user.username or None,
            }
            access_token = create_access_token(user_data)
            request.session.update({"token": access_token, "user": user_data})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.session.get("token")
        try:
            user = await get_current_user(token)
        except Exception as e:
            return False
        return user, True
