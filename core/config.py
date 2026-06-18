import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Indic-RAG Knowledge Base"
    DATABASE_URL: str = "postgresql+asyncpg://indic_user:indic_password@localhost:5433/indic_db"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    class Config:
        env_file = ".env"

settings = Settings()
