async function sendMessage() {
    const userInput = document.getElementById("userInput").value.trim();
    if (!userInput) return; // Prevent empty messages

    const messagesDiv = document.getElementById("messages");

    // Display user message
    const userMessage = document.createElement("p");
    userMessage.innerHTML = `<strong>You:</strong> ${userInput}`;
    messagesDiv.appendChild(userMessage);
    document.getElementById("userInput").value = "";

    try {
        const response = await fetch("http://localhost:3000/chatbot", { // Call the backend
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ userInput })
        });

        const data = await response.json();
        console.log("Chatbot Reply:", data); // Debugging log

        // Show chatbot response
        const botMessage = document.createElement("p");
        botMessage.innerHTML = `<strong>Bot:</strong> ${data.reply}`;
        messagesDiv.appendChild(botMessage);
    } catch (error) {
        console.error("Error:", error);
        const errorMessage = document.createElement("p");
        errorMessage.innerHTML = `<strong>Bot:</strong> Error processing request.`;
        messagesDiv.appendChild(errorMessage);
    }

    // Scroll to latest message
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
