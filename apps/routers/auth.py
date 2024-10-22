from fastapi import APIRouter, Depends
from starlette.requests import Request

from apps.utils.authentication import get_current_user
from config import templates

auth_router = APIRouter()


@auth_router.get("/login", name='login_page')
async def login_page(request: Request):
    return templates.TemplateResponse(request, 'apps/auth/login.html')
