import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse

from apps.admin import ProductAdmin, CategoryAdmin, ProductPhotoAdmin
from apps.models import db
from apps.routers import product_router, generate_router, user_router, auth_router
from apps.utils.authentication import AuthBackend
from config import conf


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists('static'):
        os.mkdir('static')

    app.mount("/static", StaticFiles(directory='static'), name='static')
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(product_router)
    app.include_router(generate_router)
    await db.create_all()

    yield


app = FastAPI(docs_url=None, lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=conf.SECRET_KEY)
admin = Admin(app, db._engine, authentication_backend=AuthBackend(conf.SECRET_KEY))
admin.add_view(ProductAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ProductPhotoAdmin)


@app.get("/media/{full_path:path}", name='media')
async def get_media(full_path):
    image_path = Path(f'media/{full_path}')
    if not image_path.is_file():
        return Response("Image not found on the server", status.HTTP_404_NOT_FOUND)
    return FileResponse(image_path)


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
def auth_exception_handler(request: Request, exc):
    return RedirectResponse(request.url_for('login_page'))
