import React, { useState } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import {
  ShieldAlert,
  FileBadge,
  CheckCircle,
  ExternalLink,
} from 'lucide-react';

export const CompliancePanel: React.FC = () => {
  const { selectedStandard } = useAssistant();
  const [activeTab, setActiveTab] = useState<'qco' | 'schemes' | 'sti'>('qco');

  const qcos = selectedStandard?.qcos || [];

  const schemes = [
    {
      id: 'Scheme-I',
      name: 'Product Certification Scheme (ISI Mark)',
      desc: 'Mandatory standard mark on packaging. Requires in-house testing laboratory, factory audit, sample verification, and STI adherence.',
      products: 'Pressure Cookers, Electric Irons, Plugs & Sockets, PVC Cables, Toys, Steel, Cement, Water Heaters',
      badge: 'Full Factory Inspection',
    },
    {
      id: 'Scheme-II (CRS)',
      name: 'Compulsory Registration Scheme (CRS)',
      desc: 'Self-declaration of conformity based on test reports from BIS recognized laboratories. No prior factory audit required.',
      products: 'Laptops, Mobile Phones, LED Lighting, Smart Watches, Solar Inverters',
      badge: 'Lab Testing Only',
    },
    {
      id: 'FMCS',
      name: 'Foreign Manufacturers Certification Scheme',
      desc: 'For offshore factories exporting goods to India. Requires Authorized Indian Representative (AIR) and overseas factory audit.',
      products: 'All overseas manufactured products under Scheme-I',
      badge: 'Overseas Audit',
    },
  ];

  const stiChecklist = [
    {
      title: 'In-House Laboratory Setup',
      desc: 'Equip manufacturing plant with calibrated test equipment specified in the standard (e.g. proof pressure rig, high-voltage spark tester).',
    },
    {
      title: 'Qualified QC Personnel',
      desc: 'Appoint qualified technical quality personnel responsible for daily testing and logging inspection records.',
    },
    {
      title: 'Scheme of Testing & Inspection (STI)',
      desc: 'Follow the prescribed sampling frequency, lot testing rules, and maintain traceable testing registers.',
    },
    {
      title: 'Online Application (Manakonline)',
      desc: 'Submit application on www.manakonline.in with layout plans, test reports, and factory documentation.',
    },
    {
      title: 'Factory Audit & Grant of License',
      desc: 'Facilitate on-site audit by BIS officer, draw verification samples, and receive CM/L (Certification Marks Licence).',
    },
  ];

  return (
    <div className="h-full flex flex-col p-4 space-y-4 overflow-y-auto bg-[#111217]">
      {/* Sub-Navigation Tabs */}
      <div className="flex items-center bg-[#0d0e13] border border-[#222430] rounded-lg p-1 shrink-0">
        <button
          onClick={() => setActiveTab('qco')}
          className={`flex-1 py-1.5 rounded-md text-xs font-medium transition-all ${
            activeTab === 'qco'
              ? 'bg-[#242634] text-[#f1f2f8] border border-[#373a4d] shadow-sm'
              : 'text-[#8c8f9f] hover:text-[#e4e5eb]'
          }`}
        >
          Quality Control Orders
        </button>
        <button
          onClick={() => setActiveTab('schemes')}
          className={`flex-1 py-1.5 rounded-md text-xs font-medium transition-all ${
            activeTab === 'schemes'
              ? 'bg-[#242634] text-[#f1f2f8] border border-[#373a4d] shadow-sm'
              : 'text-[#8c8f9f] hover:text-[#e4e5eb]'
          }`}
        >
          Schemes
        </button>
        <button
          onClick={() => setActiveTab('sti')}
          className={`flex-1 py-1.5 rounded-md text-xs font-medium transition-all ${
            activeTab === 'sti'
              ? 'bg-[#242634] text-[#f1f2f8] border border-[#373a4d] shadow-sm'
              : 'text-[#8c8f9f] hover:text-[#e4e5eb]'
          }`}
        >
          STI Checklist
        </button>
      </div>

      {activeTab === 'qco' && (
        <div className="space-y-3 animate-fade-in">
          <div className="flex items-center justify-between px-1">
            <h4 className="text-xs font-semibold text-[#f1f2f8] flex items-center gap-1.5">
              <ShieldAlert className="w-3.5 h-3.5 text-[#8c8f9f]" />
              <span>Mandatory QCO Orders</span>
            </h4>
            <span className="text-[10px] text-[#64677a] font-mono">Gazette Orders</span>
          </div>

          {qcos.length > 0 ? (
            qcos.map((q, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl bg-[#161720] border border-[#272937] space-y-2.5 shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-[#f1f2f8]">
                    {q.qco_number}
                  </span>
                  <span className="px-1.5 py-0.5 rounded text-[9px] uppercase font-semibold bg-[#242634] text-[#d4d7e6] border border-[#373a4d]">
                    {q.status}
                  </span>
                </div>

                <h5 className="text-xs font-semibold text-[#f1f2f8] leading-relaxed font-sans">{q.title}</h5>

                <div className="space-y-1 text-[11px] text-[#c5c8d8] bg-[#121319] p-2.5 rounded-lg border border-[#222430] font-sans">
                  <div className="flex justify-between">
                    <span className="text-[#64677a]">Ministry:</span>
                    <span className="text-right text-[#e4e5eb]">{q.ministry || 'DPIIT'}</span>
                  </div>
                  {q.enforcement_date && (
                    <div className="flex justify-between">
                      <span className="text-[#64677a]">Enforcement Date:</span>
                      <span className="text-[#e4e5eb] font-mono">{q.enforcement_date}</span>
                    </div>
                  )}
                </div>

                {q.source_url && (
                  <a
                    href={q.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center justify-end gap-1 text-[11px] text-[#a4a8bc] hover:text-white font-medium pt-0.5"
                  >
                    <span>View Gazette Order</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            ))
          ) : (
            <div className="p-5 rounded-xl bg-[#14151c] border border-[#232533] text-center space-y-2">
              <ShieldAlert className="w-5 h-5 text-[#64677a] mx-auto" />
              <p className="text-xs text-[#c5c8d8] font-medium">
                {selectedStandard
                  ? `No dedicated QCO directly mapped to ${selectedStandard.is_number}.`
                  : 'Select or query a standard to view its mandatory QCO status.'}
              </p>
              <p className="text-[11px] text-[#64677a]">
                Standards without QCO notifications operate under voluntary BIS certification.
              </p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'schemes' && (
        <div className="space-y-3 animate-fade-in">
          <div className="px-1">
            <h4 className="text-xs font-semibold text-[#f1f2f8] flex items-center gap-1.5">
              <FileBadge className="w-3.5 h-3.5 text-[#8c8f9f]" />
              <span>BIS Certification Schemes</span>
            </h4>
            <p className="text-[11px] text-[#64677a] mt-0.5">
              Conformity assessment schemes under BIS Regulations, 2018
            </p>
          </div>

          <div className="space-y-2.5">
            {schemes.map((s, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-[#161720] border border-[#272937] space-y-2 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-[#f1f2f8] font-mono">{s.id}</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#20222e] text-[#a4a8bc] border border-[#303344]">
                    {s.badge}
                  </span>
                </div>
                <h5 className="text-xs font-semibold text-[#f1f2f8]">{s.name}</h5>
                <p className="text-[11px] text-[#c5c8d8] leading-relaxed">{s.desc}</p>
                <div className="text-[10px] text-[#8c8f9f] pt-1 border-t border-[#222430]">
                  <span className="text-[#64677a]">Typical Products: </span>
                  {s.products}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'sti' && (
        <div className="space-y-3 animate-fade-in">
          <div className="px-1">
            <h4 className="text-xs font-semibold text-[#f1f2f8] flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5 text-[#8c8f9f]" />
              <span>Scheme of Testing & Inspection (STI)</span>
            </h4>
            <p className="text-[11px] text-[#64677a] mt-0.5">
              Manufacturer certification and factory audit roadmap
            </p>
          </div>

          <div className="space-y-2">
            {stiChecklist.map((step, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl bg-[#15161f] border border-[#242634] flex items-start gap-2.5 shadow-sm"
              >
                <span className="flex items-center justify-center w-5 h-5 rounded-md bg-[#222430] text-[#d4d7e6] font-mono text-xs font-bold shrink-0 mt-0.5 border border-[#333648]">
                  {idx + 1}
                </span>
                <div className="space-y-0.5">
                  <h5 className="text-xs font-semibold text-[#f1f2f8]">{step.title}</h5>
                  <p className="text-[11px] text-[#b4b7cb] leading-relaxed">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
