from typing import Sequence, Tuple, Optional, Any

from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    id: int = Field(nullable=False, primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    products: list["Product"] = Relationship(back_populates="category")

    def __str__(self) -> str:
        return self.name


class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    price: int = Field()
    category_id: int = Field(default=None, foreign_key="category.id")
    category: Category = Relationship(back_populates="products")

# null=True
# default=None
# nullable=True
