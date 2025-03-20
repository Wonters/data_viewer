export function initChat() {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const socket = new WebSocket("ws://" + window.location.host + "/ws/chat/");

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const message = document.createElement("p");
        message.textContent = "👤 " + data.message;
        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    document.getElementById("send-button").addEventListener("click", () => {
        socket.send(JSON.stringify({ "message": messageInput.value }));
        messageInput.value = "";
    });
}
