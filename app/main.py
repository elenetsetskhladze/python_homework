from fastapi import FastAPI
from app.routers import student, course, users

app = FastAPI()

app.include_router(student.router)


app.include_router(course.router)

app.include_router(users.router)

