from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional

class ApplicationBase(BaseModel):
    cover_letter: Optional[str] = None
    resume_url: Optional[HttpUrl] = None

class ApplicationCreate(ApplicationBase):
    post_id: int

class ApplicationStatusUpdate(BaseModel):
    status: str  # e.g. "withdrawn", "under_review", etc.

class ApplicationOut(BaseModel):
    id: int
    post_id: int
    student_id: int
    status: str
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # Optional convenience fields for frontend display
    post_title: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True  # for Pydantic v2
        orm_mode = True         # backward compatibility with v1
