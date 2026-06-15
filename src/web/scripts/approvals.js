document.addEventListener("DOMContentLoaded", init);

let user = null;

async function init() {
    await load_user();
}

async function load_user() {
    const token = localStorage.getItem("token");

    try {
        const res = await fetch("/auth/me", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        user = await res.json();
    } catch (err) {
        user = null;
    }
}

function can_act(doc) {

    if (!user) return false;

    if (user.role === "viewer") return false;

    if (doc.reviewer_status === "rejected") return false;
    if (doc.manager_status === "rejected") return false;
    if (doc.admin_status === "rejected") return false;

    if (user.role === "reviewer") {
        return doc.reviewer_status === "pending";
    }

    if (user.role === "manager") {
        return doc.reviewer_status === "approved" &&
               doc.manager_status === "pending";
    }

    if (user.role === "admin") {
        return doc.manager_status === "approved" &&
               doc.admin_status === "pending";
    }

    return false;
}

function filter_checkboxes() {

    document.querySelectorAll("input[type='checkbox']").forEach(cb => {

        const index = cb.getAttribute("data-index");
        const doc = window.invoices?.[index];

        if (!doc) return;

        const allowed = can_act(doc);

        cb.disabled = !allowed;

        if (!allowed) {
            cb.checked = false;
        }
    });
}

async function get_selected_docs() {

    const selected = [];

    document.querySelectorAll("input[type='checkbox']:checked").forEach(cb => {

        const index = cb.getAttribute("data-index");
        const doc = window.invoices?.[index];

        if (doc) {
            selected.push(doc.invoice_number);
        }
    });

    return selected;
}

async function send_action(action) {

    const invoices = await get_selected_docs();

    if (!invoices.length) return;

    if (!user || user.role === "viewer") return;

    const token = localStorage.getItem("token");

    await fetch("/documents/approve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
            action,
            role: user.role,
            invoices
        })
    });

    window.location.reload();
}

function approve_selected() {
    send_action("approve");
}

function reject_selected() {
    send_action("reject");
}