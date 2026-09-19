from fastapi import FastAPI
from app.routers import student, subject
from app.models import Student, Subject


app = FastAPI()

app.include_router(student.router)

app.include_router(subject.router)