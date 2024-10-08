# from fastapi import APIRouter
# from starlette.requests import Request
# from starlette.responses import RedirectResponse
#
# from apps.models import Product
#
# product_router = APIRouter(prefix='/products')
#
#
# @product_router.post("/")
# async def read_item(request: Request):
#     data = await request.form()
#     await Product.create(**data)
#     return RedirectResponse('/products')
#
