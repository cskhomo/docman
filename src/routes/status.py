from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from pydantic import BaseModel

from core.authorise import decode_token
from core.update import apply_status_update

from data.read import get_invoice_by_number
from data.write import update_invoice_status

router = APIRouter()

security = HTTPBearer()


class StatusRequest(BaseModel):
    invoice_number: str
    action: str


@router.post("/status")
def update_status(
    data: StatusRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = decode_token(token)

    except Exception:
        return {
            "status": "fail",
            "reason": "Invalid token"
        }

    role = payload["role"]

    if data.action not in ("approve", "reject"):
        return {
            "status": "fail",
            "reason": "Invalid action"
        }

    invoice = get_invoice_by_number(
        data.invoice_number
    )

    if not invoice:
        return {
            "status": "fail",
            "reason": "Invoice not found"
        }

    update = apply_status_update(
        invoice,
        role,
        data.action
    )

    if not update:
        return {
            "status": "fail",
            "reason": "Action not permitted"
        }

    update_invoice_status(
        data.invoice_number,
        update["column"],
        update["status"]
    )

    return {
        "status": "success"
    }