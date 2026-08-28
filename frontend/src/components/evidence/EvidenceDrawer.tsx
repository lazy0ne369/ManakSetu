import React from 'react';
import { useAssistant } from '../../context/AssistantContext';
import {
  FileText,
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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-xl glass-card rounded-3xl border border-bis-500/40 p-6 space-y-4 shadow-2xl animate-slide-up relative bg-slate-950/95">
        {/* Close Button */}
        <button
          onClick={closeEvidenceDrawer}
          className="absolute right-5 top-5 p-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
          title="Close"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-bis-600/20 text-bis-400 border border-bis-500/30">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-white font-mono">
                {activeCitation.standard}
              </h3>
              <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
                Authoritative BIS Clause
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Verified citation from indexed Indian Standard database
            </p>
          </div>
        </div>

        {/* Metadata Details */}
        <div className="grid grid-cols-3 gap-2 p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs">
          <div>
            <span className="text-slate-500 block text-[10px] uppercase font-semibold">Clause</span>
            <span className="font-mono font-bold text-bis-300">
              {activeCitation.clause || 'General'}
            </span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px] uppercase font-semibold">Section</span>
            <span className="font-mono text-slate-200">{activeCitation.section || '—'}</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px] uppercase font-semibold">Document Page</span>
            <span className="font-mono text-slate-200">
              {activeCitation.page ? `Page ${activeCitation.page}` : '—'}
            </span>
          </div>
        </div>

        {/* Verbatim Excerpt */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
            <span className="flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-bis-400" />
              <span>Verbatim Clause Text:</span>
            </span>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-slate-200 transition-colors"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-200 leading-relaxed font-mono whitespace-pre-wrap max-h-60 overflow-y-auto">
            {activeCitation.excerpt || 'Full clause text verified in BIS knowledge base.'}
          </div>
        </div>

        {/* Footer actions */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
          <span className="text-[11px] text-slate-500">
            Source: Bureau of Indian Standards (BIS)
          </span>

          <div className="flex items-center gap-2">
            {activeCitation.source_url && (
              <a
                href={activeCitation.source_url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-bis-600 hover:bg-bis-500 text-white text-xs font-semibold shadow-md shadow-bis-600/30 transition-colors"
              >
                <span>Verify on e-BIS Portal</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            )}
            <button
              onClick={closeEvidenceDrawer}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
