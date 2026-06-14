function showLogin() {
    document.getElementById("signup-view").hidden = true;
    document.getElementById("login-view").hidden = false;
}

function showSignup() {
    document.getElementById("signup-view").hidden = false;
    document.getElementById("login-view").hidden = true;
}


// -----------------------
// SIGNUP
// -----------------------
document.getElementById("signup-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;

    const res = await fetch("/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    alert(data.status + (data.reason ? " - " + data.reason : ""));
});


// -----------------------
// LOGIN
// -----------------------
document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.status === "success") {
        alert("Login successful");
        // later: store token + redirect to upload page
    } else {
        alert(data.reason || "Login failed");
    }
});