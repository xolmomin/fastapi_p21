from fastapi import APIRouter, Depends
from starlette.requests import Request

from apps.utils.authentication import get_current_user
from config import templates

user_router = APIRouter()


@user_router.get("/profile", name='user_profile')
async def user_profile(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(request, 'apps/users/profile.html')
