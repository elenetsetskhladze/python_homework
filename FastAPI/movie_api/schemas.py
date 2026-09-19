from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class MovieCreate(BaseModel):
    title: str
    genre: str
    year: int = Field(gt=0, le=2100)
    rating: float = Field(ge=0, le=10)
    description: Optional[str] = None


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = Field(default=None, gt=0, le=2100)
    rating: Optional[float] = Field(default=None, ge=0, le=10)
    description: Optional[str] = None


class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    year: int
    rating: float
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)