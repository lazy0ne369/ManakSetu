import React, { useState, useEffect } from 'react';
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
  const { activeTab, setActiveTab, selectedStandard } = useAssistant();
  // Sidebar is closed by default as requested
  const [isRightPanelOpen, setIsRightPanelOpen] = useState<boolean>(false);
  const [mobileTab, setMobileTab] = useState<'chat' | 'context'>('chat');

  // Automatically open right panel if user explicitly inspects a standard
  useEffect(() => {
    if (selectedStandard) {
      setIsRightPanelOpen(true);
    }
  }, [selectedStandard]);

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-[#070709] text-[#e4e5eb] antialiased">
      <Header
        isRightPanelOpen={isRightPanelOpen}
        onToggleRightPanel={() => setIsRightPanelOpen(!isRightPanelOpen)}
      />

      {/* Mobile Top Navigation Tabs */}
      <div className="lg:hidden flex items-center justify-around border-b border-[#21232d] bg-[#101116] py-2 px-4 shrink-0">
        <button
          onClick={() => setMobileTab('chat')}
          className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            mobileTab === 'chat'
              ? 'bg-[#222430] text-white border border-[#343746]'
              : 'text-[#9699a8] hover:text-[#e4e5eb]'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          <span>Assistant</span>
        </button>
        <button
          onClick={() => setMobileTab('context')}
          className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-xs font-medium transition-colors ${
            mobileTab === 'context'
              ? 'bg-[#222430] text-white border border-[#343746]'
              : 'text-[#9699a8] hover:text-[#e4e5eb]'
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
          className={`flex-1 flex flex-col overflow-hidden relative bg-[#0b0c10] ${
            mobileTab === 'context' ? 'hidden lg:flex' : 'flex'
          }`}
        >
          <ChatArea />
          <ChatInput />
        </div>

        {/* Right / Secondary Context & Inspector Pane with distinct graphite tint */}
        <div
          className={`w-full lg:w-[410px] xl:w-[460px] border-l border-[#20222c] bg-[#111217] flex flex-col overflow-hidden transition-all duration-200 ${
            mobileTab === 'chat' ? 'hidden lg:flex' : 'flex'
          } ${isRightPanelOpen ? 'lg:flex' : 'lg:hidden'}`}
        >
          {/* Secondary Pane Header / Tab Switcher */}
          <div className="px-4 py-3 border-b border-[#21232d] flex items-center justify-between bg-[#15161d] shrink-0">
            <div className="flex items-center bg-[#0d0e13] border border-[#232530] rounded-lg p-1">
              <button
                onClick={() => setActiveTab('standards')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                  activeTab === 'standards'
                    ? 'bg-[#242632] text-white border border-[#373a4c] shadow-sm'
                    : 'text-[#9699a8] hover:text-[#e4e5eb]'
                }`}
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Standards</span>
              </button>
              <button
                onClick={() => setActiveTab('compliance')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                  activeTab === 'compliance'
                    ? 'bg-[#242632] text-white border border-[#373a4c] shadow-sm'
                    : 'text-[#9699a8] hover:text-[#e4e5eb]'
                }`}
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Compliance & QCO</span>
              </button>
            </div>

            <button
              onClick={() => setIsRightPanelOpen(false)}
              className="hidden lg:flex p-1.5 rounded-md hover:bg-[#20222c] text-[#9699a8] hover:text-white transition-colors border border-transparent hover:border-[#2f3240]"
              title="Close Side Panel"
            >
              <PanelRightClose className="w-4 h-4" />
            </button>
          </div>

          {/* Secondary Pane Content */}
          <div className="flex-1 overflow-hidden bg-[#111217]">
            {activeTab === 'standards' ? <StandardsPanel /> : <CompliancePanel />}
          </div>
        </div>

        {/* Expand Panel Floating Button on Desktop when collapsed */}
        {!isRightPanelOpen && (
          <button
            onClick={() => setIsRightPanelOpen(true)}
            className="hidden lg:flex absolute right-4 top-16 p-2 rounded-lg bg-[#191a22] border border-[#2b2e3c] text-[#c5c8d6] hover:text-white hover:border-[#42465a] shadow-lg transition-all z-20"
            title="Open Standards & Compliance Inspector"
          >
            <PanelRightOpen className="w-4 h-4 text-[#c5c8d6]" />
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
