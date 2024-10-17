from fastapi_storages.integrations.sqlalchemy import FileType
from slugify import slugify
from sqlalchemy import BigInteger, String, VARCHAR, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import CreatedBaseModel
from config import storage


class Category(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    parent: Mapped['Category'] = relationship('Category', lazy='selectin', remote_side='Category.id',
                                              back_populates='subcategories')
    products: Mapped[list['Product']] = relationship('Product', lazy='selectin', back_populates='category')
    subcategories: Mapped[list['Category']] = relationship('Category', lazy='selectin', back_populates='parent')

    def __str__(self):
        if self.parent is None:
            return self.name
        return f"{self.parent} -> {self.name}"
    #
    # async def async_product_count(self):
    #     query = select(func.count()).select_from(Product).filter(Product.category_id == self.id)
    #     return (await db.execute(query)).scalar()

    # @property
    # def get_products(self):
    #     # Check if there is an active event loop
    #     if asyncio.get_event_loop().is_running():
    #         # If running in an event loop, create a task
    #         return asyncio.run_coroutine_threadsafe(self.async_product_count(), asyncio.get_event_loop()).result()
    #     else:
    #         # If not running in an event loop, use asyncio.run()
    #         async def inner():
    #             return await self.async_product_count()
    #
    #         return self.run_async(inner)


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    discount_price: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, server_default="0")
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', lazy='selectin', back_populates='products')
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    owner: Mapped['User'] = relationship('User', lazy='selectin', back_populates='products')

    photos: Mapped[list['ProductPhoto']] = relationship('ProductPhoto', lazy='selectin', back_populates='product')

    __table_args__ = (
        CheckConstraint('price > discount_price'),
    )

    @classmethod
    async def create(cls, **kwargs):
        _slug = slugify(kwargs['name'])
        while cls.get(cls.slug == _slug) is not None:
            _slug = slugify(kwargs['name'] + '-1')
        kwargs['slug'] = _slug
        return await super().create(**kwargs)


class ProductPhoto(CreatedBaseModel):
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'))
    product: Mapped['Product'] = relationship('Product', lazy='selectin', back_populates='photos')
    photo: Mapped[ImageField] = mapped_column(FileType(storage=storage('products/%Y/%m/%d')))
