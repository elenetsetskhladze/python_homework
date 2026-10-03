"""Cart: add, change quantity, remove; the total price is always calculated automatically.

Each cart is identified by the `X-Cart-Id` header (any string, e.g. a user name or a random id).
If the header is missing, the shared cart "default" is used.
"""
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .products import get_product_or_404

router = APIRouter(prefix="/cart", tags=["Cart"])


def cart_id_header(x_cart_id: str = Header("default", max_length=64)) -> str:
    return x_cart_id


def build_cart(db: Session, cart_id: str) -> dict:
    items = db.scalars(
        select(models.CartItem).where(models.CartItem.cart_id == cart_id).order_by(models.CartItem.id)
    ).all()
    lines = [
        {
            "product_id": i.product_id,
            "name": i.product.name,
            "image_url": i.product.image_url,
            "price": i.product.price,
            "rating": i.product.rating,
            "review_count": i.product.review_count,
            "quantity": i.quantity,
            "line_total": round(i.product.price * i.quantity, 2),
        }
        for i in items
    ]
    return {
        "cart_id": cart_id,
        "items": lines,
        "total_items": sum(line["quantity"] for line in lines),
        "total_price": round(sum(line["line_total"] for line in lines), 2),
    }


def find_item(db: Session, cart_id: str, product_id: int) -> models.CartItem | None:
    return db.scalar(
        select(models.CartItem).where(
            models.CartItem.cart_id == cart_id, models.CartItem.product_id == product_id
        )
    )


@router.get("", response_model=schemas.CartOut)
def get_cart(cart_id: str = Depends(cart_id_header), db: Session = Depends(get_db)):
    """Cart page: all items with image, name, rating, price, review count, quantity + total."""
    return build_cart(db, cart_id)


@router.post("/items", response_model=schemas.CartOut, status_code=201)
def add_to_cart(
    data: schemas.CartAdd, cart_id: str = Depends(cart_id_header), db: Session = Depends(get_db)
):
    """'Add to cart' button. Adding a product that is already in the cart increases its quantity."""
    product = get_product_or_404(db, data.product_id)
    item = find_item(db, cart_id, data.product_id)
    new_qty = (item.quantity if item else 0) + data.quantity
    if new_qty > product.stock:
        raise HTTPException(400, f"Only {product.stock} in stock")
    if item:
        item.quantity = new_qty
    else:
        db.add(models.CartItem(cart_id=cart_id, product_id=data.product_id, quantity=data.quantity))
    db.commit()
    return build_cart(db, cart_id)


@router.patch("/items/{product_id}", response_model=schemas.CartOut)
def update_quantity(
    product_id: int,
    data: schemas.CartUpdate,
    cart_id: str = Depends(cart_id_header),
    db: Session = Depends(get_db),
):
    """The + / − buttons: set a new quantity for a product in the cart."""
    item = find_item(db, cart_id, product_id)
    if item is None:
        raise HTTPException(404, "This product is not in the cart")
    if data.quantity > item.product.stock:
        raise HTTPException(400, f"Only {item.product.stock} in stock")
    item.quantity = data.quantity
    db.commit()
    return build_cart(db, cart_id)


@router.delete("/items/{product_id}", response_model=schemas.CartOut)
def remove_from_cart(
    product_id: int, cart_id: str = Depends(cart_id_header), db: Session = Depends(get_db)
):
    """Delete button: removes the product from the cart."""
    item = find_item(db, cart_id, product_id)
    if item is None:
        raise HTTPException(404, "This product is not in the cart")
    db.delete(item)
    db.commit()
    return build_cart(db, cart_id)


@router.delete("", response_model=schemas.CartOut)
def clear_cart(cart_id: str = Depends(cart_id_header), db: Session = Depends(get_db)):
    """Empty the whole cart."""
    for item in db.scalars(select(models.CartItem).where(models.CartItem.cart_id == cart_id)):
        db.delete(item)
    db.commit()
    return build_cart(db, cart_id)
