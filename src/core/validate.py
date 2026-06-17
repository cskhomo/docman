import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "storage"
TEMP_DIR = STORAGE_DIR / "temp"

TEMP_DIR.mkdir(parents=True, exist_ok=True)

NORMAL_FILE = TEMP_DIR / "invoice.json"


REQUIRED_FIELDS = [
    "invoice_number",
    "vendor",
    "date",
    "vat",
    "total"
]


def validate_invoice():

    with open(NORMAL_FILE, "r") as file:
        invoice = json.load(file)

    missing_fields = []

    for field in REQUIRED_FIELDS:

        if field not in invoice:
            missing_fields.append(field)
            continue

        value = invoice[field]

        if value is None:
            missing_fields.append(field)
            continue

        if isinstance(value, str) and value.strip() == "":
            missing_fields.append(field)

    return {
        "valid": len(missing_fields) == 0,
        "missing": missing_fields
    }