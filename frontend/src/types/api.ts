export type UserRole = 'consumer' | 'industry';

export type ConfidenceLevel = 'high' | 'medium' | 'low';

export interface ApplicableStandardItem {
  is_number: string;
  title: string;
  year?: number | null;
  status: string;
  mandatory: boolean;
  qco_number?: string | null;
  certification_scheme?: string | null;
  applicability_reason?: string | null;
  source_url?: string | null;
}

export interface QCOItem {
  qco_number: string;
  title: string;
  product_name: string;
  is_number: string;
  ministry?: string | null;
  status: string;
  enforcement_date?: string | null;
  source_url?: string | null;
}

export interface CitationItem {
  standard: string;
  clause?: string | null;
  section?: string | null;
  page?: number | null;
  source_url?: string | null;
  excerpt?: string | null;
}

export interface StructuredResponse {
  answer: string;
  applicable_standards: ApplicableStandardItem[];
  applicability_reason?: string | null;
  certification_status: string;
  certification_scheme?: string | null;
  qcos: QCOItem[];
  key_requirements: string[];
  compliance_steps: string[];
  sources: CitationItem[];
  confidence: ConfidenceLevel;
  needs_clarification: boolean;
  clarification_question?: string | null;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  responsePayload?: StructuredResponse;
  timestamp: string;
  userRole?: UserRole;
  isStreaming?: boolean;
}

export interface StandardDetail {
  id: string;
  is_number: string;
  title: string;
  year?: number | null;
  status: string;
  scope?: string | null;
  category?: string | null;
  industry?: string | null;
  committee?: string | null;
  keywords?: string | null;
  publication_date?: string | null;
  effective_date?: string | null;
  source_url?: string | null;
  is_demo: boolean;
  amendments: Array<{
    id: string;
    amendment_number: string;
    title?: string | null;
    effective_date?: string | null;
    notes?: string | null;
    source_url?: string | null;
  }>;
  qcos: Array<{
    id: string;
    qco_number: string;
    title: string;
    ministry?: string | null;
    status: string;
    enforcement_date?: string | null;
    source_url?: string | null;
  }>;
  clauses: Array<{
    section?: string | null;
    clause?: string | null;
    page?: number | null;
    content: string;
  }>;
}

export interface SourceItem {
  id: string;
  name: string;
  url: string;
  organization: string;
  source_type: string;
  description?: string | null;
  last_verified?: string | null;
}

export interface HistoryItem {
  id: string;
  session_id?: string | null;
  user_query: string;
  role_type: string;
  intent?: string | null;
  confidence: string;
  needs_clarification: boolean;
  clarification_question?: string | null;
  citations?: any[];
  execution_time_ms?: number | null;
  created_at?: string | null;
}
