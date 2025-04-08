document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value; // Now correctly includes 'patient' and 'doctor'

    const response = await fetch("https://6748-2406-7400-ce-24f8-9448-cd0b-a0bd-a452.ngrok-free.app/register", {  // Update the correct API endpoint
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, role }),
    });

    if (response.ok) {
        alert("Registration successful! Redirecting to login...");
        window.location.href = "login.html";  // Redirect after successful registration
    } else {
        const data = await response.json();
        alert("Registration failed: " + (data.message || "Please try again"));
    }
});