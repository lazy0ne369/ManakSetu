import React from 'react';
import { ApplicableStandardItem } from '../../types/api';
import { useAssistant } from '../../context/AssistantContext';
import { Award, ChevronRight, CheckCircle2, ShieldAlert } from 'lucide-react';

interface StandardCardProps {
  standard: ApplicableStandardItem;
}

export const StandardCard: React.FC<StandardCardProps> = ({ standard }) => {
  const { inspectStandard } = useAssistant();

  return (
    <div
      onClick={() => inspectStandard(standard.is_number)}
      className="p-4 rounded-2xl glass-card border border-slate-800 hover:border-bis-500/50 cursor-pointer transition-all space-y-2.5 group shadow-lg"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-bis-600/20 text-bis-400 border border-bis-500/30">
            <Award className="w-4 h-4" />
          </div>
          <div>
            <span className="font-mono text-xs font-bold text-white group-hover:text-bis-300 transition-colors">
              {standard.is_number}
            </span>
            {standard.year && (
              <span className="text-[11px] text-slate-500 ml-1.5">({standard.year})</span>
            )}
          </div>
        </div>

        {standard.mandatory ? (
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-bold uppercase bg-rose-500/10 text-rose-300 border border-rose-500/30">
            <ShieldAlert className="w-3 h-3" />
            <span>Mandatory QCO</span>
          </span>
        ) : (
          <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-800 text-slate-400 border border-slate-700">
            Voluntary
          </span>
        )}
      </div>

      <h4 className="text-xs font-medium text-slate-200 line-clamp-2 leading-relaxed">
        {standard.title}
      </h4>

      {standard.applicability_reason && (
        <p className="text-[11px] text-slate-400 line-clamp-2 leading-normal">
          {standard.applicability_reason}
        </p>
      )}

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-[11px] text-bis-400 group-hover:text-bis-300 font-medium">
        <span>View Clauses & Amendments</span>
        <ChevronRight className="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform" />
      </div>
    </div>
  );
};
