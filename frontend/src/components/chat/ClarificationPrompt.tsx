import React from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { AlertCircle, ArrowRight, CornerDownRight } from 'lucide-react';

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
    <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-100 my-3 animate-fade-in">
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400 mt-0.5">
          <AlertCircle className="w-5 h-5" />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-sm text-amber-200 mb-1 flex items-center gap-1.5">
            Clarification Needed to Provide Accurate Standard Details
          </h4>
          <p className="text-xs text-amber-200/90 leading-relaxed mb-3">
            {question}
          </p>

          <div className="text-[11px] font-medium text-amber-300/80 mb-2 flex items-center gap-1">
            <CornerDownRight className="w-3 h-3" />
            <span>Select one of the verified products below, or type your specific product name:</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {options.map((opt, idx) => (
              <button
                key={idx}
                onClick={() => sendMessage(`What BIS standard and certification applies to ${opt}?`)}
                disabled={isLoading}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 text-amber-100 hover:text-white border border-amber-500/30 text-xs font-medium transition-colors disabled:opacity-50"
              >
                <span>{opt}</span>
                <ArrowRight className="w-3 h-3 text-amber-400" />
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
