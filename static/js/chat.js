/**
 * Chat functionality for MutaSight AI Drug Discovery Platform
 * Handles real-time messaging and AI assistant interactions
 */

class ChatManager {
    constructor(projectId) {
        this.projectId = projectId;
        this.socket = null;
        this.isConnected = false;
        this.messageInput = null;
        this.aiInput = null;
        this.messagesContainer = null;
        this.typingIndicator = null;
        
        this.init();
    }

    /**
     * Initialize chat functionality
     */
    init() {
        // Initialize Socket.IO connection
        this.socket = io();
        
        // Get DOM elements
        this.messageInput = document.getElementById('messageInput');
        this.aiInput = document.getElementById('aiQuestion');
        this.messagesContainer = document.querySelector('.messages-container');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        // Set up event listeners
        this.setupEventListeners();
        this.setupSocketEvents();
        
        // Join project room
        if (this.projectId) {
            this.joinProject();
        }
    }

    /**
     * Set up DOM event listeners
     */
    setupEventListeners() {
        // Send message button
        const sendButton = document.getElementById('sendMessage');
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }

        // Ask AI button
        const askAIButton = document.getElementById('askAI');
        if (askAIButton) {
            askAIButton.addEventListener('click', () => this.askAI());
        }

        // Enter key handling
        if (this.messageInput) {
            this.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        if (this.aiInput) {
            this.aiInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.askAI();
                }
            });
        }
    }

    /**
     * Set up Socket.IO event handlers
     */
    setupSocketEvents() {
        // Connection events
        this.socket.on('connect', () => {
            console.log('Connected to chat server');
            this.isConnected = true;
            this.showConnectionStatus('Connected', 'success');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from chat server');
            this.isConnected = false;
            this.showConnectionStatus('Disconnected', 'danger');
        });

        // Message events
        this.socket.on('receive_message', (data) => {
            this.displayMessage(data);
        });

        this.socket.on('status', (data) => {
            this.displayStatusMessage(data.msg);
        });

        // Error handling
        this.socket.on('error', (error) => {
            console.error('Socket error:', error);
            this.showNotification('Connection error occurred', 'danger');
        });
    }

    /**
     * Join project chat room
     */
    joinProject() {
        if (this.socket && this.projectId) {
            this.socket.emit('join_project', { project_id: this.projectId });
        }
    }

    /**
     * Leave project chat room
     */
    leaveProject() {
        if (this.socket && this.projectId) {
            this.socket.emit('leave_project', { project_id: this.projectId });
        }
    }

    /**
     * Send a chat message
     */
    sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            this.showNotification('Please enter a message', 'warning');
            return;
        }

        if (!this.isConnected) {
            this.showNotification('Not connected to chat server', 'danger');
            return;
        }

        // Emit message to server
        this.socket.emit('send_message', {
            project_id: this.projectId,
            message: message
        });

        // Clear input
        this.messageInput.value = '';
    }

    /**
     * Ask AI assistant
     */
    askAI() {
        const question = this.aiInput.value.trim();
        
        if (!question) {
            this.showNotification('Please enter a question', 'warning');
            return;
        }

        if (!this.isConnected) {
            this.showNotification('Not connected to chat server', 'danger');
            return;
        }

        // Show typing indicator
        this.showTypingIndicator();

        // Emit question to AI
        this.socket.emit('chatbot_query', {
            project_id: this.projectId,
            query: question
        });

        // Clear input
        this.aiInput.value = '';
    }

    /**
     * Display a message in the chat
     */
    displayMessage(data) {
        const messageElement = this.createMessageElement(data);
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
        
        // Hide typing indicator if it was shown
        this.hideTypingIndicator();
        
        // Add animation
        messageElement.classList.add('fade-in-up');
    }

    /**
     * Create a message DOM element
     */
    createMessageElement(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message-item ${data.message_type === 'bot' ? 'ai-message' : 'user-message'}`;
        messageDiv.setAttribute('data-message-type', data.message_type);

        const avatarClass = data.message_type === 'bot' ? 'fas fa-robot' : data.username[0].toUpperCase();
        const username = data.message_type === 'bot' ? 'MutaSight AI Assistant' : data.username;

        messageDiv.innerHTML = `
            <div class="message-header">
                <div class="message-avatar">
                    ${data.message_type === 'bot' ? `<i class="${avatarClass}"></i>` : avatarClass}
                </div>
                <div class="message-info">
                    <span class="message-author">${username}</span>
                    <span class="message-time">${this.formatTime(data.timestamp)}</span>
                </div>
            </div>
            <div class="message-content">
                ${this.formatMessageContent(data.message)}
            </div>
        `;

        return messageDiv;
    }

    /**
     * Display a status message
     */
    displayStatusMessage(message) {
        const statusDiv = document.createElement('div');
        statusDiv.className = 'status-message text-center text-muted my-2';
        statusDiv.innerHTML = `<small><em>${message}</em></small>`;
        
        this.messagesContainer.appendChild(statusDiv);
        this.scrollToBottom();
    }

    /**
     * Format message content (handle links, mentions, etc.)
     */
    formatMessageContent(content) {
        // Convert URLs to links
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        content = content.replace(urlRegex, '<a href="$1" target="_blank" class="text-decoration-none">$1</a>');
        
        // Convert newlines to <br>
        content = content.replace(/\n/g, '<br>');
        
        // Highlight scientific terms (basic implementation)
        const scientificTerms = [
            'SMILES', 'InChI', 'molecular weight', 'LogP', 'bioavailability',
            'pharmacokinetics', 'ADMET', 'IC50', 'EC50', 'half-life'
        ];
        
        scientificTerms.forEach(term => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            content = content.replace(regex, `<strong class="text-primary">${term}</strong>`);
        });
        
        return content;
    }

    /**
     * Format timestamp for display
     */
    formatTime(timestamp) {
        if (typeof timestamp === 'string') {
            return timestamp;
        }
        
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'flex';
            this.scrollToBottom();
        }
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'none';
        }
    }

    /**
     * Scroll to bottom of messages
     */
    scrollToBottom() {
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    }

    /**
     * Show connection status
     */
    showConnectionStatus(message, type) {
        // Create or update connection status indicator
        let statusElement = document.getElementById('connection-status');
        
        if (!statusElement) {
            statusElement = document.createElement('div');
            statusElement.id = 'connection-status';
            statusElement.className = 'position-fixed top-0 end-0 m-3';
            statusElement.style.zIndex = '9999';
            document.body.appendChild(statusElement);
        }

        statusElement.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-wifi me-2"></i>${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        // Auto-hide after 3 seconds
        setTimeout(() => {
            const alert = statusElement.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 3000);
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'position-fixed top-0 end-0 m-3';
        notification.style.zIndex = '9999';
        
        notification.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 4 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 4000);
    }

    /**
     * Send quick response
     */
    sendQuickResponse(response) {
        if (this.messageInput) {
            this.messageInput.value = response;
            this.sendMessage();
        }
    }

    /**
     * Ask quick AI question
     */
    askQuickQuestion(question) {
        if (this.aiInput) {
            this.aiInput.value = question;
            this.askAI();
        }
    }

    /**
     * Clear chat history (local display only)
     */
    clearChatDisplay() {
        if (this.messagesContainer) {
            this.messagesContainer.innerHTML = '';
        }
    }

    /**
     * Export chat history
     */
    exportChatHistory() {
        const messages = Array.from(this.messagesContainer.querySelectorAll('.message-item'));
        const history = messages.map(msg => {
            const author = msg.querySelector('.message-author').textContent;
            const time = msg.querySelector('.message-time').textContent;
            const content = msg.querySelector('.message-content').textContent;
            const type = msg.getAttribute('data-message-type');
            
            return { author, time, content, type };
        });

        const blob = new Blob([JSON.stringify(history, null, 2)], { 
            type: 'application/json' 
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-history-${this.projectId}-${new Date().toISOString().slice(0,10)}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * Cleanup when leaving the page
     */
    cleanup() {
        if (this.socket) {
            this.leaveProject();
            this.socket.disconnect();
        }
    }
}

// Quick response templates
const QuickResponses = {
    greetings: [
        "Hello team!",
        "Good morning everyone",
        "Hi there!",
        "Let's get started"
    ],
    
    analysis: [
        "Let's analyze this compound",
        "Running molecular analysis...",
        "What are the key properties?",
        "Any safety concerns?"
    ],
    
    formulation: [
        "Which excipients should we consider?",
        "What's the best dosage form?",
        "Any compatibility issues?",
        "Let's review the formulation"
    ],
    
    approval: [
        "Looks good to me",
        "Approved",
        "LGTM (Looks Good To Me)",
        "Ready to proceed"
    ]
};

// AI question templates
const AIQuestions = {
    molecular: [
        "What is the mechanism of action for this compound?",
        "How do I calculate LogP?",
        "What are the ADMET properties?",
        "Is this compound drug-like?"
    ],
    
    formulation: [
        "Which excipients are compatible with this API?",
        "What's the best dosage form for this compound?",
        "How do I improve solubility?",
        "What are the stability considerations?"
    ],
    
    regulatory: [
        "What are the FDA requirements for this indication?",
        "Which clinical trials are needed?",
        "What safety studies are required?",
        "How do I prepare an IND application?"
    ]
};

// Initialize chat when DOM is loaded
function initializeChat(projectId) {
    const chatManager = new ChatManager(projectId);
    
    // Store globally for access from other functions
    window.chatManager = chatManager;
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        chatManager.cleanup();
    });
    
    return chatManager;
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChatManager, QuickResponses, AIQuestions, initializeChat };
}
