from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ....core.database import get_db
from ....schemas.post import PostCreate, PostResponse
from ....schemas.enums import WorkField
from ....crud import post as crud_post
from ....crud import company as crud_company

router = APIRouter()

@router.get("/", response_model=dict)
async def get_posts(
    page: int = Query(1, ge=1),
    search: Optional[str] = None,
    work_field: Optional[str] = None,
    location: Optional[str] = None,
    onsite: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    # Clean and prepare query parameters
    if location == "remote":
        location = None
        onsite = False

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

@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    company = crud_company.get_company(db, post.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_post = crud_post.create_post(db, post)
    
    response_data = PostResponse.from_orm(db_post)
    response_data.company_name = company.name
    response_data.company_logo = company.logo_url
    
    return response_data