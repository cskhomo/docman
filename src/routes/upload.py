from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import RedirectResponse

from core.extract import extract_document
from core.normalize import load_raw_entities
from core.normalize import transform_invoice
from core.normalize import save_invoice
from core.validate import validate_invoice

from data.write import insert_invoice
from data.log import check_duplicate
from data.log import log_invoice

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMP_DIR = BASE_DIR / "storage" / "temp"

TEMP_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = TEMP_DIR / file.filename
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    extract_document(file_path=str(file_path), mime_type="application/pdf")

    entities = load_raw_entities()
    invoice = transform_invoice(entities)
    save_invoice(invoice)
    validation = validate_invoice()

    if not validation["valid"]:
        missing = ", ".join(validation["missing"])

        return RedirectResponse(
            url=(
                "/web/pages/upload.html"
                f"?error={quote(f'Missing required fields: {missing}')}"
            ),
            status_code=303
        )

    log_record = {
        "invoice_number": invoice.get("invoice_number"),
        "vendor": invoice.get("vendor"),
        "amount": invoice.get("total")
    }

    dup_check = check_duplicate(invoice)

    if not dup_check["valid"]:
        return RedirectResponse(
            url=(
                "/web/pages/upload.html"
                f"?error={quote(dup_check['reason'])}"
            ),
            status_code=303
        )

    log_invoice(invoice)
    insert_invoice(invoice)

    return RedirectResponse(
        url="/web/pages/dashboard.html",
        status_code=303
    )