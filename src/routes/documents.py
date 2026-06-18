from fastapi import APIRouter
from data.read import get_all_invoices

router = APIRouter()

@router.get("/documents")
def get_documents():
    invoices = get_all_invoices()
    return {"documents": invoices}

