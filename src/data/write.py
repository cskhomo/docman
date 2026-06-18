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
        AND status = 'pending'
    """, (invoice_number,))

    conn.commit()
    conn.close()


def approve_invoice(invoice_number):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            i.owner_id,
            a.role
        FROM invoices i
        LEFT JOIN accounts a
            ON i.owner_id = a.id
        WHERE i.invoice_number = ?
    """, (invoice_number,))


    invoice = cursor.fetchone()


    if not invoice:
        conn.close()
        return False


    current_role = invoice["role"]

    if current_role == "reviewer":

        cursor.execute("""
            SELECT id
            FROM accounts
            WHERE role = 'manager'
        """)

        manager = cursor.fetchone()


        cursor.execute("""
            UPDATE invoices
            SET owner_id = ?
            WHERE invoice_number = ?
        """, (
            manager["id"],
            invoice_number
        ))

    elif current_role == "manager":

        cursor.execute("""
            SELECT id
            FROM accounts
            WHERE role = 'admin'
        """)

        admin = cursor.fetchone()


        cursor.execute("""
            UPDATE invoices
            SET owner_id = ?
            WHERE invoice_number = ?
        """, (
            admin["id"],
            invoice_number
        ))

    elif current_role == "admin":

        cursor.execute("""
            UPDATE invoices
            SET
                status = 'approved',
                owner_id = NULL
            WHERE invoice_number = ?
        """, (invoice_number,))


    else:
        conn.close()
        return False


    conn.commit()
    conn.close()

    return True