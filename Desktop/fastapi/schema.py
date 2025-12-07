from sqlmodel import SQLModel
from typing import List, Optional

# User Schema...........................
class UserBase(SQLModel):
    username: str
    role: str = "customer"

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int

# Category Schema........................
class CategoryBase(SQLModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryPublic(CategoryBase):
    id: int

# Review Schema............................
class ReviewBase(SQLModel):
    text: str
    rating: int

class ReviewCreate(ReviewBase):
    product_id: int
    # user_id is thken from the authenticated session of the user

class ReviewPublic(ReviewBase):
    id: int
    user: UserPublic

# Product Schema...........................
class ProductBase(SQLModel):
    name: str
    description: str 
    price: float

class ProductCreate(ProductBase):
    category_id: int

class ProductPublic(ProductBase):
    id: int
    category: CategoryPublic
    reviews: List[ReviewPublic]

# To avoid circular imports, we can create specific models for nested data
# that don't have their own nested relationships.

class CategoryPublicWithProducts(CategoryPublic):
    products: List[ProductPublic] = []

class UserPublicWithReviews(UserPublic):
    reviews: List[ReviewPublic] = []

class OrderCreate(SQLModel):
    customer_name: str
    item: str

class OrderResponse(SQLModel):
    id: int
    customer_name: str
    item: str
    status: str

    class Config:
        orm_mode = True