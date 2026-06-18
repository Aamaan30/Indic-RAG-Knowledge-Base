import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Indic-RAG Knowledge Base"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    
    class Config:
        env_file = ".env"

settings = Settings()
