import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  ChatMessage,
  UserRole,
  CitationItem,
  StandardDetail,
  StructuredResponse,
} from '../types/api';
import { sendChatMessage } from '../services/chatService';
import { getStandardById } from '../services/standardsService';
import { checkBackendHealth } from '../services/sourceService';

interface AssistantContextType {
  messages: ChatMessage[];
  userRole: UserRole;
  setUserRole: (role: UserRole) => void;
  isLoading: boolean;
  activeTab: 'standards' | 'compliance' | 'evidence';
  setActiveTab: (tab: 'standards' | 'compliance' | 'evidence') => void;
  selectedStandard: StandardDetail | null;
  selectedStandardLoading: boolean;
  activeCitation: CitationItem | null;
  isEvidenceDrawerOpen: boolean;
  backendHealthy: boolean;
  sessionId: string;
  sendMessage: (queryText: string) => Promise<void>;
  inspectStandard: (isNumberOrId: string) => Promise<void>;
  inspectCitation: (citation: CitationItem) => void;
  closeEvidenceDrawer: () => void;
  clearConversation: () => void;
}

const AssistantContext = createContext<AssistantContextType | undefined>(undefined);

export const AssistantProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [userRole, setUserRole] = useState<UserRole>('consumer');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'standards' | 'compliance' | 'evidence'>('standards');
  const [selectedStandard, setSelectedStandard] = useState<StandardDetail | null>(null);
  const [selectedStandardLoading, setSelectedStandardLoading] = useState<boolean>(false);
  const [activeCitation, setActiveCitation] = useState<CitationItem | null>(null);
  const [isEvidenceDrawerOpen, setIsEvidenceDrawerOpen] = useState<boolean>(false);
  const [backendHealthy, setBackendHealthy] = useState<boolean>(true);
  const [sessionId] = useState<string>(() => 'session-' + Math.random().toString(36).substring(2, 9));

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth()
      .then(() => setBackendHealthy(true))
      .catch(() => setBackendHealthy(false));
  }, []);

  const sendMessage = async (queryText: string) => {
    if (!queryText.trim() || isLoading) return;

    const userMsgId = 'msg-' + Date.now();
    const userMsg: ChatMessage = {
      id: userMsgId,
      sender: 'user',
      content: queryText.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      userRole,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response: StructuredResponse = await sendChatMessage({
        query: queryText.trim(),
        user_role: userRole,
        session_id: sessionId,
      });

      const assistantMsgId = 'msg-ai-' + Date.now();
      const assistantMsg: ChatMessage = {
        id: assistantMsgId,
        sender: 'assistant',
        content: response.answer,
        responsePayload: response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        userRole,
      };

      setMessages((prev) => [...prev, assistantMsg]);

      // Automatically populate first standard into context panel if present
      if (response.applicable_standards && response.applicable_standards.length > 0) {
        inspectStandard(response.applicable_standards[0].is_number);
      }
    } catch (error: any) {
      const errorMsg: ChatMessage = {
        id: 'msg-err-' + Date.now(),
        sender: 'assistant',
        content: `**Error communicating with BIS Intelligence Engine:** ${error.message || 'Unknown network error'}. Please verify that the backend server is active.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        userRole,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const inspectStandard = async (isNumberOrId: string) => {
    setSelectedStandardLoading(true);
    setActiveTab('standards');
    try {
      const detail = await getStandardById(isNumberOrId);
      setSelectedStandard(detail);
    } catch (err) {
      console.error('Failed to load standard details:', err);
    } finally {
      setSelectedStandardLoading(false);
    }
  };

  const inspectCitation = (citation: CitationItem) => {
    setActiveCitation(citation);
    setIsEvidenceDrawerOpen(true);
  };

  const closeEvidenceDrawer = () => {
    setIsEvidenceDrawerOpen(false);
    setActiveCitation(null);
  };

  const clearConversation = () => {
    setMessages([]);
    setSelectedStandard(null);
    setActiveCitation(null);
  };

  return (
    <AssistantContext.Provider
      value={{
        messages,
        userRole,
        setUserRole,
        isLoading,
        activeTab,
        setActiveTab,
        selectedStandard,
        selectedStandardLoading,
        activeCitation,
        isEvidenceDrawerOpen,
        backendHealthy,
        sessionId,
        sendMessage,
        inspectStandard,
        inspectCitation,
        closeEvidenceDrawer,
        clearConversation,
      }}
    >
      {children}
    </AssistantContext.Provider>
  );
};

export const useAssistant = (): AssistantContextType => {
  const context = useContext(AssistantContext);
  if (!context) {
    throw new Error('useAssistant must be used within an AssistantProvider');
  }
  return context;
};
