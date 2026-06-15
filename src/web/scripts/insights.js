document.addEventListener("DOMContentLoaded", init);

let report = {};
let localInsights = [];
let aiInsights = [];

async function init() {
    await load_data();
    render_all();
}

async function load_data() {
    const token = localStorage.getItem("token");

    try {
        const res = await fetch("/insights", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await res.json();

        console.log("INSIGHTS RESPONSE:", data);

        report = data.report || {
            summary: {},
            approval_status: {},
            vendors: {}
        };

        localInsights = data.local_insights || [];
        aiInsights = data.ai_insights || [];

    } catch (err) {
        console.error("Failed to load insights:", err);

        report = {
            summary: {},
            approval_status: {},
            vendors: {}
        };

        localInsights = [];
        aiInsights = [];
    }
}

function render_all() {
    render_summary();
    render_vendors();
    render_insights();
}

function render_summary() {
    const body = document.getElementById("summary_body");
    body.innerHTML = "";

    const s = report.summary || {};
    const a = report.approval_status || {};

    const rows = [
        ["Total Spend", s.total_spend ?? 0],
        ["Total VAT", s.total_vat ?? 0],
        ["Invoice Count", s.invoice_count ?? 0],
        ["Approved", a.approved ?? 0],
        ["Pending", a.pending ?? 0],
        ["Rejected", a.rejected ?? 0]
    ];

    rows.forEach(([key, value]) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${key}</td><td>${value}</td>`;
        body.appendChild(tr);
    });
}

function render_vendors() {
    const body = document.getElementById("vendor_body");
    body.innerHTML = "";

    const vendors = report.vendors || {};

    const entries = Object.entries(vendors);

    if (entries.length === 0) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td colspan="2">No vendor data available</td>`;
        body.appendChild(tr);
        return;
    }

    entries.forEach(([vendor, spend]) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${vendor}</td>
            <td>${Number(spend || 0).toFixed(2)}</td>
        `;
        body.appendChild(tr);
    });
}

function render_insights() {
    const body = document.getElementById("insight_body");
    body.innerHTML = "";

    const normalized = [];

    localInsights.forEach(i => {
        if (typeof i === "string") {
            normalized.push({ source: "local", text: i });
        } else {
            normalized.push(i);
        }
    });

    aiInsights.forEach(i => {
        if (typeof i === "string") {
            normalized.push({ source: "ai", text: i });
        } else {
            normalized.push(i);
        }
    });

    if (normalized.length === 0) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td colspan="2">No insights available</td>`;
        body.appendChild(tr);
        return;
    }

    normalized.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${(item.source || "unknown").toUpperCase()}</td>
            <td>${item.text || ""}</td>
        `;
        body.appendChild(tr);
    });
}

function export_pdf() {
    const win = window.open("", "", "width=900,height=700");

    const summary = document.querySelector(".summary_table").cloneNode(true);
    const vendors = document.querySelector(".vendor_table").cloneNode(true);
    const insights = document.querySelector(".insight_table").cloneNode(true);

    win.document.write(`
        <html>
        <head>
            <title>Insights Export</title>
            <style>
                body { font-family: Arial; padding: 20px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                td, th { border: 1px solid #ddd; padding: 8px; font-size: 12px; }
                th { background: #f5f5f5; }
            </style>
        </head>
        <body>
            <h2>Report Summary</h2>
            ${summary.outerHTML}
            <h2>Vendor Analysis</h2>
            ${vendors.outerHTML}
            <h2>Insights</h2>
            ${insights.outerHTML}
        </body>
        </html>
    `);

    win.document.close();
    win.print();
}

function export_excel() {
    let csv = [];

    csv.push(["Section", "Key", "Value"].join(","));

    const s = report.summary || {};
    const a = report.approval_status || {};
    const vendors = report.vendors || {};

    csv.push(["Summary", "Total Spend", s.total_spend ?? 0].join(","));
    csv.push(["Summary", "Total VAT", s.total_vat ?? 0].join(","));
    csv.push(["Summary", "Invoice Count", s.invoice_count ?? 0].join(","));

    csv.push(["Approval", "Approved", a.approved ?? 0].join(","));
    csv.push(["Approval", "Pending", a.pending ?? 0].join(","));
    csv.push(["Approval", "Rejected", a.rejected ?? 0].join(","));

    Object.entries(vendors).forEach(([v, s]) => {
        csv.push(["Vendor", v, s ?? 0].join(","));
    });

    [...localInsights, ...aiInsights].forEach(i => {
        if (typeof i === "string") {
            csv.push(["Insight", i, ""].join(","));
        } else {
            csv.push([i.source || "insight", i.text || "", ""].join(","));
        }
    });

    const blob = new Blob([csv.join("\n")], { type: "text/csv" });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "insights.csv";
    a.click();

    URL.revokeObjectURL(url);
}