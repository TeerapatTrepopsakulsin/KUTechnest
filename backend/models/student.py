from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pronoun = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    student_id = Column(String)
    date_of_birth = Column(DateTime)
    phone = Column(String)
    ku_generation = Column(Integer)
    faculty = Column(String)
    major = Column(String, nullable=True)
    about_me = Column(Text, nullable=True)
    email = Column(String)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="student")