document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token");
    const userRole = localStorage.getItem("role");

    // Redirect to login if not authenticated
    if (!token || userRole !== "patient") {
        window.location.href = "login.html";
        return;
    }

    // Logout functionality
    document.getElementById("logout").addEventListener("click", function () {
        localStorage.clear();
        window.location.href = "index.html";
    });

    
    const burnBtn = document.getElementById("uploadBurnImage");
    if (burnBtn) {
        burnBtn.addEventListener("click", function () {
            window.location.href = "http://192.168.0.101:8501";
        });
    }
    
    const woundBtn = document.getElementById("uploadWoundImage");
    if (woundBtn) {
        woundBtn.addEventListener("click", function () {
            window.location.href = "http://192.168.0.101:8503";
        });
    }
    
    const assistantBtn = document.getElementById("firstAidBtn");
    if (assistantBtn) {
        assistantBtn.addEventListener("click", function () {
            window.location.href = "http://192.168.0.101:8502";
        });
    }
    
    
    
});
