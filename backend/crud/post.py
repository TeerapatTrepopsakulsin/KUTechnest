from sqlalchemy.orm import Session
from ..models.post import Post
from ..models.company import Company
from ..schemas.post import PostCreate
from ..schemas.enums import WorkField
from typing import Optional

def get_posts(
    db: Session,
    page: int = 1,
    page_size: int = 12,
    search: Optional[str] = None,
    work_field: Optional[WorkField] = None,
    location: Optional[str] = None,
    onsite: Optional[bool] = None
):
    offset = (page - 1) * page_size
    query = db.query(Post).join(Company)
    
    if search:
        query = query.filter(
            Post.title.contains(search) |
            Post.description.contains(search) |
            Company.name.contains(search)
        )
    
    if work_field:
        query = query.filter(Post.work_field == work_field)
    
    if location:
        query = query.filter(Post.location == location)
    
    if onsite is not None:
        query = query.filter(Post.onsite == onsite)
    
    total = query.count()
    posts = query.order_by(Post.created_at.desc()).offset(offset).limit(page_size).all()
    
    return posts, total

def get_post(db: Session, post_id: int):
    return db.query(Post).join(Company).filter(Post.id == post_id).first()

def create_post(db: Session, post: PostCreate):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
