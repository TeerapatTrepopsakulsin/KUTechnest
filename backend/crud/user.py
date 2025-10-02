from sqlalchemy.orm import Session
from typing import Optional
from ..models.user import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_google_id(db: Session, google_id: str) -> Optional[User]:
    return db.query(User).filter(User.google_id == google_id).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    email: str,
    first_name: str,
    last_name: str,
    google_id: Optional[str] = None,
    profile_picture: Optional[str] = None
) -> User:
    db_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        google_id=google_id,
        profile_picture=profile_picture,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_oauth_info(
    db: Session,
    user: User,
    google_id: str,
    profile_picture: Optional[str] = None
) -> User:
    user.google_id = google_id
    if profile_picture:
        user.profile_picture = profile_picture
    db.commit()
    db.refresh(user)
    return user
