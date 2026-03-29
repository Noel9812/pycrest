from fastapi import FastAPI
from app.core.config import settings
from app.database.mongo import connect_db, close_db

# ✅ FIX 1: Use correct attribute name
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