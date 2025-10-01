from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    PROJECT_NAME: str = "KUTechnest API"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()