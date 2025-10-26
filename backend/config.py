import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    BACKEND_URL: str = "http://127.0.0.1:8000"
    FRONTEND_URL: str = "http://127.0.0.1:5173"
    PROJECT_NAME: str = "KUTechnest API"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "redirect-url-here"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SESSION_SECRET: str = "session-secret"

    class Config:
        env_file = ".env"
        case_sensitive = True


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
settings = Settings(_env_file=dotenv_path)
