from sqladmin import ModelView

from apps.models.products import Product, Category


class ProductAdmin(ModelView, model=Product):
    # column_list = [Product.id, Product.name, Product.photo]
    column_list = ['id', 'name', 'get_photo']
    # column_details_exclude_list = ['created_at', 'updated_at']
    form_excluded_columns = ['created_at', 'updated_at']


class CategoryAdmin(ModelView, model=Category):
    column_list = ['id', 'name']
    column_details_list = ['id', 'name']
    form_rules = [
        "name",
    ]

    can_export = False
