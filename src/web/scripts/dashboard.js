document.addEventListener("DOMContentLoaded", init);

let invoices = [];

let report = {};
let local_insights = [];
let ai_insights = [];

async function init() {
    await load_data();
    render_table();

    await load_insights();
    render_insights();
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

async function load_insights() {
    try {
        const res = await fetch("/insights");

        const data = await res.json();

        report = data.report || {};
        local_insights = data.local_insights || [];
        ai_insights = data.ai_insights || [];

    } catch (err) {

        report = {};
        local_insights = [];
        ai_insights = [];
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
    
    window.invoices = invoices;

	if (window.filter_checkboxes) window.filter_checkboxes();
}

function render_insights() {

    const summary = document.getElementById("report_summary");
    const approval = document.getElementById("approval_status");
    const vendors = document.getElementById("vendor_list");
    const local = document.getElementById("local_list");
    const ai = document.getElementById("ai_list");

    summary.innerHTML = "";
    approval.innerHTML = "";
    vendors.innerHTML = "";
    local.innerHTML = "";
    ai.innerHTML = "";

    if (report.summary) {

        summary.innerHTML = `
            <div class="report_row">
                <span class="report_label">Invoices</span>
                <span class="report_value">${report.summary.invoice_count}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Total Spend</span>
                <span class="report_value">${report.summary.total_spend}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Total VAT</span>
                <span class="report_value">${report.summary.total_vat}</span>
            </div>
        `;
    }

    if (report.approval_status) {

        approval.innerHTML = `
            <div class="report_row">
                <span class="report_label">Approved</span>
                <span class="report_value">${report.approval_status.approved}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Pending</span>
                <span class="report_value">${report.approval_status.pending}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Rejected</span>
                <span class="report_value">${report.approval_status.rejected}</span>
            </div>
        `;
    }

    if (report.vendors && report.vendors.length) {

        report.vendors.forEach(item => {

            vendors.innerHTML += `
                <div class="vendor_item">
                    <span>${item.vendor}</span>
                    <span>${item.spend}</span>
                </div>
            `;
        });

    } else {

        vendors.innerHTML = `
            <div class="empty_text">
                No vendor data available
            </div>
        `;
    }

    if (local_insights.length) {

        local_insights.forEach(item => {

            local.innerHTML += `
                <div class="insight_item">
                    ${item.text}
                </div>
            `;
        });

    } else {

        local.innerHTML = `
            <div class="empty_text">
                No insights available
            </div>
        `;
    }

    if (ai_insights.length) {

        ai_insights.forEach(item => {

            ai.innerHTML += `
                <div class="insight_item">
                    ${item.text}
                </div>
            `;
        });

    } else {

        ai.innerHTML = `
            <div class="empty_text">
                AI analysis unavailable
            </div>
        `;
    }
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

async function show_dashboard() {

    await load_data();

    render_table();

    document.getElementById("dashboard_view").hidden = false;
    document.getElementById("insights_view").hidden = true;

    document.getElementById("dashboard_tab").classList.add("active");
    document.getElementById("insights_tab").classList.remove("active");

    document.getElementById("approve_btn").hidden = false;
    document.getElementById("reject_btn").hidden = false;
    document.querySelector('[onclick="export_excel()"]').hidden = false;
}

async function show_insights() {

    await load_insights();

    render_insights();

    document.getElementById("dashboard_view").hidden = true;
    document.getElementById("insights_view").hidden = false;

    document.getElementById("dashboard_tab").classList.remove("active");
    document.getElementById("insights_tab").classList.add("active");

    document.getElementById("approve_btn").hidden = true;
    document.getElementById("reject_btn").hidden = true;
    document.querySelector('[onclick="export_excel()"]').hidden = true;
    
}

function export_pdf() {

    const dashboard = document.getElementById("dashboard_view");

    if (!dashboard.hidden) {

        const win = window.open("", "", "width=900,height=700");

        const table = document
            .querySelector(".invoice_table")
            .cloneNode(true);

        table
            .querySelectorAll("th:first-child, td:first-child")
            .forEach(el => el.remove());

        win.document.write(`
            <html>
            <head>
                <title>Invoice Report</title>
                <style>
                    body { font-family: Arial; }
                    table { width:100%; border-collapse: collapse; }
                    th, td {
                        border:1px solid #ddd;
                        padding:8px;
                        font-size:12px;
                    }
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

        return;
    }

    const win = window.open("", "", "width=900,height=700");

    win.document.write(`
        <html>
        <head>
            <title>Insights Report</title>
            <style>
                body {
                    font-family: Arial;
                    padding:20px;
                }

                h2 {
                    margin-top:20px;
                }

                p {
                    margin:8px 0;
                }
            </style>
        </head>
        <body>

            <h1>Insights Report</h1>

            <h2>Summary</h2>

            <p>Invoices: ${report.summary?.invoice_count || 0}</p>
            <p>Total Spend: ${report.summary?.total_spend || 0}</p>
            <p>Total VAT: ${report.summary?.total_vat || 0}</p>

            <h2>Approval Status</h2>

            <p>Approved: ${report.approval_status?.approved || 0}</p>
            <p>Pending: ${report.approval_status?.pending || 0}</p>
            <p>Rejected: ${report.approval_status?.rejected || 0}</p>

            <h2>Vendor Analysis</h2>

            ${report.vendors
                ? report.vendors.map(
                    item => `<p>${item.vendor}: ${item.spend}</p>`
                ).join("")
                : ""
            }

            <h2>Insights</h2>

            ${local_insights.map(
                item => `<p>${item.text}</p>`
            ).join("")}

            <h2>AI Analysis</h2>

            ${ai_insights.map(
                item => `<p>${item.text}</p>`
            ).join("")}

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

    const blob = new Blob(
        [csv.join("\n")],
        {
            type: "text/csv"
        }
    );

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

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/web/pages/welcome.html";
}