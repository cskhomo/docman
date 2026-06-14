from pathlib import Path

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from core.extract import extract_document
from core.normalize import load_raw_entities, transform_invoice, save_invoice

from data.log import log_invoice
from data.write import insert_invoice

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = BASE_DIR / "storage" / "temp"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = CACHE_DIR / file.filename

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    extract_document(
        file_path=str(file_path),
        mime_type="application/pdf"
    )

    entities = load_raw_entities()
    invoice = transform_invoice(entities)

    save_invoice(invoice)

    audit_record = log_invoice(invoice)

    insert_invoice(invoice)

    return JSONResponse({
        "message": "processed",
        "invoice": invoice,
        "audit": audit_record
    })