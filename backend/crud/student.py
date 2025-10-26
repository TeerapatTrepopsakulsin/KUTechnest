from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from ..models.student import Student
from ..schemas.student import StudentCreate

def get_students(db: Session):
    return db.query(Student).all()

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_user_id(db: Session, user_id: int) -> Optional[Student]:
    return db.query(Student).filter(Student.user_id == user_id).first()

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_student_with_user(
    db: Session,
    user_id: int,
    student_data: StudentCreate,
    dob: datetime
):
    db_student = Student(
        user_id=user_id,
        pronoun=student_data.pronoun,
        first_name=student_data.first_name,
        last_name=student_data.last_name,
        student_id=student_data.student_id,
        date_of_birth=dob,
        phone=student_data.phone,
        ku_generation=student_data.ku_generation,
        faculty=student_data.faculty,
        major=student_data.major,
        about_me=student_data.about_me,
        email=student_data.email
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student