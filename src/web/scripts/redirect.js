document.addEventListener("DOMContentLoaded", app_init);

async function app_init() {
    await auth_check();
}

function get_page() {
    const path = window.location.pathname;

    const pages = {
        "welcome.html": "welcome",
        "upload.html": "upload",
        "dashboard.html": "dashboard",
        "insights.html": "insights"
    };

    for (const file in pages) {
        if (path.includes(file)) {
            return pages[file];
        }
    }

    return "index";
}

async function auth_check() {
    const token = localStorage.getItem("token");
    const page_name = get_page();

    if (!token) {
        handle_guest(page_name);
        return;
    }

    try {
        const response = await fetch("/auth/validate", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.ok) {
            handle_auth(page_name);
            return;
        }

        clear_token();
        handle_guest(page_name);

    } catch (error) {
        clear_token();
        handle_guest(page_name);
    }
}

function handle_guest(page_name) {
    if (page_name !== "welcome") {
        goto_welcome();
    }
}

function handle_auth(page_name) {
    if (page_name === "welcome" || page_name === "index") {
        goto_dashboard();
    }
}

function clear_token() {
    localStorage.removeItem("token");
}

function goto_welcome() {
    window.location.replace("/web/pages/welcome.html");
}

function goto_dashboard() {
    window.location.replace("/web/pages/dashboard.html");
}