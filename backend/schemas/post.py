from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .enums import WorkField, EmploymentType

class PostBase(BaseModel):
    title: str
    work_field: WorkField = WorkField.OTHER
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    location: str
    onsite: bool = False
    salary: int
    min_year: int
    requirement: str
    description: str = ""
    long_description: Optional[str] = None
    image_url: Optional[str] = None

class PostCreate(PostBase):
    company_id: int

class PostResponse(PostBase):
    id: int
    company_id: int
    company_name: str
    company_logo: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True