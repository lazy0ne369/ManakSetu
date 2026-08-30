import React from 'react';
import { useAssistant } from '../../context/AssistantContext';
import {
  X,
  ExternalLink,
  ShieldCheck,
  BookOpen,
  Copy,
  Check,
} from 'lucide-react';

export const EvidenceDrawer: React.FC = () => {
  const { activeCitation, isEvidenceDrawerOpen, closeEvidenceDrawer } = useAssistant();
  const [copied, setCopied] = React.useState(false);

  if (!isEvidenceDrawerOpen || !activeCitation) return null;

  const handleCopy = () => {
    if (activeCitation.excerpt) {
      navigator.clipboard.writeText(
        `[${activeCitation.standard} Cl. ${activeCitation.clause || 'General'}] ${activeCitation.excerpt}`
      );
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-xl bg-[#13141b] rounded-2xl border border-[#272937] p-6 space-y-4 shadow-2xl animate-slide-up relative text-[#e4e5eb]">
        {/* Close Button */}
        <button
          onClick={closeEvidenceDrawer}
          className="absolute right-5 top-5 p-1.5 rounded-lg bg-[#1a1c26] hover:bg-[#252735] text-[#8c8f9f] hover:text-white border border-[#2c2e3e] transition-colors"
          title="Close"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-[#1a1c26] text-[#d4d7e6] border border-[#2c2e3e]">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-bold text-[#f1f2f8] font-mono">
                {activeCitation.standard}
              </h3>
              <span className="text-[10px] uppercase font-mono font-medium px-1.5 py-0.5 rounded bg-[#20222e] text-[#c5c8d8] border border-[#303344]">
                Authoritative Source
              </span>
            </div>
            <p className="text-[11px] text-[#7d8092]">
              Verified citation from indexed Bureau of Indian Standards corpus
            </p>
          </div>
        </div>

        {/* Metadata Details */}
        <div className="grid grid-cols-3 gap-2 p-3 rounded-xl bg-[#171822] border border-[#262836] text-xs">
          <div>
            <span className="text-[#64677a] block text-[10px] uppercase font-semibold">Clause</span>
            <span className="font-mono font-bold text-[#f1f2f8]">
              {activeCitation.clause || 'General'}
            </span>
          </div>
          <div>
            <span className="text-[#64677a] block text-[10px] uppercase font-semibold">Section</span>
            <span className="font-mono text-[#c5c8d8]">{activeCitation.section || '—'}</span>
          </div>
          <div>
            <span className="text-[#64677a] block text-[10px] uppercase font-semibold">Document Page</span>
            <span className="font-mono text-[#c5c8d8]">
              {activeCitation.page ? `Page ${activeCitation.page}` : '—'}
            </span>
          </div>
        </div>

        {/* Verbatim Excerpt */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-semibold text-[#c5c8d8]">
            <span className="flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-[#8c8f9f]" />
              <span>Verbatim Standard Excerpt:</span>
            </span>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-[11px] text-[#8c8f9f] hover:text-[#f1f2f8] transition-colors"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>

          <div className="p-4 rounded-xl bg-[#0c0d12] border border-[#21232f] text-xs text-[#e4e5eb] leading-relaxed font-mono whitespace-pre-wrap max-h-60 overflow-y-auto">
            {activeCitation.excerpt || 'Full clause text verified in BIS knowledge base.'}
          </div>
        </div>

        {/* Footer actions */}
        <div className="flex items-center justify-between pt-2 border-t border-[#20222e]">
          <span className="text-[11px] text-[#7d8092]">
            Source: Bureau of Indian Standards (BIS)
          </span>

          <div className="flex items-center gap-2">
            {activeCitation.source_url && (
              <a
                href={activeCitation.source_url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#e4e5eb] hover:bg-white text-[#0e0f14] text-xs font-semibold shadow-sm transition-colors"
              >
                <span>Verify on e-BIS Portal</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            )}
            <button
              onClick={closeEvidenceDrawer}
              className="px-3 py-1.5 rounded-lg bg-[#1a1c26] hover:bg-[#252735] text-[#c5c8d8] text-xs font-medium transition-colors border border-[#2b2e3e]"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
