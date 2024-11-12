// Function to send a message to the server
function sendMessage() {
  const userInput = document.getElementById("user-input");
  const message = userInput.value.trim();
  if (message === "") return;

  displayMessage(message, "user");
  userInput.value = "";

  console.log("Sending message:", message); // Debugging statement
  fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: message }),
  })
    .then((response) => {
      console.log("Received response:", response); // Debugging statement
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Bot response:", data);
      displayMessage(data.response, "bot");
    })
    .catch((error) => {
      console.error("Error:", error);
      displayMessage("Sorry, something went wrong. Please try again.", "bot");
    });
}

// Function to display a message
function displayMessage(text, sender) {
  const chatMessages = document.getElementById("chat-messages");

  // Create a new div element for the message
  const messageDiv = document.createElement("div");
  messageDiv.classList.add(sender === "user" ? "user-message" : "bot-message");

  // Convert Markdown or HTML formatted text to HTML for rendering
  messageDiv.innerHTML = convertFormatting(text);

  // Append the message to the chat container
  chatMessages.appendChild(messageDiv);

  // Scroll to the bottom of the chat
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to convert bold, italics, etc., using regular expressions or a library
function convertFormatting(text) {
  // Example: Convert **bold** and *italic* to HTML
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>"); // Bold
  text = text.replace(/\*(.*?)\*/g, "<em>$1</em>"); // Italics

  // If you use Markdown, you can use a library like `marked` to parse it fully
  // text = marked(text); // Uncomment if using marked.js

  return text;
}
