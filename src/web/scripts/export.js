function get_active_view() {

    const dashboard = document.getElementById("dashboard_view");
    const queue = document.getElementById("queue_view");
    const insights = document.getElementById("insights_view");

    if (!dashboard.hidden) return "dashboard";
    if (!insights.hidden) return "insights";

    return "dashboard";
}

function get_export_data() {

    const view = get_active_view();

    if (view === "dashboard") {
        return {
            type: "dashboard",
            data: window.invoices || []
        };
    }

    if (view === "insights") {
        return {
            type: "insights",
            data: {
                report: window.report || {},
                local: window.local_insights || [],
                ai: window.ai_insights || []
            }
        };
    }

    return { type: "dashboard", data: [] };
}


function export_pdf() {

    const export_state = get_export_data();

    if (export_state.type === "dashboard") {
        export_dashboard_pdf(export_state.data);
    }

    else if (export_state.type === "insights") {
        export_insights_pdf(export_state.data);
    }
}


function export_excel() {

    const export_state = get_export_data();

    if (export_state.type === "dashboard") {
        export_dashboard_csv(export_state.data);
    }

    else {
        alert("CSV export not available for insights view");
    }
}

function export_dashboard_pdf(invoices) {

    const win = window.open("", "", "width=900,height=700");

    const rows = invoices.map(doc => `
        <tr>
            <td>${doc.invoice_number || ""}</td>
            <td>${doc.vendor || ""}</td>
            <td>${doc.date || ""}</td>
            <td>${doc.vat || 0}</td>
            <td>${doc.total || 0}</td>
            <td>${doc.status || ""}</td>
        </tr>
    `).join("");

    win.document.write(`
        <html>
        <head>
            <title>Dashboard Export</title>
            <style>
                body { font-family: Arial; padding: 20px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; font-size: 12px; }
                th { background: #f5f5f5; }
            </style>
        </head>
        <body>
            <h2>All Invoices</h2>
            <table>
                <thead>
                    <tr>
                        <th>Invoice #</th>
                        <th>Vendor</th>
                        <th>Date</th>
                        <th>VAT</th>
                        <th>Total</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        </body>
        </html>
    `);

    win.document.close();
    win.print();
}

function export_dashboard_csv(invoices) {

    const csv = [];

    csv.push([
        "Invoice #",
        "Vendor",
        "Date",
        "VAT",
        "Total",
        "Status"
    ].join(","));

    invoices.forEach(doc => {

        csv.push([
            doc.invoice_number || "",
            doc.vendor || "",
            doc.date || "",
            doc.vat || 0,
            doc.total || 0,
            doc.status || ""
        ].join(","));
    });

    download_csv(csv.join("\n"), "dashboard.csv");
}

function export_insights_pdf(data) {

    const report = data.report || {};
    const local_insights = data.local || [];
    const ai_insights = data.ai || [];

    const win = window.open("", "", "width=900,height=700");

    const vendor_rows = report.vendors
        ? report.vendors.map(item => `<p>${item.vendor}: ${item.spend}</p>`).join("")
        : "";

    const local_rows = local_insights.map(i => `<p>${i.text}</p>`).join("");
    const ai_rows = ai_insights.map(i => `<p>${i.text}</p>`).join("");

    win.document.write(`
        <html>
        <head>
            <title>Insights Export</title>
            <style>
                body { font-family: Arial; padding: 20px; }
                h2 { margin-top: 20px; }
                p { margin: 5px 0; }
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
            ${vendor_rows || "<p>No vendor data</p>"}

            <h2>Local Insights</h2>
            ${local_rows || "<p>No insights</p>"}

            <h2>AI Insights</h2>
            ${ai_rows || "<p>No AI data</p>"}

        </body>
        </html>
    `);

    win.document.close();
    win.print();
}

function download_csv(content, filename) {

    const blob = new Blob([content], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();

    URL.revokeObjectURL(url);
}