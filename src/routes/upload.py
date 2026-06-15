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

    validation = validate_invoice()

    if not validation["valid"]:

        missing = ", ".join(validation["missing"])

        error_message = (
            f"Missing required fields: {missing}"
        )

        return RedirectResponse(
            url=(
                "/web/pages/upload.html"
                f"?error={quote(error_message)}"
            ),
            status_code=303
        )

    insert_invoice(invoice)

    return RedirectResponse(
        url="/web/pages/dashboard.html",
        status_code=303
    )