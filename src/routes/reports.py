from fastapi import APIRouter

from data.read import get_all_invoices
from core.report import build_report

router = APIRouter()

@router.get("/reports")
def reports():

    invoices = get_all_invoices()

    return {
        "status": "success",
        "report": build_report(invoices)
    }