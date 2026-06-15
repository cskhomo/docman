document.addEventListener("DOMContentLoaded", page_init);

const email_test = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function page_init() {
    document.getElementById("show_signup_btn").addEventListener("click", show_signup);
    document.getElementById("show_login_btn").addEventListener("click", show_login);
    document.getElementById("signup_form").addEventListener("submit", form_signup);
    document.getElementById("login_form").addEventListener("submit", form_login);
}

function show_login() {
    document.getElementById("signup_view").hidden = true;
    document.getElementById("login_view").hidden = false;
    clear_all();
}

function show_signup() {
    document.getElementById("signup_view").hidden = false;
    document.getElementById("login_view").hidden = true;
    clear_all();
}

function clear_field(field_id) {
    const error_span = document.getElementById(field_id + "_error");
    const input = document.getElementById(field_id);

    if (error_span) {
        error_span.textContent = "";
    }

    if (input) {
        input.classList.remove("error-input");
    }
}

function set_field(field_id, message) {
    const error_span = document.getElementById(field_id + "_error");
    const input = document.getElementById(field_id);

    if (error_span) {
        error_span.textContent = message;
    }

    if (input) {
        input.classList.add("error-input");
    }
}

function clear_form(form_id) {
    const error_div = document.getElementById(form_id + "_error");

    if (error_div) {
        error_div.textContent = "";
        error_div.classList.remove("show");
        error_div.classList.remove("form-success");
    }
}

function set_form(form_id, message) {
    const error_div = document.getElementById(form_id + "_error");

    if (error_div) {
        error_div.textContent = message;
        error_div.classList.add("show");
        error_div.classList.remove("form-success");
    }
}

function set_success(form_id, message) {
    const error_div = document.getElementById(form_id + "_error");

    if (error_div) {
        error_div.textContent = message;
        error_div.classList.add("show");
        error_div.classList.add("form-success");
    }
}

function clear_all() {
    ["signup_email", "signup_password", "login_email", "login_password"].forEach(clear_field);
    ["signup_form", "login_form"].forEach(clear_form);
}

function check_email(email) {
    if (!email.trim()) {
        return "Email is required";
    }

    if (!email_test.test(email)) {
        return "Enter a valid email address";
    }

    return null;
}

function check_pass(password, is_signup) {
    if (!password) {
        return "Password is required";
    }

    if (is_signup && password.length < 6) {
        return "Password must be at least 6 characters";
    }

    return null;
}

async function form_signup(e) {
    e.preventDefault();

    clear_all();

    const email = document.getElementById("signup_email").value.trim();
    const password = document.getElementById("signup_password").value;

    let has_error = false;

    const email_error = check_email(email);

    if (email_error) {
        set_field("signup_email", email_error);
        has_error = true;
    }

    const pass_error = check_pass(password, true);

    if (pass_error) {
        set_field("signup_password", pass_error);
        has_error = true;
    }

    if (has_error) {
        return;
    }

    try {
        const response = await fetch("/auth/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            document.getElementById("signup_form").reset();

            show_login();

            document.getElementById("login_email").value = email;

            set_success(
                "login_form",
                "Account created. Please sign in."
            );
        } else {
            set_form(
                "signup_form",
                data.reason || "Signup failed"
            );
        }

    } catch (error) {
        set_form(
            "signup_form",
            "Network error. Please try again."
        );
    }
}

async function form_login(e) {
    e.preventDefault();

    clear_all();

    const email = document.getElementById("login_email").value.trim();
    const password = document.getElementById("login_password").value;

    let has_error = false;

    const email_error = check_email(email);

    if (email_error) {
        set_field("login_email", email_error);
        has_error = true;
    }

    const pass_error = check_pass(password, false);

    if (pass_error) {
        set_field("login_password", pass_error);
        has_error = true;
    }

    if (has_error) {
        return;
    }

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            localStorage.setItem(
                "token",
                data.token
            );

            set_success(
                "login_form",
                "Login successful"
            );

            setTimeout(
                goto_dashboard,
                500
            );
        } else {
            set_form(
                "login_form",
                data.reason || "Login failed"
            );
        }

    } catch (error) {
        set_form(
            "login_form",
            "Network error. Please try again."
        );
    }
}

function goto_welcome() {
    window.location.replace("/web/pages/welcome.html");
}

function goto_dashboard() {
    window.location.replace("/web/pages/dashboard.html");
}

function goto_upload() {
    window.location.replace("/web/pages/upload.html");
}

function goto_insights() {
    window.location.replace("/web/pages/insights.html");
}