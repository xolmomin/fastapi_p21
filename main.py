from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from apps.admin import ProductAdmin, CategoryAdmin
from apps.models import db
from apps.routers.products import product_router
from apps.utils.authentication import AuthBackend
from config import conf

app = FastAPI(docs_url=None)
app.add_middleware(SessionMiddleware, secret_key=conf.SECRET_KEY)
admin = Admin(app, db._engine, authentication_backend=AuthBackend(conf.SECRET_KEY))
admin.add_view(ProductAdmin)
admin.add_view(CategoryAdmin)

app.mount("/static", StaticFiles(directory='static'), name='static')


@app.on_event("startup")
async def on_startup():
    app.include_router(product_router)
    await db.create_all()


@app.on_event("shutdown")
async def on_startup():
    pass
    # db.drop_all()

# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     context = {
#         'users': users
#     }
#     return templates.TemplateResponse(request, 'user-list.html', context)
#
#
# @app.get("/users/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: int):
#     _user = None
#     for user in users:
#         if user['id'] == id:
#             _user = user
#
#     context = {
#         'user': _user
#     }
#     return templates.TemplateResponse(request, 'user-detail.html', context)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
