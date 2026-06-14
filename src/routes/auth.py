import sqlite3
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel
import bcrypt


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "storage" / "transactions.db"


# ---------------------------
# REQUEST MODELS
# ---------------------------
class AuthRequest(BaseModel):
    email: str
    password: str


# ---------------------------
# DB HELPERS
# ---------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)


def fetch_user(email: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, password_hash, role FROM accounts WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def insert_user(email: str, password_hash: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO accounts (email, password_hash, role)
        VALUES (?, ?, 'viewer')
        """,
        (email, password_hash)
    )

    conn.commit()
    conn.close()


# ---------------------------
# SIGNUP
# ---------------------------
@router.post("/auth/signup")
def signup(data: AuthRequest):

    existing_user = fetch_user(data.email)

    if existing_user:
        return {
            "status": "fail",
            "reason": "email already exists"
        }

    hashed = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt()
    )

    insert_user(data.email, hashed.decode("utf-8"))

    return {
        "status": "success",
        "message": "user created"
    }


# ---------------------------
# LOGIN
# ---------------------------
@router.post("/auth/login")
def login(data: AuthRequest):

    user = fetch_user(data.email)

    if not user:
        return {
            "status": "fail",
            "reason": "invalid credentials"
        }

    email, password_hash, role = user

    password_valid = bcrypt.checkpw(
        data.password.encode("utf-8"),
        password_hash.encode("utf-8")
    )

    if not password_valid:
        return {
            "status": "fail",
            "reason": "invalid credentials"
        }

    return {
        "status": "success",
        "message": "login successful",
        "role": role
    }