"""Shapes of the data the API receives and returns (validated by Pydantic)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- catalog ----------
class BrandOut(ORM):
    id: int
    name: str


class SubcategoryOut(ORM):
    id: int
    name: str
    category_id: int


class CategoryOut(ORM):
    id: int
    name: str
    subcategories: list[SubcategoryOut] = []


# ---------- reviews ----------
class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5, description="Stars, 1 to 5")
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1, max_length=2000)


class ReviewOut(ORM):
    id: int
    product_id: int
    first_name: str
    last_name: str
    rating: int
    text: str
    created_at: datetime


# ---------- products ----------
class ProductCard(BaseModel):
    """What a main page card needs: image, name, price, rating (+ filter info)."""

    id: int
    name: str
    price: float
    image_url: str
    rating: float
    review_count: int
    brand: str
    category: str
    subcategory: str


class ProductDetail(ProductCard):
    """Detail page: adds the short description, the Details tab and the Review tab."""

    short_description: str
    details: str
    stock: int
    reviews: list[ReviewOut]


class ProductPage(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int
    items: list[ProductCard]


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    short_description: str = ""
    details: str = ""
    price: float = Field(gt=0)
    image_url: str = ""
    stock: int = Field(default=100, ge=0)
    category_id: int
    subcategory_id: int
    brand_id: int


# ---------- cart ----------
class CartAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1, le=99)


class CartUpdate(BaseModel):
    quantity: int = Field(ge=1, le=99, description="New quantity (use DELETE to remove)")


class CartItemOut(BaseModel):
    product_id: int
    name: str
    image_url: str
    price: float
    rating: float
    review_count: int
    quantity: int
    line_total: float


class CartOut(BaseModel):
    cart_id: str
    items: list[CartItemOut]
    total_items: int
    total_price: float
