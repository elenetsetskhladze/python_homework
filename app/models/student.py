from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped,  mapped_column
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)

    courses: Mapped[list["Course"]] = relationship("Course", secondary="student_course", back_populates="students")
