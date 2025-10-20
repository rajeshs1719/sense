document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatWindow = document.getElementById('chat-window');

    // --- Elements for toggle ---
    const chatContainer = document.getElementById('chat-container');
    const chatToggleIcon = document.getElementById('chat-toggle-icon');
    const chatCloseBtn = document.getElementById('chat-close-btn');

    // --- Toggle Logic ---
    // When user clicks the icon button
    if (chatToggleIcon) {
        chatToggleIcon.addEventListener('click', () => {
            chatContainer.classList.add('active'); // Show chat window
            chatToggleIcon.style.display = 'none'; // Hide icon
        });
    }

    // When user clicks the 'X' close button
    if (chatCloseBtn) {
        chatCloseBtn.addEventListener('click', () => {
            chatContainer.classList.remove('active'); // Hide chat window
            if (chatToggleIcon) {
                chatToggleIcon.style.display = 'flex'; // Show icon
            }
        });
    }

    // --- CSRF Token Helper ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // --- Add Message to UI Function ---
    function addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

        const p = document.createElement('p');
        p.textContent = message;
        messageDiv.appendChild(p);

        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to bottom
    }

    // --- Handle Form Submission (Sending a message) ---
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message === '') return;

        // 1. Display user's message
        addMessage(message, 'user');
        messageInput.value = '';

        try {
            // 2. Send message to Django backend
            const response = await fetch('/chat/send_message/', { // This URL must match your urls.py
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const data = await response.json();

            // 3. Display bot's reply
            if (data.reply) {
                addMessage(data.reply, 'bot');
            } else if (data.error) {
                addMessage(`Error: ${data.error}`, 'bot');
            }

        } catch (error) {
            console.error('Error:', error);
            addMessage('Error: Could not connect to the server.', 'bot');
        }
    });
});