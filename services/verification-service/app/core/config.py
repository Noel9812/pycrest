from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "PAY CREST API"
    API_PREFIX: str = "/api"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "pay_crest"

    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    DEFAULT_IFSC: str = "PCIN01001"

    CASHFREE_ENV: str = "sandbox"
    CASHFREE_CLIENT_ID: Optional[str] = None
    CASHFREE_CLIENT_SECRET: Optional[str] = None
    
    UPLOAD_BASE_PATH: str = "./uploads"

    # ✅ FIX for .env errors
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()