from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from core.authorise import decode_token
from data.read import get_invoices_by_owner

router = APIRouter()

security = HTTPBearer()


@router.get("/que")
def get_queue(
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

    invoices = get_invoices_by_owner(
        payload["user_id"]
    )

    return {
        "status": "success",
        "documents": invoices
    }