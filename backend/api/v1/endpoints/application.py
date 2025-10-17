from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

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

router = APIRouter()

# -------------------------------------------------
# Replace this with your real auth dependency
# -------------------------------------------------
def get_current_user():
    """
    Replace with your actual auth dependency.
    It must return an object with:
      - id (student_id)
      - role ("student" | "company" | "admin")
      - company_id (for company users)
    """
    return None


# -------------------------------------------------
# Prefill: auto-fetch CV and default cover letter
# -------------------------------------------------
@router.get("/applications/prefill/{post_id}", response_model=dict)
async def prefill_application(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user or getattr(current_user, "role", None) != "student":
        raise HTTPException(status_code=403, detail="Only students can prefill an application")

    student = db.query(Student).filter(Student.id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    post = crud_post.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "student_name": f"{student.firstname or ''} {student.lastname or ''}".strip(),
        "email": student.email,
        "phone": student.phone,
        "resume_url": student.resume_url,
        "cover_letter": student.cover_letter_default,
        "post_title": post.title,
        "company_name": post.company.name if post.company else None,
    }


# -------------------------------------------------
# Apply: student submits an application
# -------------------------------------------------
@router.post("/posts/{post_id}/apply", response_model=ApplicationOut, status_code=201)
async def apply_to_post(
    post_id: int = Path(..., ge=1),
    payload: dict = Body(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if getattr(current_user, "role", None) != "student":
        raise HTTPException(status_code=403, detail="Only students can apply")

    post = crud_post.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    student = db.query(Student).filter(Student.id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    cover_letter = (payload or {}).get("cover_letter") or student.cover_letter_default
    resume_url = (payload or {}).get("resume_url") or student.resume_url

    data = ApplicationCreate(post_id=post_id, cover_letter=cover_letter, resume_url=resume_url)
    app = crud_application.create(db, data, student_id=current_user.id)
    if app is None:
        raise HTTPException(status_code=400, detail="You have already applied to this post")

    out = ApplicationOut.model_validate(app)
    out.post_title = post.title
    out.company_name = post.company.name if post.company else None
    return out


# -------------------------------------------------
# List: show applications based on user role
# -------------------------------------------------
@router.get("/applications", response_model=List[ApplicationOut])
async def list_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    role = getattr(current_user, "role", None)
    if role == "admin":
        apps = crud_application.list_all(db)
    elif role == "student":
        apps = crud_application.list_by_student(db, current_user.id)
    elif role == "company":
        company_id = getattr(current_user, "company_id", None)
        apps = crud_application.list_by_company(db, company_id) if company_id else []
    else:
        apps = []

    results = []
    for app in apps:
        item = ApplicationOut.model_validate(app)
        if app.post:
            item.post_title = app.post.title
            item.company_name = app.post.company.name if app.post.company else None
        results.append(item)
    return results


# -------------------------------------------------
# Get a single application
# -------------------------------------------------
@router.get("/applications/{application_id}", response_model=ApplicationOut)
async def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    app = crud_application.get(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    role = getattr(current_user, "role", None)
    if role == "student" and app.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if role == "company":
        if not app.post or getattr(current_user, "company_id", None) != getattr(app.post, "company_id", None):
            raise HTTPException(status_code=403, detail="Forbidden")

    out = ApplicationOut.model_validate(app)
    if app.post:
        out.post_title = app.post.title
        out.company_name = app.post.company.name if app.post.company else None
    return out


# -------------------------------------------------
# Update status
# -------------------------------------------------
@router.patch("/applications/{application_id}/status", response_model=ApplicationOut)
async def set_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    app = crud_application.get(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    role = getattr(current_user, "role", None)
    new_status = data.status

    # Students can only withdraw their own applications
    if role == "student":
        if app.student_id != current_user.id or new_status != ApplicationStatus.WITHDRAWN:
            raise HTTPException(status_code=403, detail="Students may only withdraw their own application")

    # Company users can update only their own post applications
    if role == "company":
        if not app.post or getattr(current_user, "company_id", None) != getattr(app.post, "company_id", None):
            raise HTTPException(status_code=403, detail="Forbidden")

    updated = crud_application.set_status(db, application_id, new_status)
    out = ApplicationOut.model_validate(updated)
    if updated.post:
        out.post_title = updated.post.title
        out.company_name = updated.post.company.name if updated.post.company else None
    return out
