from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas.student import StudentCreate, StudentResponse
from ....crud import student as crud_student
from ....utils.auth import get_current_user
from ....models.user import User
from datetime import datetime

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

@router.post("/register", response_model=StudentResponse)
async def register_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_student = crud_student.get_student_by_user_id(db, current_user.id)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student profile already exists")

    try:
        dob = datetime.strptime(student_data.dob, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    db_student = crud_student.create_student_with_user(
        db=db,
        user_id=current_user.id,
        student_data=student_data,
        dob=dob
    )
    return StudentResponse.from_orm(db_student)

@router.post("/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = crud_student.create_student(db, student)
    return StudentResponse.from_orm(db_student)