import React from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { Sparkles, Utensils, Zap, Plug, Cable, ShieldCheck, HelpCircle } from 'lucide-react';

export const QuickPrompts: React.FC = () => {
  const { sendMessage, isLoading } = useAssistant();

  const prompts = [
    {
      icon: <Utensils className="w-3.5 h-3.5 text-[#b2b6cb]" />,
      label: 'Pressure Cookers (IS 2347)',
      query: 'I manufacture stainless steel pressure cookers. Which BIS standard applies and what are the proof pressure requirements?',
    },
    {
      icon: <Zap className="w-3.5 h-3.5 text-[#b2b6cb]" />,
      label: 'Electric Iron Safety (IS 302)',
      query: 'Is there a mandatory QCO for electric irons and what thermal cutout protection is required?',
    },
    {
      icon: <Plug className="w-3.5 h-3.5 text-[#b2b6cb]" />,
      label: 'Plugs & Sockets (IS 1293)',
      query: 'What are the 16A shutter mechanism and gauge specifications under IS 1293:2019?',
    },
    {
      icon: <Cable className="w-3.5 h-3.5 text-[#b2b6cb]" />,
      label: 'PVC Cables (IS 694)',
      query: 'How do I obtain an ISI mark license under Scheme-I for 1100V low voltage PVC cables?',
    },
    {
      icon: <ShieldCheck className="w-3.5 h-3.5 text-[#b2b6cb]" />,
      label: 'Toy Safety (IS 9873)',
      query: 'What are the mechanical and small parts safety rules for toys under IS 9873 (Part 1)?',
    },
    {
      icon: <HelpCircle className="w-3.5 h-3.5 text-[#b2b6cb]" />,
      label: 'Ambiguous Query (Clarification)',
      query: 'What BIS certification do I need?',
    },
  ];

  return (
    <div className="w-full max-w-3xl mx-auto pt-2">
      <div className="flex items-center justify-center gap-1.5 text-xs text-[#8c8f9f] font-medium mb-3">
        <Sparkles className="w-3.5 h-3.5 text-[#a4a8bc]" />
        <span>Suggested Queries & Case Studies</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
        {prompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => sendMessage(p.query)}
            disabled={isLoading}
            className="flex items-center gap-2.5 p-3 rounded-xl bg-[#13141b] hover:bg-[#1e202a] border border-[#232532] hover:border-[#383c4e] text-left text-xs text-[#c5c8d8] hover:text-white transition-all disabled:opacity-50 group shadow-sm"
          >
            <div className="p-1.5 rounded-md bg-[#1c1e28] border border-[#2c2f3e] group-hover:border-[#404358] transition-colors shrink-0">
              {p.icon}
            </div>
            <span className="font-medium truncate">{p.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
