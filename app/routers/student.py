from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.email == student.email).first()

    if existing_student:
        raise HTTPException(status_code=400, detail="Student already exists")

    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()



