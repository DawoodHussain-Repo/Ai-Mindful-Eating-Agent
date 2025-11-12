'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { ChatInterface } from '@/components/chat-interface';
import { CalendarView } from '@/components/calendar-view';
import { api, FoodLog, Recommendation } from '@/lib/api';

export default function DashboardPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [foodText, setFoodText] = useState('');
    const [mealType, setMealType] = useState('lunch');
    const [logs, setLogs] = useState<FoodLog[]>([]);
    const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
    const [dailyTotal, setDailyTotal] = useState({
        calories: 0,
        protein: 0,
        carbs: 0,
        fat: 0,
        fiber: 0,
    });
    const [goals, setGoals] = useState({
        daily_calories: 2000,
        daily_protein: 120,
        daily_carbs: 250,
        daily_fat: 65,
    });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [logsData, recsData] = await Promise.all([
                api.getLogs(),
                api.getRecommendations(),
            ]);

            setLogs(logsData.logs || []);
            setDailyTotal(logsData.daily_total || dailyTotal);
            setGoals(logsData.goals || goals);
            setRecommendations(recsData.recommendations || []);
        } catch (error) {
            console.error('Failed to load data:', error);
            router.push('/login');
        }
    };

    const handleLogFood = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!foodText.trim()) return;

        setLoading(true);
        try {
            await api.logFood(foodText, mealType);
            setFoodText('');
            await loadData();
        } catch (error: any) {
            alert(error.message || 'Failed to log food');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        await api.logout();
        router.push('/login');
    };

    const calorieProgress = (dailyTotal.calories / goals.daily_calories) * 100;
    const proteinProgress = (dailyTotal.protein / goals.daily_protein) * 100;
    const carbsProgress = (dailyTotal.carbs / goals.daily_carbs) * 100;
    const fatProgress = (dailyTotal.fat / goals.daily_fat) * 100;

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b">
                <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                        Mindful Eating
                    </h1>
                    <Button variant="outline" onClick={handleLogout}>
                        Logout
                    </Button>
                </div>
            </header>

            <div className="container mx-auto px-4 py-8 max-w-7xl">
                <Tabs defaultValue="chat" className="space-y-6">
                    <TabsList className="grid w-full max-w-md grid-cols-3">
                        <TabsTrigger value="chat">💬 Chat</TabsTrigger>
                        <TabsTrigger value="manual">📝 Manual</TabsTrigger>
                        <TabsTrigger value="history">📅 History</TabsTrigger>
                    </TabsList>

                    {/* Chat Tab */}
                    <TabsContent value="chat">
                        <div className="grid lg:grid-cols-3 gap-6">
                            <div className="lg:col-span-2">
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Chat with AI</CardTitle>
                                        <CardDescription>
                                            Just tell me what you ate naturally - I understand misspellings!
                                        </CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <ChatInterface onFoodLogged={loadData} />
                                    </CardContent>
                                </Card>
                            </div>

                            {/* Progress Sidebar */}
                            <div className="space-y-6">
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Today's Progress</CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span className="font-medium">Calories</span>
                                                <span>{Math.round(dailyTotal.calories)} / {goals.daily_calories}</span>
                                            </div>
                                            <Progress value={Math.min(calorieProgress, 100)} />
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span className="font-medium">Protein</span>
                                                <span>{Math.round(dailyTotal.protein)}g / {goals.daily_protein}g</span>
                                            </div>
                                            <Progress value={Math.min(proteinProgress, 100)} />
                                        </div>
                                    </CardContent>
                                </Card>

                                <Card>
                                    <CardHeader>
                                        <CardTitle>AI Insights</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        {recommendations.length === 0 ? (
                                            <p className="text-sm text-muted-foreground text-center py-4">
                                                Keep chatting to get insights!
                                            </p>
                                        ) : (
                                            <div className="space-y-2">
                                                {recommendations.map((rec, idx) => (
                                                    <div key={idx} className="bg-blue-50 border border-blue-200 rounded p-2">
                                                        <p className="text-sm">{rec.icon} {rec.message}</p>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </CardContent>
                                </Card>
                            </div>
                        </div>
                    </TabsContent>

                    {/* Manual Tab */}
                    <TabsContent value="manual">
                        <div className="grid lg:grid-cols-3 gap-6">
                            <div className="lg:col-span-2 space-y-6">
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Log Your Meal</CardTitle>
                                        <CardDescription>Describe what you ate</CardDescription>
                                    </CardHeader>
                                    <CardContent>
                                        <form onSubmit={handleLogFood} className="space-y-4">
                                            <div className="space-y-2">
                                                <Label>Meal Type</Label>
                                                <Select value={mealType} onValueChange={setMealType}>
                                                    <SelectTrigger>
                                                        <SelectValue />
                                                    </SelectTrigger>
                                                    <SelectContent>
                                                        <SelectItem value="breakfast">🌅 Breakfast</SelectItem>
                                                        <SelectItem value="lunch">☀️ Lunch</SelectItem>
                                                        <SelectItem value="dinner">🌙 Dinner</SelectItem>
                                                        <SelectItem value="snack">🍎 Snack</SelectItem>
                                                    </SelectContent>
                                                </Select>
                                            </div>
                                            <div className="space-y-2">
                                                <Label>What did you eat?</Label>
                                                <Textarea
                                                    placeholder="e.g., grilled chicken 6oz, brown rice 1 cup"
                                                    value={foodText}
                                                    onChange={(e) => setFoodText(e.target.value)}
                                                    rows={3}
                                                />
                                            </div>
                                            <Button type="submit" className="w-full" disabled={loading}>
                                                {loading ? 'Logging...' : 'Log Meal'}
                                            </Button>
                                        </form>
                                    </CardContent>
                                </Card>

                                <Card>
                                    <CardHeader>
                                        <CardTitle>Today's Meals</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        {logs.length === 0 ? (
                                            <p className="text-center text-muted-foreground py-8">
                                                No meals logged yet
                                            </p>
                                        ) : (
                                            <div className="space-y-4">
                                                {logs.map((log) => (
                                                    <div key={log._id} className="border rounded p-4">
                                                        <div className="flex justify-between mb-2">
                                                            <Badge>{log.meal_type}</Badge>
                                                            <span className="font-semibold">
                                                                {Math.round(log.total_nutrition.calories)} cal
                                                            </span>
                                                        </div>
                                                        {log.foods.map((food, idx) => (
                                                            <div key={idx} className="text-sm flex justify-between">
                                                                <span>{food.name} ({food.portion_text})</span>
                                                                <span>{Math.round(food.nutrition.calories)} cal</span>
                                                            </div>
                                                        ))}
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </CardContent>
                                </Card>
                            </div>

                            <div className="space-y-6">
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Daily Progress</CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span>Calories</span>
                                                <span>{Math.round(dailyTotal.calories)} / {goals.daily_calories}</span>
                                            </div>
                                            <Progress value={Math.min(calorieProgress, 100)} />
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span>Protein</span>
                                                <span>{Math.round(dailyTotal.protein)}g / {goals.daily_protein}g</span>
                                            </div>
                                            <Progress value={Math.min(proteinProgress, 100)} />
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span>Carbs</span>
                                                <span>{Math.round(dailyTotal.carbs)}g / {goals.daily_carbs}g</span>
                                            </div>
                                            <Progress value={Math.min(carbsProgress, 100)} />
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span>Fat</span>
                                                <span>{Math.round(dailyTotal.fat)}g / {goals.daily_fat}g</span>
                                            </div>
                                            <Progress value={Math.min(fatProgress, 100)} />
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>
                        </div>
                    </TabsContent>

                    {/* History Tab */}
                    <TabsContent value="history">
                        <CalendarView />
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}
