from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import os
from enum import Enum

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(title="KUTechnest API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Enums
class WorkField(str, Enum):
    IT_SUPPORT = "it-support"
    CLOUD = "cloud"
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    DEVOPS = "devops"
    QA = "qa"
    MOBILE = "mobile"
    DATA_ANALYST = "data-analyst"
    DATA_ENGINEER = "data-engineer"
    DATA_SCIENTIST = "data-scientist"
    AI_ML = "ai-ml"
    SECURITY = "security"
    NETWORK = "network"
    SYSADMIN = "sysadmin"
    DATABASE = "database"
    UI_UX = "ui-ux"
    PRODUCT_DESIGN = "product-designer"
    GAME_DEV = "game-dev"
    EMBEDDED = "embedded"
    OTHER = "other"

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    contacts = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="company")
    posts = relationship("Post", back_populates="company")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=True)
    nick_name = Column(String, nullable=True)
    pronoun = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    year = Column(Integer)
    ku_generation = Column(Integer)
    faculty = Column(String)
    major = Column(String, nullable=True)
    about_me = Column(Text, nullable=True)
    email = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="student")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String, index=True)
    work_field = Column(String, default=WorkField.OTHER)
    employment_type = Column(String, default=EmploymentType.FULL_TIME)
    location = Column(String)
    onsite = Column(Boolean, default=False)
    salary = Column(Integer)
    min_year = Column(Integer)
    requirement = Column(Text)
    description = Column(String, default="")
    long_description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="posts")

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
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

# API Routes
@app.get("/")
async def root():
    return {"message": "KUTechnest API"}

# Posts endpoints
@app.get("/api/posts/", response_model=dict)
async def get_posts(
    page: int = Query(1, ge=1),
    search: Optional[str] = None,
    work_field: Optional[WorkField] = None,
    location: Optional[str] = None,
    onsite: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    page_size = 12
    offset = (page - 1) * page_size
    
    query = db.query(Post).join(Company)
    
    if search:
        query = query.filter(
            Post.title.contains(search) |
            Post.description.contains(search) |
            Company.name.contains(search)
        )
    
    if work_field:
        query = query.filter(Post.work_field == work_field)
    
    if location:
        query = query.filter(Post.location == location)
    
    if onsite is not None:
        query = query.filter(Post.onsite == onsite)
    
    total = query.count()
    posts = query.order_by(Post.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Format response
    results = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "company_name": post.company.name,
            "work_field": post.work_field,
            "employment_type": post.employment_type,
            "location": post.location,
            "onsite": post.onsite,
            "salary": f"{post.salary:,}",
            "min_year": post.min_year,
            "requirement": post.requirement,
            "description": post.description,
            "image_url": post.image_url or post.company.logo_url,
            "created_at": post.created_at,
            "updated_at": post.updated_at
        }
        results.append(post_dict)
    
    return {
        "count": total,
        "results": results
    }

@app.get("/api/posts/{post_id}", response_model=dict)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).join(Company).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "id": post.id,
        "title": post.title,
        "company_name": post.company.name,
        "company_logo": post.company.logo_url,
        "work_field": post.work_field,
        "employment_type": post.employment_type,
        "location": post.location,
        "onsite": post.onsite,
        "salary": f"{post.salary:,}",
        "min_year": post.min_year,
        "requirement": post.requirement,
        "description": post.description,
        "long_description": post.long_description,
        "image_url": post.image_url or post.company.logo_url,
        "created_at": post.created_at,
        "updated_at": post.updated_at
    }

@app.post("/api/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Verify company exists
    company = db.query(Company).filter(Company.id == post.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Add company name for response
    response_data = PostResponse.from_orm(db_post)
    response_data.company_name = company.name
    response_data.company_logo = company.logo_url
    
    return response_data

# Companies endpoints
@app.get("/api/companies/", response_model=List[CompanyResponse])
async def get_companies(
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Company)
    
    if search:
        query = query.filter(
            Company.name.contains(search) |
            Company.location.contains(search)
        )
    
    companies = query.all()
    
    # Add posts count
    result = []
    for company in companies:
        company_dict = CompanyResponse.from_orm(company)
        company_dict.posts_count = len(company.posts)
        result.append(company_dict)
    
    return result

@app.get("/api/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    response = CompanyResponse.from_orm(company)
    response.posts_count = len(company.posts)
    return response

@app.post("/api/companies/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    response = CompanyResponse.from_orm(db_company)
    response.posts_count = 0
    return response

# Students endpoints
@app.get("/api/students/", response_model=List[StudentResponse])
async def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [StudentResponse.from_orm(student) for student in students]

@app.get("/api/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse.from_orm(student)

@app.post("/api/students/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return StudentResponse.from_orm(db_student)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)