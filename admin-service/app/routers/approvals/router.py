"""
services/admin-service/app/routers/approvals/router.py
"""
import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.core.security import require_roles
from app.database.mongo import get_db
from app.models.enums import LoanCollection, LoanStatus, Roles
from app.schemas.settings import SystemSettingsUpdate
from app.routers.schemas import AdminApprovePayload, AdminRejectPayload
from app.services.admin_service import (
    find_loan_any,
    get_admin_approvals_dashboard,
    list_high_value_pending,
    list_pending_admin_approvals,
    list_ready_for_disbursement,
    ADMIN_QUEUE_STATUSES,
)
from app.services.settings_service import get_settings, update_settings
from app.utils.id import loan_id_filter
from app.utils.serializers import normalize_doc

router = APIRouter()


def _mask_pan(value: str | None) -> str | None:
    pan = str(value or "").strip().upper()
    if not pan:
        return None
    if len(pan) != 10:
        return pan
    return f"{pan[:2]}******{pan[-2:]}"


def _sanitize_loan_doc(doc: dict) -> dict:
    out = normalize_doc(doc)
    if not out.get("pan_masked"):
        out["pan_masked"] = _mask_pan(out.get("pan_number"))
    if not out.get("guarantor_pan_masked"):
        out["guarantor_pan_masked"] = _mask_pan(out.get("guarantor_pan"))
    out.pop("pan_number", None)
    out.pop("guarantor_pan", None)
    out.pop("pan_hash", None)
    out.pop("guarantor_pan_hash", None)
    return out


async def get_document_binary(doc_id: str):
    return {"data": b"", "content_type": "application/octet-stream", "filename": "placeholder.bin"}


async def _find_in_collection(db, collection_name: str, loan_id: str):
    filt = loan_id_filter(loan_id)
    loan = await db[collection_name].find_one(filt)
    if not loan:
        try:
            loan = await db[collection_name].find_one({"loan_id": int(loan_id)})
        except (ValueError, TypeError):
            pass
    return loan


async def _admin_approve(collection_name, loan_id, admin_id, approved_amount=None, interest_rate=None):
    db = await get_db()
    loan = await _find_in_collection(db, collection_name, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    update = {"status": LoanStatus.ADMIN_APPROVED, "admin_id": str(admin_id), "approved_at": datetime.utcnow()}
    if approved_amount is not None:
        update["approved_amount"] = float(approved_amount)
    if interest_rate is not None:
        update["interest_rate"] = float(interest_rate)
    await db[collection_name].update_one({"_id": loan["_id"]}, {"$set": update})
    return normalize_doc(await db[collection_name].find_one({"_id": loan["_id"]}))


async def _admin_reject(collection_name, loan_id, admin_id, reason: str):
    db = await get_db()
    loan = await _find_in_collection(db, collection_name, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    await db[collection_name].update_one(
        {"_id": loan["_id"]},
        {"$set": {"status": LoanStatus.REJECTED, "admin_id": str(admin_id),
                  "rejection_reason": reason, "rejected_at": datetime.utcnow()}},
    )
    return normalize_doc(await db[collection_name].find_one({"_id": loan["_id"]}))


async def _send_sanction(collection_name, loan_id, admin_id):
    db = await get_db()
    loan = await _find_in_collection(db, collection_name, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    await db[collection_name].update_one(
        {"_id": loan["_id"]},
        {"$set": {"status": LoanStatus.SANCTION_SENT, "admin_id": str(admin_id),
                  "sanction_sent_at": datetime.utcnow()}},
    )
    return normalize_doc(await db[collection_name].find_one({"_id": loan["_id"]}))


async def _mark_signed(collection_name, loan_id, admin_id):
    db = await get_db()
    loan = await _find_in_collection(db, collection_name, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    await db[collection_name].update_one(
        {"_id": loan["_id"]},
        {"$set": {"status": LoanStatus.SIGNED_RECEIVED, "admin_id": str(admin_id),
                  "signed_received_at": datetime.utcnow()}},
    )
    return normalize_doc(await db[collection_name].find_one({"_id": loan["_id"]}))


async def _disburse(collection_name, loan_id, admin_id):
    db = await get_db()
    loan = await _find_in_collection(db, collection_name, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    await db[collection_name].update_one(
        {"_id": loan["_id"]},
        {"$set": {"status": LoanStatus.ACTIVE, "admin_id": str(admin_id),
                  "disbursed_at": datetime.utcnow()}},
    )
    return normalize_doc(await db[collection_name].find_one({"_id": loan["_id"]}))


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/pending-approvals")
async def pending(user=Depends(require_roles(Roles.ADMIN))):
    return await list_pending_admin_approvals()


@router.get("/approvals-dashboard")
async def approvals_dashboard(days: int = 30, user=Depends(require_roles(Roles.ADMIN))):
    return await get_admin_approvals_dashboard(days=days)


@router.get("/dashboard")
async def dashboard(user=Depends(require_roles(Roles.ADMIN))):
    db = await get_db()
    pending_count = 0
    ready_count = 0
    active_count = 0
    for col in ["personal_loans", "vehicle_loans", "education_loans", "home_loans"]:
        pending_count += await db[col].count_documents({"status": {"$in": ADMIN_QUEUE_STATUSES}, "loan_amount": {"$gt": 1500000}})
        ready_count += await db[col].count_documents({"status": LoanStatus.READY_FOR_DISBURSEMENT})
        active_count += await db[col].count_documents({"status": LoanStatus.ACTIVE})
    from datetime import timedelta
    now = datetime.utcnow()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    disb_today = await db.transactions.find(
        {"type": "disbursement", "created_at": {"$gte": day_start, "$lt": day_start + timedelta(days=1)}}
    ).to_list(length=5000)
    db_ping = True
    try:
        await db.command("ping")
    except Exception:
        db_ping = False
    return {
        "high_value_pending": pending_count,
        "ready_for_disbursement": ready_count,
        "active_loans": active_count,
        "total_disbursements_today": len(disb_today),
        "total_disbursed_amount_today": float(sum(float(t.get("amount") or 0) for t in disb_today)),
        "system_health": {"db_ping": db_ping},
    }


@router.get("/loans/high-value-pending")
async def high_value_pending(user=Depends(require_roles(Roles.ADMIN))):
    return await list_high_value_pending()


@router.get("/loans/ready-for-disbursement")
async def ready_for_disbursement_queue(user=Depends(require_roles(Roles.ADMIN))):
    return await list_ready_for_disbursement()


@router.get("/loans/{loan_id}/review")
async def review_any_loan(loan_id: str, user=Depends(require_roles(Roles.ADMIN))):
    loan_collection, loan = await find_loan_any(loan_id)
    if not loan_collection or not loan:
        return {"error": "Loan not found"}
    return _sanitize_loan_doc(loan)


@router.get("/loans/{loan_id}/documents/{doc_type}")
async def download_loan_document_for_admin(loan_id: str, doc_type: str, user=Depends(require_roles(Roles.ADMIN))):
    loan_collection, loan = await find_loan_any(loan_id)
    if not loan_collection or not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    field_map = {"pay_slip": "pay_slip", "vehicle_price_doc": "vehicle_price_doc",
                 "home_property_doc": "home_property_doc", "fees_structure": "fees_structure",
                 "bonafide_certificate": "bonafide_certificate", "collateral_doc": "collateral_doc"}
    field = field_map.get(doc_type)
    if not field:
        raise HTTPException(status_code=400, detail="Unsupported document type")
    raw_value = loan.get(field)
    if not raw_value:
        raise HTTPException(status_code=404, detail="Document not uploaded")
    if isinstance(raw_value, str) and (raw_value.startswith("http://") or raw_value.startswith("https://") or raw_value.startswith("/")):
        raise HTTPException(status_code=404, detail="Document binary not available")
    doc = await get_document_binary(str(raw_value))
    return StreamingResponse(io.BytesIO(doc["data"]), media_type=doc["content_type"],
                             headers={"Content-Disposition": f'inline; filename="{doc["filename"]}"'})


@router.post("/loans/{loan_id}/approve")
async def approve_high_value(loan_id: str, payload: AdminApprovePayload | None = None, user=Depends(require_roles(Roles.ADMIN))):
    loan_collection, loan = await find_loan_any(loan_id)
    if not loan_collection or not loan:
        return {"error": "Loan not found"}
    return await _admin_approve(loan_collection, loan_id, user["_id"],
                                approved_amount=payload.approved_amount if payload else None,
                                interest_rate=payload.interest_rate if payload else None)


@router.post("/loans/{loan_id}/reject")
async def reject_high_value(loan_id: str, payload: AdminRejectPayload, user=Depends(require_roles(Roles.ADMIN))):
    loan_collection, loan = await find_loan_any(loan_id)
    if not loan_collection or not loan:
        return {"error": "Loan not found"}
    return await _admin_reject(loan_collection, loan_id, user["_id"], payload.reason)


@router.post("/loans/{loan_id}/sanction-letter/generate")
async def generate_sanction_letter(loan_id: str, user=Depends(require_roles(Roles.ADMIN))):
    loan_collection, loan = await find_loan_any(loan_id)
    if not loan_collection or not loan:
        return {"error": "Loan not found"}
    res = await _send_sanction(loan_collection, loan_id, user["_id"])
    return {**res, "download_url": f"/api/customer/loans/{loan.get('loan_id')}/sanction-letter"}


@router.post("/loans/{loan_id}/disburse")
async def disburse_any(loan_id: str, user=Depends(require_roles(Roles.ADMIN))):
    loan_collection, loan = await find_loan_any(loan_id)
    if not loan_collection or not loan:
        return {"error": "Loan not found"}
    return await _disburse(loan_collection, loan_id, user["_id"])


@router.put("/approve/{loan_collection}/{loan_id}")
async def approve_route(loan_collection: LoanCollection, loan_id: str,
                        payload: AdminApprovePayload | None = None, user=Depends(require_roles(Roles.ADMIN))):
    return await _admin_approve(loan_collection.value, loan_id, user["_id"],
                                approved_amount=payload.approved_amount if payload else None,
                                interest_rate=payload.interest_rate if payload else None)


@router.put("/sanction/{loan_collection}/{loan_id}")
async def sanction_route(loan_collection: LoanCollection, loan_id: str, user=Depends(require_roles(Roles.ADMIN))):
    return await _send_sanction(loan_collection.value, loan_id, user["_id"])


@router.put("/signed/{loan_collection}/{loan_id}")
async def signed_route(loan_collection: LoanCollection, loan_id: str, user=Depends(require_roles(Roles.ADMIN))):
    return await _mark_signed(loan_collection.value, loan_id, user["_id"])


@router.put("/disburse/{loan_collection}/{loan_id}")
async def disburse_route(loan_collection: LoanCollection, loan_id: str, user=Depends(require_roles(Roles.ADMIN))):
    return await _disburse(loan_collection.value, loan_id, user["_id"])


@router.put("/settings")
async def settings_update(payload: SystemSettingsUpdate, user=Depends(require_roles(Roles.ADMIN))):
    return await update_settings(user["_id"], payload.dict())


@router.get("/settings")
async def settings_get(user=Depends(require_roles(Roles.ADMIN))):
    return await get_settings()


@router.get("/loan/{loan_collection}/{loan_id}")
async def get_loan(loan_collection: LoanCollection, loan_id: str, user=Depends(require_roles(Roles.ADMIN))):
    db = await get_db()
    loan = await db[loan_collection.value].find_one(loan_id_filter(loan_id))
    if not loan:
        return {"error": "Loan not found"}
    return _sanitize_loan_doc(loan)