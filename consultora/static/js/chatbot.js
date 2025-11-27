document.addEventListener('DOMContentLoaded', () => {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotModal = document.getElementById('chatbot-modal');
    const closeChatbot = document.getElementById('close-chatbot');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send-btn');
    const chatMessages = document.getElementById('chat-messages');

    // Stores the conversation history to maintain context
    let chatHistory = [];
    
    // URL to the Django backend endpoint
    const CHATBOT_API_URL = '/api/chatbot/';

    // System prompt for the chatbot's persona and context
    const SYSTEM_PROMPT = `
        Eres un asistente de servicio al cliente amable y cordial para la consultora "IA Consultores".
        Tu misión es ayudar a los visitantes a entender nuestros servicios y a animarlos a dejar sus datos de contacto.

        Sobre nosotros:
        - Somos "IA Consultores", una empresa dedicada a transformar y optimizar pequeñas y medianas empresas (PYMES) a través de soluciones de Inteligencia Artificial.        
        - Ofrecemos servicios como automatización de procesos, análisis de datos y chatbots para atención al cliente.
        - Nuestra especialidad es la implementación de soluciones de IA a medida para PYMES.
        - No damos soporte técnico para productos de terceros.

        Instrucciones de interacción:
        - Mantén un tono profesional, pero amigable.
        - Sé conciso y directo en tus respuestas.
        - Si el usuario pregunta por precios, explícale que las cotizaciones son personalizadas y que necesita contactar a un consultor.
        - Después de que el usuario haya hecho 2 preguntas sobre nuestros servicios, sugiere que deje sus datos en el formulario de contacto para una consulta gratuita.
        - Usa emojis de manera moderada para mantener un tono cordial.
    `;

    // Function to parse and format Markdown in bot's responses
    const formatBotResponse = (text) => {
        let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        html = html.replace(/_(\s*.*?)\s*_/g, '<em>$1</em>');

        // Handles lists
        html = html.replace(/^\*\s(.+)/gm, '<li>$1</li>');
        if (html.includes('<li>')) {
            html = `<ul>${html}</ul>`;
        }

        return html;
    };

    const sendMessage = async (userMessage) => {
        if (!userMessage.trim()) return;

        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'message-user');
        userMessageDiv.textContent = userMessage;
        chatMessages.appendChild(userMessageDiv);

        chatInput.value = '';
        chatHistory.push({ role: 'user', parts: [{ text: userMessage }] });
        
        const botTyping = showTypingIndicator();

        try {
            const response = await fetch(CHATBOT_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                    system_prompt: SYSTEM_PROMPT,
                    chat_history: chatHistory
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            botTyping.remove();

            const botResponseText = data.message;
            addMessage(botResponseText, 'bot');
        } catch (error) {
            console.error('Error fetching response from the AI:', error);
            botTyping.remove();
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('message', 'message-bot', 'text-red-400');
            errorMessage.textContent = 'Ocurrió un error. Por favor, inténtalo de nuevo más tarde.';
            chatMessages.appendChild(errorMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    };

    const addMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `message-${sender}`);
        if (sender === 'bot') {
            messageDiv.innerHTML = formatBotResponse(text);
        } else {
            messageDiv.textContent = text;
        }
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        if (sender === 'bot') {
            chatHistory.push({ role: 'model', parts: [{ text }] });
        }
    };

    const showTypingIndicator = () => {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('message', 'message-bot', 'animate-pulse');
        typingIndicator.innerHTML = `
            <div class="flex space-x-1">
                <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
                <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
                <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
            </div>
        `;
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingIndicator;
    };

    // Event listener for showing/hiding the modal
    chatbotToggle.addEventListener('click', () => {
        chatbotModal.classList.toggle('hidden');
        if (!chatbotModal.classList.contains('hidden') && chatMessages.children.length === 0) {
            addMessage('¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?', 'bot');
        }
    });

    closeChatbot.addEventListener('click', () => {
        chatbotModal.classList.add('hidden');
    });

    // Event listener for the send button
    chatSendBtn.addEventListener('click', () => {
        const messageText = chatInput.value.trim();
        if (messageText !== '') {
            sendMessage(messageText);
        }
    });

    // Event listener for the Enter key in the input field
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const messageText = chatInput.value.trim();
            if (messageText !== '') {
                sendMessage(messageText);
            }
        }
    });
});
