/*
  # Create Initial KUTechnest Schema

  1. New Tables
    - `users`
      - `id` (integer, primary key) - User ID
      - `email` (text, unique) - User email address
      - `first_name` (text) - User first name
      - `last_name` (text) - User last name
      - `is_active` (boolean) - Account active status
      - `google_id` (text, unique) - Google OAuth ID
      - `profile_picture` (text) - Profile picture URL
      - `created_at` (timestamptz) - Account creation timestamp

    - `students`
      - `id` (integer, primary key) - Student ID
      - `user_id` (integer, foreign key) - Reference to users table
      - `name` (text) - Student name
      - `nick_name` (text) - Nickname
      - `pronoun` (text) - Preferred pronoun
      - `age` (integer) - Student age
      - `year` (integer) - Academic year
      - `ku_generation` (integer) - KU generation number
      - `faculty` (text) - Faculty name
      - `major` (text) - Major/field of study
      - `about_me` (text) - Student bio
      - `email` (text) - Contact email
      - `created_at` (timestamptz) - Record creation timestamp

    - `companies`
      - `id` (integer, primary key) - Company ID
      - `user_id` (integer, foreign key) - Reference to users table
      - `name` (text, indexed) - Company name
      - `website` (text) - Company website URL
      - `logo_url` (text) - Company logo URL
      - `location` (text) - Company location
      - `description` (text) - Company description
      - `contacts` (text) - Contact information
      - `created_at` (timestamptz) - Record creation timestamp
      - `updated_at` (timestamptz) - Last update timestamp

    - `posts`
      - `id` (integer, primary key) - Post ID
      - `company_id` (integer, foreign key) - Reference to companies table
      - `title` (text, indexed) - Job title
      - `work_field` (text) - Field of work
      - `employment_type` (text) - Employment type (full-time, part-time, etc)
      - `location` (text) - Job location
      - `onsite` (boolean) - Onsite requirement
      - `salary` (integer) - Salary amount
      - `min_year` (integer) - Minimum years of experience
      - `requirement` (text) - Job requirements
      - `description` (text) - Short job description
      - `long_description` (text) - Detailed job description
      - `image_url` (text) - Job post image URL
      - `created_at` (timestamptz) - Post creation timestamp
      - `updated_at` (timestamptz) - Last update timestamp

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users to read public data
    - Add policies for users to manage their own data
*/

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  is_active BOOLEAN DEFAULT true,
  google_id TEXT UNIQUE,
  profile_picture TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);

-- Create students table
CREATE TABLE IF NOT EXISTS students (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  nick_name TEXT,
  pronoun TEXT,
  age INTEGER,
  year INTEGER NOT NULL,
  ku_generation INTEGER NOT NULL,
  faculty TEXT NOT NULL,
  major TEXT,
  about_me TEXT,
  email TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_students_user_id ON students(user_id);

-- Create companies table
CREATE TABLE IF NOT EXISTS companies (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  website TEXT,
  logo_url TEXT,
  location TEXT,
  description TEXT,
  contacts TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_companies_user_id ON companies(user_id);
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);

-- Create posts table
CREATE TABLE IF NOT EXISTS posts (
  id SERIAL PRIMARY KEY,
  company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  work_field TEXT NOT NULL,
  employment_type TEXT NOT NULL,
  location TEXT NOT NULL,
  onsite BOOLEAN DEFAULT false,
  salary INTEGER NOT NULL,
  min_year INTEGER NOT NULL,
  requirement TEXT NOT NULL,
  description TEXT DEFAULT '',
  long_description TEXT,
  image_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_posts_company_id ON posts(company_id);
CREATE INDEX IF NOT EXISTS idx_posts_title ON posts(title);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can read all user profiles"
  ON users FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  TO authenticated
  USING (id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer)
  WITH CHECK (id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer);

-- Students policies
CREATE POLICY "Anyone can view student profiles"
  ON students FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Students can insert own profile"
  ON students FOR INSERT
  TO authenticated
  WITH CHECK (user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer);

CREATE POLICY "Students can update own profile"
  ON students FOR UPDATE
  TO authenticated
  USING (user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer)
  WITH CHECK (user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer);

-- Companies policies
CREATE POLICY "Anyone can view companies"
  ON companies FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Companies can insert own profile"
  ON companies FOR INSERT
  TO authenticated
  WITH CHECK (user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer);

CREATE POLICY "Companies can update own profile"
  ON companies FOR UPDATE
  TO authenticated
  USING (user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer)
  WITH CHECK (user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer);

-- Posts policies
CREATE POLICY "Anyone can view posts"
  ON posts FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Companies can insert own posts"
  ON posts FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM companies
      WHERE companies.id = posts.company_id
      AND companies.user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer
    )
  );

CREATE POLICY "Companies can update own posts"
  ON posts FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM companies
      WHERE companies.id = posts.company_id
      AND companies.user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM companies
      WHERE companies.id = posts.company_id
      AND companies.user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer
    )
  );

CREATE POLICY "Companies can delete own posts"
  ON posts FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM companies
      WHERE companies.id = posts.company_id
      AND companies.user_id = (current_setting('request.jwt.claims', true)::json->>'sub')::integer
    )
  );