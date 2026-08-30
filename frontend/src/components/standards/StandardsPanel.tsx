import React, { useState, useEffect } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import { searchStandards } from '../../services/standardsService';
import {
  Search,
  BookOpen,
  FileCheck,
  ExternalLink,
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
    <div className="h-full flex flex-col p-4 space-y-4 overflow-y-auto bg-[#111217]">
      {/* Search Standards Bar */}
      <form onSubmit={handleSearch} className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search Indian Standards (e.g. IS 2347, cables, iron)..."
          className="w-full bg-[#161720] border border-[#272937] rounded-xl pl-9 pr-4 py-2 text-xs text-[#f1f2f8] placeholder-[#64677a] focus:outline-none focus:border-[#43475d]"
        />
        <Search className="w-4 h-4 text-[#7d8092] absolute left-3 top-2.5" />
      </form>

      {selectedStandardLoading ? (
        <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
          <Loader2 className="w-6 h-6 text-[#8c8f9f] animate-spin" />
          <p className="text-xs text-[#8c8f9f]">Loading Standard Specification & Clauses...</p>
        </div>
      ) : selectedStandard ? (
        <div className="space-y-4 animate-fade-in">
          {/* Active Standard Header Card */}
          <div className="p-4 rounded-xl bg-[#161720] border border-[#272937] space-y-3 shadow-sm">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs font-bold text-[#f1f2f8]">
                  {selectedStandard.is_number}
                </span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-[#222430] text-[#c5c8d8] border border-[#323546]">
                  {selectedStandard.status}
                </span>
              </div>
              {selectedStandard.source_url && (
                <a
                  href={selectedStandard.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1 text-[11px] text-[#a4a8bc] hover:text-white transition-colors"
                >
                  <span>e-BIS Portal</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>

            <h3 className="text-xs font-semibold text-[#f1f2f8] leading-relaxed font-sans">
              {selectedStandard.title}
            </h3>

            {selectedStandard.scope && (
              <div className="text-[11px] text-[#c5c8d8] leading-relaxed bg-[#121319] p-3 rounded-lg border border-[#222430] space-y-1">
                <span className="font-semibold text-[#8c8f9f] block uppercase text-[10px]">Scope</span>
                <p>{selectedStandard.scope}</p>
              </div>
            )}

            <div className="grid grid-cols-2 gap-2 text-[11px] text-[#8c8f9f] pt-1 border-t border-[#222430]">
              <div>
                <span className="text-[#64677a]">Category: </span>
                <span className="text-[#c5c8d8]">{selectedStandard.category || 'Standard'}</span>
              </div>
              <div>
                <span className="text-[#64677a]">Committee: </span>
                <span className="text-[#c5c8d8]">{selectedStandard.committee || 'BIS Panel'}</span>
              </div>
            </div>
          </div>

          {/* Clauses Breakdown Accordion */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-[#c5c8d8] flex items-center gap-1.5 px-1">
              <BookOpen className="w-3.5 h-3.5 text-[#8c8f9f]" />
              <span>Standard Clauses ({selectedStandard.clauses?.length || 0})</span>
            </h4>

            {selectedStandard.clauses && selectedStandard.clauses.length > 0 ? (
              <div className="space-y-1.5">
                {selectedStandard.clauses.map((clause, idx) => {
                  const isExpanded = expandedClause === `${clause.clause}-${idx}`;
                  return (
                    <div
                      key={idx}
                      className="rounded-lg bg-[#15161f] border border-[#242634] overflow-hidden"
                    >
                      <button
                        onClick={() =>
                          setExpandedClause(isExpanded ? null : `${clause.clause}-${idx}`)
                        }
                        className="w-full flex items-center justify-between p-3 text-left hover:bg-[#1e202a] transition-colors"
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-[#d4d7e6]">
                            Cl. {clause.clause || 'General'}
                          </span>
                          <span className="text-xs text-[#b4b7cb] line-clamp-1">
                            {clause.content.split('\n')[0].replace(/^\[.*?\]\s*/, '')}
                          </span>
                        </div>
                        {isExpanded ? (
                          <ChevronUp className="w-3.5 h-3.5 text-[#7d8092] shrink-0" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5 text-[#7d8092] shrink-0" />
                        )}
                      </button>

                      {isExpanded && (
                        <div className="p-3 pt-0 text-xs text-[#c5c8d8] leading-relaxed border-t border-[#232533] bg-[#111218] font-mono text-[11px]">
                          <p className="whitespace-pre-wrap">{clause.content}</p>
                          {clause.page && (
                            <span className="inline-block mt-2 text-[10px] text-[#64677a]">
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
              <div className="p-4 rounded-xl bg-[#14151c] border border-[#232533] text-center text-xs text-[#8c8f9f]">
                No indexed clause excerpts available for this standard.
              </div>
            )}
          </div>

          {/* Active Amendments */}
          {selectedStandard.amendments && selectedStandard.amendments.length > 0 && (
            <div className="space-y-2 pt-1">
              <h4 className="text-xs font-semibold text-[#c5c8d8] flex items-center gap-1.5 px-1">
                <FileCheck className="w-3.5 h-3.5 text-[#8c8f9f]" />
                <span>Active Amendments ({selectedStandard.amendments.length})</span>
              </h4>
              <div className="space-y-1.5">
                {selectedStandard.amendments.map((amd, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-xl bg-[#15161f] border border-[#242634] space-y-1 text-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-[#e4e5eb]">
                        {amd.amendment_number}
                      </span>
                      {amd.effective_date && (
                        <span className="text-[10px] text-[#7d8092] font-mono">
                          Effective: {amd.effective_date}
                        </span>
                      )}
                    </div>
                    {amd.title && <p className="text-[#c5c8d8] text-[11px]">{amd.title}</p>}
                    {amd.notes && <p className="text-[#8c8f9f] text-[11px]">{amd.notes}</p>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Standards Search Results List */
        <div className="space-y-2.5">
          <h4 className="text-xs font-semibold text-[#8c8f9f] px-1">
            Browse Indian Standards ({searchResults.length})
          </h4>
          <div className="space-y-2">
            {searchResults.map((item) => (
              <div
                key={item.id}
                onClick={() => inspectStandard(item.is_number)}
                className="p-3 rounded-xl bg-[#15161f] hover:bg-[#1e202a] border border-[#242634] hover:border-[#383b4d] cursor-pointer transition-all space-y-1.5 group shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-[#e4e5eb] group-hover:text-white">
                    {item.is_number}
                  </span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#20222e] text-[#a4a8bc] border border-[#2f3243]">
                    {item.status}
                  </span>
                </div>
                <p className="text-xs text-[#c5c8d8] line-clamp-1">{item.title}</p>
                <div className="text-[10px] text-[#64677a] flex items-center justify-between pt-0.5">
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
