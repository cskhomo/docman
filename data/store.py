import sqlite3
from pathlib import Path


DB_PATH = "storage/transactions.db"


def get_connection():
    Path("storage/").mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def insert_document(uploader, document, document_type):
    """
    Inserts a normalized document into the existing documents table.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (
            uploader,
            vendor,
            invoice_date,
            amount,
            vat,
            invoice_number,
            type,
            reviewer_status,
            manager_status,
            admin_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', 'pending', 'pending')
    """, (
        uploader,
        document.get("vendor"),
        document.get("invoice_date"),
        document.get("amount"),
        document.get("vat"),
        document.get("invoice_number"),
        document_type
    ))

    conn.commit()
    conn.close()