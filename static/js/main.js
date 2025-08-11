// FashionHub Kenya Chatbot - JavaScript Functionality
// File: static/js/main.js

// Global variables
let currentLanguage = 'en';
let isTyping = false;
let conversationHistory = [];

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    const messageInput = document.getElementById('messageInput');
    
    // Auto-resize textarea
    messageInput.addEventListener('input', autoResizeTextarea);
    
    // Send on Enter (but allow Shift+Enter for new line)
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Focus on input field
    messageInput.focus();
    
    console.log('🇰🇪 FashionHub Kenya Chatbot initialized!');
}

// Auto-resize textarea function
function autoResizeTextarea() {
    const textarea = document.getElementById('messageInput');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

// Add message to chat interface
function addMessage(content, sender, timestamp = null) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const time = timestamp ? new Date(timestamp).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'}) 
                           : new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
    const senderName = sender === 'user' ? 'You' : 'AI Assistant';
    
    // Format message content (preserve line breaks and emojis)
    const formattedContent = content.replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            <div class="message-content">${formattedContent}</div>
            <div class="message-time">${senderName} • ${time}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Add to conversation history
    conversationHistory.push({
        content: content,
        sender: sender,
        timestamp: timestamp || new Date().toISOString()
    });
}

// Show typing indicator
function showTypingIndicator() {
    if (isTyping) return;
    isTyping = true;
    
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.style.display = 'flex';
    
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.style.display = 'none';
    isTyping = false;
}

// Scroll chat to bottom
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Send message function
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Disable send button temporarily
    const sendButton = document.getElementById('sendButton');
    sendButton.disabled = true;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input and reset height
    input.value = '';
    autoResizeTextarea();
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send message to backend API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                context: {
                    language: currentLanguage,
                    history_length: conversationHistory.length
                }
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Simulate realistic typing delay
        const typingDelay = Math.min(data.response.length * 20 + 1000, 3000);
        
        setTimeout(() => {
            hideTypingIndicator();
            addMessage(data.response, 'bot', data.timestamp);
            
            // Update language if detected
            if (data.language && data.language !== currentLanguage) {
                updateLanguageDisplay(data.language);
            }
            
            // Re-enable send button
            sendButton.disabled = false;
            
            // Focus back on input
            input.focus();
            
        }, typingDelay);
        
    } catch (error) {
        console.error('Error sending message:', error);
        
        hideTypingIndicator();
        
        // Show error message
        const errorMessage = "Sorry, I'm having trouble connecting right now. Please try again! 😊\n\nTip: Make sure you're connected to the internet.";
        addMessage(errorMessage, 'bot');
        
        // Re-enable send button
        sendButton.disabled = false;
        input.focus();
    }
}

// Send quick reply
function sendQuickReply(message) {
    const input = document.getElementById('messageInput');
    input.value = message;
    input.focus();
    autoResizeTextarea();
    sendMessage();
}

// Toggle language
function toggleLanguage() {
    currentLanguage = currentLanguage === 'en' ? 'sw' : 'en';
    updateLanguageDisplay(currentLanguage);
    updateInputPlaceholder();
    
    // Add a system message about language change
    const langMessage = currentLanguage === 'en' 
        ? "Language switched to English. I can help you in both English and Swahili! 🇬🇧"
        : "Lugha imebadilishwa kuwa Kiswahili. Naweza kukusaidia kwa Kiingereza na Kiswahili! 🇰🇪";
    
    addMessage(langMessage, 'bot');
}

// Update language display
function updateLanguageDisplay(language) {
    const langText = document.getElementById('langText');
    if (language === 'sw') {
        langText.textContent = 'SW/EN';
        currentLanguage = 'sw';
    } else {
        langText.textContent = 'EN/SW';
        currentLanguage = 'en';
    }
}

// Update input placeholder based on language
function updateInputPlaceholder() {
    const input = document.getElementById('messageInput');
    input.placeholder = currentLanguage === 'en' 
        ? 'Type your message...' 
        : 'Andika ujumbe wako...';
}

// Clear conversation function
async function clearConversation() {
    if (!confirm('Are you sure you want to clear the conversation? / Je, una uhakika unataka kufuta mazungumzo?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/conversation/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Clear the chat interface
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="message bot">
                    <div class="message-bubble">
                        <div class="message-content">
                            Conversation cleared! How can I help you today? / Mazungumzo yamefutwa! Ninawezaje kukusaidia leo?
                        </div>
                        <div class="message-time">AI Assistant • now</div>
                    </div>
                </div>
            `;
            
            // Clear local history
            conversationHistory = [];
            
        } else {
            throw new Error('Failed to clear conversation');
        }
    } catch (error) {
        console.error('Error clearing conversation:', error);
        alert('Failed to clear conversation. Please try again.');
    }
}

// Get conversation history
async function getConversationHistory() {
    try {
        const response = await fetch('/api/conversation/history');
        const history = await response.json();
        return history;
    } catch (error) {
        console.error('Error fetching conversation history:', error);
        return [];
    }
}

// Download conversation as text file
function downloadConversation() {
    if (conversationHistory.length === 0) {
        alert('No conversation to download!');
        return;
    }
    
    let conversationText = 'FashionHub Kenya - Conversation History\n';
    conversationText += '=====================================\n\n';
    
    conversationHistory.forEach(msg => {
        const time = new Date(msg.timestamp).toLocaleString();
        const sender = msg.sender === 'user' ? 'Customer' : 'AI Assistant';
        conversationText += `[${time}] ${sender}:\n${msg.content}\n\n`;
    });
    
    // Create and download file
    const blob = new Blob([conversationText], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `FashionHub-Conversation-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Show/hide features based on screen size
function handleResponsiveFeatures() {
    const width = window.innerWidth;
    const quickReplies = document.querySelector('.quick-replies-grid');
    
    if (width < 768) {
        // Mobile optimizations
        quickReplies.style.gridTemplateColumns = 'repeat(2, 1fr)';
    } else if (width < 480) {
        // Very small screens
        quickReplies.style.gridTemplateColumns = '1fr';
    } else {
        // Desktop
        quickReplies.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
    }
}

// Handle window resize
window.addEventListener('resize', handleResponsiveFeatures);

// Initialize responsive features
handleResponsiveFeatures();

// Service Worker for offline functionality (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
    
    // Ctrl/Cmd + L to clear conversation
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        clearConversation();
    }
    
    // Ctrl/Cmd + D to download conversation
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        downloadConversation();
    }
});

// Add copy message functionality
function copyMessage(element) {
    const messageContent = element.querySelector('.message-content').textContent;
    navigator.clipboard.writeText(messageContent).then(() => {
        // Show temporary feedback
        const originalContent = element.innerHTML;
        element.innerHTML = '<div class="copy-feedback">Copied! ✓</div>';
        setTimeout(() => {
            element.innerHTML = originalContent;
        }, 1000);
    });
}

// Add click handlers for messages (for copying)
document.addEventListener('click', function(e) {
    if (e.target.closest('.message-bubble')) {
        const messageBubble = e.target.closest('.message-bubble');
        if (e.detail === 2) { // Double click
            copyMessage(messageBubble);
        }
    }
});

// Add connection status monitoring
function monitorConnection() {
    function updateConnectionStatus() {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-indicator span');
        
        if (navigator.onLine) {
            statusDot.style.background = '#22c55e';
            statusText.textContent = 'Online';
        } else {
            statusDot.style.background = '#ef4444';
            statusText.textContent = 'Offline';
        }
    }
    
    window.addEventListener('online', updateConnectionStatus);
    window.addEventListener('offline', updateConnectionStatus);
    
    // Initial check
    updateConnectionStatus();
}

// Initialize connection monitoring
monitorConnection();

// Export functions for global access
window.fashionHubChat = {
    sendMessage,
    sendQuickReply,
    toggleLanguage,
    clearConversation,
    downloadConversation,
    addMessage
};

console.log('🛍️ FashionHub Kenya Chatbot JavaScript loaded successfully!');