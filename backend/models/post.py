from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String, index=True)
    work_field = Column(String)
    employment_type = Column(String)
    location = Column(String)
    onsite = Column(Boolean, default=False)
    salary = Column(Integer)
    min_year = Column(Integer)
    requirement = Column(Text)
    description = Column(String, default="")
    long_description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    applications = relationship(
        "Application",
        back_populates="post",
        cascade="all, delete-orphan"
    )
    # Relationships
    company = relationship("Company", back_populates="posts")