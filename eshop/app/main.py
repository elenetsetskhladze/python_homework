"""Online shop API — run with:  uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs to try every endpoint.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routers import cart, products
from .seed import seed_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # creates the tables the first time
    with SessionLocal() as db:
        seed_if_empty(db)  # fills the shop with sample products the first time
    yield


app = FastAPI(
    title="Online Shop API",
    description="Course project 1: products, search, filters, reviews and cart.",
    version="1.0.0",
    lifespan=lifespan,
)

# lets a website on another address (e.g. a frontend) call this API
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(products.router)
app.include_router(cart.router)


@app.get("/", tags=["Info"])
def root():
    return {"message": "Online Shop API is running", "docs": "/docs"}
