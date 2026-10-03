"""Run with:  pytest"""
import os

os.environ["DATABASE_URL"] = "sqlite:///./test_eshop.db"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="module")
def client():
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as c:  # startup creates tables + sample data
        yield c
    engine.dispose()
    os.remove("test_eshop.db")


def test_list_products(client):
    r = client.get("/products")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 17
    card = body["items"][0]
    for key in ("id", "name", "price", "image_url", "rating"):
        assert key in card


def test_search_by_name(client):
    names = [p["name"] for p in client.get("/products", params={"search": "galaxy"}).json()["items"]]
    assert names and all("Galaxy" in n for n in names)


def test_filters(client):
    cats = client.get("/categories").json()
    electronics = next(c for c in cats if c["name"] == "Electronics")
    phones = next(s for s in electronics["subcategories"] if s["name"] == "Phones")
    samsung = next(b for b in client.get("/brands").json() if b["name"] == "Samsung")

    r = client.get("/products", params={
        "category_id": electronics["id"], "subcategory_id": phones["id"],
        "brand_id": samsung["id"], "min_price": 1000, "max_price": 2000,
    }).json()
    assert [p["name"] for p in r["items"]] == ["Galaxy A56"]

    rated = client.get("/products", params={"min_rating": 4.5}).json()["items"]
    assert rated and all(p["rating"] >= 4.5 for p in rated)

    by_price = client.get("/products", params={"sort": "price_desc", "page_size": 100}).json()["items"]
    prices = [p["price"] for p in by_price]
    assert prices == sorted(prices, reverse=True)


def test_detail_and_review(client):
    pid = client.get("/products", params={"search": "KALLAX"}).json()["items"][0]["id"]
    before = client.get(f"/products/{pid}").json()
    assert before["details"] and before["short_description"]

    r = client.post(f"/products/{pid}/reviews",
                    json={"rating": 5, "first_name": "Eka", "last_name": "Meladze", "text": "Nice"})
    assert r.status_code == 201
    after = client.get(f"/products/{pid}").json()
    assert after["review_count"] == before["review_count"] + 1
    assert after["rating"] == 4.0  # (3 + 5) / 2

    bad = client.post(f"/products/{pid}/reviews",
                      json={"rating": 6, "first_name": "A", "last_name": "B", "text": "x"})
    assert bad.status_code == 422
    assert client.get("/products/9999").status_code == 404


def test_cart_flow(client):
    h = {"X-Cart-Id": "test-user"}
    items = client.get("/products", params={"sort": "price_asc"}).json()["items"]
    cheap, other = items[0], items[1]  # 69.0 and 89.0

    client.post("/cart/items", json={"product_id": cheap["id"], "quantity": 2}, headers=h)
    cart = client.post("/cart/items", json={"product_id": other["id"]}, headers=h).json()
    assert cart["total_items"] == 3
    assert cart["total_price"] == round(2 * cheap["price"] + other["price"], 2)

    cart = client.patch(f"/cart/items/{cheap['id']}", json={"quantity": 5}, headers=h).json()
    assert cart["total_price"] == round(5 * cheap["price"] + other["price"], 2)

    cart = client.delete(f"/cart/items/{other['id']}", headers=h).json()
    assert [i["product_id"] for i in cart["items"]] == [cheap["id"]]

    # a different cart id is a separate cart
    assert client.get("/cart", headers={"X-Cart-Id": "someone-else"}).json()["items"] == []

    assert client.delete("/cart", headers=h).json()["total_price"] == 0
