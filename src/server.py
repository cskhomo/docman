from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from data.extract import extract_document
from data.normalize import load_raw_entities, transform_invoice, save_invoice
from data.audit import log_invoice
from data.store import insert_document


app = FastAPI()

WEB_DIR = Path(__file__).parent / "web"
CACHE_DIR = Path("storage/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------
# PIPELINE (UPLOAD ENDPOINT)
# ---------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    # 1. Save PDF
    file_path = CACHE_DIR / file.filename

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # 2. Extract (Document AI)
    extract_document(
        file_path=str(file_path),
        mime_type="application/pdf"
    )

    # 3. Normalize
    entities = load_raw_entities()
    invoice = transform_invoice(entities)

    save_invoice(invoice)

    # 4. Audit log (hash)
    audit_record = log_invoice(invoice)

    # 5. Store in DB
    insert_document(
        uploader=1,
        document=invoice,
        document_type="invoice"
    )

    # 6. Response
    return JSONResponse({
        "message": "processed",
        "invoice": invoice,
        "audit": audit_record
    })


# ---------------------------
# FRONTEND
# ---------------------------
app.mount("/web", StaticFiles(directory=WEB_DIR, html=True), name="web")


@app.get("/")
def root():
    return {"status": "running"}