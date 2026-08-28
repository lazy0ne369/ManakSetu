import React, { useRef, useEffect } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { MessageBubble } from './MessageBubble';
import { QuickPrompts } from './QuickPrompts';
import { ShieldCheck, Sparkles, Loader2, Bot } from 'lucide-react';

export const ChatArea: React.FC = () => {
  const { messages, isLoading, userRole } = useAssistant();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto px-4 lg:px-8 py-6 space-y-6 flex flex-col">
      {messages.length === 0 ? (
        <div className="my-auto max-w-2xl mx-auto text-center space-y-6 animate-fade-in py-8">
          <div className="inline-flex p-4 rounded-3xl bg-gradient-to-br from-bis-600/20 to-bis-900/40 border border-bis-500/30 text-bis-400 shadow-2xl shadow-bis-600/20">
            <ShieldCheck className="w-12 h-12 text-bis-400" />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
              Indian Standards & BIS Compliance Assistant
            </h2>
            <p className="text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
              Explore official Indian Standards (IS), mandatory Quality Control Orders (QCO),
              certification routes (Scheme-I ISI Mark, Scheme-II CRS), and technical test methods.
            </p>
          </div>

          <QuickPrompts />
        </div>
      ) : (
        <div className="max-w-4xl mx-auto w-full space-y-6">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {isLoading && (
            <div className="flex items-center gap-3 glass-card p-4 rounded-2xl border border-slate-800 animate-pulse-subtle max-w-md">
              <div className="p-2 rounded-xl bg-bis-600/20 text-bis-400 border border-bis-500/30">
                <Bot className="w-5 h-5 animate-spin" />
              </div>
              <div className="space-y-1">
                <p className="text-xs font-semibold text-bis-300">
                  Retrieving BIS Evidence & Evaluating Regulations...
                </p>
                <p className="text-[11px] text-slate-400">
                  Querying vector database, BM25 index, and QCO registries
                </p>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
};
