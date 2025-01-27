from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str = "postgresql://postgres:new_password@localhost:5432/loyalty"  # Added port 5432
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_URL: str = "redis://localhost:6379"
    PROJECT_NAME: str = "Micro Loyalty API"

    class Config:
        env_file = ".env"

settings = Settings()