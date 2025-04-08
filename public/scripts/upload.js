function predictBurn() {
    let imageInput = document.getElementById("imageInput");
    let file = imageInput.files[0];

    if (!file) {
        alert("Please select an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/predict", {  // Flask backend URL
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errData => { throw errData });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerHTML = `<b style='color:red;'>Error: ${data.error}</b>`;
        } else {
            document.getElementById("result").innerHTML = `
                <b>Prediction:</b> ${data.predicted_class} <br>
                <b>Confidence:</b> ${data.confidence.toFixed(2)}
            `;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = `<b style='color:red;'>Error: ${error.error || "Unknown error"}</b>`;
    });
}
