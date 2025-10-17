from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    logo_url: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    contacts: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    posts_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True