from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.upload import router as upload_router
from routes.auth import router as auth_router

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = Path(__file__).parent / "web"


# ---------------------------
# ROUTES
# ---------------------------
app.include_router(upload_router)
app.include_router(auth_router)


# ---------------------------
# FRONTEND
# ---------------------------
app.mount("/web", StaticFiles(directory=WEB_DIR, html=True), name="web")


@app.get("/")
def root():
    return {"status": "running"}