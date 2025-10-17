from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: Optional[str] = None
    nick_name: Optional[str] = None
    pronoun: Optional[str] = None
    age: Optional[int] = None
    year: int
    ku_generation: int
    faculty: str
    major: Optional[str] = None
    about_me: Optional[str] = None
    email: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True