import React, { useState, useEffect } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { searchStandards, getStandardById } from '../../services/standardsService';
import {
  Award,
  Search,
  BookOpen,
  FileCheck,
  Calendar,
  ExternalLink,
  Layers,
  Shield,
  Loader2,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

export const StandardsPanel: React.FC = () => {
  const { selectedStandard, selectedStandardLoading, inspectStandard } = useAssistant();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [expandedClause, setExpandedClause] = useState<string | null>(null);

  // Quick initial standards load if none selected
  useEffect(() => {
    if (!selectedStandard) {
      setIsSearching(true);
      searchStandards('', undefined, undefined, undefined, 6)
        .then((res) => setSearchResults(res.items))
        .catch((err) => console.error(err))
        .finally(() => setIsSearching(false));
    }
  }, [selectedStandard]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const res = await searchStandards(searchQuery.trim());
      setSearchResults(res.items);
    } catch (err) {
      console.error('Search error:', err);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="h-full flex flex-col p-4 space-y-4 overflow-y-auto">
      {/* Search Standards Bar */}
      <form onSubmit={handleSearch} className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search Indian Standards (e.g., IS 2347, cables, iron)..."
          className="w-full bg-slate-900 border border-slate-700/80 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-bis-500"
        />
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
      </form>

      {selectedStandardLoading ? (
        <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
          <Loader2 className="w-7 h-7 text-bis-400 animate-spin" />
          <p className="text-xs text-slate-400">Loading Standard Specification & Clauses...</p>
        </div>
      ) : selectedStandard ? (
        <div className="space-y-4 animate-fade-in">
          {/* Active Standard Header Card */}
          <div className="p-4 rounded-2xl glass-card border border-bis-500/30 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-mono text-sm font-bold text-bis-300">
                  {selectedStandard.is_number}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
                  {selectedStandard.status}
                </span>
              </div>
              {selectedStandard.source_url && (
                <a
                  href={selectedStandard.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1 text-[11px] text-bis-400 hover:text-bis-300 transition-colors"
                >
                  <span>e-BIS Portal</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>

            <h3 className="text-xs font-semibold text-white leading-relaxed">
              {selectedStandard.title}
            </h3>

            {selectedStandard.scope && (
              <p className="text-[11px] text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                <span className="font-semibold text-bis-300">Scope: </span>
                {selectedStandard.scope}
              </p>
            )}

            <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-400 pt-1">
              <div>
                <span className="text-slate-500">Category: </span>
                {selectedStandard.category || 'Standard'}
              </div>
              <div>
                <span className="text-slate-500">Committee: </span>
                {selectedStandard.committee || 'BIS Technical Panel'}
              </div>
            </div>
          </div>

          {/* Clauses Breakdown Accordion */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-300 flex items-center gap-1.5 px-1">
              <BookOpen className="w-3.5 h-3.5 text-bis-400" />
              <span>Standard Clauses ({selectedStandard.clauses?.length || 0})</span>
            </h4>

            {selectedStandard.clauses && selectedStandard.clauses.length > 0 ? (
              <div className="space-y-2">
                {selectedStandard.clauses.map((clause, idx) => {
                  const isExpanded = expandedClause === `${clause.clause}-${idx}`;
                  return (
                    <div
                      key={idx}
                      className="rounded-xl glass-card border border-slate-800 overflow-hidden"
                    >
                      <button
                        onClick={() =>
                          setExpandedClause(isExpanded ? null : `${clause.clause}-${idx}`)
                        }
                        className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-800/40 transition-colors"
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-bis-400">
                            Cl. {clause.clause || 'General'}
                          </span>
                          <span className="text-xs text-slate-200 line-clamp-1">
                            {clause.content.split('\n')[0].replace(/^\[.*?\]\s*/, '')}
                          </span>
                        </div>
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                        )}
                      </button>

                      {isExpanded && (
                        <div className="p-3 pt-0 text-xs text-slate-300 leading-relaxed border-t border-slate-800/60 bg-slate-900/40 font-mono text-[11px]">
                          <p className="whitespace-pre-wrap">{clause.content}</p>
                          {clause.page && (
                            <span className="inline-block mt-2 text-[10px] text-slate-500">
                              Document Page {clause.page}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-slate-900/50 text-center text-xs text-slate-400">
                No indexed clause excerpts available for this standard.
              </div>
            )}
          </div>

          {/* Active Amendments */}
          {selectedStandard.amendments && selectedStandard.amendments.length > 0 && (
            <div className="space-y-2 pt-2">
              <h4 className="text-xs font-bold text-slate-300 flex items-center gap-1.5 px-1">
                <FileCheck className="w-3.5 h-3.5 text-amber-400" />
                <span>Active Amendments ({selectedStandard.amendments.length})</span>
              </h4>
              <div className="space-y-2">
                {selectedStandard.amendments.map((amd, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-xl glass-card border border-slate-800 space-y-1 text-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-amber-300">
                        {amd.amendment_number}
                      </span>
                      {amd.effective_date && (
                        <span className="text-[10px] text-slate-400">
                          Effective: {amd.effective_date}
                        </span>
                      )}
                    </div>
                    {amd.title && <p className="text-slate-200 text-[11px]">{amd.title}</p>}
                    {amd.notes && <p className="text-slate-400 text-[11px]">{amd.notes}</p>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Standards Search Results List */
        <div className="space-y-3">
          <h4 className="text-xs font-bold text-slate-400 px-1">
            Browse Indian Standards ({searchResults.length})
          </h4>
          <div className="space-y-2">
            {searchResults.map((item) => (
              <div
                key={item.id}
                onClick={() => inspectStandard(item.is_number)}
                className="p-3 rounded-xl glass-card border border-slate-800 hover:border-bis-500/50 cursor-pointer transition-all space-y-1 group"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-bis-300 group-hover:text-bis-200">
                    {item.is_number}
                  </span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                    {item.status}
                  </span>
                </div>
                <p className="text-xs text-slate-200 line-clamp-1">{item.title}</p>
                <div className="text-[10px] text-slate-500 flex items-center justify-between pt-1">
                  <span>{item.category}</span>
                  <span>{item.amendments_count} Amendments</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
