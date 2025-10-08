from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ....core.database import get_db
from ....core.llm import validate_job_post
from ....schemas.post import PostCreate, PostResponse
from ....schemas.enums import WorkField
from ....crud import post as crud_post
from ....crud import company as crud_company

router = APIRouter()

@router.get("/", response_model=dict)
async def get_posts(
    page: int = Query(1, ge=1),
    search: Optional[str] = None,
    work_field: Optional[WorkField] = None,
    location: Optional[str] = None,
    onsite: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    posts, total = crud_post.get_posts(
        db, page=page, search=search, work_field=work_field,
        location=location, onsite=onsite
    )
    
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
    
    return {"count": total, "results": results}

@router.get("/{post_id}", response_model=dict)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud_post.get_post(db, post_id)
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

@router.post("", response_model=dict)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    company = crud_company.get_company(db, post.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    validation_result = validate_job_post(
        title=post.title,
        work_field=post.work_field,
        employment_type=post.employment_type,
        location=post.location,
        salary=post.salary,
        min_year=post.min_year,
        requirement=post.requirement,
        description=post.description,
        long_description=post.long_description
    )

    if not validation_result.is_valid:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Job posting validation failed",
                "reason": validation_result.reason,
                "issues": validation_result.issues,
                "recommendations": validation_result.recommendations,
                "confidence_score": validation_result.confidence_score
            }
        )

    if validation_result.confidence_score < 0.7:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Job posting has low confidence score",
                "reason": validation_result.reason,
                "issues": validation_result.issues,
                "recommendations": validation_result.recommendations,
                "confidence_score": validation_result.confidence_score
            }
        )

    db_post = crud_post.create_post(db, post)

    db_post.company_name = company.name
    db_post.company_logo = company.logo_url
    response_data = PostResponse.model_validate(db_post)

    return {
        "post": response_data.model_dump(),
        "validation": {
            "is_valid": validation_result.is_valid,
            "confidence_score": validation_result.confidence_score,
            "issues": validation_result.issues,
            "recommendations": validation_result.recommendations,
            "reason": validation_result.reason
        }
    }