import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "storage" / "transactions.db"


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_email(email: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, email, password_hash, role
        FROM accounts
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None