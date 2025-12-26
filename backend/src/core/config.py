from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Config
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "local"
    DEBUG: bool = True

    # Security (Legacy JWT - mantener para backward compatibility)
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Auth0 Configuration
    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str
    AUTH0_ALGORITHMS: List[str] = ["RS256"]

    # CORS origins - accepts comma-separated string from environment
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:8000"

    # Database Config
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    # Computed property for the connection string
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Configuration to read environment variables
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()