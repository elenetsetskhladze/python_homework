"""Products: list with search + filters, detail page, reviews, catalog lists."""
import math
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Products"])


# ---------- helpers ----------
def to_card(p: models.Product) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "image_url": p.image_url,
        "rating": p.rating,
        "review_count": p.review_count,
        "brand": p.brand.name,
        "category": p.category.name,
        "subcategory": p.subcategory.name,
    }


def get_product_or_404(db: Session, product_id: int) -> models.Product:
    product = db.get(models.Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


class SortBy(str, Enum):
    name = "name"
    price_asc = "price_asc"
    price_desc = "price_desc"
    rating = "rating"


# ---------- catalog lists (for the filter sidebar) ----------
@router.get("/categories", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """All categories with their subcategories."""
    stmt = select(models.Category).options(selectinload(models.Category.subcategories))
    return db.scalars(stmt.order_by(models.Category.name)).all()


@router.get("/brands", response_model=list[schemas.BrandOut])
def list_brands(db: Session = Depends(get_db)):
    return db.scalars(select(models.Brand).order_by(models.Brand.name)).all()


# ---------- products ----------
@router.get("/products", response_model=schemas.ProductPage)
def list_products(
    search: str | None = Query(None, description="Search by product name"),
    category_id: int | None = None,
    subcategory_id: int | None = None,
    brand_id: list[int] | None = Query(None, description="One or more brand ids"),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    min_rating: float | None = Query(None, ge=0, le=5, description="Only products rated at least this"),
    sort: SortBy = SortBy.name,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Main page: every product as a card, with search, sidebar filters, sorting and pages."""
    # average rating of each product, computed in the database
    avg = (
        select(models.Review.product_id, func.avg(models.Review.rating).label("avg"))
        .group_by(models.Review.product_id)
        .subquery()
    )
    rating_col = func.coalesce(avg.c.avg, 0)

    stmt = select(models.Product).outerjoin(avg, avg.c.product_id == models.Product.id)

    if search:
        stmt = stmt.where(models.Product.name.ilike(f"%{search.strip()}%"))
    if category_id is not None:
        stmt = stmt.where(models.Product.category_id == category_id)
    if subcategory_id is not None:
        stmt = stmt.where(models.Product.subcategory_id == subcategory_id)
    if brand_id:
        stmt = stmt.where(models.Product.brand_id.in_(brand_id))
    if min_price is not None:
        stmt = stmt.where(models.Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(models.Product.price <= max_price)
    if min_rating is not None:
        stmt = stmt.where(rating_col >= min_rating)

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))

    order = {
        SortBy.name: models.Product.name.asc(),
        SortBy.price_asc: models.Product.price.asc(),
        SortBy.price_desc: models.Product.price.desc(),
        SortBy.rating: rating_col.desc(),
    }[sort]
    stmt = (
        stmt.order_by(order, models.Product.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .options(
            selectinload(models.Product.reviews),
            selectinload(models.Product.brand),
            selectinload(models.Product.category),
            selectinload(models.Product.subcategory),
        )
    )
    products = db.scalars(stmt).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": math.ceil(total / page_size) if total else 0,
        "items": [to_card(p) for p in products],
    }


@router.get("/products/{product_id}", response_model=schemas.ProductDetail)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Detail page: image, short description, price, Details tab and Reviews tab."""
    p = get_product_or_404(db, product_id)
    return {
        **to_card(p),
        "short_description": p.short_description,
        "details": p.details,
        "stock": p.stock,
        "reviews": p.reviews,
    }


@router.post("/products", response_model=schemas.ProductDetail, status_code=201)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product (handy for filling the shop)."""
    sub = db.get(models.Subcategory, data.subcategory_id)
    if sub is None or sub.category_id != data.category_id:
        raise HTTPException(400, "Subcategory does not exist in that category")
    if db.get(models.Brand, data.brand_id) is None:
        raise HTTPException(400, "Brand does not exist")
    product = models.Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return get_product(product.id, db)


# ---------- reviews ----------
@router.get("/products/{product_id}/reviews", response_model=list[schemas.ReviewOut])
def list_reviews(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(db, product_id).reviews


@router.post("/products/{product_id}/reviews", response_model=schemas.ReviewOut, status_code=201)
def add_review(product_id: int, data: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """The review modal: star rating, first + last name, text. Updates the product's rating."""
    get_product_or_404(db, product_id)
    review = models.Review(product_id=product_id, **data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
