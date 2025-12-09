from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: str = Field(default="customer")
    reviews: List["Review"] = Relationship(back_populates="user")  # one user -> many reviews


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    products: List["Product"] = Relationship(back_populates="category")  # one category -> many products


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    price: float
    category_id: int = Field(foreign_key="category.id")
    category: "Category" = Relationship(back_populates="products")  # many products -> one category
    reviews: List["Review"] = Relationship(back_populates="product")  # one product -> many reviews


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    rating: int
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="reviews")  # many reviews -> one user
    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="reviews")  # many reviews -> one product


class ProductOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    item: str
    status: str = Field(default="Order Is Placed")