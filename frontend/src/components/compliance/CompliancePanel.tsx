import React, { useState } from 'react';
import { useAssistant } from '../../context/AssistantContext';
import {
  ShieldAlert,
  FileBadge,
  CheckCircle,
  Building,
  ExternalLink,
  HelpCircle,
  Clock,
  Layers,
} from 'lucide-react';

export const CompliancePanel: React.FC = () => {
  const { selectedStandard, userRole } = useAssistant();
  const [activeTab, setActiveTab] = useState<'qco' | 'schemes' | 'sti'>('qco');

  const qcos = selectedStandard?.qcos || [];

  const schemes = [
    {
      id: 'Scheme-I',
      name: 'Product Certification Scheme (ISI Mark)',
      desc: 'Mandatory standard mark on packaging. Requires in-house testing lab, factory audit, sample verification, and STI adherence.',
      products: 'Pressure Cookers, Electric Irons, Plugs & Sockets, PVC Cables, Toys, Steel, Cement',
      badge: 'Full Factory Inspection',
    },
    {
      id: 'Scheme-II (CRS)',
      name: 'Compulsory Registration Scheme (CRS)',
      desc: 'Self-declaration of conformity based on test reports from BIS recognized labs. No prior factory audit required.',
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
    <div className="h-full flex flex-col p-4 space-y-4 overflow-y-auto">
      {/* Sub-Navigation Tabs */}
      <div className="flex items-center bg-slate-900/90 border border-slate-800 rounded-xl p-1 shrink-0">
        <button
          onClick={() => setActiveTab('qco')}
          className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all ${
            activeTab === 'qco'
              ? 'bg-bis-600 text-white shadow-md'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Quality Control Orders
        </button>
        <button
          onClick={() => setActiveTab('schemes')}
          className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all ${
            activeTab === 'schemes'
              ? 'bg-bis-600 text-white shadow-md'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Schemes
        </button>
        <button
          onClick={() => setActiveTab('sti')}
          className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all ${
            activeTab === 'sti'
              ? 'bg-bis-600 text-white shadow-md'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          STI Checklist
        </button>
      </div>

      {activeTab === 'qco' && (
        <div className="space-y-3 animate-fade-in">
          <div className="flex items-center justify-between px-1">
            <h4 className="text-xs font-bold text-white flex items-center gap-1.5">
              <ShieldAlert className="w-4 h-4 text-rose-400" />
              <span>Mandatory QCO Orders</span>
            </h4>
            <span className="text-[10px] text-slate-400">Legal Gazette Notifications</span>
          </div>

          {qcos.length > 0 ? (
            qcos.map((q, idx) => (
              <div
                key={idx}
                className="p-4 rounded-2xl glass-card border border-rose-500/30 space-y-2.5 shadow-lg"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-rose-300">
                    {q.qco_number}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[9px] uppercase font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                    {q.status}
                  </span>
                </div>

                <h5 className="text-xs font-semibold text-white leading-relaxed">{q.title}</h5>

                <div className="space-y-1 text-[11px] text-slate-300 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/80">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Ministry:</span>
                    <span className="text-right text-slate-200">{q.ministry || 'DPIIT'}</span>
                  </div>
                  {q.enforcement_date && (
                    <div className="flex justify-between">
                      <span className="text-slate-400">Enforcement Date:</span>
                      <span className="text-amber-300 font-medium">{q.enforcement_date}</span>
                    </div>
                  )}
                </div>

                {q.source_url && (
                  <a
                    href={q.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center justify-end gap-1 text-[11px] text-bis-400 hover:text-bis-300 font-medium pt-1"
                  >
                    <span>View Gazette Notification</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            ))
          ) : (
            <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 text-center space-y-2">
              <ShieldAlert className="w-6 h-6 text-slate-500 mx-auto" />
              <p className="text-xs text-slate-300 font-medium">
                {selectedStandard
                  ? `No dedicated QCO directly mapped to ${selectedStandard.is_number}.`
                  : 'Select or query a standard to view its mandatory QCO status.'}
              </p>
              <p className="text-[11px] text-slate-500">
                Standards without QCO notifications operate under voluntary BIS certification.
              </p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'schemes' && (
        <div className="space-y-3 animate-fade-in">
          <div className="px-1">
            <h4 className="text-xs font-bold text-white flex items-center gap-1.5">
              <FileBadge className="w-4 h-4 text-bis-400" />
              <span>BIS Certification Schemes</span>
            </h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Conformity assessment schemes under BIS Regulations, 2018
            </p>
          </div>

          <div className="space-y-3">
            {schemes.map((s, idx) => (
              <div key={idx} className="p-4 rounded-2xl glass-card border border-slate-800 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-bis-300 font-mono">{s.id}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-bis-500/10 text-bis-300 border border-bis-500/30">
                    {s.badge}
                  </span>
                </div>
                <h5 className="text-xs font-semibold text-white">{s.name}</h5>
                <p className="text-[11px] text-slate-300 leading-relaxed">{s.desc}</p>
                <div className="text-[10px] text-slate-400 pt-1 border-t border-slate-800/80">
                  <span className="text-slate-500">Typical Products: </span>
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
            <h4 className="text-xs font-bold text-white flex items-center gap-1.5">
              <CheckCircle className="w-4 h-4 text-emerald-400" />
              <span>Scheme of Testing & Inspection (STI)</span>
            </h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Manufacturer certification and factory audit roadmap
            </p>
          </div>

          <div className="space-y-2">
            {stiChecklist.map((step, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 flex items-start gap-3"
              >
                <span className="flex items-center justify-center w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono text-xs font-bold shrink-0 mt-0.5">
                  {idx + 1}
                </span>
                <div className="space-y-0.5">
                  <h5 className="text-xs font-semibold text-white">{step.title}</h5>
                  <p className="text-[11px] text-slate-300 leading-relaxed">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
