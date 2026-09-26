from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=10, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    confirm_password: str = Field(min_length=8, max_length=50)


    @model_validator(mode="before")
    def password_match(cls, value):
        password = value.get("password")
        confirm_password = value.get("confirm_password")
        if password != confirm_password:
            raise ValueError("Passwords don't match")

        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=8, max_length=50)






