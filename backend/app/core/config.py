import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "ForgeAI Workspace"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_V1_STR: str = "/api/v1"
    
    # Database (PostgreSQL default)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:postgres@localhost:5432/forgeai"
    )
    
    # JWT Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = os.getenv(
        "BACKEND_CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:5173,http://localhost:8000"
    )

    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v: str, info) -> str:
        # In non-test environments, fail if SECRET_KEY is missing or insecure default
        env = os.getenv("ENVIRONMENT", "development")
        if env != "testing":
            if not v or v.strip() == "" or v == "super-secret-key-change-in-production-123456789":
                raise ValueError("SECRET_KEY environment variable MUST be set and secure in non-testing environment")
        return v or "test-secret-key-only-for-pytest-execution-32-chars-min"

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]
        return self.BACKEND_CORS_ORIGINS

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
