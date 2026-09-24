from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    duration: int


class CourseResponse(BaseModel):
    id: int
    name: str
    duration: int

