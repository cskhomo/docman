from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from data.read import get_user_by_email
from data.write import create_user
from core.authorise import (
    hash_password,
    verify_password,
    create_token,
    decode_token
)

router = APIRouter()
security = HTTPBearer()


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/auth/signup")
def signup(data: AuthRequest):

    existing = get_user_by_email(data.email)

    if existing:
        return {"status": "fail", "reason": "Email already exists"}

    password_hash = hash_password(data.password)

    create_user(
        email=data.email,
        password_hash=password_hash,
        role="viewer"
    )

    return {"status": "success"}


@router.post("/auth/login")
def login(data: AuthRequest):

    user = get_user_by_email(data.email)

    if not user:
        return {"status": "fail", "reason": "Invalid credentials"}

    if not verify_password(data.password, user["password_hash"]):
        return {"status": "fail", "reason": "Invalid credentials"}

    token = create_token(user["id"], user["email"], user["role"])

    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"]
        }
    }


@router.get("/auth/validate")
def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = decode_token(token)

        return {
            "status": "success",
            "user": {
                "id": payload["user_id"],
                "email": payload["email"],
                "role": payload["role"]
            }
        }

    except Exception:
        return {
            "status": "fail",
            "reason": "Invalid or expired token"
        }