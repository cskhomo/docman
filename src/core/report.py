from collections import defaultdict


def build_report(invoices):

    total_spend = 0
    total_vat = 0

    approved = 0
    pending = 0
    rejected = 0

    vendor_spend = defaultdict(float)

    for invoice in invoices:

        total_spend += invoice["total"] or 0
        total_vat += invoice["vat"] or 0

        vendor_spend[invoice["vendor"]] += invoice["total"] or 0

        statuses = [
            invoice["reviewer_status"],
            invoice["manager_status"],
            invoice["admin_status"]
        ]

        if "rejected" in statuses:
            rejected += 1

        elif "pending" in statuses:
            pending += 1

        else:
            approved += 1

    return {
        "summary": {
            "total_spend": total_spend,
            "total_vat": total_vat,
            "invoice_count": len(invoices)
        },

        "approval_status": {
            "approved": approved,
            "pending": pending,
            "rejected": rejected
        },

        "vendors": dict(vendor_spend)
    }