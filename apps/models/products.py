from fastapi_storages.integrations.sqlalchemy import FileType
from slugify import slugify
from sqlalchemy import BigInteger, String, VARCHAR, ForeignKey, select, Integer, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import CreatedBaseModel, db
from config import storage


class Category(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')

    def __str__(self):
        return super().__str__() + f" - {self.name}"


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    photo: Mapped[ImageField] = mapped_column(FileType(storage=storage('products/%Y/%m/%d')))
    discount_price: Mapped[int] = mapped_column(Integer, nullable=True)
    # quantity: Mapped[int] = mapped_column(Integer, server_default="0")
    price: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', lazy='selectin', back_populates='products')
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    owner: Mapped['User'] = relationship('User', lazy='selectin', back_populates='products')
    __table_args__ = (
        CheckConstraint('price > discount_price'),
    )

    @classmethod
    async def get_by_slug(cls, slug: str):
        query = select(cls).where(cls.slug == slug)
        return (await db.execute(query)).scalar()

    @classmethod
    async def create(cls, **kwargs):
        _slug = slugify(kwargs['name'])
        while cls.get_by_slug(_slug) is not None:
            _slug = slugify(kwargs['name'] + '-1')
        kwargs['slug'] = _slug
        return await super().create(**kwargs)
