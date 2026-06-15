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
                Authorization: `Bearer ${token}`
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
            <td><input type="checkbox" data-index="${index}"></td>
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

function get_status(doc) {
    if (doc.reviewer_status === "rejected") return "rejected by reviewer";
    if (doc.manager_status === "rejected") return "rejected by manager";
    if (doc.admin_status === "rejected") return "rejected by admin";

    if (doc.reviewer_status === "pending") return "pending reviewer approval";
    if (doc.manager_status === "pending") return "pending manager approval";
    if (doc.admin_status === "pending") return "pending final approval";

    return "approved";
}

function export_pdf() {
    const win = window.open("", "", "width=900,height=700");

    const table = document.querySelector(".invoice_table").cloneNode(true);

    table.querySelectorAll("th:first-child, td:first-child").forEach(el => el.remove());

    win.document.write(`
        <html>
        <head>
            <title>Invoice Export</title>
            <style>
                body { font-family: Arial; }
                table { width:100%; border-collapse: collapse; }
                th, td { border:1px solid #ddd; padding:8px; font-size:12px; }
                th { background:#f5f5f5; }
            </style>
        </head>
        <body>
            <h3>Invoice Report</h3>
            ${table.outerHTML}
        </body>
        </html>
    `);

    win.document.close();
    win.print();
}

function export_excel() {
    let csv = [];

    csv.push([
        "Invoice #",
        "Vendor",
        "Date",
        "Due",
        "VAT",
        "Total",
        "Status"
    ].join(","));

    invoices.forEach(doc => {
        csv.push([
            doc.invoice_number || "",
            doc.vendor || "",
            doc.date || "",
            doc.due || "",
            doc.vat || 0,
            doc.total || 0,
            get_status(doc)
        ].join(","));
    });

    const blob = new Blob([csv.join("\n")], { type: "text/csv" });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "invoices.csv";
    a.click();

    URL.revokeObjectURL(url);
}

function approve_selected() {}

function reject_selected() {}

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