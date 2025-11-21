document.addEventListener('DOMContentLoaded', function() {
    loadCalendarData();
    loadWeeklyInsight();
});

async function loadCalendarData() {
    const container = document.getElementById('calendarDays');
    if (!container) return;

    try {
        const response = await fetch('/api/calendar-logs?days=30');
        const data = await response.json();

        if (!data.calendar || data.calendar.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📆</div>
                    <p>No meals logged yet for this period.</p>
                    <p style="font-size: 13px; margin-top: 5px;">Log meals in the chat and they'll appear here.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = '';

        data.calendar.forEach(day => {
            const summary = day.data || {}; // API returns { date: ..., data: { ... } }
            
            // Calculate totals from the 'data' object which contains 'total_calories', etc.
            // Wait, let's check app.py again.
            // app.py: logs_by_date[date]['total_calories'] ...
            // calendar_data = [ { 'date': date, 'data': data } ]
            // So day.data has the stats.
            
            const dateLabel = new Date(day.date).toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric'
            });

            const dayDiv = document.createElement('div');
            dayDiv.className = 'calendar-day-card';
            
            // Create meal list HTML
            let mealsHtml = '';
            if (summary.meals && summary.meals.length > 0) {
                mealsHtml = '<div class="day-meals-list">';
                summary.meals.forEach(meal => {
                    const time = new Date(meal.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                    mealsHtml += `
                        <div class="mini-meal-item">
                            <span class="mini-meal-time">${time}</span>
                            <span class="mini-meal-name">${meal.meal_type}</span>
                            <span class="mini-meal-cal">${Math.round(meal.total_nutrition.calories)}</span>
                        </div>
                    `;
                });
                mealsHtml += '</div>';
            }

            dayDiv.innerHTML = `
                <div class="calendar-day-header">
                    <span class="calendar-day-date">${dateLabel}</span>
                    <span class="calendar-day-calories">${Math.round(summary.total_calories || 0)} cal</span>
                </div>
                <div class="calendar-day-macros">
                    <div class="macro-pill protein">P: ${Math.round(summary.total_protein || 0)}g</div>
                    <div class="macro-pill carbs">C: ${Math.round(summary.total_carbs || 0)}g</div>
                    <div class="macro-pill fat">F: ${Math.round(summary.total_fat || 0)}g</div>
                </div>
                ${mealsHtml}
            `;

            container.appendChild(dayDiv);
        });
    } catch (error) {
        console.error('Error loading calendar data:', error);
        container.innerHTML = '<div class="error">Error loading calendar. Please try again.</div>';
    }
}

async function loadWeeklyInsight() {
    const summaryContainer = document.getElementById('weeklySummary');
    const insightContainer = document.getElementById('weeklyInsight');
    if (!summaryContainer || !insightContainer) return;

    try {
        const response = await fetch('/api/weekly-insight');
        const data = await response.json();

        if (!data.summary) {
            summaryContainer.innerHTML = '<p class="empty-text">Not enough data yet for a weekly summary.</p>';
        } else {
            const s = data.summary;
            summaryContainer.innerHTML = `
                <div class="calendar-summary-grid">
                    <div class="calendar-summary-item">
                        <div class="calendar-summary-label">Days tracked</div>
                        <div class="calendar-summary-value">${s.days_considered}</div>
                    </div>
                    <div class="calendar-summary-item">
                        <div class="calendar-summary-label">Avg calories</div>
                        <div class="calendar-summary-value">${s.avg_calories}</div>
                    </div>
                    <div class="calendar-summary-item">
                        <div class="calendar-summary-label">Avg protein</div>
                        <div class="calendar-summary-value">${s.avg_protein}g</div>
                    </div>
                    <div class="calendar-summary-item">
                        <div class="calendar-summary-label">Fast food</div>
                        <div class="calendar-summary-value">${s.fast_food_meals}</div>
                    </div>
                </div>
            `;
        }

        const insightText = data.insight || 'Log a few days of meals and I will summarize your week.';
        const suggestions = data.suggestions || [];

        let suggestionsHtml = '';
        if (suggestions.length > 0) {
            suggestionsHtml = '<ul class="calendar-insight-list">' +
                suggestions.map(s => `<li>${s}</li>`).join('') +
                '</ul>';
        }

        insightContainer.innerHTML = `
            <div class="insight-bubble-content">
                <p class="calendar-insight-text">${insightText}</p>
                ${suggestionsHtml}
            </div>
        `;
    } catch (error) {
        console.error('Error loading weekly insight:', error);
        insightContainer.innerHTML = '<div class="error">Error loading weekly insight. Please try again.</div>';
    }
}
