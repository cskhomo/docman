window.report = {};
window.local_insights = [];
window.ai_insights = [];

async function load_insights() {

    try {

        const res = await fetch("/insights");
        const data = await res.json();

        window.report = data.report || {};
        window.local_insights = data.local_insights || [];
        window.ai_insights = data.ai_insights || [];
    }

    catch (err) {

        window.report = {};
        window.local_insights = [];
        window.ai_insights = [];
    }
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

    if (window.report.summary) {

        summary.innerHTML = `
            <div class="report_row">
                <span class="report_label">Invoices</span>
                <span class="report_value">${window.report.summary.invoice_count || 0}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Total Spend</span>
                <span class="report_value">${window.report.summary.total_spend || 0}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Total VAT</span>
                <span class="report_value">${window.report.summary.total_vat || 0}</span>
            </div>
        `;
    }

    if (window.report.approval_status) {

        approval.innerHTML = `
            <div class="report_row">
                <span class="report_label">Approved</span>
                <span class="report_value">${window.report.approval_status.approved || 0}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Pending</span>
                <span class="report_value">${window.report.approval_status.pending || 0}</span>
            </div>

            <div class="report_row">
                <span class="report_label">Rejected</span>
                <span class="report_value">${window.report.approval_status.rejected || 0}</span>
            </div>
        `;
    }

    if (window.report.vendors?.length) {

        window.report.vendors.forEach(item => {

            vendors.innerHTML += `
                <div class="vendor_item">
                    <span>${item.vendor}</span>
                    <span>${item.spend}</span>
                </div>
            `;
        });
    }

    else {

        vendors.innerHTML = `
            <div class="empty_state">
                No vendor data available
            </div>
        `;
    }

    if (window.local_insights.length) {

        window.local_insights.forEach(item => {

            local.innerHTML += `
                <div class="insight_item">
                    ${item.text || ""}
                </div>
            `;
        });
    }

    else {

        local.innerHTML = `
            <div class="empty_state">
                No insights available
            </div>
        `;
    }

    if (window.ai_insights.length) {

        window.ai_insights.forEach(item => {

            ai.innerHTML += `
                <div class="insight_item">
                    ${item.text || ""}
                </div>
            `;
        });
    }

    else {

        ai.innerHTML = `
            <div class="empty_state">
                AI analysis unavailable
            </div>
        `;
    }
}

async function show_insights() {

    await load_insights();

    render_insights();

    document.getElementById("dashboard_view").hidden = true;
    document.getElementById("queue_view").hidden = true;
    document.getElementById("insights_view").hidden = false;

    document.getElementById("dashboard_tab").classList.remove("active");
    document.getElementById("queue_tab").classList.remove("active");
    document.getElementById("insights_tab").classList.add("active");

    document.getElementById("approve_btn").hidden = true;
    document.getElementById("reject_btn").hidden = true;

    document.getElementById("export_excel_btn").hidden = true;
    document.getElementById("export_pdf_btn").hidden = false;

}
