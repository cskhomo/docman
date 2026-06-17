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
        SELECT id
        FROM accounts
        WHERE role = 'reviewer'
    """)

    reviewer_id = cursor.fetchone()["id"]

    cursor.execute("""
        INSERT INTO invoices (
            invoice_number,
            vendor,
            date,
            vat,
            total,
            status,
            owner_id
        )
        VALUES (?, ?, ?, ?, ?, 'pending', ?)
    """, (
        document.get("invoice_number"),
        document.get("vendor"),
        document.get("date"),
        document.get("vat"),
        document.get("total"),
        reviewer_id
    ))

    conn.commit()
    conn.close()
    
def reject_invoice(invoice_number):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE invoices
        SET
            status = 'rejected',
            owner_id = NULL
        WHERE invoice_number = ?
    """, (invoice_number,))

    conn.commit()
    conn.close()
    
def approve_invoice(invoice_number: str):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.role
        FROM invoices i
        JOIN accounts a
            ON i.owner_id = a.id
        WHERE i.invoice_number = ?
    """, (invoice_number,))

    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise ValueError("Invoice not found")

    next_role = {
        "reviewer": "manager",
        "manager": "admin"
    }

    role = row["role"]

    if role == "admin":

        cursor.execute("""
            UPDATE invoices
            SET
                status = 'approved',
                owner_id = NULL
            WHERE invoice_number = ?
        """, (invoice_number,))

    elif role in next_role:

        cursor.execute("""
            SELECT id
            FROM accounts
            WHERE role = ?
        """, (next_role[role],))

        next_owner = cursor.fetchone()

        if next_owner is None:
            conn.close()
            raise ValueError(
                f"No account found for role '{next_role[role]}'"
            )

        cursor.execute("""
            UPDATE invoices
            SET owner_id = ?
            WHERE invoice_number = ?
        """, (
            next_owner["id"],
            invoice_number
        ))

    else:

        conn.close()
        raise ValueError(f"Invalid role: {role}")

    conn.commit()
    conn.close()