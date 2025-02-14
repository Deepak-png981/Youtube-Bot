import os
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    youtube_api_key: str = os.getenv("YOUTUBE_API_KEY")
    whisper_model_size: str = "base"
    
    class Config:
        env_file = ".env"

settings = Settings()