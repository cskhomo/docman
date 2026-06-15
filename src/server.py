from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.upload import router as upload_router
from routes.auth import router as auth_router
from routes.documents import router as documents_router
from routes.insights import router as insights_router
from routes.reports import router as reports_router
from routes.status import router as status_router

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = Path(__file__).parent / "web"

app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(insights_router)
app.include_router(reports_router)
app.include_router(status_router)

app.mount("/web", StaticFiles(directory=WEB_DIR, html=True), name="web")

@app.get("/")
def root():
    return {"status": "running"}