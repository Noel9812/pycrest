from __future__ import annotations
from datetime import datetime
from fastapi import HTTPException
from ...database.mongo import get_db
from ...utils.dates import next_month_date
from ...utils.serializers import normalize_doc
from .constants import EMI_STATUS_OVERDUE, EMI_STATUS_PAID, EMI_STATUS_PENDING


async def ensure_emi_schedule_generated(loan_id, loan_type: str, loan_doc: dict) -> list:
    """
    Generate EMI schedule for a loan if not already created.
    Returns list of EMI instalment documents.
    """
    db = await get_db()
    existing = await db.emi_schedules.find({"loan_id": loan_id}).to_list(length=500)
    if existing:
        return [normalize_doc(e) for e in existing]

    tenure = int(loan_doc.get("tenure_months") or loan_doc.get("loan_tenure_months") or 0)
    emi_amount = float(loan_doc.get("emi_amount") or loan_doc.get("monthly_emi") or 0)
    customer_id = loan_doc.get("customer_id")
    disbursed_at = loan_doc.get("disbursed_at") or loan_doc.get("approved_at") or datetime.utcnow()

    if not tenure or not emi_amount:
        return []

    schedule = []
    due_date = next_month_date(disbursed_at)
    for i in range(1, tenure + 1):
        doc = {
            "loan_id": loan_id,
            "loan_type": loan_type,
            "customer_id": customer_id,
            "instalment_number": i,
            "due_date": due_date,
            "emi_amount": emi_amount,
            "principal_component": 0.0,
            "interest_component": 0.0,
            "penalty_amount": 0.0,
            "status": EMI_STATUS_PENDING,
            "paid_at": None,
            "created_at": datetime.utcnow(),
        }
        schedule.append(doc)
        due_date = next_month_date(due_date)

    if schedule:
        await db.emi_schedules.insert_many(schedule)

    return [normalize_doc(d) for d in schedule]


async def pay_next_installment(loan_id, loan_type: str, customer_id) -> dict:
    """
    Mark the next pending EMI instalment as paid.
    Debit is handled by the calling layer (wallet_service).
    """
    db = await get_db()
    instalment = await db.emi_schedules.find_one(
        {"loan_id": loan_id, "status": {"$in": [EMI_STATUS_PENDING, EMI_STATUS_OVERDUE]}},
        sort=[("instalment_number", 1)],
    )
    if not instalment:
        raise HTTPException(status_code=404, detail="No pending EMI instalment found")

    await db.emi_schedules.update_one(
        {"_id": instalment["_id"]},
        {"$set": {"status": EMI_STATUS_PAID, "paid_at": datetime.utcnow()}},
    )
    updated = await db.emi_schedules.find_one({"_id": instalment["_id"]})
    return normalize_doc(updated)


async def refresh_overdue(db=None) -> dict:
    """Mark all past-due pending EMIs as overdue."""
    if db is None:
        db = await get_db()
    now = datetime.utcnow()
    result = await db.emi_schedules.update_many(
        {"status": EMI_STATUS_PENDING, "due_date": {"$lt": now}},
        {"$set": {"status": EMI_STATUS_OVERDUE}},
    )
    return {"updated": result.modified_count}


async def refresh_escalations(db=None) -> dict:
    """Placeholder — escalation logic lives in emi-service."""
    return {"status": "ok", "escalated": 0}