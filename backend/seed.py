"""
Seed script for KUTechnest database

This script populates the database with sample data from fixtures/data.json.

Usage from backend directory:
    python seed.py
    python -m seed

Or from project root:
    python backend/seed.py

The script uses relative imports to work with the existing backend structure.
"""

import json
import os
import sys
from pathlib import Path

# Get the backend directory
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Change to backend directory to ensure relative imports work
os.chdir(backend_dir)

from core.database import SessionLocal, engine, Base
from models.user import User
from models.student import Student
from models.company import Company
from models.post import Post


def load_fixture_data():
    """Load data from fixtures/data.json"""
    fixture_path = Path(__file__).parent / "fixtures" / "data.json"

    if not fixture_path.exists():
        print(f"Warning: Fixture file not found at {fixture_path}")
        return []

    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_tables():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def clear_tables(db):
    """Clear all existing data from tables"""
    print("Clearing existing data...")
    db.query(Post).delete()
    db.query(Company).delete()
    db.query(Student).delete()
    db.query(User).delete()
    db.commit()
    print("✓ Existing data cleared")


def seed_users(db, data):
    """Seed users table from fixture data"""
    print("Seeding users...")

    users_data = [item for item in data if item.get('model') == 'auth.user']
    user_map = {}

    for item in users_data:
        pk = item['pk']
        fields = item['fields']

        user = User(
            id=pk,
            email=fields.get('email', f'user{pk}@example.com'),
            first_name=fields.get('first_name', ''),
            last_name=fields.get('last_name', ''),
            is_active=fields.get('is_active', True),
            google_id=None,
            profile_picture=None
        )

        db.add(user)
        user_map[pk] = user

    db.commit()
    print(f"✓ Seeded {len(users_data)} users")
    return user_map


def seed_companies(db, data, user_map):
    """Seed companies table from fixture data"""
    print("Seeding companies...")

    companies_data = [item for item in data if item.get('model') == 'jobs.company']
    company_map = {}

    for item in companies_data:
        pk = item['pk']
        fields = item['fields']
        user_id = fields.get('user')

        if user_id not in user_map:
            print(f"Warning: Skipping company {pk} - user {user_id} not found")
            continue

        company = Company(
            id=pk,
            user_id=user_id,
            name=fields.get('name', 'Unknown Company'),
            website=fields.get('website'),
            logo_url=fields.get('logo_url'),
            location=fields.get('location'),
            description=fields.get('description'),
            contacts=fields.get('contacts')
        )

        db.add(company)
        company_map[pk] = company

    db.commit()
    print(f"✓ Seeded {len(companies_data)} companies")
    return company_map


def seed_students(db, data, user_map):
    """Seed students table from fixture data"""
    print("Seeding students...")

    students_data = [item for item in data if item.get('model') == 'students.student']

    if not students_data:
        print("No student data found in fixtures, creating sample students...")
        # Create some sample students for testing
        sample_students = [
            {
                'user_id': 1,
                'name': 'John Doe',
                'nick_name': 'John',
                'year': 3,
                'ku_generation': 67,
                'faculty': 'Engineering',
                'major': 'Computer Engineering',
                'email': 'john.doe@ku.th',
                'about_me': 'Passionate about software development'
            }
        ]

        for student_data in sample_students:
            if student_data['user_id'] in user_map:
                student = Student(**student_data)
                db.add(student)

        db.commit()
        print(f"✓ Created {len(sample_students)} sample students")
        return

    for item in students_data:
        fields = item['fields']
        user_id = fields.get('user')

        if user_id not in user_map:
            print(f"Warning: Skipping student - user {user_id} not found")
            continue

        student = Student(
            user_id=user_id,
            name=fields.get('name'),
            nick_name=fields.get('nick_name'),
            pronoun=fields.get('pronoun'),
            age=fields.get('age'),
            year=fields.get('year', 1),
            ku_generation=fields.get('ku_generation', 67),
            faculty=fields.get('faculty', 'Unknown'),
            major=fields.get('major'),
            about_me=fields.get('about_me'),
            email=fields.get('email', f'student{user_id}@ku.th')
        )

        db.add(student)

    db.commit()
    print(f"✓ Seeded {len(students_data)} students")


def seed_posts(db, data, company_map):
    """Seed posts table from fixture data"""
    print("Seeding posts...")

    posts_data = [item for item in data if item.get('model') == 'jobs.post']

    for item in posts_data:
        pk = item['pk']
        fields = item['fields']
        company_id = fields.get('company')

        if company_id not in company_map:
            print(f"Warning: Skipping post {pk} - company {company_id} not found")
            continue

        post = Post(
            id=pk,
            company_id=company_id,
            title=fields.get('title', 'Untitled Position'),
            work_field=fields.get('work_field', 'general'),
            employment_type=fields.get('employment_type', 'full-time'),
            location=fields.get('location', 'Unknown'),
            onsite=fields.get('onsite', False),
            salary=fields.get('salary', 0),
            min_year=fields.get('min_year', 0),
            requirement=fields.get('requirement', ''),
            description=fields.get('description', ''),
            long_description=fields.get('long_description'),
            image_url=fields.get('image_url')
        )

        db.add(post)

    db.commit()
    print(f"✓ Seeded {len(posts_data)} posts")


def seed_database():
    """Main function to seed the database"""
    print("\n" + "="*60)
    print("KUTechnest Database Seeding Script")
    print("="*60 + "\n")

    # Create tables
    create_tables()

    # Load fixture data
    print("\nLoading fixture data...")
    data = load_fixture_data()
    print(f"✓ Loaded {len(data)} records from fixtures\n")

    # Create database session
    db = SessionLocal()

    try:
        # Clear existing data
        clear_tables(db)

        # Seed tables in order of dependencies
        print("\nSeeding tables...\n")
        user_map = seed_users(db, data)
        company_map = seed_companies(db, data, user_map)
        seed_students(db, data, user_map)
        seed_posts(db, data, company_map)

        print("\n" + "="*60)
        print("✓ Database seeding completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
