document.addEventListener("DOMContentLoaded", page_init);

function page_init() {
    document
        .getElementById("upload_form")
        .addEventListener("submit", check_file);

    document
        .getElementById("back_btn")
        .addEventListener("click", goto_dashboard);

    check_error();
}

function show_error(message) {
    const error_div = document.getElementById("error_text");

    error_div.textContent = message;
    error_div.classList.add("show");
}

function hide_error() {
    const error_div = document.getElementById("error_text");

    error_div.textContent = "";
    error_div.classList.remove("show");
}

function check_file(e) {
    hide_error();

    const file_input =
        document.getElementById("file_input");

    if (!file_input.files.length) {
        e.preventDefault();

        show_error(
            "Please select a PDF file."
        );

        return;
    }

    const file = file_input.files[0];

    const is_pdf =
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf");

    if (!is_pdf) {
        e.preventDefault();

        show_error(
            "Only PDF files are allowed."
        );

        return;
    }
}

function check_error() {
    const url_params =
        new URLSearchParams(
            window.location.search
        );

    const error_param =
        url_params.get("error");

    if (!error_param) {
        return;
    }

    show_error(
        decodeURIComponent(error_param)
    );

    window.history.replaceState(
        {},
        document.title,
        window.location.pathname
    );
}

function goto_dashboard() {
    window.location.replace(
        "/web/pages/dashboard.html"
    );
}