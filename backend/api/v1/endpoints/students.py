from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas.student import StudentCreate, StudentResponse
from ....crud import student as crud_student

router = APIRouter()

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

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = crud_student.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_student = crud_student.update_student(db, db_student, student)
    return StudentResponse.from_orm(updated_student)
