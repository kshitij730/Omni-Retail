'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Send, Cpu, Database, Play, Square, Bot, User } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

// Types
interface Message {
    role: 'user' | 'agent';
    content: string;
}

interface ChatResponse {
    response: string;
    thought_process: string[];
}

export default function OmniAgentUI() {
    // Shared send logic for text and voice
    const handleSendWithText = async (textToSubmit: string) => {
        if (!textToSubmit.trim()) return;

        setMessages(prev => [...prev, { role: 'user', content: textToSubmit }]);
        setInput('');
        setLoading(true);
        setThoughts([]);

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: textToSubmit, session_id: 'demo-user' })
            });

            const data: ChatResponse = await res.json();
            setThoughts(data.thought_process);
            setMessages(prev => [...prev, { role: 'agent', content: data.response }]);

            // Secure one-time speech logic
            const plainText = data.response.replace(/<[^>]*>/g, '').trim();
            if (plainText !== lastSpokenRef.current) {
                lastSpokenRef.current = plainText;
                speak(plainText);
            }

        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'agent', content: "Sorry, I lost connection to the Matrix." }]);
        } finally {
            setLoading(false);
            isProcessingVoiceRef.current = false;
        }
    };
    const [messages, setMessages] = useState<Message[]>([
        { role: 'agent', content: "Hello! I'm the Omni-Retail Super Agent. How can I assist you today?" }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [thoughts, setThoughts] = useState<string[]>([]);
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [permissionError, setPermissionError] = useState<string | null>(null);
    const recognitionRef = useRef<any>(null);
    const isProcessingVoiceRef = useRef<boolean>(false);
    const lastSpokenRef = useRef<string>("");

    const messagesEndRef = useRef<HTMLDivElement>(null);
    const synthesisRef = useRef<SpeechSynthesis | null>(null);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            synthesisRef.current = window.speechSynthesis;
        }
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = () => handleSendWithText(input);

    const speak = (text: string) => {
        if (!synthesisRef.current) return;

        if (synthesisRef.current.speaking) {
            synthesisRef.current.cancel();
            setIsSpeaking(false);
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        // Try to find a good voice
        const voices = synthesisRef.current.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Google') || v.name.includes('Female')) || voices[0];
        if (preferredVoice) utterance.voice = preferredVoice;

        utterance.onend = () => setIsSpeaking(false);

        setIsSpeaking(true);
        synthesisRef.current.speak(utterance);
    };

    const toggleListening = () => {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert("Browser does not support Speech API. Please use Chrome or Edge.");
            return;
        }

        if (isListening) {
            recognitionRef.current?.stop();
            setIsListening(false);
            return;
        }

        // @ts-ignore
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognitionRef.current = recognition;

        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            setIsListening(true);
        };

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setInput(transcript);

            if (event.results[0].isFinal && !isProcessingVoiceRef.current) {
                isProcessingVoiceRef.current = true;
                setIsListening(false);
                const finalTranscript = transcript;
                setTimeout(() => {
                    handleSendWithText(finalTranscript);
                }, 100);
            }
        };

        recognition.onerror = (event: any) => {
            console.error("Speech Recognition Error:", event.error);
            setIsListening(false);
            if (event.error === 'not-allowed') {
                setPermissionError("Microphone access is blocked. Please allow microphone access in your browser settings to use voice search.");
                // Auto-clear after 8 seconds
                setTimeout(() => setPermissionError(null), 8000);
            }
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        try {
            recognition.start();
        } catch (e) {
            console.error("Failed to start recognition:", e);
        }
    };

    return (
        <div className="flex h-full w-full bg-slate-900 overflow-hidden">
            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col relative bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black">
                <header className="p-4 border-b border-white/5 flex justify-between items-center backdrop-blur-md sticky top-0 z-10">
                    <h1 className="text-lg font-semibold text-slate-200">Omni-Retail Assistant</h1>
                    <div className="flex items-center gap-4">
                        {permissionError && (
                            <motion.div
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="text-[10px] bg-red-500/20 text-red-400 px-3 py-1 rounded-full border border-red-500/30 animate-pulse"
                            >
                                ⚠️ {permissionError}
                            </motion.div>
                        )}
                        <div className="text-xs text-emerald-400 flex items-center gap-1.5">
                            <span className="relative flex h-2 w-2">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                            </span>
                            System Online
                        </div>
                    </div>
                </header>

                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {messages.map((msg, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={cn(
                                "flex gap-4 max-w-3xl",
                                msg.role === 'user' ? "ml-auto flex-row-reverse" : ""
                            )}
                        >
                            <div className={cn(
                                "w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-lg",
                                msg.role === 'agent' ? "bg-indigo-600" : "bg-emerald-600"
                            )}>
                                {msg.role === 'agent' ? <Bot className="w-6 h-6 text-white" /> : <User className="w-6 h-6 text-white" />}
                            </div>

                            <div
                                className={cn(
                                    "p-4 rounded-2xl shadow-md text-sm leading-relaxed max-w-[80%] prose-chat",
                                    msg.role === 'agent'
                                        ? "bg-slate-800/80 text-slate-100 rounded-tl-none border border-slate-700"
                                        : "bg-emerald-600 text-white rounded-tr-none"
                                )}
                                dangerouslySetInnerHTML={{
                                    __html: msg.content
                                        .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>') // Handle **bold**
                                        .replace(/\n/g, '<br/>') // Handle newlines
                                }}
                            />
                            {msg.role === 'agent' && (
                                <div className="mt-2 flex self-end">
                                    <button
                                        onClick={() => speak(msg.content)}
                                        className="p-1 hover:bg-white/10 rounded-full transition-colors text-slate-400"
                                        title="Read Aloud"
                                    >
                                        {isSpeaking ? <Square className="w-3 h-3 fill-current" /> : <Play className="w-3 h-3 fill-current" />}
                                    </button>
                                </div>
                            )}
                        </motion.div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                <div className="p-6 border-t border-white/5 bg-slate-950/50 backdrop-blur-sm">
                    <div className="relative flex items-center gap-3 max-w-4xl mx-auto">
                        <button
                            onClick={toggleListening}
                            className={cn(
                                "p-3 rounded-full transition-all duration-300 shadow-lg border border-slate-700 hover:border-red-500/50",
                                isListening ? "bg-red-500/20 text-red-400 animate-pulse border-red-500" : "bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white"
                            )}
                        >
                            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                        </button>

                        <input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder={isListening ? "Listening..." : "Ask about orders, refunds, shipments..."}
                            className="flex-1 bg-slate-900 border border-slate-700 text-slate-100 rounded-full px-6 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all placeholder:text-slate-600"
                        />

                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || loading}
                            className="p-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:hover:bg-indigo-600 rounded-full text-white shadow-lg transition-all hover:scale-105 active:scale-95"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>
                    <div className="text-center mt-2 text-[10px] text-slate-600">
                        Powered by Groq • Llama 3.3 70B • Omni-Retail Core
                    </div>
                </div>
            </div>
        </div>
    );
}
