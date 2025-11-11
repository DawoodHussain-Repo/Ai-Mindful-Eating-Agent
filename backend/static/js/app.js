// Mindful Eating Agent - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('foodInput')) {
        loadDailyProgress();
        loadRecommendations();
        loadTodayLogs();
        
        // Allow Enter key to submit
        document.getElementById('foodInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                logFood();
            }
        });
    }
});

// Log food function
async function logFood() {
    const foodText = document.getElementById('foodInput').value;
    const mealType = document.getElementById('mealType').value;
    
    if (!foodText.trim()) {
        showError('Please enter a food description');
        return;
    }
    
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<div class="loading">Analyzing your food</div>';
    resultsDiv.classList.add('show');
    
    try {
        const response = await fetch('/api/log-food', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                food_text: foodText,
                meal_type: mealType
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<div class="error">${data.error}</div>`;
            return;
        }
        
        displayResults(data);
        document.getElementById('foodInput').value = '';
        
        // Refresh dashboard
        setTimeout(() => {
            loadDailyProgress();
            loadRecommendations();
            loadTodayLogs();
        }, 500);
        
    } catch (error) {
        resultsDiv.innerHTML = '<div class="error">Error logging food. Please try again.</div>';
        console.error('Error:', error);
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    
    let html = '<h4>✓ Parsed Foods:</h4>';
    
    data.foods.forEach(food => {
        html += `
            <div class="food-item">
                <strong>${food.name}</strong> <span style="color: #999;">(${food.portion_text})</span>
                <div class="food-details">
                    ${Math.round(food.nutrition.calories)} cal | 
                    ${Math.round(food.nutrition.protein)}g protein | 
                    ${Math.round(food.nutrition.carbs)}g carbs | 
                    ${Math.round(food.nutrition.fat)}g fat
                </div>
            </div>
        `;
    });
    
    html += '<h4 style="margin-top: 25px;">📊 Total Nutrition:</h4>';
    html += `
        <div class="nutrition-grid">
            <div class="nutrition-item">
                <div class="value">${Math.round(data.total_nutrition.calories)}</div>
                <div class="label">Calories</div>
            </div>
            <div class="nutrition-item">
                <div class="value">${Math.round(data.total_nutrition.protein)}g</div>
                <div class="label">Protein</div>
            </div>
            <div class="nutrition-item">
                <div class="value">${Math.round(data.total_nutrition.carbs)}g</div>
                <div class="label">Carbs</div>
            </div>
            <div class="nutrition-item">
                <div class="value">${Math.round(data.total_nutrition.fat)}g</div>
                <div class="label">Fat</div>
            </div>
            <div class="nutrition-item">
                <div class="value">${Math.round(data.total_nutrition.fiber)}g</div>
                <div class="label">Fiber</div>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

async function loadDailyProgress() {
    try {
        const response = await fetch('/api/get-logs');
        const data = await response.json();
        
        const dailyTotal = data.daily_total;
        const goals = data.goals;
        
        const caloriePercent = Math.min((dailyTotal.calories / goals.daily_calories) * 100, 100);
        const proteinPercent = Math.min((dailyTotal.protein / goals.daily_protein) * 100, 100);
        
        // Calorie progress
        document.getElementById('calorieProgress').innerHTML = `
            <div class="progress-header">
                <span>Calories</span>
                <span>${Math.round(dailyTotal.calories)} / ${goals.daily_calories}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${caloriePercent}%">
                    ${Math.round(caloriePercent)}%
                </div>
            </div>
        `;
        
        // Protein progress
        document.getElementById('proteinProgress').innerHTML = `
            <div class="progress-header">
                <span>Protein</span>
                <span>${Math.round(dailyTotal.protein)}g / ${goals.daily_protein}g</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${proteinPercent}%">
                    ${Math.round(proteinPercent)}%
                </div>
            </div>
        `;
        
        // Macro breakdown
        document.getElementById('macroBreakdown').innerHTML = `
            <div class="macro-breakdown">
                <div class="macro-item">
                    <div class="macro-value">${Math.round(dailyTotal.carbs)}g</div>
                    <div class="macro-label">Carbs</div>
                </div>
                <div class="macro-item">
                    <div class="macro-value">${Math.round(dailyTotal.fat)}g</div>
                    <div class="macro-label">Fat</div>
                </div>
                <div class="macro-item">
                    <div class="macro-value">${Math.round(dailyTotal.fiber)}g</div>
                    <div class="macro-label">Fiber</div>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading progress:', error);
    }
}

async function loadRecommendations() {
    try {
        const response = await fetch('/api/get-recommendations');
        const data = await response.json();
        
        const container = document.getElementById('recommendations');
        
        if (!data.recommendations || data.recommendations.length === 0) {
            container.innerHTML = '<div class="empty-state">No recommendations yet. Keep logging meals!</div>';
            return;
        }
        
        container.innerHTML = '';
        
        data.recommendations.forEach(rec => {
            const recClass = rec.type === 'positive' ? 'positive' : 
                           rec.type === 'calories' ? 'warning' : 
                           rec.type === 'protein' ? 'protein' : '';
            
            container.innerHTML += `
                <div class="recommendation ${recClass}">
                    <span class="icon">${rec.icon}</span>
                    <div>${rec.message}</div>
                </div>
            `;
        });
        
    } catch (error) {
        console.error('Error loading recommendations:', error);
    }
}

async function loadTodayLogs() {
    try {
        const response = await fetch('/api/get-logs');
        const data = await response.json();
        
        const container = document.getElementById('todayLogs');
        
        if (!data.logs || data.logs.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🍽️</div>
                    <p>No meals logged today yet.</p>
                    <p style="font-size: 13px; margin-top: 5px;">Start by logging your first meal above!</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = '';
        
        // Reverse to show most recent first
        const reversedLogs = [...data.logs].reverse();
        
        reversedLogs.forEach(log => {
            const time = new Date(log.timestamp).toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit'
            });
            
            const foodNames = log.foods.map(f => f.name).join(', ');
            
            container.innerHTML += `
                <div class="meal-log">
                    <div class="meal-header">
                        <span class="meal-type">${log.meal_type}</span>
                        <span class="meal-time">${time}</span>
                    </div>
                    <div class="meal-foods">${foodNames}</div>
                    <div class="meal-nutrition">
                        ${Math.round(log.total_nutrition.calories)} cal | 
                        ${Math.round(log.total_nutrition.protein)}g protein | 
                        ${Math.round(log.total_nutrition.carbs)}g carbs | 
                        ${Math.round(log.total_nutrition.fat)}g fat
                    </div>
                </div>
            `;
        });
        
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

function showError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<div class="error">${message}</div>`;
    resultsDiv.classList.add('show');
    
    setTimeout(() => {
        resultsDiv.classList.remove('show');
    }, 3000);
}

// Auto-refresh every 30 seconds
setInterval(() => {
    if (document.getElementById('foodInput')) {
        loadRecommendations();
    }
}, 30000);
