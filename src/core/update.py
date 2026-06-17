from data.write import approve_invoice, reject_invoice


def update_status(invoice, user, action):

    owner_id = invoice["owner_id"]
    user_id = user.get("id")

    if owner_id != user_id:
        return {"ok": False, "reason": "Not assigned to this user"}

    if action == "reject":
        reject_invoice(invoice["invoice_number"])
        return {"ok": True}

    if action == "approve":
        approve_invoice(invoice["invoice_number"])
        return {"ok": True}

    return {"ok": False, "reason": "Invalid action"}