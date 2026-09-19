from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from app.database import Base


student_subject = Table("student_subject", Base.metadata, Column("student_id", ForeignKey("students.id"), primary_key=True), Column("subject_id", ForeignKey("subjects.id"), primary_key=True), Column("joined_at", DateTime, default=datetime.utcnow))



class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    students = relationship("Student", secondary=student_subject, back_populates="subjects")