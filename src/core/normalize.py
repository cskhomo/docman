from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "storage"
TEMP_DIR = STORAGE_DIR / "temp"

TEMP_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = TEMP_DIR / "raw_invoice.json"
NORMAL_FILE = TEMP_DIR / "invoice.json"


def load_raw_entities():
    with open(RAW_FILE, "r") as file:
        return json.load(file)

def transform_invoice(entities):

    invoice = {
        "invoice_number": None,
        "vendor": None,
        "date": None,
        "vat": None,
        "total": None
    }

    due_date = None
    invoice_date = None

    for entity in entities:

        entity_type = entity["type"]
        value = get_value(entity)

        if entity_type == "invoice_id":
            invoice["invoice_number"] = value

        elif entity_type == "supplier_name":
            invoice["vendor"] = value

        elif entity_type == "invoice_date":
            invoice_date = value

        elif entity_type == "due_date":
            due_date = value

        elif entity_type == "total_tax_amount":
            invoice["vat"] = parse_amount(value)

        elif entity_type == "total_amount":
            invoice["total"] = parse_amount(value)

    invoice["date"] = due_date or invoice_date

    return invoice
    
def parse_amount(value):

    if value is None:
        return None

    value = str(value)

    value = re.sub(r"[^\d.,-]", "", value)

    if "," in value and "." in value:
        value = value.replace(",", "")

    elif "," in value:
        value = value.replace(",", ".")

    try:
        return float(value)
    except ValueError:
        return None
        

def get_value(entity):
    return entity.get("normalized_value") or entity.get("mention_text")


def save_invoice(invoice):
    with open(NORMAL_FILE, "w") as file:
        json.dump(invoice, file, indent=4)