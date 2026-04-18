import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis://localhost:6379")
    GENAI_API_KEY: str = os.getenv("GENAI_API_KEY", "")
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", 604800))  # Default to 7 days
    
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", 0.85))

    class Config:
        env_file = ".env"

settings = Settings()
