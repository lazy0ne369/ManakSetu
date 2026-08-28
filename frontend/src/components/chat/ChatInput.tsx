import React, { useState, useRef, useEffect } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { Send, Loader2, Sparkles, CornerDownLeft } from 'lucide-react';

export const ChatInput: React.FC = () => {
  const { sendMessage, isLoading, userRole } = useAssistant();
  const [input, setInput] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on input content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [input]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="p-4 glass-panel border-t border-slate-800/80 sticky bottom-0 z-20">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
        <div className="flex items-end gap-2 p-2 rounded-2xl bg-slate-900/90 border border-slate-700/80 focus-within:border-bis-500 focus-within:ring-2 focus-within:ring-bis-500/20 shadow-2xl transition-all">
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            placeholder={
              userRole === 'industry'
                ? 'Ask about Indian Standards, QCOs, testing parameters, or Scheme-I/II requirements... (Press Enter)'
                : 'Ask how to check ISI marks, verify safe domestic appliances, or find standard numbers... (Press Enter)'
            }
            className="w-full bg-transparent text-sm text-slate-100 placeholder-slate-500 resize-none px-3 py-2 focus:outline-none max-h-40 leading-relaxed font-sans"
          />

          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="p-2.5 rounded-xl bg-gradient-to-r from-bis-600 to-bis-700 hover:from-bis-500 hover:to-bis-600 text-white transition-all disabled:opacity-30 disabled:cursor-not-allowed shadow-md shadow-bis-600/30 shrink-0"
            title="Send query"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>

        <div className="flex items-center justify-between text-[11px] text-slate-500 mt-2 px-2">
          <span>
            {userRole === 'industry' ? '⚡ Industry & Compliance Mode' : '🛡️ Consumer & Safety Mode'}
          </span>
          <span className="flex items-center gap-1">
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] text-slate-400 font-mono">
              Enter
            </kbd>{' '}
            to send,{' '}
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] text-slate-400 font-mono">
              Shift+Enter
            </kbd>{' '}
            for new line
          </span>
        </div>
      </form>
    </div>
  );
};
