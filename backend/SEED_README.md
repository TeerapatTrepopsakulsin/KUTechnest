# Database Seeding Guide

## Overview

The `seed.py` script populates the database with sample data from `fixtures/data.json`. It creates users, companies, students, and job posts for testing and development.

## Prerequisites

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your `.env` file is configured with the correct `DATABASE_URL`

## Usage

### From backend directory:
```bash
cd backend
python seed.py
```

Or using module syntax:
```bash
cd backend
python -m seed
```

### From project root:
```bash
python backend/seed.py
```

## What it does

The seed script:

1. **Creates tables** - Sets up all database tables based on SQLAlchemy models
2. **Clears existing data** - Removes all existing records (⚠️ destructive!)
3. **Seeds users** - Creates user accounts from fixture data
4. **Seeds companies** - Creates company profiles linked to users
5. **Seeds students** - Creates student profiles linked to users
6. **Seeds posts** - Creates job postings linked to companies

## Data Sources

The script reads from `backend/fixtures/data.json`, which contains:
- User accounts (from Django auth.user)
- Company profiles (from jobs.company)
- Student profiles (from students.student)
- Job posts (from jobs.post)

## Important Notes

⚠️ **Warning**: This script will **DELETE ALL EXISTING DATA** before seeding!

- The script maintains referential integrity by seeding in order:
  1. Users (no dependencies)
  2. Companies (depends on users)
  3. Students (depends on users)
  4. Posts (depends on companies)

- If a referenced user or company doesn't exist, the script will skip that record with a warning

- Sample students are auto-generated if no student data exists in fixtures

## Troubleshooting

### Import Errors
If you get import errors about relative imports, make sure you're running from the correct directory. The script adjusts the Python path automatically.

### Database Errors
- Check that `DATABASE_URL` in your `.env` file is correct
- Ensure the database file/server is accessible
- Verify you have write permissions

### Missing Data
If certain records are skipped, check the console output for warnings about missing user or company references.

## Extending the Seed Script

To add more data types:

1. Add the model import at the top
2. Create a `seed_<model>` function following the existing patterns
3. Call your function in `seed_database()` in the correct dependency order
4. Ensure your fixture data includes the new model type

## Example Output

```
============================================================
KUTechnest Database Seeding Script
============================================================

Creating database tables...
✓ Tables created successfully

Loading fixture data...
✓ Loaded 1523 records from fixtures

Seeding tables...

Clearing existing data...
✓ Existing data cleared
Seeding users...
✓ Seeded 45 users
Seeding companies...
✓ Seeded 32 companies
Seeding students...
✓ Created 1 sample students
Seeding posts...
✓ Seeded 184 posts

============================================================
✓ Database seeding completed successfully!
============================================================
```
