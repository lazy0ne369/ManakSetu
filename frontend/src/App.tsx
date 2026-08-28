import React, { useState } from 'react';
import { AssistantProvider, useAssistant } from './context/AssistantContext';
import { Header } from './components/layout/Header';
import { ChatArea } from './components/chat/ChatArea';
import { ChatInput } from './components/chat/ChatInput';
import { StandardsPanel } from './components/standards/StandardsPanel';
import { CompliancePanel } from './components/compliance/CompliancePanel';
import { EvidenceDrawer } from './components/evidence/EvidenceDrawer';
import {
  MessageSquare,
  BookOpen,
  ShieldCheck,
  PanelRightClose,
  PanelRightOpen,
} from 'lucide-react';

const MainWorkspace: React.FC = () => {
  const { activeTab, setActiveTab } = useAssistant();
  const [isRightPanelOpen, setIsRightPanelOpen] = useState<boolean>(true);
  const [mobileTab, setMobileTab] = useState<'chat' | 'context'>('chat');

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-slate-950">
      <Header />

      {/* Mobile Top Navigation Tabs */}
      <div className="lg:hidden flex items-center justify-around border-b border-slate-800 bg-slate-900/90 py-2 px-4 shrink-0">
        <button
          onClick={() => setMobileTab('chat')}
          className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-xs font-semibold ${
            mobileTab === 'chat'
              ? 'bg-bis-600 text-white shadow-md'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          <span>Assistant Chat</span>
        </button>
        <button
          onClick={() => setMobileTab('context')}
          className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-xs font-semibold ${
            mobileTab === 'context'
              ? 'bg-bis-600 text-white shadow-md'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          <span>Standards & QCO</span>
        </button>
      </div>

      {/* Main Dual-Pane Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left / Primary Chat Pane */}
        <div
          className={`flex-1 flex flex-col overflow-hidden relative ${
            mobileTab === 'context' ? 'hidden lg:flex' : 'flex'
          }`}
        >
          <ChatArea />
          <ChatInput />
        </div>

        {/* Right / Secondary Context & Inspector Pane */}
        <div
          className={`w-full lg:w-[420px] xl:w-[480px] border-l border-slate-800/80 glass-panel flex flex-col overflow-hidden transition-all duration-300 ${
            mobileTab === 'chat' ? 'hidden lg:flex' : 'flex'
          } ${isRightPanelOpen ? 'lg:flex' : 'lg:hidden'}`}
        >
          {/* Secondary Pane Header / Tab Switcher */}
          <div className="p-3 border-b border-slate-800/80 flex items-center justify-between bg-slate-900/60 shrink-0">
            <div className="flex items-center bg-slate-950/80 border border-slate-800 rounded-xl p-1">
              <button
                onClick={() => setActiveTab('standards')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === 'standards'
                    ? 'bg-bis-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Standards</span>
              </button>
              <button
                onClick={() => setActiveTab('compliance')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === 'compliance'
                    ? 'bg-bis-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Compliance & QCO</span>
              </button>
            </div>

            <button
              onClick={() => setIsRightPanelOpen(false)}
              className="hidden lg:flex p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
              title="Collapse Side Panel"
            >
              <PanelRightClose className="w-4 h-4" />
            </button>
          </div>

          {/* Secondary Pane Content */}
          <div className="flex-1 overflow-hidden">
            {activeTab === 'standards' ? <StandardsPanel /> : <CompliancePanel />}
          </div>
        </div>

        {/* Expand Panel Floating Button on Desktop when collapsed */}
        {!isRightPanelOpen && (
          <button
            onClick={() => setIsRightPanelOpen(true)}
            className="hidden lg:flex absolute right-4 top-16 p-2 rounded-xl glass-card border border-slate-700 text-slate-300 hover:text-white hover:border-bis-500 shadow-xl transition-all z-20"
            title="Expand Standards & Compliance Inspector"
          >
            <PanelRightOpen className="w-5 h-5 text-bis-400" />
          </button>
        )}
      </div>

      {/* Authoritative Evidence Modal Drawer */}
      <EvidenceDrawer />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AssistantProvider>
      <MainWorkspace />
    </AssistantProvider>
  );
};

export default App;
