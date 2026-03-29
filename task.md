# Paycrest Microservices Remediation — Task Status

## Phase 1 — Routing Fixes (Critical)
- [x] **Fix 1.1: Remove recursive prefixes**
    - Removed `/manager`, `/payments`, `/verification`, `/wallet`, `/transactions` prefixes from `APIRouter` in respective services to align with API Gateway path stripping.
- [x] **Fix 1.2: EMI routing void**
    - Updated `api-gateway/server.js` to prioritize `/api/admin/emi` routing to the `emi-service`.
- [x] **Fix 1.3: Loan service explicit prefix**
    - Updated `loan-service/app/main.py` to use an explicit `/customer` prefix.

## Phase 2 — Security & Reliability
- [x] **Fix 2.1: IdempotencyMiddleware Registration**
    - Registered `IdempotencyMiddleware` in all 8 microservices (`admin`, `auth`, `emi`, `loan`, `manager`, `payment`, `verification`, `wallet`).
- [x] **Fix 2.2: Roles Enum Standardization**
    - Standardized `Roles` to inherit from `(str, Enum)` in all 8 microservices to ensure case-insensitive JWT claim matching.
- [x] **Fix 2.3: M2M httpx Calls**
    - Refactored `payment-service` and `emi-service` to use `httpx.AsyncClient` for `wallet-service` communication.
    - Added `INTERNAL_SERVICE_TOKEN` and `WALLET_SERVICE_URL` to settings and `.env.example`.
    - Added `POST /internal/credit` and `POST /internal/debit` endpoints to `wallet-service`.

## Phase 3 — Data Contracts & Storage
- [x] **Fix 3.1: RegisterResponse Alignment**
    - Restored `full_name` to `RegisterResponse` schema and auth router return value.
- [x] **Fix 3.2: Shared Upload Path**
    - Migrated `loan-service` and `verification-service` document storage from MongoDB Binary to local filesystem using `settings.UPLOAD_BASE_PATH`.
    - Added `UPLOAD_BASE_PATH` to configuration.

## Phase 4 — Cleanup & Standardization
- [x] **Fix 4.1: Health Check Standardization**
    - Standardized `/health` response across all 8 microservices to return `{"status": "ok", "service": "...", "version": "1.0.0"}`.

---

### Infrastructure Requirements (Action Required)
- **Shared Volume**: Deployment environment must mount a shared volume at the path specified in `UPLOAD_BASE_PATH` (default `./uploads`) across all microservice containers to allow cross-service document access.
- **M2M Secret**: `INTERNAL_SERVICE_TOKEN` must be generated and added to all `.env` files.
