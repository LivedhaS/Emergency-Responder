document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const role = document.getElementById("role").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("https://6748-2406-7400-ce-24f8-9448-cd0b-a0bd-a452.ngrok-free.app/login", {  // Ensure correct API endpoint
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, role }),
        });

        if (!response.ok) {
            throw new Error("Invalid login credentials");
        }

        const user = await response.json();
        localStorage.setItem("token", user.token);
        localStorage.setItem("role", user.role);

        // ✅ Correct redirection to dashboards based on role
        if (user.role === "patient") {
            window.location.href = "patient-dashboard.html";
        } else if (user.role === "doctor") {
            window.location.href = "doctor-dashboard.html";
        } else {
            alert("Invalid role detected!");
        }
    } catch (error) {
        alert(error.message);
    }
});

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById("password");
    passwordInput.type = passwordInput.type === "password" ? "text" : "password";
}