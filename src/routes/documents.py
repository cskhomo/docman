from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from data.read import get_all_invoices, get_db

router = APIRouter()

class ActionPayload(BaseModel):
    action: str
    role: str
    invoices: list[str]

def get_stage_field(role: str):
    if role == "reviewer":
        return "reviewer_status"
    if role == "manager":
        return "manager_status"
    if role == "admin":
        return "admin_status"
    return None

@router.get("/documents")
def get_documents():
    invoices = get_all_invoices()
    return {"documents": invoices}

@router.post("/documents/approve")
def update_documents(payload: ActionPayload):

    conn = get_db()
    cursor = conn.cursor()

    field = get_stage_field(payload.role)

    if not field:
        raise HTTPException(status_code=403, detail="Invalid role")

    for inv in payload.invoices:

        cursor.execute("""
            SELECT reviewer_status, manager_status, admin_status
            FROM invoices
            WHERE invoice_number = ?
        """, (inv,))

        row = cursor.fetchone()

        if not row:
            continue

        reviewer_status, manager_status, admin_status = row

        if "rejected" in [reviewer_status, manager_status, admin_status]:
            continue

        if payload.role == "reviewer":
            if reviewer_status != "pending":
                continue

        if payload.role == "manager":
            if reviewer_status != "approved" or manager_status != "pending":
                continue

        if payload.role == "admin":
            if manager_status != "approved" or admin_status != "pending":
                continue

        new_status = "approved" if payload.action == "approve" else "rejected"

        cursor.execute(f"""
            UPDATE invoices
            SET {field} = ?
            WHERE invoice_number = ?
        """, (new_status, inv))

    conn.commit()
    conn.close()

    return {"status": "success"}