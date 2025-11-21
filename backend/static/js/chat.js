// Chat Interface JavaScript

let conversationHistory = [];

document.addEventListener('DOMContentLoaded', function() {
    loadSidebarData();
    setupChatInput();
    updateMessageTimes();
    setInterval(updateMessageTimes, 60000); // Update times every minute
    loadDailySuggestion();
});

function setupChatInput() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    
    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });
    
    // Send on Enter (but allow Shift+Enter for new line)
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message to UI
    addMessage('user', message);
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Get selected meal type from global variable (set by selectMealType function)
        const mealType = window.selectedMealType || 'breakfast';
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                meal_type: mealType,
                conversation_history: conversationHistory
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.error) {
            addMessage('agent', data.error || 'Sorry, something went wrong.');
            return;
        }
        
        // Add agent response
        addMessage('agent', data.agent_response, data.foods, data.total_nutrition);
        
        // Add AI insights if available
        if (data.recommendations && data.recommendations.length > 0) {
            addInsightsMessage(data.recommendations);
        }
        
        // Update conversation history
        conversationHistory.push({
            role: 'user',
            content: message
        });
        conversationHistory.push({
            role: 'agent',
            content: data.agent_response
        });
        
        // Refresh sidebar
        if (data.success) {
            setTimeout(loadSidebarData, 500);
        }
        
    } catch (error) {
        removeTypingIndicator();
        addMessage('agent', "Oops! Something went wrong. Let's try that again.");
        console.error('Chat error:', error);
    }
}

function addMessage(role, content, foods = null, nutrition = null) {
    const text = content != null ? content.toString().trim() : '';
    if (!text) {
        return;
    }

    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const timestamp = new Date().toISOString();
    
    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-bubble user-bubble">
                    <p>${escapeHtml(text)}</p>
                </div>
                <div class="message-time" data-time="${timestamp}">Just now</div>
            </div>
            <div class="message-avatar user-avatar">👤</div>
        `;
    } else {
        let foodsHtml = '';
        if (foods && foods.length > 0) {
            foodsHtml = '<div class="message-foods">';
            foodsHtml += '<p class="foods-title">Logged Foods:</p>';
            foods.forEach(food => {
                foodsHtml += `
                    <div class="food-item-inline">
                        <span class="food-name">• ${food.name} (${food.portion_text})</span>
                        <span class="food-calories">${Math.round(food.nutrition.calories)} cal</span>
                    </div>
                `;
            });
            foodsHtml += '</div>';
        }
        
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-bubble">
                    <p>${formatMessage(text)}</p>
                </div>
                ${foodsHtml}
                <div class="message-time" data-time="${timestamp}">Just now</div>
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addInsightsMessage(recommendations) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message insight-message';
    
    const timestamp = new Date().toISOString();
    
    let recsHtml = '';
    recommendations.forEach(rec => {
        recsHtml += `
            <div class="insight-item">
                <span class="insight-icon">${rec.icon}</span>
                <span class="insight-text">${escapeHtml(rec.message)}</span>
            </div>
        `;
    });
    
    messageDiv.innerHTML = `
        <div class="message-avatar insight-avatar">✨</div>
        <div class="message-content">
            <div class="message-bubble insight-bubble">
                <div class="insight-header">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                    </svg>
                    <span>AI Insights</span>
                </div>
                ${recsHtml}
            </div>
            <div class="message-time" data-time="${timestamp}">Just now</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message agent-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatMessage(text) {
    // Convert markdown-style formatting to HTML
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\n/g, '<br>');
    return text;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function updateMessageTimes() {
    const timeElements = document.querySelectorAll('.message-time[data-time]');
    timeElements.forEach(el => {
        const timestamp = el.getAttribute('data-time');
        if (timestamp === 'now') return;
        
        const time = new Date(timestamp);
        const now = new Date();
        const diff = Math.floor((now - time) / 1000); // seconds
        
        let timeText;
        if (diff < 60) {
            timeText = 'Just now';
        } else if (diff < 3600) {
            const mins = Math.floor(diff / 60);
            timeText = `${mins} min${mins > 1 ? 's' : ''} ago`;
        } else if (diff < 86400) {
            const hours = Math.floor(diff / 3600);
            timeText = `${hours} hour${hours > 1 ? 's' : ''} ago`;
        } else {
            timeText = time.toLocaleTimeString('en-US', {
                hour: 'numeric',
                minute: '2-digit'
            });
        }
        
        el.textContent = timeText;
    });
}

async function loadSidebarData() {
    try {
        const response = await fetch('/api/get-logs');
        const data = await response.json();
        
        // Update progress
        const progressDiv = document.getElementById('sidebarProgress');
        const dailyTotal = data.daily_total;
        const goals = data.goals;
        
        const caloriePercent = Math.min((dailyTotal.calories / goals.daily_calories) * 100, 100);
        const proteinPercent = Math.min((dailyTotal.protein / goals.daily_protein) * 100, 100);
        
        progressDiv.innerHTML = `
            <div class="progress-item-compact">
                <div class="progress-label-compact">
                    <span>Calories</span>
                    <span class="progress-value-compact">${Math.round(dailyTotal.calories)} / ${goals.daily_calories}</span>
                </div>
                <div class="progress-bar-compact">
                    <div class="progress-fill-compact" style="width: ${caloriePercent}%"></div>
                </div>
            </div>
            <div class="progress-item-compact">
                <div class="progress-label-compact">
                    <span>Protein</span>
                    <span class="progress-value-compact">${Math.round(dailyTotal.protein)}g / ${goals.daily_protein}g</span>
                </div>
                <div class="progress-bar-compact">
                    <div class="progress-fill-compact" style="width: ${proteinPercent}%"></div>
                </div>
            </div>
            <div class="progress-item-compact">
                <div class="progress-label-compact">
                    <span>Carbs</span>
                    <span class="progress-value-compact">${Math.round(dailyTotal.carbs)}g / ${goals.daily_carbs}g</span>
                </div>
                <div class="progress-bar-compact">
                    <div class="progress-fill-compact" style="width: ${Math.min((dailyTotal.carbs / goals.daily_carbs) * 100, 100)}%"></div>
                </div>
            </div>
            <div class="progress-item-compact">
                <div class="progress-label-compact">
                    <span>Fat</span>
                    <span class="progress-value-compact">${Math.round(dailyTotal.fat)}g / ${goals.daily_fat}g</span>
                </div>
                <div class="progress-bar-compact">
                    <div class="progress-fill-compact" style="width: ${Math.min((dailyTotal.fat / goals.daily_fat) * 100, 100)}%"></div>
                </div>
            </div>
        `;
        
        // Update meals
        const mealsDiv = document.getElementById('sidebarMeals');
        if (!data.logs || data.logs.length === 0) {
            mealsDiv.innerHTML = '<p class="empty-text">No meals yet</p>';
        } else {
            mealsDiv.innerHTML = '';
            data.logs.slice(0, 3).forEach(log => {
                const foodNames = log.foods.map(f => f.name).join(', ');
                mealsDiv.innerHTML += `
                    <div class="meal-compact">
                        <div class="meal-compact-header">
                            <span class="meal-compact-type">${log.meal_type}</span>
                            <span class="meal-compact-cal">${Math.round(log.total_nutrition.calories)} cal</span>
                        </div>
                        <p class="meal-compact-foods">${foodNames}</p>
                    </div>
                `;
            });
        }
        
    } catch (error) {
        console.error('Error loading sidebar data:', error);
    }
}

async function loadDailySuggestion() {
    try {
        const response = await fetch('/api/chat-daily-suggestion');
        if (!response.ok) {
            return;
        }
        const data = await response.json();
        
        if (data.error) {
            return;
        }
        
        if (data.agent_response && data.agent_response.trim()) {
            addMessage('agent', data.agent_response);
        }
        
        if (data.recommendations && data.recommendations.length > 0) {
            addInsightsMessage(data.recommendations);
        }
    } catch (error) {
        console.error('Error loading daily suggestion:', error);
    }
}
