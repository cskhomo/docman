import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
TOKEN_EXP_MINUTES = 60 * 24


if not JWT_SECRET:
    raise RuntimeError(f"JWT_SECRET missing. Tried loading: {ENV_PATH}")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, hash_pw: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hash_pw.encode("utf-8")
    )


def create_token(user_id: int, email: str, role: str):
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXP_MINUTES)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])