from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from typing import List
from ....core.database import get_db
from ....schemas.student import StudentCreate, StudentResponse
from ....crud import student as crud_student

router = APIRouter()
applications = relationship("Application", back_populates="post", cascade="all, delete-orphan")

@router.get("/", response_model=List[StudentResponse])
async def get_students(db: Session = Depends(get_db)):
    students = crud_student.get_students(db)
    return [StudentResponse.from_orm(student) for student in students]

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud_student.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse.from_orm(student)

@router.post("/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = crud_student.create_student(db, student)
    return StudentResponse.from_orm(db_student)