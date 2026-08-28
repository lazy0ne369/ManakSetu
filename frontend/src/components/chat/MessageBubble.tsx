import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChatMessage, CitationItem } from '../../types/api';
import { useAssistant } from '../../context/AssistantContext';
import { submitFeedback } from '../../services/sourceService';
import { ClarificationPrompt } from './ClarificationPrompt';
import {
  ShieldCheck,
  Building,
  CheckCircle2,
  ListOrdered,
  FileText,
  ExternalLink,
  ThumbsUp,
  ThumbsDown,
  Sparkles,
  Award,
  AlertTriangle,
  Info,
} from 'lucide-react';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const { inspectStandard, inspectCitation, userRole } = useAssistant();
  const [feedbackRating, setFeedbackRating] = useState<number | null>(null);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState<boolean>(false);

  const isUser = message.sender === 'user';
  const payload = message.responsePayload;

  const handleFeedback = async (rating: number) => {
    if (feedbackSubmitted) return;
    setFeedbackRating(rating);
    try {
      await submitFeedback(message.id, rating);
      setFeedbackSubmitted(true);
    } catch (e) {
      console.warn('Feedback submit error:', e);
      setFeedbackSubmitted(true);
    }
  };

  if (isUser) {
    return (
      <div className="flex justify-end my-4 animate-fade-in">
        <div className="max-w-2xl bg-gradient-to-r from-bis-600 to-bis-700 text-white rounded-2xl rounded-tr-sm px-5 py-3.5 shadow-md shadow-bis-900/30">
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          <div className="flex items-center justify-end gap-1.5 mt-1.5 text-[11px] text-bis-200">
            <span>{message.timestamp}</span>
            {message.userRole && (
              <span className="uppercase text-[9px] font-bold px-1.5 py-0.5 rounded bg-black/20">
                {message.userRole}
              </span>
            )}
          </div>
        </div>
      </div>
    );
  }

  const confidence = payload?.confidence || 'medium';
  const confidenceConfig = {
    high: {
      color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
      label: 'High Factual Confidence (Verified Standard & QCO)',
    },
    medium: {
      color: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
      label: 'Medium Confidence (Standard Match)',
    },
    low: {
      color: 'text-slate-400 bg-slate-500/10 border-slate-500/30',
      label: 'Low Confidence (General / Clarification Needed)',
    },
  }[confidence];

  return (
    <div className="flex flex-col my-4 max-w-4xl animate-fade-in">
      <div className="glass-card rounded-2xl rounded-tl-sm p-5 border border-slate-800 shadow-xl space-y-4">
        {/* Header with AI Persona & Confidence indicator */}
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-bis-600/20 text-bis-400 border border-bis-500/30">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs font-bold text-white tracking-wide">
                ManakSetu AI Assistant
              </span>
              <span className="text-[11px] text-slate-400 ml-2">
                {message.timestamp}
              </span>
            </div>
          </div>

          {payload && (
            <div
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium border ${confidenceConfig.color}`}
              title={confidenceConfig.label}
            >
              <Sparkles className="w-3 h-3" />
              <span className="uppercase font-semibold tracking-wider text-[10px]">
                {confidence} Confidence
              </span>
            </div>
          )}
        </div>

        {/* Clarification prompt if triggered */}
        {payload?.needs_clarification && payload.clarification_question && (
          <ClarificationPrompt question={payload.clarification_question} />
        )}

        {/* Main Text Content (Markdown) */}
        <div className="prose prose-invert prose-sm max-w-none text-slate-200 leading-relaxed">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Applicable Standards Quick Chips */}
        {payload?.applicable_standards && payload.applicable_standards.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-slate-800/80">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-bis-300">
              <Award className="w-3.5 h-3.5" />
              <span>Applicable Indian Standards (Click to Inspect Clauses):</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {payload.applicable_standards.map((std, idx) => (
                <button
                  key={idx}
                  onClick={() => inspectStandard(std.is_number)}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-900/90 hover:bg-bis-950/80 border border-bis-500/30 hover:border-bis-400 text-left transition-all group"
                >
                  <span className="font-mono text-xs font-bold text-bis-300 group-hover:text-bis-200">
                    {std.is_number}
                  </span>
                  <span className="text-xs text-slate-300 max-w-[200px] truncate">
                    {std.title}
                  </span>
                  {std.mandatory && (
                    <span className="px-1.5 py-0.5 rounded text-[9px] uppercase font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                      Mandatory
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Key Technical Requirements / Checklist */}
        {payload?.key_requirements && payload.key_requirements.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-slate-800/80">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-300">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Key Standard & Testing Requirements:</span>
            </div>
            <ul className="grid grid-cols-1 gap-1.5 text-xs text-slate-300">
              {payload.key_requirements.map((req, idx) => (
                <li
                  key={idx}
                  className="flex items-start gap-2 p-2 rounded-lg bg-slate-900/50 border border-slate-800/60"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                  <span className="leading-relaxed">{req}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Compliance Roadmap Steps */}
        {payload?.compliance_steps && payload.compliance_steps.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-slate-800/80">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-sky-300">
              <ListOrdered className="w-3.5 h-3.5" />
              <span>
                {userRole === 'industry'
                  ? 'BIS Licensing & Compliance Steps (STI):'
                  : 'Consumer Safety & Verification Checklist:'}
              </span>
            </div>
            <div className="space-y-1.5 text-xs text-slate-300">
              {payload.compliance_steps.map((step, idx) => (
                <div
                  key={idx}
                  className="p-2 rounded-lg bg-slate-900/60 border border-slate-800/60 leading-relaxed font-sans"
                >
                  {step}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Verified Citations & Evidence Drawer Trigger */}
        {payload?.sources && payload.sources.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-slate-800/80">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-400">
              <FileText className="w-3.5 h-3.5" />
              <span>Authoritative Citations (Click to view clause text):</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {payload.sources.map((cit, idx) => (
                <button
                  key={idx}
                  onClick={() => inspectCitation(cit)}
                  className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/80 text-[11px] font-mono transition-colors"
                  title="Click to view verbatim standard clause excerpt"
                >
                  <span className="text-bis-400 font-semibold">{cit.standard}</span>
                  {cit.clause && <span className="text-slate-400">Cl. {cit.clause}</span>}
                  {cit.page && <span className="text-slate-500">p.{cit.page}</span>}
                  <ExternalLink className="w-3 h-3 text-slate-500 ml-0.5" />
                </button>
              ))}
            </div>
          </div>
        )}

        {/* User Feedback & Rating Bar */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <span>Was this answer accurate & helpful?</span>
            <button
              onClick={() => handleFeedback(5)}
              disabled={feedbackSubmitted}
              className={`p-1.5 rounded-lg hover:bg-slate-800 transition-colors ${
                feedbackRating === 5 ? 'text-emerald-400 bg-emerald-500/20' : 'text-slate-400'
              }`}
              title="Helpful"
            >
              <ThumbsUp className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => handleFeedback(1)}
              disabled={feedbackSubmitted}
              className={`p-1.5 rounded-lg hover:bg-slate-800 transition-colors ${
                feedbackRating === 1 ? 'text-rose-400 bg-rose-500/20' : 'text-slate-400'
              }`}
              title="Not helpful"
            >
              <ThumbsDown className="w-3.5 h-3.5" />
            </button>
            {feedbackSubmitted && (
              <span className="text-[11px] text-emerald-400 font-medium">
                Thank you for your feedback!
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
