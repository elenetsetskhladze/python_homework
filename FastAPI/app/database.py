from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


database_url = "postgresql://postgres:Elene!123@localhost:5432/homework42"

engine = create_engine(database_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass
