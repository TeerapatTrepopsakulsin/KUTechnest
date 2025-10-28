from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..core.database import Base  # same Base used by your other models

class ApplicationStatus:
    """Possible application statuses."""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    HIRED = "hired"
    WITHDRAWN = "withdrawn"

class Application(Base):
    """Job application model linking a Student and a Post."""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), index=True, nullable=False)

    cover_letter = Column(Text, nullable=True)
    resume_url = Column(String(512), nullable=True)
    status = Column(String(32), default=ApplicationStatus.SUBMITTED, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="applications")
    student = relationship("Student", back_populates="applications")

    __table_args__ = (
        UniqueConstraint("post_id", "student_id", name="uq_application_post_student"),
    )
