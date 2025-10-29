from sqlalchemy.orm import Session
from .. import models
from ..schemas.registration import StudentRegistrationRequest, CompanyRegistrationRequest


def register_student(db: Session, user_id: int, student_data: StudentRegistrationRequest):
    """Register a new student profile for a user."""
    # Check if student profile already exists
    existing = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if existing:
        return existing
    if existing:
        return existing

    # Get the user
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # Create student profile
    student = models.Student(
        user_id=user_id,
        name=student_data.name,
        nick_name=student_data.nick_name,
        pronoun=student_data.pronoun,
        age=student_data.age,
        year=student_data.year,
        ku_generation=student_data.ku_generation,
        faculty=student_data.faculty,
        major=student_data.major,
        about_me=student_data.about_me,
        email=user.email  # Use email from user record
    )
    db.add(student)

    # Update user role
    user.role = "student"
    user.status = "approved"

    db.commit()
    db.refresh(student)
    return student


def register_company(db: Session, user_id: int, company_data: CompanyRegistrationRequest):
    """Register a new company profile for a user."""
    # Check if company profile already exists
    existing = db.query(models.Company).filter(models.Company.user_id == user_id).first()
    if existing:
        return existing

    # Get the user
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # Create company profile
    company = models.Company(
        user_id=user_id,
        name=company_data.name,
        website=company_data.website,
        logo_url=company_data.logo_url,
        location=company_data.location,
        description=company_data.description,
        contacts=company_data.contacts
    )
    db.add(company)

    # Update user role
    user.role = "company"
    user.status = "approved"

    db.commit()
    db.refresh(company)
    return company