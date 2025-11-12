'use client';

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';

interface Message {
    role: 'user' | 'agent';
    content: string;
    timestamp: Date;
}

interface ChatInterfaceProps {
    onFoodLogged?: () => void;
}

export function ChatInterface({ onFoodLogged }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'agent',
            content: "Hey! 👋 What did you eat? Just tell me naturally - like 'had a burger and fries' or 'ate chicken with rice'",
            timestamp: new Date(),
        },
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMessage: Message = {
            role: 'user',
            content: input,
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/api/chat', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: input,
                    conversation_history: messages.map((m) => ({
                        role: m.role,
                        content: m.content,
                    })),
                }),
            });

            const data = await response.json();

            const agentMessage: Message = {
                role: 'agent',
                content: data.agent_response || 'Sorry, I had trouble understanding that.',
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, agentMessage]);

            // If food was logged successfully, notify parent
            if (data.success && onFoodLogged) {
                onFoodLogged();
            }
        } catch (error) {
            const errorMessage: Message = {
                role: 'agent',
                content: "Oops! Something went wrong. Let's try that again.",
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <Card className="flex flex-col h-[500px]">
            <ScrollArea className="flex-1 p-4" ref={scrollRef}>
                <div className="space-y-4">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] rounded-lg px-4 py-2 ${message.role === 'user'
                                        ? 'bg-primary text-primary-foreground'
                                        : 'bg-muted'
                                    }`}
                            >
                                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                                <p className="text-xs opacity-70 mt-1">
                                    {message.timestamp.toLocaleTimeString('en-US', {
                                        hour: 'numeric',
                                        minute: '2-digit',
                                    })}
                                </p>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-muted rounded-lg px-4 py-2">
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </ScrollArea>

            <div className="p-4 border-t">
                <div className="flex gap-2">
                    <Input
                        placeholder="Type what you ate... (e.g., 'had a burger and fries')"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        disabled={loading}
                    />
                    <Button onClick={handleSend} disabled={loading || !input.trim()}>
                        Send
                    </Button>
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                    💡 Tip: Just type naturally! I understand misspellings and can guess foods.
                </p>
            </div>
        </Card>
    );
}
