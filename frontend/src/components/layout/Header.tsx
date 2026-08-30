import React, { useState, useRef, useEffect } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import {
  ShieldCheck,
  ChevronDown,
  User,
  Building2,
  Plus,
  Check,
  PanelRight,
} from 'lucide-react';

interface HeaderProps {
  isRightPanelOpen?: boolean;
  onToggleRightPanel?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ isRightPanelOpen, onToggleRightPanel }) => {
  const { userRole, setUserRole, backendHealthy, clearConversation, isLoading } = useAssistant();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicked outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="h-14 bg-[#0d0e13] border-b border-[#1f212c] px-4 lg:px-6 flex items-center justify-between sticky top-0 z-30 shrink-0 select-none">
      {/* Left: Prominent Branding & Subtitles */}
      <div className="flex items-center gap-3.5">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-[#161822] border border-[#2a2d3c] text-white shadow-sm">
          <ShieldCheck className="w-4 h-4 text-zinc-100" />
        </div>

        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-sm md:text-base tracking-tight text-white flex items-center gap-1.5 font-sans">
              ManakSetu
              <span className="text-xs text-zinc-400 font-normal font-sans hidden sm:inline">(मानकसेतु)</span>
            </h1>
            <span className="text-[11px] uppercase font-mono font-semibold px-2 py-0.5 rounded-md bg-[#1a1c26] text-zinc-300 border border-[#2c2f40]">
              SIH26107
            </span>
          </div>
          <p className="text-xs text-zinc-400 hidden sm:block font-sans">
            AI Assistant for Indian Standards & BIS Services
          </p>
        </div>
      </div>

      {/* Center / Right: Persona Switcher + API Status + New Query Button + Sidebar Toggle */}
      <div className="flex items-center gap-2.5">
        {/* Model / Regulatory Persona Dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#161720] hover:bg-[#1e202c] border border-[#282a38] hover:border-[#3a3d50] text-zinc-200 transition-all text-xs font-medium"
            title="Click to change regulatory mode"
          >
            {userRole === 'industry' ? (
              <Building2 className="w-3.5 h-3.5 text-zinc-300" />
            ) : (
              <User className="w-3.5 h-3.5 text-zinc-300" />
            )}
            <span className="font-semibold text-zinc-100">
              {userRole === 'industry' ? 'Industry / Pro Mode' : 'Consumer Mode'}
            </span>
            <ChevronDown className="w-3.5 h-3.5 text-zinc-400 transition-transform" />
          </button>

          {/* Floating Dropdown Selector */}
          {dropdownOpen && (
            <div className="absolute right-0 sm:left-0 top-full mt-1.5 w-72 bg-[#12131a] border border-[#282a38] rounded-xl p-1.5 shadow-2xl z-50 animate-slide-up">
              <div className="px-2.5 py-1 text-[10px] uppercase font-mono font-bold text-zinc-400">
                Select Regulatory Persona
              </div>

              <button
                onClick={() => {
                  setUserRole('consumer');
                  setDropdownOpen(false);
                }}
                className={`w-full flex items-start gap-2.5 p-2 rounded-lg text-left transition-colors ${
                  userRole === 'consumer'
                    ? 'bg-[#1f212d] text-white border border-[#343748]'
                    : 'hover:bg-[#181922] text-zinc-300'
                }`}
              >
                <User className="w-4 h-4 text-zinc-300 mt-0.5 shrink-0" />
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-zinc-100">Consumer Mode</span>
                    {userRole === 'consumer' && <Check className="w-3.5 h-3.5 text-emerald-400" />}
                  </div>
                  <p className="text-[11px] text-zinc-400 leading-tight mt-0.5">
                    Plain-language answers, product safety & ISI mark verification.
                  </p>
                </div>
              </button>

              <button
                onClick={() => {
                  setUserRole('industry');
                  setDropdownOpen(false);
                }}
                className={`w-full flex items-start gap-2.5 p-2 rounded-lg text-left transition-colors mt-1 ${
                  userRole === 'industry'
                    ? 'bg-[#1f212d] text-white border border-[#343748]'
                    : 'hover:bg-[#181922] text-zinc-300'
                }`}
              >
                <Building2 className="w-4 h-4 text-zinc-300 mt-0.5 shrink-0" />
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-zinc-100">Industry / Pro Mode</span>
                    {userRole === 'industry' && <Check className="w-3.5 h-3.5 text-emerald-400" />}
                  </div>
                  <p className="text-[11px] text-zinc-400 leading-tight mt-0.5">
                    Technical clauses, mandatory QCOs, testing rules & Scheme-I/II.
                  </p>
                </div>
              </button>
            </div>
          )}
        </div>

        {/* API Status Pill */}
        <div
          className="hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs bg-[#14151c] border border-[#242634]"
          title={backendHealthy ? 'Backend API Online' : 'Backend API Disconnected'}
        >
          <span
            className={`w-2 h-2 rounded-full ${
              backendHealthy
                ? 'bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.5)]'
                : 'bg-rose-500'
            }`}
          />
          <span className="font-mono text-xs font-medium text-zinc-300">
            {backendHealthy ? 'API Online' : 'Offline'}
          </span>
        </div>

        {/* "+ New Query" Button */}
        <button
          onClick={clearConversation}
          disabled={isLoading}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#181922] hover:bg-[#232532] text-zinc-200 hover:text-white border border-[#282a38] hover:border-[#3c4054] text-xs font-medium transition-all disabled:opacity-40 shadow-sm"
          title="Start a new query"
        >
          <Plus className="w-3.5 h-3.5 text-zinc-300" />
          <span className="font-medium">New Query</span>
        </button>

        {/* Optional Sidebar Toggle Button on top-right */}
        {onToggleRightPanel && (
          <button
            onClick={onToggleRightPanel}
            className={`hidden lg:flex p-2 rounded-lg text-xs font-medium transition-all border ${
              isRightPanelOpen
                ? 'bg-[#222430] text-white border-[#383b4e]'
                : 'bg-[#181922] hover:bg-[#232532] text-zinc-400 hover:text-zinc-200 border-[#282a38]'
            }`}
            title={isRightPanelOpen ? 'Hide Standards & QCO Panel' : 'Show Standards & QCO Panel'}
          >
            <PanelRight className="w-4 h-4" />
          </button>
        )}
      </div>
    </header>
  );
};
