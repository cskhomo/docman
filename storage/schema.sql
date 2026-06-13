CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('viewer', 'reviewer', 'manager', 'admin'))
);
	   
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uploader INTEGER NOT NULL,
    vendor TEXT,
    invoice_number TEXT,
    invoice_date TEXT,
    amount REAL,
    vat REAL,
    type TEXT NOT NULL
		CHECK(type IN ('invoice', 'credit_note')),
    
    reviewer_status TEXT NOT NULL DEFAULT 'pending'
        CHECK(reviewer_status IN ('pending', 'approved', 'rejected')),

    manager_status TEXT NOT NULL DEFAULT 'pending'
        CHECK(manager_status IN ('pending', 'approved', 'rejected')),

    admin_status TEXT NOT NULL DEFAULT 'pending'
        CHECK(admin_status IN ('pending', 'approved', 'rejected')),

    FOREIGN KEY (uploader) REFERENCES accounts(id)
);