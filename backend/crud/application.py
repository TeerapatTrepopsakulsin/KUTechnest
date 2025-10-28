from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.application import Application, ApplicationStatus
from ..models.post import Post
from ..models.student import Student
from ..schemas.application import ApplicationCreate


def get(db: Session, app_id: int) -> Optional[Application]:
    return db.query(Application).filter(Application.id == app_id).first()


def list_all(db: Session) -> List[Application]:
    return db.query(Application).all()


def list_by_student(db: Session, student_id: int) -> List[Application]:
    return db.query(Application).filter(Application.student_id == student_id).all()


def list_by_company(db: Session, company_id: int) -> List[Application]:
    return (
        db.query(Application)
        .join(Post, Post.id == Application.post_id)
        .filter(Post.company_id == company_id)
        .all()
    )


def create(db: Session, data: ApplicationCreate, student_id: int) -> Optional[Application]:
    """Creates an application; auto-fills data from the student profile if available."""
    exists = (
        db.query(Application)
        .filter(and_(Application.post_id == data.post_id, Application.student_id == student_id))
        .first()
    )
    if exists:
        return None  # already applied

    student = db.query(Student).filter(Student.id == student_id).first()

    app = Application(
        post_id=data.post_id,
        student_id=student_id,
        cover_letter=data.cover_letter or (student.cover_letter_default if student else None),
        resume_url=str(data.resume_url or (student.resume_url if student else None)),
        status=ApplicationStatus.SUBMITTED,
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def set_status(db: Session, app_id: int, new_status: str) -> Optional[Application]:
    app = get(db, app_id)
    if not app:
        return None
    app.status = new_status
    db.commit()
    db.refresh(app)
    return app
