import React, { useState, useRef, useEffect } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { ArrowUp, Loader2, User, Building2 } from 'lucide-react';

export const ChatInput: React.FC = () => {
  const { sendMessage, isLoading, userRole, setUserRole } = useAssistant();
  const [input, setInput] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
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
    <div className="p-4 bg-[#070709] border-t border-[#181922] sticky bottom-0 z-20">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
        <div className="p-3 rounded-2xl bg-[#121319] border border-[#242634] focus-within:border-[#43475d] shadow-xl transition-all space-y-2">
          {/* Main Textarea */}
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            placeholder={
              userRole === 'industry'
                ? 'Ask about Indian Standards, QCOs, testing limits, or Scheme-I/II certification...'
                : 'Ask how to verify ISI marks, check domestic safety standards, or find IS numbers...'
            }
            className="w-full bg-transparent text-sm text-[#f1f2f8] placeholder-[#5a5c6e] resize-none px-1 py-0.5 focus:outline-none max-h-36 leading-relaxed font-sans"
          />

          {/* Bottom Toolbar: Mode Switcher + Send Button (Perplexity style) */}
          <div className="flex items-center justify-between pt-1">
            {/* Mode Pills inside input toolbar */}
            <div className="flex items-center gap-1 bg-[#181a23] p-0.5 rounded-lg border border-[#262936]">
              <button
                type="button"
                onClick={() => setUserRole('consumer')}
                className={`flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-all ${
                  userRole === 'consumer'
                    ? 'bg-[#262837] text-white shadow-sm'
                    : 'text-[#7d8092] hover:text-[#c5c8d8]'
                }`}
                title="Consumer Mode: Plain-language guidance & safety verification"
              >
                <User className="w-3 h-3" />
                <span>Consumer</span>
              </button>

              <button
                type="button"
                onClick={() => setUserRole('industry')}
                className={`flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-all ${
                  userRole === 'industry'
                    ? 'bg-[#262837] text-white shadow-sm'
                    : 'text-[#7d8092] hover:text-[#c5c8d8]'
                }`}
                title="Industry Mode: Technical standard clauses, mandatory QCOs, Scheme-I/II"
              >
                <Building2 className="w-3 h-3" />
                <span>Industry / Pro</span>
              </button>
            </div>

            {/* Right: Shortcut indicator & Submit button */}
            <div className="flex items-center gap-2">
              <span className="hidden sm:inline font-mono text-[10px] text-[#555768]">
                Enter ↵
              </span>

              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="w-7 h-7 rounded-full bg-[#e4e5eb] hover:bg-white text-[#070709] flex items-center justify-center transition-all disabled:opacity-20 disabled:cursor-not-allowed shadow-sm shrink-0"
                title="Send query"
              >
                {isLoading ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-[#070709]" />
                ) : (
                  <ArrowUp className="w-3.5 h-3.5 text-[#070709] stroke-[2.5]" />
                )}
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};
