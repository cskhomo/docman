import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_FILE = BASE_DIR / "storage" / "log.json"


def ensure_log_exists():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not LOG_FILE.exists():
        with open(LOG_FILE, "w") as f:
            json.dump([], f)


def generate_hash(invoice):
    payload = json.dumps(invoice, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_log():
    ensure_log_exists()

    with open(LOG_FILE, "r") as f:
        return json.load(f)


def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)


def extract_fields(invoice):
    return {
        "invoice_number": invoice.get("invoice_number"),
        "vendor": invoice.get("vendor"),
        "amount": invoice.get("total")
    }


def log_invoice(invoice):
    existing_log = load_log()

    record = extract_fields(invoice)
    record["hash"] = generate_hash(invoice)

    existing_log.append(record)
    save_log(existing_log)

    return record
    
def check_duplicate(invoice):

    existing_log = load_log()

    invoice_number = invoice.get("invoice_number")
    vendor = invoice.get("vendor")
    amount = invoice.get("total")

    for record in existing_log:

        if record.get("invoice_number") == invoice_number:
            return {"valid": False, "reason": "duplicate invoice number"}

        if (record.get("vendor") == vendor and record.get("amount") == amount):
            return {"valid": False, "reason": "duplicate document / double charge detected"}

    return {"valid": True, "reason": None}