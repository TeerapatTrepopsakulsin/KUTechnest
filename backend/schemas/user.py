from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .student import StudentResponse
from .company import CompanyResponse


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    google_id: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserRoleResponse(BaseModel):
    role: str
    status: str
    data: StudentResponse | CompanyResponse | None = None

    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class GoogleLoginURLResponse(BaseModel):
    url: str
