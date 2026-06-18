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
    
def get_all_invoices():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            invoice_number,
            vendor,
            date,
            vat,
            total,
            status,
            owner_id
        FROM invoices
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_invoices_by_owner(owner_id: int):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            invoice_number,
            vendor,
            date,
            vat,
            total,
            status,
            owner_id
        FROM invoices
        WHERE owner_id = ?
        AND status = 'pending'
        ORDER BY id DESC
    """, (owner_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
    
    
def get_invoice_by_number(invoice_number: str):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            invoice_number,
            vendor,
            date,
            vat,
            total,
            status,
            owner_id
        FROM invoices
        WHERE invoice_number = ?
    """, (invoice_number,))

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None