from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PREFIX: str = "/api"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/smart_car")

settings = Settings()
