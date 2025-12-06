# KUTechnest

## Project Description
KUTechnest is a platform where KU’s students(CPE/SKE), alumni, and employers can easily connect and find each other. Employers can easily post job ads and monitor the number of applicants. It helps tech students and alumni to find perhaps their first job in the studied field or discover new job opportunities.
and job opportunities. It provides:
- OAuth-based authentication (Google) and JWT sessions for API access.
- A backend API (FastAPI + SQLAlchemy) exposing user, student, company and post resources.
- A frontend (Vue 3 + Vite) with a simple authentication flow and registration forms.

The project is intended as a learning/demo app and a starting point for building a
more complete placement portal.

## Overview
- Backend: FastAPI, SQLAlchemy, JWT auth, Google OAuth integration.
- Frontend: Vite + Vue 3, Pinia store for auth flows.

## Prerequisites
- Python 3.10+
- Node.js 18+ and npm/yarn
- (Optional) SQLite (a file `db.sqlite3` is included in repo root)

## Environment
Create a `.env` file in `backend/` (or set environment variables). Example keys used by the app:

```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:5173/auth/callback
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
BACKEND_URL=http://127.0.0.1:8000
FRONTEND_URL=http://localhost:5173
DATABASE_URL=sqlite:///./db.sqlite3
```

The backend copies settings from `backend/config.py` and loads `.env` next to that file.

## Run (PowerShell)

Backend (development):
```powershell
cd C:\Users\trepo\PycharmProjects\KUTechnest
uvicorn backend.main:app --reload
```

Frontend (development):
```powershell
cd C:\Users\trepo\PycharmProjects\KUTechnest\frontend
npm install
npm run dev
```

If you need to run both on one line in PowerShell, separate with `;`:
```powershell
cd C:\Users\trepo\PycharmProjects\KUTechnest; uvicorn backend.main:app --reload
```

## LLM Verification (LangChain + groqAI)

This project includes an optional LLM-powered validation layer that verifies:
- Job posts (suitable for students, realistic requirements, salary, content safety)
- Company profiles (legitimacy, contact quality, website)
- Student profiles (format, plausibility and content appropriateness)

Implementation notes:
- The LLM integration is implemented under `backend/core/llm/` using LangChain-style chains (`prompts.py`, `chains.py`, `parsers.py`, `groq_client.py`).
- Job validation is exposed in the backend at the `POST /api/posts` endpoint (see `backend/api/v1/endpoints/posts.py`). The endpoint calls `validate_job_post(...)` before creating a post.
- Validation returns a `ValidationReport` JSON object with: `is_valid` (bool), `confidence_score` (0.0-1.0), `issues` (list), `recommendations` (list) and `reason` (string).
- The current threshold used by the endpoint is `confidence_score >= 0.7` — posts below that threshold are rejected with a 400 response containing the validation details.

Required environment variables:

```
GROQ_API_KEY=<your-groq-api-key>
LLM_MODEL=<model-name>        # e.g. "gpt-4o-mini"
LLM_TEMPERATURE=0.0           # float, e.g. 0.0-1.0
```

These variables are read from `backend/config.py` (add them to `backend/.env`). The required dependencies are already listed in `backend/requirements.txt` (`langchain_core`, `langchain_groq`).

How it works (high level):
- `chains.validate_job_post()` builds a prompt (see `prompts.py`) and invokes the LLM client from `groq_client.py`.
- Output is parsed by a Pydantic `ValidationReport` parsed by `parsers.py`.
- The endpoint inspects `is_valid` and `confidence_score` and either creates the post or returns a validation error with recommendations.

Security & cost notes:
- LLM calls may be rate-limited and incur cost from groqAI — enable in production only when you have API access and monitoring.
- Consider caching validation results for identical posts to reduce calls.
