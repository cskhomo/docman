from fastapi import APIRouter

from data.read import get_all_invoices
from core.report import build_report
from core.analyze import generate_local_insights
from core.analyze import generate_ai_insights

router = APIRouter()


@router.get("/insights")
def insights():

    invoices = get_all_invoices()
    report = build_report(invoices)

    return {
        "status": "success",
        "report": report,
        "local_insights": generate_local_insights(report),
        "ai_insights": generate_ai_insights(report)
    }