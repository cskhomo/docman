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

    invoice = get_invoice_by_number(data.invoice_number)

    if not invoice:
        return {
            "status": "fail",
            "reason": "Invoice not found"
        }


    if data.action == "approve":

        approve_invoice(data.invoice_number)


    elif data.action == "reject":

        reject_invoice(data.invoice_number)


    else:
        return {
            "status": "fail",
            "reason": "Invalid action"
        }


    return {
        "status": "success"
    }