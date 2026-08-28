import React from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { Sparkles, Utensils, Zap, Plug, ShieldAlert, Cable, HelpCircle } from 'lucide-react';

export const QuickPrompts: React.FC = () => {
  const { sendMessage, isLoading, userRole } = useAssistant();

  const prompts = [
    {
      icon: <Utensils className="w-3.5 h-3.5 text-amber-400" />,
      label: 'Pressure Cookers (IS 2347)',
      query: 'I manufacture stainless steel pressure cookers. Which BIS standard applies and what are the proof pressure requirements?',
    },
    {
      icon: <Zap className="w-3.5 h-3.5 text-yellow-400" />,
      label: 'Electric Iron Safety (IS 302)',
      query: 'Is there a mandatory QCO for electric irons and what thermal cutout protection is required?',
    },
    {
      icon: <Plug className="w-3.5 h-3.5 text-sky-400" />,
      label: 'Plugs & Sockets (IS 1293)',
      query: 'What are the 16A shutter mechanism and gauge specifications under IS 1293:2019?',
    },
    {
      icon: <Cable className="w-3.5 h-3.5 text-emerald-400" />,
      label: 'PVC Cables (IS 694)',
      query: 'How do I obtain an ISI mark license under Scheme-I for 1100V low voltage PVC cables?',
    },
    {
      icon: <ShieldAlert className="w-3.5 h-3.5 text-pink-400" />,
      label: 'Toy Safety (IS 9873)',
      query: 'What are the mechanical and small parts safety rules for toys under IS 9873 (Part 1)?',
    },
    {
      icon: <HelpCircle className="w-3.5 h-3.5 text-indigo-400" />,
      label: 'Ambiguous Query (Clarification)',
      query: 'What BIS certification do I need?',
    },
  ];

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-3">
      <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium mb-2.5">
        <Sparkles className="w-3.5 h-3.5 text-amber-400" />
        <span>Suggested BIS & Standards Queries:</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
        {prompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => sendMessage(p.query)}
            disabled={isLoading}
            className="flex items-center gap-2 p-2.5 rounded-xl glass-card text-left text-xs text-slate-300 hover:text-white transition-all disabled:opacity-50 group border border-slate-800 hover:border-bis-500/40"
          >
            <div className="p-1.5 rounded-lg bg-slate-800/80 group-hover:bg-slate-700/90 transition-colors">
              {p.icon}
            </div>
            <span className="font-medium truncate">{p.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
