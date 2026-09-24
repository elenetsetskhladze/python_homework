from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(225))
    duration: Mapped[int] = mapped_column(Integer)

    students: Mapped[list["Student"]] = relationship("Student", secondary="student_course", back_populates="courses")





