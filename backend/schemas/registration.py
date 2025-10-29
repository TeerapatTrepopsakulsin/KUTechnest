from pydantic import BaseModel, EmailStr

class StudentRegistrationRequest(BaseModel):
    name: str
    nick_name: str | None = None
    pronoun: str | None = None
    age: int | None = None
    year: int
    ku_generation: int
    faculty: str
    major: str | None = None
    about_me: str | None = None
    email: EmailStr

class CompanyRegistrationRequest(BaseModel):
    name: str
    website: str | None = None
    logo_url: str | None = None
    location: str | None = None
    description: str | None = None
    contacts: str | None = None