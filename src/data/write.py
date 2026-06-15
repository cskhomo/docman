import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "storage" / "transactions.db"


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def create_user(email: str, password_hash: str, role: str = "viewer"):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO accounts (email, password_hash, role)
        VALUES (?, ?, ?)
    """, (email, password_hash, role))

    conn.commit()
    conn.close()


def insert_invoice(document):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invoices (
            invoice_number,
            vendor,
            date,
            due,
            currency,
            vat,
            total,
            reviewer_status,
            manager_status,
            admin_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', 'pending', 'pending')
    """, (
        document.get("invoice_number"),
        document.get("vendor"),
        document.get("date"),
        document.get("due"),
        document.get("currency"),
        document.get("vat"),
        document.get("total")
    ))

    conn.commit()
    conn.close()