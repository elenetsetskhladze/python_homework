from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Elene!123@localhost:5432/main"

engine = create_engine(DATABASE_URL)