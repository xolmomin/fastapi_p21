from fastapi import APIRouter
from sqlalchemy import select, or_
from starlette.requests import Request

from apps.models import Product, Category
from config import templates

product_router = APIRouter()


# @product_router.post("/")
# async def read_item(request: Request):
#     data = await request.form()
#     await Product.create(**data)
#     return RedirectResponse('/products')
#

@product_router.get("/", name='product_list')
async def get_all_products(request: Request, category: int = None):
    if category:
        subquery = select(Category.id).where(or_(Category.parent_id == category, Category.id == category))
        products = await Product.filter(Product.category_id.in_(subquery))
    else:
        products = await Product.all()
    categories = await Category.filter(Category.parent_id == None, relationship=Category.subcategories)
    context = {
        'products': products,
        'categories': categories
    }
    return templates.TemplateResponse(request, 'apps/products/product-list.html', context)


@product_router.get("/detail/{slug}", name='product_detail')
async def get_product(request: Request, slug: str):
    product = await Product.get(Product.slug == slug)
    context = {
        'product': product
    }
    return templates.TemplateResponse(request, 'apps/products/product-detail.html', context)
