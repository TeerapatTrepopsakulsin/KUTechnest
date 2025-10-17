from sqlalchemy.orm import sessionmaker
from backend.core.database import engine  # ✅ correct import
from backend.models import Company, Post, User, Student  # ✅ make sure models/__init__.py imports all
from backend.schemas.enums import WorkField, EmploymentType  # ✅ enums
import random
from backend.models import Company, Post, User, Student, Application  # Application import is key
from backend.schemas.enums import WorkField, EmploymentType

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Sample data
companies_data = [
    {
        "name": "Gogo Bike",
        "logo_url": "https://play-lh.googleusercontent.com/yAseCUtav8OBWf8pIUMO57YCBXDlTPuNF0JGhr1Tl4VvMihG406nrFJWkXGoz8Oxbz8L8cwG1N_YOIQ61oMooA8=w480-h960",
        "location": "bangkok",
        "description": "Leading bike sharing platform in Thailand"
    },
    {
        "name": "GCOO",
        "logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2tIhgxNOTnu5DnOEomC-2nNRLAbnnepte6A&s",
        "location": "bangkok",
        "description": "Electric scooter company"
    },
    {
        "name": "ทุเรียนสวนคุณยาย",
        "logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSu1uR-7MlN1gLLt-yUfzFCK4FCZoX3o0lNmg&s",
        "location": "chiang-mai",
        "description": "Premium durian farm and distribution"
    },
    {
        "name": "FoodieTech",
        "logo_url": "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
        "location": "bangkok",
        "description": "Food delivery technology platform"
    },
    {
        "name": "ZenRide",
        "logo_url": "https://cdn-icons-png.flaticon.com/512/888/888859.png",
        "location": "phuket",
        "description": "Electric scooter rental service"
    },
    {
        "name": "SmartMart",
        "logo_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "location": "bangkok",
        "description": "Smart retail solutions"
    },
    {
        "name": "SkyNet Cloud",
        "logo_url": "https://cdn-icons-png.flaticon.com/512/919/919830.png",
        "location": "bangkok",
        "description": "Cloud infrastructure provider"
    },
    {
        "name": "SecureIT",
        "logo_url": "https://cdn-icons-png.flaticon.com/512/1048/1048941.png",
        "location": "chiang-mai",
        "description": "Cybersecurity solutions"
    }
]

jobs_data = [
    {
        "title": "UI/UX Designer",
        "work_field": WorkField.UI_UX,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "bangkok",
        "onsite": True,
        "salary": 45000,
        "min_year": 2,
        "requirement": "Experience with Figma, Adobe Creative Suite, user research",
        "description": "Design intuitive and modern interfaces for mobile apps.",
        "long_description": "We are looking for a talented UI/UX Designer to join our team. You will be responsible for creating user-centered designs for our mobile applications and web platforms."
    },
    {
        "title": "Backend Developer",
        "work_field": WorkField.BACKEND,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "bangkok",
        "onsite": False,
        "salary": 60000,
        "min_year": 3,
        "requirement": "Python, Django/FastAPI, PostgreSQL, Docker",
        "description": "Develop REST APIs and manage scalable backend services.",
        "long_description": "Join our backend team to build robust and scalable APIs. You'll work with modern technologies and contribute to our microservices architecture."
    },
    {
        "title": "Frontend Developer",
        "work_field": WorkField.FRONTEND,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "chiang-mai",
        "onsite": True,
        "salary": 50000,
        "min_year": 2,
        "requirement": "Vue.js, React, TypeScript, TailwindCSS",
        "description": "Build responsive UIs with Vue and TailwindCSS.",
        "long_description": "We need a skilled frontend developer to create beautiful and responsive user interfaces using modern frameworks."
    },
    {
        "title": "Fullstack Engineer",
        "work_field": WorkField.FULLSTACK,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "bangkok",
        "onsite": False,
        "salary": 70000,
        "min_year": 4,
        "requirement": "Full-stack development, Node.js, React, databases",
        "description": "Develop end-to-end features for food delivery platforms.",
        "long_description": "Looking for a versatile fullstack engineer to work on our food delivery platform from frontend to backend."
    },
    {
        "title": "Mobile App Developer",
        "work_field": WorkField.MOBILE,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "phuket",
        "onsite": True,
        "salary": 55000,
        "min_year": 3,
        "requirement": "React Native, Flutter, iOS/Android development",
        "description": "Build cross-platform apps for electric scooter rentals.",
        "long_description": "Join our mobile team to develop innovative apps for our electric scooter rental platform."
    },
    {
        "title": "Data Analyst",
        "work_field": WorkField.DATA_ANALYST,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "bangkok",
        "onsite": True,
        "salary": 48000,
        "min_year": 2,
        "requirement": "Python, SQL, Tableau, statistical analysis",
        "description": "Analyze customer data to drive better business decisions.",
        "long_description": "We're seeking a data analyst to help us understand customer behavior and optimize our business operations."
    },
    {
        "title": "Cloud Engineer",
        "work_field": WorkField.CLOUD,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "bangkok",
        "onsite": False,
        "salary": 75000,
        "min_year": 4,
        "requirement": "AWS, Docker, Kubernetes, CI/CD",
        "description": "Maintain cloud infrastructure and CI/CD pipelines.",
        "long_description": "Join our DevOps team to manage and optimize our cloud infrastructure on AWS."
    },
    {
        "title": "Cybersecurity Specialist",
        "work_field": WorkField.SECURITY,
        "employment_type": EmploymentType.FULL_TIME,
        "location": "chiang-mai",
        "onsite": True,
        "salary": 65000,
        "min_year": 3,
        "requirement": "Security frameworks, penetration testing, compliance",
        "description": "Implement and monitor enterprise security policies.",
        "long_description": "We need a cybersecurity specialist to strengthen our security posture and ensure compliance."
    }
]

def seed_database():
    # Clear existing data
    db.query(Post).delete()
    db.query(Company).delete()
    db.query(Student).delete()
    db.query(User).delete()
    db.commit()
    
    # Create companies
    companies = []
    for i, company_data in enumerate(companies_data):
        # Create user for company
        user = User(
            email=f"company{i+1}@example.com",
            first_name="Company",
            last_name=f"User {i+1}"
        )
        db.add(user)
        db.flush()  # Get the user ID
        
        # Create company
        company = Company(
            user_id=user.id,
            **company_data
        )
        db.add(company)
        companies.append(company)
    
    db.commit()
    
    # Create posts
    for i, job_data in enumerate(jobs_data):
        company = companies[i % len(companies)]
        post = Post(
            company_id=company.id,
            **job_data
        )
        db.add(post)
    
    db.commit()

    # Create you as a student
    me_user = User(
        email="teerapat.tre@ku.th",
        first_name="Teerapat",
        last_name="TREPOPSAKULSIN"
    )
    db.add(me_user)
    db.flush()  # Get the me_user ID
    
    student_data = {
        "name": "Alice Johnson",
        "nick_name": "Ally",
        "pronoun": "She/Her",
        "age": 20,
        "year": 2,
        "ku_generation": 60,
        "faculty": "Science",
        "major": "Computer Science",
        "about_me": "Loves coding and AI research.",
        "email": "alice.johnson@example.com",
    }
    # Create company
    student = Student(
        user_id=me_user.id,
        **student_data
    )
    db.add(student)

    db.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()