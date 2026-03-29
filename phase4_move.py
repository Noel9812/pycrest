import os
import shutil

ROOT_DIR = "/Users/chandana/Desktop/Pycrest/paycrest"
SERVICES_DIR = os.path.join(ROOT_DIR, "services")
BACKEND_DIR = os.path.join(ROOT_DIR, "lms_backend", "app")

if not os.path.exists(BACKEND_DIR):
    print("Backend dir not found", BACKEND_DIR)
    exit(0)

# Simplistic map to copy modules based on Phase 0 Matrix
MODULE_MAP = {
    "auth-service": ["routers/auth.py", "services/auth_service.py", "schemas/user.py", "schemas/common.py"],
    "loan-service": ["modules/customer", "services/loan", "services/customer_service.py", "services/document_service.py", "schemas/loan.py"],
    "emi-service": ["modules/admin/emi", "services/emi", "schemas/loan.py"], # Shared schema
    "wallet-service": ["modules/wallet", "modules/transactions", "services/wallet", "services/transaction_service.py", "services/wallet_service.py", "schemas/wallet.py", "schemas/transactions.py"],
    "payment-service": ["modules/payments", "schemas/wallet.py"],
    "verification-service": ["modules/verification", "services/verification_service.py", "services/kyc_service.py", "schemas/kyc.py"],
    "admin-service": ["modules/admin/approvals", "modules/admin/audit", "modules/admin/staff", "modules/admin/support", "services/admin_service.py", "services/audit_service.py", "services/settings_service.py", "schemas/settings.py", "schemas/support.py"],
    "manager-service": ["modules/manager", "services/manager_service.py", "services/sanction_service.py", "schemas/loan.py"]
}

for svc, paths in MODULE_MAP.items():
    svc_app = os.path.join(SERVICES_DIR, svc, "app")
    
    # Base copies
    try:
        shutil.copytree(os.path.join(BACKEND_DIR, "core"), os.path.join(svc_app, "core"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(BACKEND_DIR, "database"), os.path.join(svc_app, "database"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(BACKEND_DIR, "middleware"), os.path.join(svc_app, "middleware"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(BACKEND_DIR, "models"), os.path.join(svc_app, "models"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(BACKEND_DIR, "utils"), os.path.join(svc_app, "utils"), dirs_exist_ok=True)
    except Exception as e:
        print(f"Error copying base files to {svc}: {e}")

    for src_path in paths:
        full_src = os.path.join(BACKEND_DIR, src_path)
        if not os.path.exists(full_src):
            continue
            
        is_dir = os.path.isdir(full_src)
        
        # Decide destination folder based on src_path type
        dest_folder = "routers" if "modules/" in src_path or "routers/" in src_path else \
                      "services" if "services/" in src_path else \
                      "schemas" if "schemas/" in src_path else "misc"
                      
        dest = os.path.join(svc_app, dest_folder, os.path.basename(full_src))
        
        try:
            if is_dir:
                shutil.copytree(full_src, dest, dirs_exist_ok=True)
            else:
                shutil.copy(full_src, dest)
        except Exception as e:
            print(f"Failed to copy {full_src} -> {dest}: {e}")
            
    # Generate main.py
    main_py = f"""from fastapi import FastAPI
from app.core.config import settings
from app.database.mongo import connect_db, close_db

app = FastAPI(title=settings.service_name + " API")

@app.on_event("startup")
async def startup_db_client():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()

@app.get("/health")
async def health_check():
    return {{"status": "ok", "service": settings.service_name}}
"""
    with open(os.path.join(svc_app, "main.py"), "w") as f:
        f.write(main_py)

print("Phase 4 Internal Structure scaffolding completed.")
