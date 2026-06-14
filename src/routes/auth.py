from pathlib import Path
import os
import sqlite3
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# ----------------------------
# PATH RESOLUTION (CRITICAL)
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent        # src/
ROOT_DIR = BASE_DIR.parent                               # docman/
ENV_PATH = BASE_DIR / ".env"
STORAGE_DIR = ROOT_DIR / "storage"
DB_PATH = STORAGE_DIR / "transactions.db"

load_dotenv(dotenv_path=ENV_PATH)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
TOKEN_EXP_MINUTES = 60 * 24  # 24h session


if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET not loaded. Check src/.env")


# ----------------------------
# REQUEST MODELS
# ----------------------------
class AuthRequest(BaseModel):
    email: str
    password: str


# ----------------------------
# DB HELPER
# ----------------------------
def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# TOKEN CREATION
# ----------------------------
def create_token(user_id: int, email: str, role: str):
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXP_MINUTES)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# ----------------------------
# SIGNUP
# ----------------------------
@router.post("/auth/signup")
def signup(data: AuthRequest):

    conn = get_db()
    cursor = conn.cursor()

    # check duplicate email
    cursor.execute("SELECT id FROM accounts WHERE email = ?", (data.email,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {"status": "fail", "reason": "Email already exists"}

    # hash password
    password_hash = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute(
        "INSERT INTO accounts (email, password_hash, role) VALUES (?, ?, ?)",
        (data.email, password_hash, "viewer")
    )

    conn.commit()
    conn.close()

    return {"status": "success"}


# ----------------------------
# LOGIN
# ----------------------------
@router.post("/auth/login")
def login(data: AuthRequest):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, password_hash, role FROM accounts WHERE email = ?",
        (data.email,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"status": "fail", "reason": "Invalid credentials"}

    # verify password
    if not bcrypt.checkpw(
        data.password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    ):
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