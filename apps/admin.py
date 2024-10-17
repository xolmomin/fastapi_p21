from typing import Any, List

from slugify import slugify
from sqladmin import ModelView
from starlette.requests import Request

from apps.models import Product, Category


class ProductAdmin(ModelView, model=Product):
    # column_list = [Product.id, Product.name, Product.photo]
    column_list = ['id', 'name']
    # column_details_exclude_list = ['created_at', 'updated_at']
    # form_excluded_columns = ['created_at', 'updated_at', 'slug', 'owner']
    form_columns = [
        'category',
        'name',
        'photo',
        'discount_price',
        'price',
        'quantity',
    ]
    name_plural = 'Mahsulotlar'
    name = 'Mahsulot'

    async def insert_model(self, request: Request, data: dict) -> Any:
        data['slug'] = slugify(data['name'])
        data['owner_id'] = request.session['user']['id']
        return await super().insert_model(request, data)


class CategoryAdmin(ModelView, model=Category):
    column_list = ['id', 'name']
    column_details_list = ['id', 'name']
    form_rules = [
        "name",
        "parent"
    ]
    can_export = False
    name_plural = 'Kategoriyalar'
    name = 'Kategoriya'
