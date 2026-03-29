from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    SERVICE_NAME: Optional[str] = "admin-service"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "pay_crest"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()