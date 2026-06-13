from pathlib import Path

from data.extract import extract_document
from data.normalize import load_raw_entities
from data.normalize import transform_invoice
from data.normalize import save_invoice
from data.audit import log_invoice
from data.store import insert_document


def main():

    Path("storage/temp").mkdir(parents=True, exist_ok=True)

    extract_document(
        file_path="storage/cache/invoice.pdf",
        mime_type="application/pdf"
    )

    entities = load_raw_entities()

    invoice = transform_invoice(entities)

    save_invoice(invoice)

    audit_record = log_invoice(invoice)

    insert_document(
        uploader=1,
        document=invoice,
        document_type="invoice"
    )

    print("Saved raw_invoice.json")
    print("Saved invoice.json")
    print("Inserted into database:")


if __name__ == "__main__":
    main()