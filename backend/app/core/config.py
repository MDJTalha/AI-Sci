from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    CHROMA_DB_PATH: str = "./chroma_db"
    
    class Config:
        env_file = ".env"


settings = Settings()
