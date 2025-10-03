// Chat functionality
function initializeChat() {
    const messageInput = document.querySelector('.message-field');
    const sendButton = document.querySelector('.message-input .btn-primary');
    const chatMessages = document.querySelector('.chat-messages');

    if (messageInput && sendButton) {
        function sendMessage() {
            const message = messageInput.value.trim();
            if (message) {
                addMessageToChat('Alex Chen', message, 'just now');
                messageInput.value = '';
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }

        sendButton.addEventListener('click', sendMessage);

        messageInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendMessage();
        });
    }
}

function addMessageToChat(sender, message, timestamp) {
    const chatMessages = document.querySelector('.chat-messages');
    if (!chatMessages) return;

    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.innerHTML = `
        <img src="https://via.placeholder.com/32x32/4A90E2/FFFFFF?text=${sender.charAt(0)}" alt="${sender}">
        <div class="message-content">
            <div class="message-header">
                <span class="sender">${sender}</span>
                <span class="timestamp">${timestamp}</span>
            </div>
            <p>${message}</p>
        </div>
    `;
    chatMessages.appendChild(messageElement);
}