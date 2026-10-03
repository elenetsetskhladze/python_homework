from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    First_name: str
    Last_name: str
    email: EmailStr

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True



