import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Logo/Title */}
          <div className="space-y-4">
            <h1 className="text-6xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
              Mindful Eating
            </h1>
            <p className="text-2xl text-muted-foreground">
              Your AI-Powered Nutrition Coach
            </p>
          </div>

          {/* Value Proposition */}
          <div className="max-w-2xl mx-auto space-y-4">
            <p className="text-lg text-gray-700">
              Transform your eating habits with intelligent food tracking, personalized recommendations,
              and behavioral insights powered by advanced AI.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
            <Link href="/onboarding">
              <Button size="lg" className="text-lg px-8 py-6">
                Get Started Free
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="text-lg px-8 py-6">
                Sign In
              </Button>
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 pt-16">
            <div className="bg-white rounded-lg p-6 shadow-sm space-y-3">
              <div className="text-4xl">📝</div>
              <h3 className="text-xl font-semibold">Simple Logging</h3>
              <p className="text-muted-foreground">
                Just describe what you ate. Our AI handles the rest.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm space-y-3">
              <div className="text-4xl">🧠</div>
              <h3 className="text-xl font-semibold">Smart Insights</h3>
              <p className="text-muted-foreground">
                Learn your patterns and get personalized recommendations.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm space-y-3">
              <div className="text-4xl">🎯</div>
              <h3 className="text-xl font-semibold">Goal Tracking</h3>
              <p className="text-muted-foreground">
                Set and achieve your nutrition goals with AI guidance.
              </p>
            </div>
          </div>

          {/* How It Works */}
          <div className="pt-16 space-y-8">
            <h2 className="text-3xl font-bold">How It Works</h2>
            <div className="grid md:grid-cols-4 gap-6 text-left">
              <div className="space-y-2">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold text-xl">
                  1
                </div>
                <h4 className="font-semibold">Set Your Goals</h4>
                <p className="text-sm text-muted-foreground">
                  Tell us your daily calorie, protein, and macro targets
                </p>
              </div>

              <div className="space-y-2">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-xl">
                  2
                </div>
                <h4 className="font-semibold">Log Your Meals</h4>
                <p className="text-sm text-muted-foreground">
                  Describe what you ate in plain English
                </p>
              </div>

              <div className="space-y-2">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-bold text-xl">
                  3
                </div>
                <h4 className="font-semibold">Get Insights</h4>
                <p className="text-sm text-muted-foreground">
                  AI analyzes your patterns and nutrition
                </p>
              </div>

              <div className="space-y-2">
                <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-bold text-xl">
                  4
                </div>
                <h4 className="font-semibold">Improve Daily</h4>
                <p className="text-sm text-muted-foreground">
                  Receive personalized recommendations
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
