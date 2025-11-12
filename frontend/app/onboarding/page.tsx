'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { api } from '@/lib/api';

export default function OnboardingPage() {
    const router = useRouter();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Form data
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        daily_calories: 2000,
        daily_protein: 120,
        daily_carbs: 250,
        daily_fat: 65,
    });

    const totalSteps = 3;
    const progress = (step / totalSteps) * 100;

    const handleNext = () => {
        if (step < totalSteps) {
            setStep(step + 1);
            setError('');
        }
    };

    const handleBack = () => {
        if (step > 1) {
            setStep(step - 1);
            setError('');
        }
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError('');

        try {
            const goals = {
                daily_calories: formData.daily_calories,
                daily_protein: formData.daily_protein,
                daily_carbs: formData.daily_carbs,
                daily_fat: formData.daily_fat,
            };

            await api.register(formData.email, formData.password, formData.name, goals);
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.message || 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
            <Card className="w-full max-w-2xl">
                <CardHeader className="space-y-4">
                    <div className="space-y-2">
                        <CardTitle className="text-3xl font-bold text-center">
                            Welcome to Mindful Eating
                        </CardTitle>
                        <CardDescription className="text-center text-base">
                            Let's personalize your nutrition journey
                        </CardDescription>
                    </div>
                    <Progress value={progress} className="h-2" />
                    <p className="text-sm text-center text-muted-foreground">
                        Step {step} of {totalSteps}
                    </p>
                </CardHeader>

                <CardContent className="space-y-6">
                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                            {error}
                        </div>
                    )}

                    {/* Step 1: Basic Info */}
                    {step === 1 && (
                        <div className="space-y-6 animate-in fade-in duration-500">
                            <div className="space-y-2">
                                <h3 className="text-xl font-semibold">Tell us about yourself</h3>
                                <p className="text-sm text-muted-foreground">
                                    We'll use this to create your account
                                </p>
                            </div>

                            <div className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="name">Full Name</Label>
                                    <Input
                                        id="name"
                                        placeholder="John Doe"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    />
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="email">Email</Label>
                                    <Input
                                        id="email"
                                        type="email"
                                        placeholder="john@example.com"
                                        value={formData.email}
                                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    />
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="password">Password</Label>
                                    <Input
                                        id="password"
                                        type="password"
                                        placeholder="••••••••"
                                        value={formData.password}
                                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Step 2: Calorie & Protein Goals */}
                    {step === 2 && (
                        <div className="space-y-6 animate-in fade-in duration-500">
                            <div className="space-y-2">
                                <h3 className="text-xl font-semibold">Set your daily goals</h3>
                                <p className="text-sm text-muted-foreground">
                                    These help us provide personalized recommendations
                                </p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="calories">Daily Calories Goal</Label>
                                    <Input
                                        id="calories"
                                        type="number"
                                        value={formData.daily_calories}
                                        onChange={(e) =>
                                            setFormData({ ...formData, daily_calories: parseInt(e.target.value) })
                                        }
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        Recommended: 1800-2500 for most adults
                                    </p>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="protein">Daily Protein Goal (g)</Label>
                                    <Input
                                        id="protein"
                                        type="number"
                                        value={formData.daily_protein}
                                        onChange={(e) =>
                                            setFormData({ ...formData, daily_protein: parseInt(e.target.value) })
                                        }
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        Recommended: 0.8-1.2g per kg body weight
                                    </p>
                                </div>
                            </div>

                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                <p className="text-sm text-blue-900">
                                    💡 <strong>Tip:</strong> You can always adjust these goals later in settings
                                </p>
                            </div>
                        </div>
                    )}

                    {/* Step 3: Macros Goals */}
                    {step === 3 && (
                        <div className="space-y-6 animate-in fade-in duration-500">
                            <div className="space-y-2">
                                <h3 className="text-xl font-semibold">Fine-tune your macros</h3>
                                <p className="text-sm text-muted-foreground">
                                    Balance your carbs and fats for optimal nutrition
                                </p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="carbs">Daily Carbs Goal (g)</Label>
                                    <Input
                                        id="carbs"
                                        type="number"
                                        value={formData.daily_carbs}
                                        onChange={(e) =>
                                            setFormData({ ...formData, daily_carbs: parseInt(e.target.value) })
                                        }
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        Recommended: 45-65% of total calories
                                    </p>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="fat">Daily Fat Goal (g)</Label>
                                    <Input
                                        id="fat"
                                        type="number"
                                        value={formData.daily_fat}
                                        onChange={(e) =>
                                            setFormData({ ...formData, daily_fat: parseInt(e.target.value) })
                                        }
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        Recommended: 20-35% of total calories
                                    </p>
                                </div>
                            </div>

                            <div className="bg-green-50 border border-green-200 rounded-lg p-4 space-y-2">
                                <p className="text-sm font-medium text-green-900">Your Daily Goals Summary:</p>
                                <div className="grid grid-cols-2 gap-2 text-sm text-green-800">
                                    <div>🔥 Calories: {formData.daily_calories}</div>
                                    <div>💪 Protein: {formData.daily_protein}g</div>
                                    <div>🍞 Carbs: {formData.daily_carbs}g</div>
                                    <div>🥑 Fat: {formData.daily_fat}g</div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Navigation Buttons */}
                    <div className="flex justify-between pt-4">
                        <Button
                            variant="outline"
                            onClick={handleBack}
                            disabled={step === 1 || loading}
                        >
                            Back
                        </Button>

                        {step < totalSteps ? (
                            <Button
                                onClick={handleNext}
                                disabled={
                                    loading ||
                                    (step === 1 && (!formData.name || !formData.email || !formData.password))
                                }
                            >
                                Continue
                            </Button>
                        ) : (
                            <Button onClick={handleSubmit} disabled={loading}>
                                {loading ? 'Creating Account...' : 'Complete Setup'}
                            </Button>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
