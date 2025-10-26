from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .core.database import Base, engine
from .api.v1.api import api_router
from .config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

SESSION_SECRET = settings.SESSION_SECRET


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    session_cookie="app_session",  # optional: cookie name
    same_site="none",               # "lax" or "strict"
    https_only=False,              # set True in production (requires HTTPS)
    max_age=60 * 60 * 2,           # 2 hours
)

@app.get("/")
async def root():
    return {"message": settings.PROJECT_NAME}

# Include API router
app.include_router(api_router, prefix="/api/v1")
