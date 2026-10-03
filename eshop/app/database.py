"""Database connection (SQLite file: eshop.db)."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Put your real address in an environment variable (or a .env file), not in the code, e.g.
#   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/Online_Shop
# If it is not set, a local SQLite file is used.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eshop.db")

# this option is only needed (and only allowed) for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Gives each request its own database session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
