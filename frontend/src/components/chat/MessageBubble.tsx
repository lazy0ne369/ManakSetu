import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChatMessage, CitationItem } from '../../types/api';
import { useAssistant } from '../../context/AssistantContext';
import { submitFeedback } from '../../services/sourceService';
import { ClarificationPrompt } from './ClarificationPrompt';
import {
  ShieldCheck,
  CheckCircle2,
  ListOrdered,
  FileText,
  ExternalLink,
  ThumbsUp,
  ThumbsDown,
  Award,
} from 'lucide-react';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const { inspectStandard, inspectCitation } = useAssistant();
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
      <div className="flex justify-end my-3 animate-fade-in">
        <div className="max-w-2xl bg-[#21232e] text-[#f1f2f8] border border-[#343748] rounded-2xl px-4 py-3 shadow-sm">
          <p className="text-sm leading-relaxed whitespace-pre-wrap font-sans">{message.content}</p>
          <div className="flex items-center justify-end gap-2 mt-1.5 text-[10px] text-[#8c8f9f] font-mono">
            <span>{message.timestamp}</span>
            {message.userRole && (
              <span className="uppercase font-semibold px-1.5 py-0.2 rounded bg-[#161822] text-[#b4b7cb] border border-[#2d3040]">
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
      color: 'text-emerald-400 bg-emerald-950/40 border-emerald-800/60',
      label: 'Verified Official Standard & QCO Match',
    },
    medium: {
      color: 'text-amber-400 bg-amber-950/40 border-amber-800/60',
      label: 'Standard Identified (General Match)',
    },
    low: {
      color: 'text-[#8c8f9f] bg-[#1a1b24] border-[#2d303f]',
      label: 'General / Clarification Needed',
    },
  }[confidence];

  return (
    <div className="flex flex-col my-3 max-w-4xl animate-fade-in">
      <div className="bg-[#121319] rounded-2xl p-5 border border-[#222430] shadow-sm space-y-4">
        {/* Header with Assistant Persona & Confidence indicator */}
        <div className="flex items-center justify-between border-b border-[#20222e] pb-3">
          <div className="flex items-center gap-2">
            <div className="p-1 rounded-md bg-[#1c1e27] text-[#d4d7e6] border border-[#2d3040]">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs font-semibold text-[#f1f2f8] tracking-wide font-sans">
                ManakSetu AI
              </span>
              <span className="text-[10px] text-[#7d8092] ml-2 font-mono">
                {message.timestamp}
              </span>
            </div>
          </div>

          {payload && (
            <div
              className={`flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[10px] font-medium border ${confidenceConfig.color}`}
              title={confidenceConfig.label}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-current" />
              <span className="uppercase font-semibold tracking-wider font-mono">
                {confidence} Confidence
              </span>
            </div>
          )}
        </div>

        {/* Ambiguity / Clarification Prompt Card if required */}
        {payload?.needs_clarification && payload.clarification_question && (
          <ClarificationPrompt question={payload.clarification_question} />
        )}

        {/* Main Markdown Text Response */}
        <div className="text-sm text-[#e4e5eb] leading-relaxed font-sans prose prose-invert max-w-none prose-p:my-2 prose-headings:text-[#f1f2f8] prose-headings:font-semibold prose-headings:text-sm prose-li:my-0.5 prose-strong:text-[#f1f2f8]">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {payload?.answer || message.content}
          </ReactMarkdown>
        </div>

        {/* Structured Data: Applicable Standards Chips */}
        {payload?.applicable_standards && payload.applicable_standards.length > 0 && (
          <div className="space-y-2 pt-1 border-t border-[#20222e]">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-[#c5c8d8]">
              <Award className="w-3.5 h-3.5 text-[#8c8f9f]" />
              <span>Applicable Indian Standards:</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {payload.applicable_standards.map((std, idx) => (
                <div
                  key={idx}
                  onClick={() => inspectStandard(std.is_number)}
                  className="p-3 rounded-xl bg-[#171922] hover:bg-[#20222e] border border-[#272a38] hover:border-[#3c4054] cursor-pointer transition-all space-y-1.5 group"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-[#f1f2f8] group-hover:text-white">
                      {std.is_number}
                    </span>
                    <span
                      className={`text-[9px] uppercase font-semibold px-1.5 py-0.5 rounded border ${
                        std.mandatory
                          ? 'bg-rose-950/40 text-rose-300 border-rose-800/60'
                          : 'bg-[#222430] text-[#a4a8bc] border-[#343746]'
                      }`}
                    >
                      {std.mandatory ? 'Mandatory QCO' : 'Voluntary'}
                    </span>
                  </div>
                  <p className="text-xs text-[#c5c8d8] line-clamp-2">{std.title}</p>
                  <div className="flex items-center justify-between text-[10px] text-[#7d8092] pt-0.5">
                    <span>{std.certification_scheme || 'Scheme-I (ISI Mark)'}</span>
                    <span className="text-[#a4a8bc] group-hover:underline flex items-center gap-0.5">
                      Inspect <ExternalLink className="w-2.5 h-2.5" />
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Structured Data: Key Requirements & STI Steps in Minimalist Containers */}
        {((payload?.key_requirements && payload.key_requirements.length > 0) ||
          (payload?.compliance_steps && payload.compliance_steps.length > 0)) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 pt-1">
            {payload.key_requirements && payload.key_requirements.length > 0 && (
              <div className="p-3.5 rounded-xl bg-[#161720] border border-[#252836] space-y-2">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-[#c5c8d8]">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#8c8f9f]" />
                  <span>Key Technical Requirements:</span>
                </div>
                <ul className="space-y-1 text-xs text-[#b4b7cb]">
                  {payload.key_requirements.map((req, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-[#64677a] font-mono text-[10px] mt-0.5">•</span>
                      <span>{req}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {payload.compliance_steps && payload.compliance_steps.length > 0 && (
              <div className="p-3.5 rounded-xl bg-[#161720] border border-[#252836] space-y-2">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-[#c5c8d8]">
                  <ListOrdered className="w-3.5 h-3.5 text-[#8c8f9f]" />
                  <span>Compliance & Licensing Steps:</span>
                </div>
                <ol className="space-y-1 text-xs text-[#b4b7cb]">
                  {payload.compliance_steps.map((step, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="font-mono text-[#7d8092] text-[10px] mt-0.5">
                        {idx + 1}.
                      </span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        )}

        {/* Citations & Provenance Pills */}
        {payload?.sources && payload.sources.length > 0 && (
          <div className="pt-2 border-t border-[#20222e] space-y-2">
            <div className="flex items-center gap-1.5 text-xs font-medium text-[#8c8f9f]">
              <FileText className="w-3.5 h-3.5 text-[#7d8092]" />
              <span>Authoritative Citations & Source Evidence:</span>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {payload.sources.map((cit: CitationItem, idx: number) => (
                <button
                  key={idx}
                  onClick={() => inspectCitation(cit)}
                  className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#181a23] hover:bg-[#222432] border border-[#2b2e3e] hover:border-[#43475e] text-[#c5c8d8] hover:text-white text-xs transition-all font-mono shadow-sm"
                  title="Click to view verbatim excerpt in Evidence Drawer"
                >
                  <span className="font-semibold text-[#e4e5eb]">
                    [{cit.standard} {cit.clause ? `Cl. ${cit.clause}` : ''}]
                  </span>
                  {cit.page && <span className="text-[#7d8092] text-[10px]">p.{cit.page}</span>}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Footer with Feedback Controls */}
        <div className="flex items-center justify-between pt-2 border-t border-[#20222e] text-[11px] text-[#7d8092]">
          <span>Official Bureau of Indian Standards Intelligence</span>

          <div className="flex items-center gap-2">
            <span className="text-[10px]">Was this helpful?</span>
            <button
              onClick={() => handleFeedback(1)}
              disabled={feedbackSubmitted}
              className={`p-1 rounded hover:bg-[#20222e] transition-colors ${
                feedbackRating === 1 ? 'text-[#f1f2f8]' : 'text-[#7d8092] hover:text-[#e4e5eb]'
              }`}
              title="Helpful"
            >
              <ThumbsUp className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => handleFeedback(-1)}
              disabled={feedbackSubmitted}
              className={`p-1 rounded hover:bg-[#20222e] transition-colors ${
                feedbackRating === -1 ? 'text-[#f1f2f8]' : 'text-[#7d8092] hover:text-[#e4e5eb]'
              }`}
              title="Not helpful"
            >
              <ThumbsDown className="w-3.5 h-3.5" />
            </button>
            {feedbackSubmitted && (
              <span className="text-[10px] text-[#a4a8bc] font-mono ml-1">Feedback saved</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
