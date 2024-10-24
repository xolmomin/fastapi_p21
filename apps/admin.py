from typing import Any

from slugify import slugify
from sqladmin import ModelView
from sqlalchemy import Select
from starlette.requests import Request

from apps.models import Product, Category
from apps.models.products import ProductPhoto


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


class ProductAdmin(ModelView, model=Product):
    # column_list = [Product.id, Product.name, Product.photo]
    column_labels = dict(id="ID", name="Nomi", price="Narxi")
    column_formatters = {Product.price: lambda obj, a: f"${obj.price}"}
    column_list = ['id', 'name', 'price']
    column_searchable_list = [Product.name]
    # column_details_exclude_list = ['created_at', 'updated_at']
    # form_excluded_columns = ['created_at', 'updated_at', 'slug', 'owner']
    form_columns = [
        'category',
        'name',
        'discount_price',
        'description',
        'price',
        'currency',
        'quantity',
    ]
    name_plural = 'Mahsulotlar'
    name = 'Mahsulot'


    async def insert_model(self, request: Request, data: dict) -> Any:
        data['slug'] = slugify(data['name'])
        data['owner_id'] = request.session['user']['id']
        return await super().insert_model(request, data)


class ProductPhotoAdmin(ModelView, model=ProductPhoto):
    # column_list = ['id', 'name']
    column_details_list = ['id', 'name']
    # form_rules = [
    #     "name",
    #     "parent"
    # ]
    form_excluded_columns = ['created_at', 'updated_at']
    can_export = False
