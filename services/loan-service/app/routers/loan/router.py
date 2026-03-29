"""
services/loan-service/app/routers/loan/router.py
Internal routes called by other microservices (not the frontend).
"""
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from ...core.config import settings
from ...database.mongo import get_db
from ...utils.serializers import normalize_doc

router = APIRouter(prefix="/internal", tags=["internal"])


class VerificationCompletePayload(BaseModel):
    loan_collection: str
    loan_id: str
    approved: bool
    verifier_id: str


@router.post("/verification-complete")
async def verification_complete(
    payload: VerificationCompletePayload,
    x_internal_token: str = Header(..., alias="X-Internal-Token"),
):
    if x_internal_token != settings.INTERNAL_SERVICE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid internal token")

    db = await get_db()
    collection_map = {
        "personal_loans": db.personal_loans,
        "vehicle_loans": db.vehicle_loans,
        "education_loans": db.education_loans,
        "home_loans": db.home_loans,
    }
    collection = collection_map.get(payload.loan_collection)
    # FIX: PyMongo collections cannot be tested with bool() — use `is None`
    if collection is None:
        raise HTTPException(status_code=400, detail=f"Unknown loan collection: {payload.loan_collection}")

    loan = None
    try:
        loan = await collection.find_one({"loan_id": int(payload.loan_id)})
    except (ValueError, TypeError):
        pass
    if not loan:
        loan = await collection.find_one({"loan_id": payload.loan_id})
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    new_status = "verified" if payload.approved else "verification_rejected"
    await collection.update_one(
        {"_id": loan["_id"]},
        {
            "$set": {
                "status": new_status,
                "verified_by": payload.verifier_id,
                "verification_approved": payload.approved,
            }
        },
    )
    updated = await collection.find_one({"_id": loan["_id"]})
    return normalize_doc(updated)