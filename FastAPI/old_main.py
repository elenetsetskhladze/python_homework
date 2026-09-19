from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

app = FastAPI()

movies = [
    {
        "id": 1,
        "title": "The Matrix",
        "genre": "sci-fi",
        "year": 1999,
        "rating": 8.7
    },

    {
        "id": 2,
        "title": "Inception",
        "genre": "sci-fi",
        "year": 2010,
        "rating": 8.8
    },

    {
        "id": 3,
        "title": "The Dark Knight",
        "genre": "action",
        "year": 2008,
        "rating": 9.0
    },

    {
        "id": 4,
        "title": "Forrest Gump",
        "genre": "drama",
        "year": 1994,
        "rating": 8.8
    },

    {
        "id": 5,
        "title": "The Hangover",
        "genre": "comedy",
        "year": 2009,
        "rating": 7.7
    },

    {
        "id": 6,
        "title": "Interstellar",
        "genre": "sci-fi",
        "year": 2014,
        "rating": 8.7
    },

    {
        "id": 7,
        "title": "Parasite",
        "genre": "drama",
        "year": 2019,
        "rating": 8.5
    },

    {
        "id": 8,
        "title": "Barbie",
        "genre": "comedy",
        "year": 2023,
        "rating": 6.8
    }
]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):

    for movie in movies:
        if movie["id"] == movie_id:
            return movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )


@app.get("/movies")
def get_movies(genre: str | None = None, year: int | None = None, min_raiting: float | None = None, search: str | None = None):
    result = movies

    if genre is not None:
        result = [movie for movie in result
                  if movie["genre"].lower() == genre.lower()]


    if year is not None:
        result = [movie for movie in result
                  if movie["year"] == year]


    if min_raiting is not None:
        result =[ movie for movie in result
                 if movie["raiting"] >= min_raiting]

    if search is not None:
        result =[ movie for movie in result
                 if search.lower() in movie["title"].lower()]

    return result


class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    discount_price: float | None = None
    quantity: int = Field(ge=0)
    category: str
    sku: str = Field(min_length=5, max_length=20)
    email: EmailStr
    stock: bool = True

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str):
        return value.strip()

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: str):
        if " " in value:
            raise ValueError("SKU must not contain spaces")

        return value.upper()

    @model_validator(mode="after")
    def validate_discount_price(self):
        if self.discount_price is not None:
            if self.discount_price >= self.price:
                raise ValueError("discount_price must be less than price")

        return self


class ProductResponse(BaseModel):
    name: str
    price: float
    discount_price: float | None = None
    quantity: int
    category: str
    stock: bool


@app.get("/products", response_model=list[ProductResponse])
def get_products():
    return [
        {
            "name": "MacBook Pro",
            "price": 3000,
            "discount_price": 2700,
            "quantity": 10,
            "category": "Laptop",
            "sku": "MAC-123",
            "email": "supplier@gmail.com",
            "stock": True
        }
    ]


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    return {
        "name": "MacBook Pro",
        "price": 3000,
        "discount_price": 2700,
        "quantity": 10,
        "category": "Laptop",
        "sku": "MAC-123",
        "email": "supplier@gmail.com",
        "stock": True
    }


@app.post("/products", response_model=ProductResponse)
def create_product(product: Product):
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: Product):
    return product


@app.patch("/products/{product_id}", response_model=ProductResponse)
def patch_product(product_id: int, product: Product):
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {"message": "Product deleted"}

        


