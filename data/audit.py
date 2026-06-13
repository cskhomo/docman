import json
import hashlib
from pathlib import Path


AUDIT_FILE = "storage/cache/log.json"


def ensure_log_exists():
    Path("storage/cache").mkdir(parents=True, exist_ok=True)

    if not Path(AUDIT_FILE).exists():
        with open(AUDIT_FILE, "w") as f:
            json.dump([], f)


def generate_hash(invoice):
    payload = json.dumps(
        invoice,
        sort_keys=True
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()


def load_log():
    ensure_log_exists()

    with open(AUDIT_FILE, "r") as f:
        return json.load(f)


def save_log(log):
    with open(AUDIT_FILE, "w") as f:
        json.dump(log, f, indent=4)


def extract_fields(invoice):
    return {
        "invoice_number": invoice.get("invoice_number"),
        "vendor": invoice.get("vendor"),
        "amount": invoice.get("amount"),
    }


def log_invoice(invoice):

    existing_log = load_log()

    record = extract_fields(invoice)
    record["hash"] = generate_hash(invoice)

    existing_log.append(record)

    save_log(existing_log)

    return record