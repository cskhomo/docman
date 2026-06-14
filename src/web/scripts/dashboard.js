document.addEventListener("DOMContentLoaded", init);

let invoices = [];

async function init() {
    await load_data();
    render_table();
}

async function load_data() {
    const token = localStorage.getItem("token");

    try {
        const res = await fetch("/documents", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        invoices = data.documents || [];

    } catch (err) {
        invoices = [];
    }
}

function render_table() {
    const body = document.getElementById("table_body");
    body.innerHTML = "";

    invoices.forEach((doc, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <input type="checkbox" data-index="${index}">
            </td>

            <td>${doc.invoice_number || ""}</td>
            <td>${doc.vendor || ""}</td>
            <td>${doc.date || ""}</td>
            <td>${doc.due || ""}</td>
            <td>${doc.vat || 0}</td>
            <td>${doc.total || 0}</td>

            <td>${get_status(doc)}</td>
        `;

        body.appendChild(row);
    });
}

function get_selected() {
    const checks = document.querySelectorAll("input[type='checkbox']:checked");

    return Array.from(checks).map(c => {
        return invoices[c.dataset.index];
    });
}

function get_status(doc) {

    if (
        doc.reviewer_status === "rejected" ||
        doc.manager_status === "rejected" ||
        doc.admin_status === "rejected"
    ) {
        return "rejected";
    }

    if (doc.reviewer_status === "pending") {
        return "pending_reviewer";
    }

    if (doc.manager_status === "pending") {
        return "pending_manager";
    }

    if (doc.admin_status === "pending") {
        return "pending_admin";
    }

    return "approved";
}


async function approve_selected() {
    const selected = get_selected();

    for (const doc of selected) {
        await send_action(doc.id, "approve");
    }

    await reload();
}

async function reject_selected() {
    const selected = get_selected();

    for (const doc of selected) {
        await send_action(doc.id, "reject");
    }

    await reload();
}

async function send_action(id, action) {
    const token = localStorage.getItem("token");

    try {
        await fetch("/documents/update_status", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                id,
                action
            })
        });

    } catch (err) {
        console.log("update failed", err);
    }
}

async function reload() {
    await load_data();
    render_table();
}


function goto_upload() {
    window.location.href = "/web/pages/upload.html";
}

function goto_insights() {
    window.location.href = "/web/pages/insights.html";
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/web/pages/welcome.html";
}