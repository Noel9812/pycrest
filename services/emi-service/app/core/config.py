from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Core
    SERVICE_NAME: Optional[str] = "emi-service"
    PORT: Optional[int] = 3003
    ENVIRONMENT: Optional[str] = "development"

    # Mongo
    MONGO_URI: Optional[str] = None
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: Optional[str] = None
    MONGODB_DB: str = "pay_crest"

    # JWT
    SECRET_KEY: Optional[str] = None
    JWT_SECRET: str = "CHANGE_ME"
    ALGORITHM: Optional[str] = "HS256"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 60
    JWT_EXPIRE_MINUTES: int = 60 * 24

    DEFAULT_IFSC: str = "PCIN01001"

    # Cashfree
    CASHFREE_ENV: str = "sandbox"
    CASHFREE_CLIENT_ID: Optional[str] = None
    CASHFREE_CLIENT_SECRET: Optional[str] = None
    CASHFREE_API_VERSION: str = "2023-08-01"
    CASHFREE_RETURN_URL: str = "http://localhost:5173/customer/dashboard"
    CASHFREE_RETURN_URL_WALLET: str = "http://localhost:5173/customer/wallet"
    CASHFREE_RETURN_URL_EMI: str = "http://localhost:5173/customer/emi"
    CASHFREE_WEBHOOK_URL: str = "http://localhost:8010/api/payments/cashfree/webhook"
    CASHFREE_ORDER_PREFIX: str = "pc_emi_"
    CASHFREE_HTTP_TIMEOUT_SECONDS: int = 20

    # Idempotency
    IDEMPOTENCY_ENABLED: bool = True
    IDEMPOTENCY_TTL_HOURS: int = 24

    # Service URLs
    AUTH_SERVICE_URL: Optional[str] = None
    LOAN_SERVICE_URL: Optional[str] = None
    EMI_SERVICE_URL: Optional[str] = None
    WALLET_SERVICE_URL: Optional[str] = None
    INTERNAL_SERVICE_TOKEN: str = "CHANGE_ME"
    PAYMENT_SERVICE_URL: Optional[str] = None
    VERIFICATION_SERVICE_URL: Optional[str] = None
    ADMIN_SERVICE_URL: Optional[str] = None
    MANAGER_SERVICE_URL: Optional[str] = None

    # ✅ IMPORTANT FIX
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()