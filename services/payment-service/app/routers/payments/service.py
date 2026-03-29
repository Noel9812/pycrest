import httpx
from ...database.mongo import get_db
from ...core.config import settings
from fastapi import HTTPException

async def _wallet_call(method: str, path: str, json: dict = None):
    """Internal M2M call to Wallet Service."""
    async with httpx.AsyncClient() as client:
        url = f"{settings.WALLET_SERVICE_URL}{path}"
        headers = {"Authorization": f"Bearer {settings.INTERNAL_SERVICE_TOKEN}"}
        try:
            resp = await client.request(method, url, json=json, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Wallet service communication error: {str(e)}")

async def credit_wallet(customer_id: str | int, amount: float, description: str):
    return await _wallet_call("POST", "/internal/credit", json={
        "customer_id": str(customer_id),
        "amount": amount,
        "description": description
    })

async def verify_mpin(customer_id: str | int, mpin: str):
    """Verify customer M-PIN via Wallet Service."""
    # We use the public verify endpoint but call it internally
    return await _wallet_call("POST", "/mpin/verify", json={
        "customer_id": str(customer_id),
        "mpin": mpin
    })

async def get_wallet_balance(customer_id: str | int):
    return await _wallet_call("GET", f"/admin/customer/{customer_id}/balance")

async def add_money(customer_id: str | int, amount: float):
    return await credit_wallet(customer_id, amount, "Add money")

# --- PLACEHOLDERS FOR BROKEN SERVICE IMPORTS ---
# These should ideally call their respective microservices or have logic here

async def cashfree_create_order(payload: dict):
    # Basic placeholder for Cashfree order creation
    return {"order_id": payload.get("order_id"), "status": "created", "payment_session_id": "dummy_session"}

async def cashfree_get_order(order_id: str):
    # Basic placeholder for Cashfree order status
    return {"order_id": order_id, "order_status": "PAID"}

async def pay_emi_any_gateway(loan_id: str, customer_id: str):
    # This should call the EMI service /loans/pay endpoint
    return {"success": True, "message": "EMI Paid via Gateway (Simulated)"}

async def pay_emi_any_wallet(loan_id: str, customer_id: str):
    # This should call the EMI service /loans/pay endpoint
    return {"success": True, "message": "EMI Paid via Wallet (Simulated)"}
