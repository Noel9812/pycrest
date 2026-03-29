
# File: services/admin-service/app/core/config.py
`python
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
``n
# File: services/emi-service/app/core/config.py
`python
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

    # âœ… IMPORTANT FIX
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()
``n
# File: services/auth-service/app/core/config.py
`python
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Core
    SERVICE_NAME: Optional[str] = "auth-service"
    API_PREFIX: str = "/api"
    PORT: Optional[int] = 3001
    ENVIRONMENT: Optional[str] = "development"
    DEFAULT_IFSC: str = "TEST0001234"

    # Mongo
    MONGO_URI: Optional[str] = None
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: Optional[str] = None
    MONGODB_DB: str = "pay_crest"

    # JWT
    SECRET_KEY: Optional[str] = None
    JWT_SECRET_KEY: str  # This is the required field causing the error
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 
    ALGORITHM: Optional[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = 60

    # Service URLs
    AUTH_SERVICE_URL: Optional[str] = None
    LOAN_SERVICE_URL: Optional[str] = None
    EMI_SERVICE_URL: Optional[str] = None
    WALLET_SERVICE_URL: Optional[str] = None
    PAYMENT_SERVICE_URL: Optional[str] = None
    VERIFICATION_SERVICE_URL: Optional[str] = None
    ADMIN_SERVICE_URL: Optional[str] = None
    MANAGER_SERVICE_URL: Optional[str] = None

    # âœ… THIS MUST BE INSIDE THE CLASS INDENTATION
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra="allow"
    )

# Now it will correctly load the variables from .env
settings = Settings()
``n
# File: services/loan-service/app/core/config.py
`python
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Core (ADD THESE â†’ FIXES YOUR ERROR)
    SERVICE_NAME: Optional[str] = "service"
    PORT: Optional[int] = 8000
    ENVIRONMENT: Optional[str] = "development"
    API_PREFIX: str = "/api"

    # Mongo
    MONGO_URI: Optional[str] = None
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: Optional[str] = None
    MONGODB_DB: str = "pay_crest"

    # JWT
    SECRET_KEY: Optional[str] = None
    JWT_SECRET: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Service URLs
    AUTH_SERVICE_URL: Optional[str] = None
    LOAN_SERVICE_URL: Optional[str] = None
    EMI_SERVICE_URL: Optional[str] = None
    WALLET_SERVICE_URL: Optional[str] = None
    PAYMENT_SERVICE_URL: Optional[str] = None
    VERIFICATION_SERVICE_URL: Optional[str] = None
    ADMIN_SERVICE_URL: Optional[str] = None
    MANAGER_SERVICE_URL: Optional[str] = None

    # Cashfree
    CASHFREE_ENV: str = "sandbox"
    CASHFREE_CLIENT_ID: Optional[str] = None
    CASHFREE_CLIENT_SECRET: Optional[str] = None
    
    UPLOAD_BASE_PATH: str = "./uploads"

    # âœ… IMPORTANT FIX
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"   # ðŸ”¥ THIS FIXES YOUR ERROR
    )


settings = Settings()
``n
# File: services/manager-service/app/core/config.py
`python
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    # âœ… ADD THESE (VERY IMPORTANT)
    SERVICE_NAME: str = "emi-service"
    PORT: int = 8000
    ENVIRONMENT: str = "development"

    # Core
    APP_NAME: str = "PAY CREST API"
    API_PREFIX: str = "/api"

    # Mongo
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "pay_crest"

    # JWT
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
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

    # âœ… CRITICAL FIX
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"   # ðŸ”¥ prevents crash from extra .env fields
    )


settings = Settings()
``n
# File: services/payment-service/app/core/config.py
`python
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
    
    WALLET_SERVICE_URL: str = "http://localhost:3008"
    INTERNAL_SERVICE_TOKEN: str = "CHANGE_ME"

    # âœ… IMPORTANT FIX
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()
``n
# File: services/verification-service/app/core/config.py
`python
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

    # âœ… FIX for .env errors
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()
``n
# File: services/wallet-service/app/core/config.py
`python
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "EMI Service"
    API_PREFIX: str = "/api"

    # Mongo
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "pay_crest"

    # JWT
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
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

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"   # ðŸ”¥ prevents crash from unknown env vars


settings = Settings()
``n
# File: lms_backend/app/core/config.py
`python

from pydantic_settings import BaseSettings
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

    # Cashfree (Payment Gateway)
    CASHFREE_ENV: str = "sandbox"  # sandbox | production
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

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

``n
# File: services/admin-service/app/core/security.py
`python

import time
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from ..core.config import settings
from ..database.mongo import get_db
from bson import ObjectId
from ..utils.id import to_object_id

# OAuth2 scheme points to /auth/token endpoint
# username field in the form will be treated as email
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


def create_access_token(subject: dict, expires_minutes: int | None = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.JWT_EXPIRE_MINUTES)
    payload = {**subject, "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    role = payload.get("role")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    db = await get_db()
    # support numeric user ids or ObjectId strings
    user = None
    target_is_customer = role == "customer"
    primary = db.users if target_is_customer else db.staff_users
    fallback = db.staff_users if target_is_customer else db.users

    try:
        uid = int(user_id)
        user = await primary.find_one({"_id": uid})
        if not user:
            user = await fallback.find_one({"_id": uid})
    except Exception:
        oid = to_object_id(user_id)
        user = await primary.find_one({"_id": oid})
        if not user:
            user = await fallback.find_one({"_id": oid})
    if not user or not user.get("is_active", True):
        raise HTTPException(status_code=401, detail="User inactive or not found")
    # Note: Don't convert _id to string here - it causes lookup failures in services
    # Services expect the original _id type (numeric or ObjectId)
    return user


def require_roles(*allowed_roles: str):
    async def dep(user = Depends(get_current_user)):
        if user.get("role") not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized for this operation")
        return user
    return dep

``n
# File: lms_backend/app/schemas/kyc.py
`python
from pydantic import BaseModel, Field
from typing import Optional , Union
from datetime import date


class KYCSubmit(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)

    dob: date = Field(
        ...,
        description="Date of birth in YYYY-MM-DD format"
    )

    nationality: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="Indian"
    )

    gender: Optional[str] = Field(
        None,
        pattern=r"(?i)^(male|female|other)$"
    )

    father_or_spouse_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100
    )

    marital_status: Optional[str] = Field(
        None,
        pattern=r"(?i)^(single|married|divorced|widowed)$"
    )

    phone_number: Optional[str] = Field(
        None,
        pattern=r"^\+?\d{10,15}$"
    )

    pan_number: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    )

    aadhaar_number: Optional[str] = Field(
        None,
        pattern=r"^\d{12}$"
    )

    employment_status: Optional[str] = Field(
        None,
        pattern=r"(?i)^(employed|self-employed|unemployed|student|retired)$"
    )

    employment_type: Optional[str] = Field(
        None,
        pattern=r"(?i)^(private|government|business|freelancer)$"
    )

    company_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=150
    )

    monthly_income: Optional[float] = Field(
        None,
        ge=0,
        le=10_000_000
    )

    existing_emi_months: Optional[int] = Field(
        None,
        ge=0,
        le=360
    )

    years_of_experience: Optional[int] = Field(
        None,
        ge=0,
        le=60
    )

    address: Optional[str] = Field(
        None,
        min_length=10,
        max_length=300
    )

    # file references (Mongo Binary or ObjectId stored elsewhere)
    photo: Optional[str] = Field(None, max_length=100)
    pan_card: Optional[str] = Field(None, max_length=100)
    aadhar_card: Optional[str] = Field(None, max_length=100)


class KYCOut(BaseModel):
    id: str = Field(alias="_id")

    customer_id: Optional[int] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    employment_status: Optional[str] = None
    monthly_income: Optional[float] = None

    kyc_status: str = Field(
        ...,
        pattern=r"(?i)^(pending|approved|rejected)$"
    )

    total_score: Optional[int] = Field(None, ge=0, le=100)
    cibil_score: Optional[int] = Field(None, ge=300, le=900)

    loan_eligible: Optional[bool] = None

    dob: Optional[Union[str,date]] = None
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    aadhar_number: Optional[str] = None
    pan_masked: Optional[str] = None
    aadhaar_masked: Optional[str] = None

    photo: Optional[str] = None
    pan_card: Optional[str] = None
    aadhar_card: Optional[str] = None


class KYCVerify(BaseModel):
    approve: bool

    employment_score: int = Field(..., ge=0, le=25)
    income_score: int = Field(..., ge=0, le=25)
    emi_score: int = Field(..., ge=0, le=25)
    experience_score: int = Field(..., ge=0, le=25)
    total_score: Optional[int] = Field(None, ge=0, le=100)
    cibil_score: Optional[int] = Field(None, ge=300, le=900)

    remarks: Optional[str] = Field(
        None,
        min_length=3,
        max_length=300
    )

``n
# File: services/loan-service/app/routers/customer/router.py
`python
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import io
from datetime import datetime
from uuid import uuid4
from ...core.security import require_roles
from ...models.enums import Roles, VechicleType, PropertyType, EmploymentStatus, Gender, MaritalStatus
from ...schemas.kyc import KYCOut
from ...schemas.loan import LoanOut, LoanApplyResponse
from ...schemas.support import SupportTicketCreate
from ...utils.serializers import normalize_doc
from .service import get_db
from .service import (
    add_money,
    profile_dashboard,
    submit_kyc,
    get_kyc_by_customer,
    apply_loan,
    compute_customer_eligibility,
    list_customer_loans,
    pay_emi_any_wallet,
    upload_signed_sanction_letter,
    get_customer_emi_details,
    get_customer_noc,
    calculate_settlement_any,
    foreclose_any,
    list_customer_notifications,
    get_settings,
    upload_document,
    attach_kyc_document,
    get_document_binary,
    write_audit_log,
)


router = APIRouter(tags=["customer"])

LOAN_PRODUCT_CONFIG: dict[str, dict] = {
    "personal": {"min_amount": 10000, "max_amount": 2500000, "min_tenure_months": 12, "max_tenure_months": 120, "eligibility_factor": 1.0},
    "vehicle": {"min_amount": 500000, "max_amount": 6000000, "min_tenure_months": 12, "max_tenure_months": 84, "eligibility_factor": 1.25},
    "education": {"min_amount": 200000, "max_amount": 3500000, "min_tenure_months": 12, "max_tenure_months": 120, "eligibility_factor": 1.1},
    "home": {"min_amount": 1500000, "max_amount": 20000000, "min_tenure_months": 60, "max_tenure_months": 360, "eligibility_factor": 3.5},
}

@router.post('/add-money')
async def add_money_route(amount: float, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await add_money(cid, amount)

@router.get('/get/profile')
async def profile(user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await profile_dashboard(cid)

@router.get('/kyc')
async def customer_kyc(user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await get_kyc_by_customer(cid)

@router.get("/notifications")
async def customer_notifications(limit: int = 100, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await list_customer_notifications(cid, limit=limit)


@router.post("/support/tickets")
async def create_support_ticket(payload: SupportTicketCreate, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = str(user.get("customer_id") or user.get("_id"))
    now = datetime.utcnow()
    db = await get_db()
    ticket_id = f"TKT-{now.strftime('%Y%m%d')}-{uuid4().hex[:8].upper()}"
    doc = {
        "ticket_id": ticket_id,
        "customer_id": cid,
        "category": payload.category,
        "subject": payload.subject.strip(),
        "message": payload.message.strip(),
        "attachment": payload.attachment.dict() if payload.attachment else None,
        "status": "open",
        "admin_reply": None,
        "resolved_at": None,
        "resolved_by": None,
        "created_at": now,
        "updated_at": now,
    }
    await db.support_tickets.insert_one(doc)
    await write_audit_log(
        action="support_ticket_created",
        actor_role=Roles.CUSTOMER,
        actor_id=cid,
        entity_type="support_ticket",
        entity_id=ticket_id,
        details={"category": payload.category, "subject": payload.subject.strip()},
    )
    return normalize_doc(doc)


@router.get("/support/tickets")
async def list_support_tickets(user=Depends(require_roles(Roles.CUSTOMER))):
    cid = str(user.get("customer_id") or user.get("_id"))
    db = await get_db()
    rows = (
        await db.support_tickets.find({"customer_id": cid})
        .sort([("created_at", -1), ("_id", -1)])
        .to_list(length=300)
    )
    return [normalize_doc(r) for r in rows]

@router.get("/loan-offers")
async def loan_offers(user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    eligibility = await compute_customer_eligibility(cid)
    settings = await get_settings()

    suggested_max = float(eligibility.get("suggested_max_loan") or 0.0)
    cibil_score = int(eligibility.get("cibil_score") or 0)
    min_cibil_required = int(settings.get("min_cibil_required") or 650)
    cibil_eligible = cibil_score >= min_cibil_required
    rate_map = {
        "personal": float(settings.get("personal_loan_interest") or 12.0),
        "vehicle": float(settings.get("vehicle_loan_interest") or settings.get("personal_loan_interest") or 12.0),
        "education": float(settings.get("education_loan_interest") or settings.get("personal_loan_interest") or 12.0),
        "home": float(settings.get("home_loan_interest") or settings.get("personal_loan_interest") or 12.0),
    }

    offers: dict[str, dict] = {}
    for loan_type, cfg in LOAN_PRODUCT_CONFIG.items():
        raw_max = min(float(cfg["max_amount"]), suggested_max * float(cfg["eligibility_factor"]))
        eligible_max = round(max(0.0, raw_max), 2)
        base_min = float(cfg["min_amount"])
        if eligible_max <= 0:
            eligible_min = 0.0
        elif eligible_max < base_min:
            eligible_min = round(max(0.0, eligible_max * 0.5), 2)
        else:
            eligible_min = base_min
        offers[loan_type] = {
            "loan_type": loan_type,
            "interest_rate": rate_map[loan_type],
            "min_amount": float(cfg["min_amount"]),
            "max_amount": float(cfg["max_amount"]),
            "eligible_min_amount": eligible_min,
            "eligible_max_amount": eligible_max,
            "min_tenure_months": int(cfg["min_tenure_months"]),
            "max_tenure_months": int(cfg["max_tenure_months"]),
            "cibil_eligible": cibil_eligible,
        }

    return {
        "cibil_score": cibil_score,
        "min_cibil_required": min_cibil_required,
        "score": float(eligibility.get("score") or 0),
        "suggested_max_loan": suggested_max,
        "offers": offers,
    }

@router.post('/submit-kyc', response_model=KYCOut)
async def submit_kyc_route(
    full_name: str = Form(...),
    dob: str = Form(...),
    nationality: str = Form(...),
    gender: Optional[Gender] = Form(None),
    father_or_spouse_name: Optional[str] = Form(None),
    marital_status: Optional[MaritalStatus] = Form(None),
    phone_number: Optional[str] = Form(None),
    pan_number: Optional[str] = Form(None),
    aadhaar_number: Optional[str] = Form(None),
    employment_status: Optional[EmploymentStatus] = Form(None),
    employment_type: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    monthly_income: Optional[float] = Form(None),
    existing_emi_months: Optional[int] = Form(None),
    years_of_experience: Optional[int] = Form(None),
    address: Optional[str] = Form(None),
    pan_card: UploadFile = File(None),
    aadhar_card: UploadFile = File(None),
    photo: UploadFile = File(None),
    user=Depends(require_roles(Roles.CUSTOMER)),
):
    cid = user.get("customer_id") or user.get("_id")

    payload = {
        "full_name": full_name,
        "dob": dob,
        "nationality": nationality,
        "gender": gender,
        "father_or_spouse_name": father_or_spouse_name,
        "marital_status": marital_status,
        "phone_number": phone_number,
        "pan_number": pan_number,
        "aadhaar_number": aadhaar_number,
        "employment_status": employment_status,
        "employment_type": employment_type,
        "company_name": company_name,
        "monthly_income": monthly_income,
        "existing_emi_months": existing_emi_months,
        "years_of_experience": years_of_experience,
        "address": address,
    }

    # 1. Submit base KYC (no files yet)
    await submit_kyc(cid, payload)

    # 2. Upload & attach documents
    if pan_card:
        doc_id = await upload_document(pan_card, cid, "pan_card")
        await attach_kyc_document(cid, "pan_card", doc_id)

    if aadhar_card:
        doc_id = await upload_document(aadhar_card, cid, "aadhar_card")
        await attach_kyc_document(cid, "aadhar_card", doc_id)

    if photo:
        doc_id = await upload_document(photo, cid, "photo")
        await attach_kyc_document(cid, "photo", doc_id)

    # 3. Return sanitized updated KYC
    return await get_kyc_by_customer(cid)



@router.post('/apply-personal-loan', response_model=LoanApplyResponse)
async def apply_personal(
    bank_account_number: int = Form(...),
    full_name: str = Form(...),
    pan_number: Optional[str] = Form(None),
    loan_amount: float = Form(...),
    loan_purpose: str = Form(...),
    salary_income: float = Form(...),
    monthly_avg_balance: float = Form(...),
    tenure_months: int = Form(...),
    guarantor_name: Optional[str] = Form(None),
    guarantor_phone: Optional[str] = Form(None),
    guarantor_pan: Optional[str] = Form(None),
    pay_slip: UploadFile = File(None),
    user=Depends(require_roles(Roles.CUSTOMER)),
):
    settings = await get_settings()
    cid = user.get("customer_id") or user.get("_id")
    
    payload = {
        "bank_account_number": bank_account_number,
        "full_name": full_name,
        "pan_number": pan_number,
        "loan_amount": loan_amount,
        "loan_purpose": loan_purpose,
        "salary_income": salary_income,
        "monthly_avg_balance": monthly_avg_balance,
        "tenure_months": tenure_months,
        "guarantor_name": guarantor_name,
        "guarantor_phone": guarantor_phone,
        "guarantor_pan": guarantor_pan,
    }
    
    if pay_slip :
        pay_slip_path = await upload_document(pay_slip, cid, "pay_slip")
        payload["pay_slip"] = pay_slip_path
    
    return await apply_loan('personal_loans', cid, payload, settings['personal_loan_interest'])

@router.post('/apply-vehicle-loan', response_model=LoanApplyResponse)
async def apply_vehicle(
    bank_account_number: int = Form(...),
    full_name: str = Form(...),
    pan_number: Optional[str] = Form(None),
    loan_amount: float = Form(...),
    loan_purpose: str = Form(...),
    salary_income: float = Form(...),
    monthly_avg_balance: float = Form(...),
    tenure_months: int = Form(...),
    vehicle_type: VechicleType = Form(...),
    vehicle_model: str = Form(...),
    guarantor_name: Optional[str] = Form(None),
    guarantor_phone: Optional[str] = Form(None),
    guarantor_pan: Optional[str] = Form(None),
    pay_slip: UploadFile = File(None),
    vehicle_price_doc: UploadFile = File(None),
    user=Depends(require_roles(Roles.CUSTOMER)),
):
    settings = await get_settings()
    cid = user.get("customer_id") or user.get("_id")
    
    payload = {
        "bank_account_number": bank_account_number,
        "full_name": full_name,
        "pan_number": pan_number,
        "loan_amount": loan_amount,
        "loan_purpose": loan_purpose,
        "salary_income": salary_income,
        "monthly_avg_balance": monthly_avg_balance,
        "tenure_months": tenure_months,
        "vehicle_type": vehicle_type,
        "vehicle_model": vehicle_model,
        "guarantor_name": guarantor_name,
        "guarantor_phone": guarantor_phone,
        "guarantor_pan": guarantor_pan,
    }
    if pay_slip is not None:
        pay_slip_id = await upload_document(
        pay_slip,
        cid,              # âœ… customer_id ONLY
        "pay_slip"        # âœ… exact doc_type
    )
        payload["pay_slip"] = pay_slip_id

    if vehicle_price_doc is not None:
        vehicle_price_id = await upload_document(
        vehicle_price_doc,
        cid,                   # âœ… customer_id ONLY
        "vehicle_price_doc"    # âœ… exact doc_type
    )
        payload["vehicle_price_doc"] = vehicle_price_id

    
    return await apply_loan('vehicle_loans', cid, payload, settings['vehicle_loan_interest'])


@router.post('/apply-education-loan', response_model=LoanApplyResponse)
async def apply_education(
    bank_account_number: int = Form(...),
    full_name: str = Form(...),
    pan_number: Optional[str] = Form(None),
    college_details: str = Form(...),
    course_details: str = Form(...),
    loan_amount: float = Form(...),
    tenure_months: int = Form(...),
    guarantor_name: Optional[str] = Form(None),
    guarantor_phone: Optional[str] = Form(None),
    guarantor_pan: Optional[str] = Form(None),
    collateral: Optional[str] = Form(None),
    pay_slip: UploadFile = File(None),
    fees_structure: UploadFile = File(...),
    bonafide_certificate: UploadFile = File(...),
    collateral_doc: UploadFile = File(None),
    user=Depends(require_roles(Roles.CUSTOMER)),
):
    settings = await get_settings()
    cid = user.get("customer_id") or user.get("_id")

    payload = {
        "bank_account_number": bank_account_number,
        "full_name": full_name,
        "pan_number": pan_number,
        "college_details": college_details,
        "course_details": course_details,
        "loan_amount": loan_amount,
        "loan_purpose": "Education",
        "salary_income": 0,
        "monthly_avg_balance": 0,
        "tenure_months": tenure_months,
        "guarantor_name": guarantor_name,
        "guarantor_phone": guarantor_phone,
        "guarantor_pan": guarantor_pan,
        "collateral": collateral,
    }

    payload["fees_structure"] = await upload_document(fees_structure, cid, "fees_structure")
    payload["bonafide_certificate"] = await upload_document(bonafide_certificate, cid, "bonafide_certificate")
    if pay_slip is not None:
        payload["pay_slip"] = await upload_document(pay_slip, cid, "pay_slip")

    if collateral_doc is not None:
        payload["collateral_doc"] = await upload_document(collateral_doc, cid, "collateral_doc")

    return await apply_loan(
        'education_loans',
        cid,
        payload,
        float(settings.get('education_loan_interest', settings.get('personal_loan_interest', 12.0))),
    )


@router.post('/apply-home-loan', response_model=LoanApplyResponse)
async def apply_home(
    bank_account_number: int = Form(...),
    full_name: str = Form(...),
    pan_number: Optional[str] = Form(None),
    loan_amount: float = Form(...),
    loan_purpose: str = Form(...),
    salary_income: float = Form(...),
    monthly_avg_balance: float = Form(...),
    tenure_months: int = Form(...),
    property_type: PropertyType = Form(...),
    property_address: str = Form(...),
    property_value: float = Form(...),
    down_payment: float = Form(...),
    guarantor_name: Optional[str] = Form(None),
    guarantor_phone: Optional[str] = Form(None),
    guarantor_pan: Optional[str] = Form(None),
    pay_slip: UploadFile = File(None),
    home_property_doc: UploadFile = File(...),
    user=Depends(require_roles(Roles.CUSTOMER)),
):
    settings = await get_settings()
    cid = user.get("customer_id") or user.get("_id")

    payload = {
        "bank_account_number": bank_account_number,
        "full_name": full_name,
        "pan_number": pan_number,
        "loan_amount": loan_amount,
        "loan_purpose": loan_purpose,
        "salary_income": salary_income,
        "monthly_avg_balance": monthly_avg_balance,
        "tenure_months": tenure_months,
        "property_type": property_type.value,
        "property_address": property_address,
        "property_value": property_value,
        "down_payment": down_payment,
        "guarantor_name": guarantor_name,
        "guarantor_phone": guarantor_phone,
        "guarantor_pan": guarantor_pan,
    }

    if pay_slip is not None:
        payload["pay_slip"] = await upload_document(pay_slip, cid, "pay_slip")

    payload["home_property_doc"] = await upload_document(home_property_doc, cid, "home_property_doc")

    return await apply_loan(
        'home_loans',
        cid,
        payload,
        float(settings.get('home_loan_interest', settings.get('personal_loan_interest', 12.0))),
    )

@router.get('/loans')
async def customer_loans(user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await list_customer_loans(cid)

@router.get("/loans/{loan_id}/emi-details")
async def loan_emi_details(loan_id: str, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await get_customer_emi_details(loan_id, cid)


@router.post('/pay-emi/{loan_id}')
async def pay_emi_by_id(loan_id: str, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await pay_emi_any_wallet(loan_id, cid)


@router.get('/loans/{loan_id}/settlement')
async def get_settlement(loan_id: str, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await calculate_settlement_any(loan_id, cid)


@router.post('/loans/{loan_id}/foreclose')
async def foreclose_loan_route(loan_id: str, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    return await foreclose_any(loan_id, cid)

@router.get("/loans/{loan_id}/noc")
async def download_loan_noc(loan_id: str, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    noc = await get_customer_noc(loan_id, cid)
    document_id = noc.get("document_id")
    if not document_id:
        raise HTTPException(status_code=404, detail="NOC document not available")
    doc = await get_document_binary(str(document_id))
    return StreamingResponse(
        io.BytesIO(doc["data"]),
        media_type=doc["content_type"],
        headers={"Content-Disposition": f'inline; filename="{doc.get("filename") or f"loan_noc_{loan_id}.pdf"}"'},
    )


@router.get("/loans/{loan_id}/sanction-letter")
async def download_sanction_letter(loan_id: str, user=Depends(require_roles(Roles.CUSTOMER))):
    cid = user.get("customer_id") or user.get("_id")
    db = await get_db()
    from ...utils.id import loan_id_filter
    filt = loan_id_filter(loan_id)
    filt["customer_id"] = cid

    loan = await db.personal_loans.find_one(filt)
    if not loan:
        loan = await db.vehicle_loans.find_one(filt)
    if not loan:
        loan = await db.education_loans.find_one(filt)
    if not loan:
        loan = await db.home_loans.find_one(filt)

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    doc_id = loan.get("sanction_letter_document_id")
    if not doc_id:
        raise HTTPException(status_code=404, detail="Sanction letter not generated yet")

    doc = await get_document_binary(str(doc_id))
    return StreamingResponse(
        io.BytesIO(doc["data"]),
        media_type=doc["content_type"],
        headers={"Content-Disposition": f'inline; filename="{doc["filename"]}"'},
    )


@router.post("/loans/{loan_id}/sanction-letter/upload")
async def upload_signed_sanction_letter_route(
    loan_id: str,
    signed_sanction_letter: UploadFile = File(...),
    user=Depends(require_roles(Roles.CUSTOMER)),
):
    cid = user.get("customer_id") or user.get("_id")
    doc_id = await upload_document(signed_sanction_letter, cid, "signed_sanction_letter")
    return await upload_signed_sanction_letter(loan_id, cid, doc_id)




``n
# File: services/loan-service/app/schemas/loan.py
`python
from pydantic import BaseModel, Field
from typing import Optional


class ApplyPersonalLoan(BaseModel):
    bank_account_number: str = Field(
        ...,
        min_length=9,
        max_length=18,
        pattern=r"^\d+$"
    )

    full_name: str = Field(..., min_length=3, max_length=100)

    pan_number: str = Field(
        ...,
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    )

    loan_amount: float = Field(
        ...,
        gt=0,
        le=50_000_000
    )

    loan_purpose: str = Field(
        ...,
        min_length=5,
        max_length=200
    )

    salary_income: float = Field(
        ...,
        ge=0,
        le=10_000_000
    )

    monthly_avg_balance: float = Field(
        ...,
        ge=0
    )

    tenure_months: int = Field(
        ...,
        ge=6,
        le=360
    )

    pay_slip: Optional[str] = Field(None, max_length=100)

    guarantor_name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100
    )

    guarantor_phone: Optional[str] = Field(
        None,
        pattern=r"^\+?\d{10,15}$"
    )

    guarantor_pan: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    )

class ApplyVehicleLoan(ApplyPersonalLoan):
    vehicle_type: str = Field(
        ...,
        pattern=r"(?i)^(two-wheeler|four-wheeler|commercial)$"
    )

    vehicle_model: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    vehicle_price_doc: Optional[str] = Field(None, max_length=100)


class ApplyEducationLoan(BaseModel):
    bank_account_number: str = Field(..., min_length=9, max_length=18, pattern=r"^\d+$")
    full_name: str = Field(..., min_length=3, max_length=100)
    pan_number: str = Field(..., pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$")
    college_details: str = Field(..., min_length=3, max_length=300)
    course_details: str = Field(..., min_length=3, max_length=300)
    loan_amount: float = Field(..., gt=0, le=50_000_000)
    tenure_months: int = Field(..., ge=6, le=360)
    guarantor_name: Optional[str] = Field(None, min_length=3, max_length=100)
    guarantor_phone: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")
    guarantor_pan: Optional[str] = Field(None, pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$")
    collateral: Optional[str] = Field(None, max_length=200)
    fees_structure: Optional[str] = Field(None, max_length=100)
    bonafide_certificate: Optional[str] = Field(None, max_length=100)
    collateral_doc: Optional[str] = Field(None, max_length=100)


class ApplyHomeLoan(ApplyPersonalLoan):
    property_type: str = Field(..., max_length=60)
    property_address: str = Field(..., min_length=3, max_length=300)
    property_value: float = Field(..., gt=0)
    down_payment: float = Field(..., ge=0)
    home_property_doc: Optional[str] = Field(None, max_length=100)


class LoanOut(BaseModel):
    id: str = Field(alias="_id")
    loan_amount: float
    tenure_months: int
    remaining_tenure: int
    emi_per_month: float
    remaining_amount: float
    status: str

class LoanApplyResponse(BaseModel):
    message: str
    loan_id: int
    status: str
    emi_per_month: float
    tenure_months: int


class LoanApprovalResponse(BaseModel):
    message: str
    loan_id: int
    status: str

``n
# File: services/verification-service/app/routers/verification/service.py
`python
from ...database.mongo import get_db
from ...services.kyc_service import get_verification_dashboard, verify_kyc, get_kyc_by_customer
from ...services.loan_service import verification_complete
from ...services.document_service import get_document_binary


``n
# File: lms_backend/app/services/loan_service.py
`python
from .loan.admin import admin_final_approve, admin_reject, disburse, mark_signed_received, send_sanction
from .loan.applications import apply_loan
from .loan.calculations import compute_emi
from .loan.customer import (
    get_customer_emi_details,
    list_customer_loans,
    pay_emi,
    pay_emi_any,
    pay_emi_any_wallet,
    pay_emi_any_gateway,
)
from .loan.documents import attach_loan_document, upload_signed_sanction_letter
from .loan.eligibility import compute_customer_eligibility
from .loan.manager import (
    list_manager_loans,
    manager_approve_or_reject,
    manager_forward_to_admin,
    manager_verify_signed_sanction,
)
from .loan.noc import get_customer_noc
from .loan.queries import _find_loan_any, _find_loan_any_by_customer
from .loan.settlement import calculate_settlement_admin, calculate_settlement_any, foreclose_any, manager_foreclose_any
from .loan.verification import assign_verification, verification_complete

__all__ = [
    "admin_final_approve",
    "admin_reject",
    "apply_loan",
    "assign_verification",
    "attach_loan_document",
    "calculate_settlement_admin",
    "calculate_settlement_any",
    "compute_customer_eligibility",
    "compute_emi",
    "disburse",
    "foreclose_any",
    "get_customer_emi_details",
    "get_customer_noc",
    "list_customer_loans",
    "list_manager_loans",
    "manager_approve_or_reject",
    "manager_foreclose_any",
    "manager_forward_to_admin",
    "manager_verify_signed_sanction",
    "mark_signed_received",
    "pay_emi",
    "pay_emi_any",
    "pay_emi_any_wallet",
    "pay_emi_any_gateway",
    "send_sanction",
    "upload_signed_sanction_letter",
    "verification_complete",
    # Backward-compatible internal helpers
    "_find_loan_any",
    "_find_loan_any_by_customer",
]

``n
# File: lms_backend/app/services/loan/verification.py
`python
from datetime import datetime

from fastapi import HTTPException

from ...database.mongo import get_db
from ...models.enums import LoanStatus
from ...utils.id import loan_id_filter

from ..audit_service import write_audit_log
from .actor_meta import resolve_actor_meta


# =========================
# ASSIGN TO VERIFICATION
# =========================
async def assign_verification(
    loan_collection: str,
    loan_id: str,
    verification_id: str,
    assigned_by_id: str | int | None = None,
):
    db = await get_db()
    filt = loan_id_filter(loan_id)
    now = datetime.utcnow()
    assigned_by = await resolve_actor_meta(assigned_by_id, fallback_role="manager")
    assigned_to = await resolve_actor_meta(verification_id, fallback_role="verification")

    await db[loan_collection].update_one(
        filt,
        {"$set": {
            "verification_id": verification_id,
            "status": LoanStatus.ASSIGNED_TO_VERIFICATION,
            "verification_assigned_at": now,
            "verification_assigned_by_id": assigned_by["actor_id"],
            "verification_assigned_by_name": assigned_by["actor_name"],
            "verification_assigned_by_role": assigned_by["actor_role"],
            "verification_assigned_to_id": assigned_to["actor_id"],
            "verification_assigned_to_name": assigned_to["actor_name"],
            "verification_assigned_to_role": assigned_to["actor_role"],
        }}
    )
    return {"message": "Loan assigned to verification team"}


# =========================
# VERIFICATION COMPLETE
# =========================
async def verification_complete(
    loan_collection: str,
    loan_id: str,
    approved: bool,
    verified_by_id: str | int | None = None,
):
    db = await get_db()
    filt = loan_id_filter(loan_id)
    loan = await db[loan_collection].find_one(filt)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.get("status") != LoanStatus.ASSIGNED_TO_VERIFICATION:
        raise HTTPException(status_code=400, detail="Loan not assigned to verification")

    now = datetime.utcnow()
    verifier = await resolve_actor_meta(verified_by_id or loan.get("verification_id"), fallback_role="verification")

    if approved:
        await db[loan_collection].update_one(
            filt,
            {"$set": {
                "status": LoanStatus.VERIFICATION_DONE,
                "verification_completed_at": now,
                "verification_completed_by_id": verifier["actor_id"],
                "verification_completed_by_name": verifier["actor_name"],
                "verification_completed_by_role": verifier["actor_role"],
            }}
        )
        await write_audit_log(
            action="loan_verification_approve",
            actor_role="verification",
            actor_id=verifier["actor_id"],
            entity_type="loan",
            entity_id=loan.get("loan_id"),
            details={"loan_collection": loan_collection},
        )
        return {
            "message": "Loan verified successfully",
            "loan_id": int(loan_id),
            "status": LoanStatus.VERIFICATION_DONE
        }
    else:
        await db[loan_collection].update_one(
            filt,
            {
                "$set": {
                    "status": LoanStatus.REJECTED,
                    "verification_completed_at": now,
                    "rejected_by": "verification",
                    "rejected_at": now,
                    "rejected_by_id": verifier["actor_id"],
                    "rejected_by_name": verifier["actor_name"],
                    "rejected_by_role": verifier["actor_role"],
                    "verification_completed_by_id": verifier["actor_id"],
                    "verification_completed_by_name": verifier["actor_name"],
                    "verification_completed_by_role": verifier["actor_role"],
                }
            }
        )
        await write_audit_log(
            action="loan_verification_reject",
            actor_role="verification",
            actor_id=verifier["actor_id"],
            entity_type="loan",
            entity_id=loan.get("loan_id"),
            details={"loan_collection": loan_collection},
        )
        return {
            "message": "Loan rejected during verification",
            "loan_id": int(loan_id),
            "status": LoanStatus.REJECTED
        }

``n
# File: services/verification-service/app/services/verification_service.py
`python

# placeholder for future shared verification checks

``n
# File: services/loan-service/app/main.py
`python
from fastapi import FastAPI
from app.core.config import settings
from app.database.mongo import connect_db, close_db

# âœ… FIX 1: Use correct attribute name
from app.routers.customer.router import router as customer_router

from app.middleware.idempotency import IdempotencyMiddleware

app = FastAPI(title=settings.SERVICE_NAME + " API")
app.add_middleware(IdempotencyMiddleware)

app.include_router(customer_router, prefix="/customer")


@app.on_event("startup")
async def startup_db_client():
    await connect_db()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": (settings.SERVICE_NAME or "loan-service"), "version": "1.0.0"}
``n
