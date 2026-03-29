# loan-service/app/services/wallet_service.py
#
# loan/customer.py imports debit_wallet from here to deduct EMI payments
# from a customer's wallet. In microservices this must be an HTTP call
# to wallet-service rather than a direct DB operation.

import httpx
from fastapi import HTTPException
from ..core.config import settings


async def debit_wallet(customer_id, amount: float, description: str = "EMI payment") -> dict:
    """
    Debit the customer's wallet for EMI payment.
    Calls wallet-service via HTTP instead of touching the DB directly.
    """
    url = f"{settings.WALLET_SERVICE_URL}/api/wallet/internal/debit"
    payload = {
        "customer_id": str(customer_id),
        "amount": float(amount),
        "description": description,
    }
    headers = {
        "X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN,
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=f"wallet-service debit error: {response.text}",
            )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="wallet-service is unavailable")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="wallet-service timed out")


async def get_wallet_balance(customer_id) -> float:
    """Get customer wallet balance from wallet-service."""
    url = f"{settings.WALLET_SERVICE_URL}/api/wallet/internal/balance/{customer_id}"
    headers = {"X-Internal-Token": settings.INTERNAL_SERVICE_TOKEN}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return float(data.get("balance", 0))
            return 0.0
    except Exception:
        return 0.0