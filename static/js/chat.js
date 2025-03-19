const chatId = window.chatData.chatId;
const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const wsUrl = `${wsProtocol}${window.location.host}/ws/chat/${chatId}/`;
const chatMessages = document.getElementById('chat-messages');
let chatSocket;

function connectWebSocket() {
    chatSocket = new WebSocket(wsUrl);

    chatSocket.onopen = () => console.log("✅ WebSocket открыт");

    chatSocket.onmessage = (e) => {
        console.log("Получено сообщение:", e.data);
        try {
            const data = JSON.parse(e.data);
            if (data.message) {
                addMessageToChat(data);
            }
        } catch (error) {
            console.error("Ошибка парсинга JSON:", error);
        }
    };

    chatSocket.onclose = () => {
        console.warn("⚠️ WebSocket закрыт, пытаемся переподключиться...");
        setTimeout(connectWebSocket, 2000);
    };

    chatSocket.onerror = (error) => {
        console.error("WebSocket ошибка:", error);
    };
}

function addMessageToChat(data) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(
        'chat-message',
        data.sender_id.toString() === window.chatData.userId.toString() ? 'sent' : 'received'
    );

    const timestamp = data.timestamp ? new Date(data.timestamp) : new Date();
    const timeString = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.innerHTML = `
        <img src="${data.avatar || "{% static 'avatars/def_icon.png' %}"}" class="message-avatar" alt="Avatar">
        <div class="message-content">
            <span class="message-sender"><a href="${data.profile_url || '#'}">${data.sender}</a></span>
            <span class="message-text">${data.message}</span>
            <span class="message-time">${timeString}</span>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

document.getElementById('chat-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const input = document.getElementById('message-input');
    if (!input.value.trim()) return;
    chatSocket.send(JSON.stringify({ message: input.value }));
    input.value = '';
});

window.onload = function() {
    var chatContainer = document.getElementById('chat-messages');
    chatContainer.scrollTop = chatContainer.scrollHeight;
};

connectWebSocket();