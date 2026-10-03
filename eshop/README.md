# Online Shop API (Course Project 1)

Python backend for an online shop, built with FastAPI and SQLite.

## How to run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs**. You can try every endpoint there.
The first start creates `eshop.db` and fills it with 17 sample products and reviews.
To start over, delete `eshop.db`.

Run the tests with `pytest`.

## What each requirement uses

| Requirement from the assignment | Endpoint |
|---|---|
| Main page: all products as cards (image, name, price, rating) | `GET /products` |
| Search by name | `GET /products?search=galaxy` |
| Filter by category / subcategory / brand / price / rating | `GET /products?category_id=1&subcategory_id=2&brand_id=2&min_price=1000&max_price=3000&min_rating=4` |
| Sorting and pages (extra) | `&sort=price_asc` (`name`, `price_asc`, `price_desc`, `rating`), `&page=1&page_size=12` |
| Sidebar lists | `GET /categories` (with subcategories), `GET /brands` |
| Product detail page (image, short description, price, Details, Reviews) | `GET /products/{id}` |
| Review modal (stars, first + last name, text) | `POST /products/{id}/reviews` |
| Add to cart | `POST /cart/items` `{"product_id": 1, "quantity": 1}` |
| Cart page (image, name, rating, price, review count, quantity, total) | `GET /cart` |
| Increase / decrease quantity | `PATCH /cart/items/{product_id}` `{"quantity": 3}` |
| Remove from cart | `DELETE /cart/items/{product_id}` |
| Total price calculated automatically | `total_price` in every cart response |

Extra: `POST /products` adds a product. `DELETE /cart` empties the cart.

A product's rating is the average of its reviews, so it updates on its own when someone adds a review.

Each cart belongs to the `X-Cart-Id` header, so different users get separate carts. If the header is left out, everyone shares the cart called `default`.

## Project structure

```
app/
  main.py        starts the app, creates tables, adds sample data
  database.py    SQLite connection
  models.py      tables: Category, Subcategory, Brand, Product, Review, CartItem
  schemas.py     request/response shapes and validation (e.g. rating must be 1-5)
  seed.py        sample products and reviews
  routers/
    products.py  products, search, filters, categories, brands, reviews
    cart.py      cart
tests/test_api.py
```
