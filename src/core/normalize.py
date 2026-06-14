import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "storage"
TEMP_DIR = STORAGE_DIR / "temp"

TEMP_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = TEMP_DIR / "raw_invoice.json"
NORMAL_FILE = TEMP_DIR / "invoice.json"


def get_value(entity):
    return entity["normalized_value"] or entity["mention_text"]


def load_raw_entities():
    with open(RAW_FILE, "r") as file:
        return json.load(file)


def transform_invoice(entities):

    invoice = {
        "invoice_number": None,
        "vendor": None,
        "date": None,
        "due": None,
        "currency": None,
        "vat": None,
        "total": None
    }

    field_mapping = {
        "invoice_id": "invoice_number",
        "supplier_name": "vendor",
        "invoice_date": "date",
        "due_date": "due",
        "currency": "currency",
        "total_tax_amount": "vat",
        "total_amount": "total"
    }

    for entity in entities:

        entity_type = entity["type"]

        if entity_type not in field_mapping:
            continue

        field = field_mapping[entity_type]
        value = get_value(entity)

        if field in ("vat", "total"):
            try:
                value = float(value)
            except:
                value = None

        invoice[field] = value

    return invoice


def save_invoice(invoice):
    with open(NORMAL_FILE, "w") as file:
        json.dump(invoice, file, indent=4)