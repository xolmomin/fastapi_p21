from typing import Any

from slugify import slugify
from sqladmin import ModelView
from starlette.requests import Request

from apps.models import Product, Category


class ProductAdmin(ModelView, model=Product):
    # column_list = [Product.id, Product.name, Product.photo]
    column_list = ['id', 'name']
    # column_details_exclude_list = ['created_at', 'updated_at']
    form_excluded_columns = ['created_at', 'updated_at', 'slug']

    async def insert_model(self, request: Request, data: dict) -> Any:
        data['slug'] = slugify(data['name'])
        data['owner_id'] = request.session['user']['id']
        return await super().insert_model(request, data)


class CategoryAdmin(ModelView, model=Category):
    column_list = ['id', 'name']
    column_details_list = ['id', 'name']
    form_rules = [
        "name",
    ]

    can_export = False
