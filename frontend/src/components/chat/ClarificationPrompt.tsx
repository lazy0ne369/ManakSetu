import React from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { HelpCircle, ArrowRight } from 'lucide-react';

interface ClarificationPromptProps {
  question: string;
}

export const ClarificationPrompt: React.FC<ClarificationPromptProps> = ({ question }) => {
  const { sendMessage, isLoading } = useAssistant();

  const options = [
    'Domestic Pressure Cookers (IS 2347)',
    'Electric Dry & Steam Irons (IS 302-2-3)',
    'Plugs & Socket Outlets 6A/16A (IS 1293)',
    'PVC Insulated Electric Cables (IS 694)',
    'Safety of Toys (IS 9873)',
    'Insulating Mats (IS 15652)',
  ];

  return (
    <div className="p-4 rounded-xl bg-[#161720] border border-[#2b2d3c] text-[#e4e5eb] my-2 animate-fade-in space-y-3 shadow-sm">
      <div className="flex items-start gap-2.5">
        <div className="p-1.5 rounded-lg bg-[#20222e] text-[#d4d7e6] border border-[#2f3244] mt-0.5 shrink-0">
          <HelpCircle className="w-4 h-4" />
        </div>
        <div className="space-y-1">
          <h4 className="font-semibold text-xs text-[#f1f2f8] font-sans">
            Additional Context Needed
          </h4>
          <p className="text-xs text-[#c5c8d8] leading-relaxed">
            {question}
          </p>
        </div>
      </div>

      <div className="pt-2 border-t border-[#252734] space-y-2">
        <span className="text-[11px] text-[#8c8f9f] block font-medium">
          Select a verified product category below or type your specific query:
        </span>

        <div className="flex flex-wrap gap-1.5">
          {options.map((opt, idx) => (
            <button
              key={idx}
              onClick={() => sendMessage(`What BIS standard and certification applies to ${opt}?`)}
              disabled={isLoading}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#20222e] hover:bg-[#2a2c3a] text-[#c5c8d8] hover:text-white border border-[#303344] text-xs font-medium transition-colors disabled:opacity-50 shadow-sm"
            >
              <span>{opt}</span>
              <ArrowRight className="w-3 h-3 text-[#8c8f9f]" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
