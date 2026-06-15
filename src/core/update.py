def apply_status_update(invoice, role: str, action: str):

    if role == "viewer":
        return False

    statuses = [
        invoice["reviewer_status"],
        invoice["manager_status"],
        invoice["admin_status"]
    ]

    if "rejected" in statuses:
        return False

    if statuses == ["approved", "approved", "approved"]:
        return False

    if role == "reviewer":

        if invoice["reviewer_status"] != "pending":
            return False

        return {
            "column": "reviewer_status",
            "status": "approved" if action == "approve" else "rejected"
        }

    if role == "manager":

        if (
            invoice["reviewer_status"] != "approved"
            or invoice["manager_status"] != "pending"
        ):
            return False

        return {
            "column": "manager_status",
            "status": "approved" if action == "approve" else "rejected"
        }

    if role == "admin":

        if (
            invoice["reviewer_status"] != "approved"
            or invoice["manager_status"] != "approved"
            or invoice["admin_status"] != "pending"
        ):
            return False

        return {
            "column": "admin_status",
            "status": "approved" if action == "approve" else "rejected"
        }

    return False