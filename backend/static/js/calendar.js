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

        if (!data.calendar_data || data.calendar_data.length === 0) {
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

        data.calendar_data.forEach(day => {
            const summary = day.summary || {};
            const dateLabel = new Date(day.date).toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric'
            });

            const dayDiv = document.createElement('div');
            dayDiv.className = 'calendar-day-card';
            dayDiv.innerHTML = `
                <div class="calendar-day-header">
                    <span class="calendar-day-date">${dateLabel}</span>
                    <span class="calendar-day-calories">${Math.round(summary.total_calories || 0)} cal</span>
                </div>
                <div class="calendar-day-macros">
                    Protein: ${Math.round(summary.total_protein || 0)}g ·
                    Carbs: ${Math.round(summary.total_carbs || 0)}g ·
                    Fat: ${Math.round(summary.total_fat || 0)}g ·
                    Meals: ${summary.meal_count || 0}
                </div>
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
                        <div class="calendar-summary-label">Fast food / treats</div>
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
                suggestions.map(s => `<li>• ${s}</li>`).join('') +
                '</ul>';
        }

        insightContainer.innerHTML = `
            <p class="calendar-insight-text">${insightText}</p>
            ${suggestionsHtml}
        `;
    } catch (error) {
        console.error('Error loading weekly insight:', error);
        insightContainer.innerHTML = '<div class="error">Error loading weekly insight. Please try again.</div>';
    }
}
