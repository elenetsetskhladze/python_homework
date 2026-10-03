"""Database tables."""
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    subcategories: Mapped[list["Subcategory"]] = relationship(back_populates="category")


class Subcategory(Base):
    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped[Category] = relationship(back_populates="subcategories")


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    short_description: Mapped[str] = mapped_column(String(500), default="")
    details: Mapped[str] = mapped_column(Text, default="")  # text for the "Details" tab
    price: Mapped[float] = mapped_column(Float)
    image_url: Mapped[str] = mapped_column(String(500), default="")
    stock: Mapped[int] = mapped_column(Integer, default=100)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id"))
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))

    category: Mapped[Category] = relationship()
    subcategory: Mapped[Subcategory] = relationship()
    brand: Mapped[Brand] = relationship()
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="product", cascade="all, delete-orphan", order_by="Review.created_at.desc()"
    )

    @property
    def review_count(self) -> int:
        return len(self.reviews)

    @property
    def rating(self) -> float:
        """Average of all review ratings, rounded to 1 decimal (0 if no reviews)."""
        if not self.reviews:
            return 0.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    rating: Mapped[int] = mapped_column(Integer)  # 1..5 stars
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    product: Mapped[Product] = relationship(back_populates="reviews")


class CartItem(Base):
    """One row per product in a cart. `cart_id` lets several users have separate carts."""

    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[str] = mapped_column(String(64), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    product: Mapped[Product] = relationship()
