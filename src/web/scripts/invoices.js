document.addEventListener("DOMContentLoaded", init);

window.invoices = [];

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

        window.invoices = data.documents || [];
    }

    catch (err) {

        window.invoices = [];
    }
}

function render_table() {

    const body = document.getElementById("dashboard_table_body");
    const empty = document.getElementById("dashboard_empty");

    body.innerHTML = "";

    if (!window.invoices.length) {

        empty.hidden = false;
        return;
    }

    empty.hidden = true;

    window.invoices.forEach(doc => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${doc.invoice_number || ""}</td>
            <td>${doc.vendor || ""}</td>
            <td>${doc.date || ""}</td>
            <td>${doc.vat || 0}</td>
            <td>${doc.total || 0}</td>
            <td>${doc.status || ""}</td>
        `;

        body.appendChild(row);
    });
}

async function show_dashboard() {

    await load_data();

    render_table();

    document.getElementById("dashboard_view").hidden = false;
    document.getElementById("queue_view").hidden = true;
    document.getElementById("insights_view").hidden = true;

    document.getElementById("dashboard_tab").classList.add("active");
    document.getElementById("queue_tab").classList.remove("active");
    document.getElementById("insights_tab").classList.remove("active");

    document.getElementById("approve_btn").hidden = true;
    document.getElementById("reject_btn").hidden = true;

    document.getElementById("export_excel_btn").hidden = false;
    document.getElementById("export_pdf_btn").hidden = false; 
}

function goto_upload() {

    window.location.href =
        "/web/pages/upload.html";
}

function logout() {

    localStorage.removeItem("token");

    window.location.href =
        "/web/pages/welcome.html";
}