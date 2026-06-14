import json
import sqlite3
from pathlib import Path


def main():

    create_temp()
    create_log()

    connection = sqlite3.connect("transactions.db")

    create_tables(connection)
    seed_accounts(connection)

    connection.close()

def create_temp():
    Path("temp").mkdir(exist_ok=True)


def create_log():
    if not Path("log.json").exists():
        with open("log.json", "w") as file:
            json.dump([], file, indent=4)


def create_tables(connection):

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('viewer', 'reviewer', 'manager', 'admin'))
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            invoice_date TEXT,
            amount REAL,
            currency TEXT,
            vat REAL,
            invoice_number TEXT,
            
            type TEXT NOT NULL
                CHECK(type IN ('invoice', 'credit_note')),

            reviewer_status TEXT NOT NULL DEFAULT 'pending'
                CHECK(reviewer_status IN ('pending', 'approved', 'rejected')),

            manager_status TEXT NOT NULL DEFAULT 'pending'
                CHECK(manager_status IN ('pending', 'approved', 'rejected')),

            admin_status TEXT NOT NULL DEFAULT 'pending'
                CHECK(admin_status IN ('pending', 'approved', 'rejected'))
        );
    """)

    connection.commit()


def seed_accounts(connection):

    cursor = connection.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO accounts (
            email,
            password_hash,
            role
        )
        VALUES (?, ?, ?)
    """, [
        (
            "turing@docman.com",
            "$2b$12$k3fsOiDkDQBlzB.80YOkc.YYwFsqDZXveZu.yQ7h5LFkpG7cJ3qvC",
            "viewer"
        ),
        (
            "lovelace@docman.com",
            "$2b$12$9yqwEZA/sGVVrXplX5cL0.7Nt49HsQxBZPHXWsRS4daBqRWOwjPSO",
            "reviewer"
        ),
        (
            "linus@docman.com",
            "$2b$12$8yKPRAqg5UQhKjPYUtcT8enA7tjU9anXyuqoKbL0JFl2VXtaG57qy",
            "manager"
        ),
        (
            "stallman@docman.com",
            "$2b$12$ADE6eNkEt00fbRpE1px1p.zFEOLScvTPzOxptFy.ZdmN0YJmT9yZu",
            "admin"
        )
    ])

    connection.commit()

if __name__ == "__main__":
    main()