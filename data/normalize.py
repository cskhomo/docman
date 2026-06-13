import json


RAW_FILE = "storage/temp/raw_invoice.json"
INVOICE_FILE = "storage/temp/invoice.json"


def get_value(entity):

    return (
        entity["normalized_value"]
        or entity["mention_text"]
    )


def load_raw_entities():

    with open(RAW_FILE, "r") as file:
        return json.load(file)


def transform_invoice(entities):

    invoice = {
        "vendor": None,
        "invoice_date": None,
        "amount": None,
        "currency": None,
        "vat": None,
        "invoice_number": None
    }

    field_mapping = {
        "supplier_name": "vendor",
        "invoice_date": "invoice_date",
        "total_amount": "amount",
        "currency": "currency",
        "total_tax_amount": "vat",
        "invoice_id": "invoice_number"
    }

    for entity in entities:

        entity_type = entity["type"]

        if entity_type not in field_mapping:
            continue

        field = field_mapping[entity_type]
        value = get_value(entity)

        if field in ("amount", "vat"):
            value = float(value)

        invoice[field] = value

    return invoice


def save_invoice(invoice):

    with open(INVOICE_FILE, "w") as file:
        json.dump(
            invoice,
            file,
            indent=4
        )