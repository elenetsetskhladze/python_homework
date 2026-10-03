from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):

    existing_course = db.query(Course).filter(Course.name == course.name).first()

    if existing_course:
        raise HTTPException(status_code=400, detail="Course already exists")

    new_course = Course(
        name=course.name,
        duration=course.duration
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):

    course_to_delete = db.query(Course).filter(Course.id == course_id).first()

    if not course_to_delete:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course_to_delete)
    db.commit()

