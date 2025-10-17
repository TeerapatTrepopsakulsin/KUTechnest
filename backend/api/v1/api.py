from fastapi import APIRouter
from ...api.v1.endpoints import posts, companies, students, auth, application

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(application.router, prefix="/application", tags=["application"])
