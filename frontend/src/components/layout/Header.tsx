import React from 'react';
import { useAssistant } from '../../context/AssistantContext';
import {
  ShieldCheck,
  Building2,
  User,
  PlusCircle,
  Activity,
  ExternalLink,
  Sparkles,
} from 'lucide-react';

export const Header: React.FC = () => {
  const { userRole, setUserRole, backendHealthy, clearConversation, isLoading } = useAssistant();

  return (
    <header className="glass-panel border-b border-slate-800/80 px-4 lg:px-6 py-3 flex items-center justify-between sticky top-0 z-30">
      {/* Brand & Identity */}
      <div className="flex items-center gap-3">
        <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-bis-600 to-bis-900 border border-bis-400/30 shadow-lg shadow-bis-600/20">
          <ShieldCheck className="w-6 h-6 text-white" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-amber-400 rounded-full border-2 border-slate-950 animate-pulse-subtle" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-base md:text-lg tracking-tight text-white flex items-center gap-1.5">
              ManakSetu
              <span className="text-xs text-amber-400 font-normal font-sans hidden sm:inline">(मानकसेतु)</span>
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-md bg-bis-500/20 text-bis-300 border border-bis-500/30">
                SIH26107
              </span>
            </h1>
          </div>
          <p className="text-xs text-slate-400 hidden sm:block">
            AI-Powered Intelligent Assistant for Indian Standards & BIS Services
          </p>
        </div>
      </div>

      {/* Center / Right controls */}
      <div className="flex items-center gap-3">
        {/* Persona Mode Switcher */}
        <div className="flex items-center bg-slate-900/90 border border-slate-700/60 rounded-xl p-1 shadow-inner">
          <button
            onClick={() => setUserRole('consumer')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              userRole === 'consumer'
                ? 'bg-bis-600 text-white shadow-md shadow-bis-600/30 font-semibold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
            title="Switch to Consumer Persona: Plain-language, safety-focused, ISI mark verification"
          >
            <User className="w-3.5 h-3.5" />
            <span>Consumer</span>
          </button>

          <button
            onClick={() => setUserRole('industry')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              userRole === 'industry'
                ? 'bg-amber-600 text-white shadow-md shadow-amber-600/30 font-semibold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
            title="Switch to Industry Persona: Technical clauses, QCO details, testing requirements"
          >
            <Building2 className="w-3.5 h-3.5" />
            <span>Industry / Pro</span>
          </button>
        </div>

        {/* Backend Status */}
        <div
          className={`hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs border ${
            backendHealthy
              ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
              : 'bg-rose-500/10 text-rose-300 border-rose-500/30'
          }`}
          title={backendHealthy ? 'Backend API Online' : 'Backend API Disconnected'}
        >
          <Activity className={`w-3.5 h-3.5 ${backendHealthy ? 'animate-pulse' : ''}`} />
          <span className="font-mono text-[11px]">{backendHealthy ? 'LIVE' : 'OFFLINE'}</span>
        </div>

        {/* New Chat Button */}
        <button
          onClick={clearConversation}
          disabled={isLoading}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-200 border border-slate-700/70 text-xs font-medium transition-colors disabled:opacity-50"
          title="Start a new conversation"
        >
          <PlusCircle className="w-3.5 h-3.5 text-slate-400" />
          <span className="hidden sm:inline">New Query</span>
        </button>
      </div>
    </header>
  );
};
