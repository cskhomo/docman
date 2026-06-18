let queue_invoices = [];

async function load_queue() {

    const token = localStorage.getItem("token");

    try {

        const res = await fetch("/que", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await res.json();

        queue_invoices = data.documents || [];
    }

    catch (err) {

        queue_invoices = [];
    }
}

function render_queue() {

    const body = document.getElementById("queue_table_body");
    const empty = document.getElementById("queue_empty");

    body.innerHTML = "";

    if (!queue_invoices.length) {

        empty.hidden = false;
        return;
    }

    empty.hidden = true;

    queue_invoices.forEach((invoice, index) => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <input
                    type="checkbox"
                    data-index="${index}"
                >
            </td>

            <td>${invoice.invoice_number || ""}</td>
            <td>${invoice.vendor || ""}</td>
            <td>${invoice.date || ""}</td>
            <td>${invoice.vat || 0}</td>
            <td>${invoice.total || 0}</td>
        `;

        body.appendChild(row);
    });

    attach_single_selection();
}

function attach_single_selection() {

    const checkboxes = document.querySelectorAll(
        "#queue_table_body input[type='checkbox']"
    );

    checkboxes.forEach(box => {

        box.addEventListener("change", () => {

            if (!box.checked) {
                return;
            }

            checkboxes.forEach(other => {

                if (other !== box) {
                    other.checked = false;
                }
            });
        });
    });
}

function get_selected_invoice() {

    const selected = document.querySelector(
        "#queue_table_body input[type='checkbox']:checked"
    );

    if (!selected) {
        return null;
    }

    return queue_invoices[
        Number(selected.dataset.index)
    ];
}

async function approve_selected() {

    const invoice = get_selected_invoice();

    if (!invoice) {
        return;
    }

    const token = localStorage.getItem("token");

    try {

        const res = await fetch("/status", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify({
                invoice_number: invoice.invoice_number,
                action: "approve"
            })
        });

        const data = await res.json();

        if (data.status !== "success") {
            return;
        }

        await load_queue();
        render_queue();

        if (typeof load_data === "function") {
            await load_data();
            render_table();
        }
    }

    catch (err) {}
}

async function reject_selected() {

    const invoice = get_selected_invoice();

    if (!invoice) {
        return;
    }

    const token = localStorage.getItem("token");

    try {

        const res = await fetch("/status", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify({
                invoice_number: invoice.invoice_number,
                action: "reject"
            })
        });

        const data = await res.json();

        if (data.status !== "success") {
            return;
        }

        await load_queue();
        render_queue();

        if (typeof load_data === "function") {
            await load_data();
            render_table();
        }
    }

    catch (err) {}
}

async function show_queue() {

    await load_queue();

    render_queue();

    document.getElementById("dashboard_view").hidden = true;
    document.getElementById("insights_view").hidden = true;
    document.getElementById("queue_view").hidden = false;

    document.getElementById("dashboard_tab").classList.remove("active");
    document.getElementById("insights_tab").classList.remove("active");
    document.getElementById("queue_tab").classList.add("active");

    document.getElementById("approve_btn").hidden = false;
    document.getElementById("reject_btn").hidden = false;

    document.getElementById("export_excel_btn").hidden = false;
}