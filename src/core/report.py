from collections import defaultdict


def build_report(invoices):

    total_spend = 0
    total_vat = 0

    approved = 0
    pending = 0
    rejected = 0

    vendor_spend = defaultdict(float)

    for invoice in invoices:

        total = invoice.get("total") or 0
        vat = invoice.get("vat") or 0

        total_spend += total
        total_vat += vat

        vendor = invoice.get("vendor") or "Unknown"
        vendor_spend[vendor] += total

        status = invoice.get("status")

        if status == "approved":
            approved += 1

        elif status == "rejected":
            rejected += 1

        else:
            pending += 1

    vendors = sorted(
        vendor_spend.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return {
        "summary": {
            "invoice_count": len(invoices),
            "total_spend": round(total_spend, 2),
            "total_vat": round(total_vat, 2)
        },

        "approval_status": {
            "approved": approved,
            "pending": pending,
            "rejected": rejected
        },

        "vendors": [
            {
                "vendor": vendor,
                "spend": round(spend, 2)
            }
            for vendor, spend in vendors
        ]
    }