from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from apps.admin import ProductAdmin, CategoryAdmin
from apps.models import db
from apps.utils.authentication import AuthBackend
from config import conf

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=conf.SECRET_KEY)
admin = Admin(app, db._engine, authentication_backend=AuthBackend(conf.SECRET_KEY))
admin.add_view(ProductAdmin)
admin.add_view(CategoryAdmin)

app.mount("/static", StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

users = [
    {
        "id": 1,
        "full_name": "Botirjon",
        "position": "Frontend developer",
        "projects": 45,
        "tasks": 15,
        "completed_projects": 6,
        "followers": 76
    },
    {
        "id": 2,
        "full_name": "Gayratjon",
        "position": "Backend engineer",
        "projects": 435,
        "tasks": 154,
        "completed_projects": 66,
        "followers": 7
    },
    {
        "id": 3,
        "full_name": "Nadia Carmichael",
        "position": "Lead Developer",
        "projects": 2,
        "tasks": 64,
        "completed_projects": 16,
        "followers": 842
    },
]


@app.on_event("startup")
async def on_startup():
    await db.create_all()


@app.on_event("shutdown")
async def on_startup():
    pass
    # db.drop_all()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    context = {
        'users': users
    }
    return templates.TemplateResponse(request, 'user-list.html', context)


@app.get("/users/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    _user = None
    for user in users:
        if user['id'] == id:
            _user = user

    context = {
        'user': _user
    }
    return templates.TemplateResponse(request, 'user-detail.html', context)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
