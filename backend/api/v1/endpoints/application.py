from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ....core.database import get_db
from ....crud import application as crud_application
from ....crud import post as crud_post
from ....models.application import ApplicationStatus
from ....models.student import Student
from ....schemas.application import (
    ApplicationCreate,
    ApplicationOut,
    ApplicationStatusUpdate,
)

router = APIRouter(prefix="/applications", tags=["Applications"])


# -------------------------------------------------
# Auth placeholder (replace with JWT later)
# -------------------------------------------------
class CurrentUser(BaseModel):
    id: int
    role: str  # "student" | "company" | "admin"
    company_id: Optional[int] = None


def get_current_user():
    """Stub for real authentication dependency."""
    return CurrentUser(id=1, role="student", company_id=None)


# -------------------------------------------------
# Response model for /prefill endpoint
# -------------------------------------------------
class ApplicationPrefillOut(BaseModel):
    student_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    post_title: Optional[str] = None
    company_name: Optional[str] = None


# -------------------------------------------------
# Request model for /apply endpoint
# -------------------------------------------------
class ApplicationApplyIn(BaseModel):
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None


# -------------------------------------------------
# Prefill: student gets auto-filled data before applying
# -------------------------------------------------
@router.get("/prefill/{post_id}", response_model=ApplicationPrefillOut)
async def prefill_application(
    post_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can prefill an application")

    student = db.query(Student).filter(Student.id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    post = crud_post.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return ApplicationPrefillOut(
        student_name=f"{student.firstname or ''} {student.lastname or ''}".strip(),
        email=student.email,
        phone=student.phone,
        resume_url=student.resume_url,
        cover_letter=student.cover_letter_default,
        post_title=post.title,
        company_name=post.company.name if post.company else None,
    )


# -------------------------------------------------
# Apply: student submits an application
# -------------------------------------------------
@router.post("/posts/{post_id}/apply", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
async def apply_to_post(
    post_id: int = Path(..., ge=1),
    post_data: ApplicationApplyIn = Body(...),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can apply")

    post = crud_post.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    student = db.query(Student).filter(Student.id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    cover_letter = post_data.cover_letter or student.cover_letter_default
    resume_url = post_data.resume_url or student.resume_url

    app_data = ApplicationCreate(
        post_id=post_id,
        cover_letter=cover_letter,
        resume_url=resume_url,
    )

    new_app = crud_application.create(db, app_data, student_id=current_user.id)
    if new_app is None:
        raise HTTPException(status_code=400, detail="You have already applied to this post")

    out = ApplicationOut.model_validate(new_app)
    out.post_title = post.title
    out.company_name = post.company.name if post.company else None
    return out


# -------------------------------------------------
# List: applications based on role
# -------------------------------------------------
@router.get("/", response_model=List[ApplicationOut])
async def list_applications(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    role = current_user.role
    if role == "admin":
        apps = crud_application.list_all(db)
    elif role == "student":
        apps = crud_application.list_by_student(db, current_user.id)
    elif role == "company":
        apps = crud_application.list_by_company(db, current_user.company_id)
    else:
        apps = []

    results = []
    for app in apps:
        item = ApplicationOut.model_validate(app)
        item.post_title = app.post.title if app.post else None
        item.company_name = app.post.company.name if app.post and app.post.company else None
        results.append(item)
    return results


# -------------------------------------------------
# Get single application
# -------------------------------------------------
@router.get("/{application_id}", response_model=ApplicationOut)
async def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    app = crud_application.get(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    if current_user.role == "student" and app.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if current_user.role == "company":
        if not app.post or app.post.company_id != current_user.company_id:
            raise HTTPException(status_code=403, detail="Forbidden")

    out = ApplicationOut.model_validate(app)
    out.post_title = app.post.title if app.post else None
    out.company_name = app.post.company.name if app.post and app.post.company else None
    return out


# -------------------------------------------------
# Update application status
# -------------------------------------------------
@router.patch("/{application_id}/status", response_model=ApplicationOut)
async def update_application_status(
    application_id: int,
    update_data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    app = crud_application.get(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    if current_user.role == "student":
        if app.student_id != current_user.id or update_data.status != ApplicationStatus.WITHDRAWN:
            raise HTTPException(status_code=403, detail="Students may only withdraw their own applications")

    if current_user.role == "company":
        if not app.post or app.post.company_id != current_user.company_id:
            raise HTTPException(status_code=403, detail="Forbidden")

    updated = crud_application.set_status(db, application_id, update_data.status)
    out = ApplicationOut.model_validate(updated)
    out.post_title = updated.post.title if updated.post else None
    out.company_name = updated.post.company.name if updated.post and updated.post.company else None
    return out
