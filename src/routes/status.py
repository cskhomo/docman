from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from core.authorise import decode_token
from core.update import update_status
from data.read import get_invoice_by_number
from data.write import approve_invoice
from data.write import reject_invoice


router = APIRouter()
security = HTTPBearer()


class StatusRequest(BaseModel):
    invoice_number: str
    action: str


@router.post("/status")
def status_update(
    data: StatusRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = decode_token(token)
    except Exception:
        return {"status": "fail", "reason": "Invalid token"}

    invoice = get_invoice_by_number(data.invoice_number)

    if not invoice:
        return {"status": "fail", "reason": "Invoice not found"}

    result = update_status(invoice=invoice, user=payload, action=data.action)

    if not result["ok"]:
        return {"status": "fail", "reason": result["reason"]}

    return {"status": "success"}