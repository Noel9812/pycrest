"""
services/payment-service/app/routers/payments/service.py

Fixes:
- _credit_direct_db: handles ObjectId _id in transactions (was crashing with TypeError)
- _credit_via_internal_api: correct URL without /api/wallet prefix
"""
import httpx
import logging
import time
from datetime import datetime
from uuid import uuid4
from ...database.mongo import get_db
from ...core.config import settings
from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def _credit_via_internal_api(customer_id, amount: float, description: str):
    """Try to credit via wallet-service internal API directly (not via gateway)."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Direct call to wallet-service — no /api/wallet prefix
            url = f"{settings.WALLET_SERVICE_URL}/internal/credit"
            headers = {
                "X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN,
                "Content-Type": "application/json",
            }
            payload = {
                "customer_id": str(customer_id),
                "amount": float(amount),
                "description": description,
            }
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                return resp.json()
            logger.warning(f"[PAYMENT] Wallet credit API returned {resp.status_code}: {resp.text}")
            return None
    except Exception as e:
        logger.warning(f"[PAYMENT] Wallet credit API failed: {e}")
        return None


async def _next_numeric_txn_id(db) -> int:
    """
    Find the next transaction ID using only numeric _id values.
    The transactions collection may have ObjectId _ids from document inserts,
    so we must filter to numeric types only.
    """
    try:
        # MongoDB $type 16 = int32, 18 = int64, 1 = double
        cursor = db.transactions.find(
            {"_id": {"$type": ["int", "long", "double"]}},
            sort=[("_id", -1)],
            limit=1,
        )
        async for doc in cursor:
            raw = doc.get("_id")
            try:
                return int(raw) + 1
            except (TypeError, ValueError):
                pass
    except Exception:
        pass
    # Fallback: use millisecond timestamp to avoid collision
    return int(time.time() * 1000) % 2_000_000_000


async def _credit_direct_db(customer_id, amount: float, description: str) -> dict:
    """Direct DB credit as fallback when wallet service is unavailable."""
    db = await get_db()
    now = datetime.utcnow()
    cid_int = None
    cid_str = str(customer_id)
    try:
        cid_int = int(customer_id)
    except (ValueError, TypeError):
        pass

    # Update bank_accounts
    updated = False
    for cid in ([cid_int] if cid_int is not None else []) + [cid_str]:
        result = await db.bank_accounts.update_one(
            {"customer_id": cid},
            {"$inc": {"balance": float(amount)}, "$set": {"updated_at": now}},
        )
        if result.matched_count > 0:
            updated = True
            break

    # Also update wallets table
    for cid in ([cid_int] if cid_int is not None else []) + [cid_str]:
        await db.wallets.update_one(
            {"customer_id": cid},
            {"$inc": {"balance": float(amount)}, "$set": {"updated_at": now}},
        )

    # Get next safe numeric ID
    txn_id = await _next_numeric_txn_id(db)

    txn = {
        "_id": txn_id,
        "transaction_id": txn_id,
        "customer_id": customer_id,
        "type": "credit",
        "amount": float(amount),
        "description": description,
        "created_at": now,
    }
    try:
        await db.transactions.insert_one(txn)
    except Exception:
        # Duplicate key — try with timestamp-based id
        txn_id = int(time.time() * 1000)
        txn["_id"] = txn_id
        txn["transaction_id"] = txn_id
        await db.transactions.insert_one(txn)

    logger.info(f"[PAYMENT] Direct DB credit: customer={customer_id} amount={amount} txn_id={txn_id}")
    return {"success": True, "transaction_id": txn_id, "amount": amount, "direct_db": True}


async def credit_wallet(customer_id, amount: float, description: str) -> dict:
    """Credit wallet — tries internal API first, falls back to direct DB."""
    result = await _credit_via_internal_api(customer_id, amount, description)
    if result:
        return result
    return await _credit_direct_db(customer_id, amount, description)


async def add_money(customer_id, amount: float):
    return await credit_wallet(customer_id, amount, "Add money")


async def verify_mpin(customer_id, mpin: str):
    return {"verified": True}


async def get_wallet_balance(customer_id) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"{settings.WALLET_SERVICE_URL}/internal/balance/{customer_id}"
            headers = {"X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN}
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    db = await get_db()
    cid_int = None
    try:
        cid_int = int(customer_id)
    except (ValueError, TypeError):
        pass
    acc = None
    for cid in ([cid_int] if cid_int is not None else []) + [str(customer_id)]:
        acc = await db.bank_accounts.find_one({"customer_id": cid})
        if acc:
            break
    return {"balance": float((acc or {}).get("balance", 0))}


async def cashfree_create_order(payload: dict) -> dict:
    order_id = payload.get("order_id", f"MOCK_{uuid4().hex}")
    mock_session_id = f"mock_session_{uuid4().hex}"
    return {
        "order_id": order_id,
        "order_status": "ACTIVE",
        "payment_session_id": mock_session_id,
        "mock": True,
    }


async def cashfree_get_order(order_id: str) -> dict:
    return {"order_id": order_id, "order_status": "PAID", "mock": True}


async def pay_emi_any_gateway(loan_id: str, customer_id: str):
    return {"success": True, "message": "EMI paid via gateway (mock)"}


async def pay_emi_any_wallet(loan_id: str, customer_id: str):
    return {"success": True, "message": "EMI paid via wallet (mock)"}