import time

from fastapi import APIRouter
from starlette.requests import Request
from apps.models import Product, Category, User
generate_router = APIRouter()


@generate_router.get("/generate", name='product_list')
async def get_all_products(request: Request):
    data = {
        'category': Category,
        'user': User
    }
    start = time.time()
    for k, count in dict(request.query_params).items():
        await data[k].generate(int(count))
    end = time.time()
    return {"message": "OK", "spend_time": int(end - start)}
