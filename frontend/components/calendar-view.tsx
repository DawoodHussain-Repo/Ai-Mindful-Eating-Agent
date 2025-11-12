'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';

interface DayLog {
    date: string;
    meals: Array<{
        _id: string;
        timestamp: string;
        meal_type: string;
        foods: Array<{
            name: string;
            portion_text: string;
            nutrition: {
                calories: number;
                protein: number;
            };
        }>;
        total_nutrition: {
            calories: number;
            protein: number;
            carbs: number;
            fat: number;
        };
    }>;
    summary: {
        total_calories: number;
        total_protein: number;
        total_carbs: number;
        total_fat: number;
        meal_count: number;
    };
}

export function CalendarView() {
    const [calendarData, setCalendarData] = useState<DayLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedDate, setSelectedDate] = useState<string | null>(null);

    useEffect(() => {
        loadCalendarData();
    }, []);

    const loadCalendarData = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/calendar-logs?days=30', {
                credentials: 'include',
            });
            const data = await response.json();
            setCalendarData(data.calendar_data || []);
        } catch (error) {
            console.error('Failed to load calendar data:', error);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        if (date.toDateString() === today.toDateString()) {
            return 'Today';
        } else if (date.toDateString() === yesterday.toDateString()) {
            return 'Yesterday';
        } else {
            return date.toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric',
            });
        }
    };

    const getMealEmoji = (mealType: string) => {
        const emojis: Record<string, string> = {
            breakfast: '🌅',
            lunch: '☀️',
            dinner: '🌙',
            snack: '🍎',
        };
        return emojis[mealType] || '🍽️';
    };

    if (loading) {
        return (
            <Card>
                <CardContent className="p-8 text-center">
                    <p className="text-muted-foreground">Loading your meal history...</p>
                </CardContent>
            </Card>
        );
    }

    if (calendarData.length === 0) {
        return (
            <Card>
                <CardContent className="p-8 text-center">
                    <p className="text-muted-foreground">
                        No meal history yet. Start logging to see your calendar!
                    </p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Meal History</CardTitle>
                <CardDescription>Your eating patterns over the last 30 days</CardDescription>
            </CardHeader>
            <CardContent>
                <ScrollArea className="h-[600px] pr-4">
                    <div className="space-y-4">
                        {calendarData.map((day) => (
                            <div
                                key={day.date}
                                className="border rounded-lg p-4 hover:bg-muted/50 transition-colors cursor-pointer"
                                onClick={() =>
                                    setSelectedDate(selectedDate === day.date ? null : day.date)
                                }
                            >
                                {/* Date Header */}
                                <div className="flex justify-between items-start mb-3">
                                    <div>
                                        <h3 className="font-semibold text-lg">{formatDate(day.date)}</h3>
                                        <p className="text-sm text-muted-foreground">
                                            {day.summary.meal_count} meal{day.summary.meal_count !== 1 ? 's' : ''}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <p className="font-semibold">{day.summary.total_calories} cal</p>
                                        <p className="text-sm text-muted-foreground">
                                            {day.summary.total_protein}g protein
                                        </p>
                                    </div>
                                </div>

                                {/* Quick Summary */}
                                <div className="grid grid-cols-3 gap-2 mb-3">
                                    <div className="text-center bg-muted rounded p-2">
                                        <p className="text-xs text-muted-foreground">Carbs</p>
                                        <p className="font-semibold text-sm">{day.summary.total_carbs}g</p>
                                    </div>
                                    <div className="text-center bg-muted rounded p-2">
                                        <p className="text-xs text-muted-foreground">Fat</p>
                                        <p className="font-semibold text-sm">{day.summary.total_fat}g</p>
                                    </div>
                                    <div className="text-center bg-muted rounded p-2">
                                        <p className="text-xs text-muted-foreground">Fiber</p>
                                        <p className="font-semibold text-sm">
                                            {day.meals.reduce(
                                                (sum, meal) => sum + (meal.total_nutrition as any).fiber || 0,
                                                0
                                            )}
                                            g
                                        </p>
                                    </div>
                                </div>

                                {/* Expanded Meal Details */}
                                {selectedDate === day.date && (
                                    <>
                                        <Separator className="my-3" />
                                        <div className="space-y-3">
                                            {day.meals.map((meal) => (
                                                <div key={meal._id} className="bg-muted/50 rounded-lg p-3">
                                                    <div className="flex justify-between items-start mb-2">
                                                        <div className="flex items-center gap-2">
                                                            <span className="text-xl">{getMealEmoji(meal.meal_type)}</span>
                                                            <div>
                                                                <Badge variant="secondary" className="mb-1">
                                                                    {meal.meal_type}
                                                                </Badge>
                                                                <p className="text-xs text-muted-foreground">
                                                                    {new Date(meal.timestamp).toLocaleTimeString('en-US', {
                                                                        hour: 'numeric',
                                                                        minute: '2-digit',
                                                                    })}
                                                                </p>
                                                            </div>
                                                        </div>
                                                        <p className="font-semibold">
                                                            {Math.round(meal.total_nutrition.calories)} cal
                                                        </p>
                                                    </div>

                                                    <div className="space-y-1">
                                                        {meal.foods.map((food, idx) => (
                                                            <div key={idx} className="flex justify-between text-sm">
                                                                <span>
                                                                    {food.name} ({food.portion_text})
                                                                </span>
                                                                <span className="text-muted-foreground">
                                                                    {Math.round(food.nutrition.calories)} cal
                                                                </span>
                                                            </div>
                                                        ))}
                                                    </div>

                                                    <Separator className="my-2" />

                                                    <div className="grid grid-cols-4 gap-2 text-xs text-center">
                                                        <div>
                                                            <p className="text-muted-foreground">Protein</p>
                                                            <p className="font-semibold">
                                                                {Math.round(meal.total_nutrition.protein)}g
                                                            </p>
                                                        </div>
                                                        <div>
                                                            <p className="text-muted-foreground">Carbs</p>
                                                            <p className="font-semibold">
                                                                {Math.round(meal.total_nutrition.carbs)}g
                                                            </p>
                                                        </div>
                                                        <div>
                                                            <p className="text-muted-foreground">Fat</p>
                                                            <p className="font-semibold">
                                                                {Math.round(meal.total_nutrition.fat)}g
                                                            </p>
                                                        </div>
                                                        <div>
                                                            <p className="text-muted-foreground">Fiber</p>
                                                            <p className="font-semibold">
                                                                {Math.round((meal.total_nutrition as any).fiber || 0)}g
                                                            </p>
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </>
                                )}

                                {selectedDate !== day.date && (
                                    <p className="text-xs text-muted-foreground text-center mt-2">
                                        Click to see details
                                    </p>
                                )}
                            </div>
                        ))}
                    </div>
                </ScrollArea>
            </CardContent>
        </Card>
    );
}
