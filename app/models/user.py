from datetime import datetime
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    registered_at: Mapped[datetime] = mapped_column(DateTime (timezone=True), server_default=func.now())