import React, { useRef, useEffect } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { MessageBubble } from './MessageBubble';
import { QuickPrompts } from './QuickPrompts';
import { ShieldCheck, Loader2 } from 'lucide-react';

export const ChatArea: React.FC = () => {
  const { messages, isLoading } = useAssistant();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto px-4 lg:px-8 py-6 flex flex-col bg-[#0b0c10]">
      {messages.length === 0 ? (
        <div className="my-auto max-w-3xl mx-auto w-full text-center space-y-6 animate-fade-in py-6">
          <div className="inline-flex p-3 rounded-2xl bg-[#15161e] border border-[#262837] text-[#d4d7e6] shadow-sm">
            <ShieldCheck className="w-8 h-8 text-[#b2b6cb]" />
          </div>

          <div className="space-y-1.5 max-w-xl mx-auto">
            <h2 className="text-xl lg:text-2xl font-bold text-[#f1f2f8] tracking-tight font-sans">
              What Indian Standard or BIS service can I help you verify?
            </h2>
            <p className="text-xs text-[#8c8f9f] leading-relaxed">
              Authoritative intelligence on Indian Standards (IS), mandatory Quality Control Orders (QCO),
              and certification schemes (Scheme-I ISI Mark & Scheme-II CRS).
            </p>
          </div>

          <QuickPrompts />
        </div>
      ) : (
        <div className="max-w-4xl mx-auto w-full space-y-5">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {isLoading && (
            <div className="flex items-center gap-3 p-4 rounded-xl bg-[#14151c] border border-[#232533] max-w-md animate-fade-in">
              <Loader2 className="w-4 h-4 text-[#8c8f9f] animate-spin shrink-0" />
              <div className="space-y-0.5 text-left">
                <p className="text-xs font-medium text-[#e4e5eb]">
                  Retrieving BIS Evidence & Regulatory Clauses...
                </p>
                <p className="text-[11px] text-[#7d8092] font-mono">
                  Vector search + BM25Okapi + QCO registries
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
