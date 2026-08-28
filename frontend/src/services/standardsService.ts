import { apiClient } from './apiConfig';
import { StandardDetail } from '../types/api';

export interface StandardsSearchResult {
  total: number;
  limit: number;
  offset: number;
  items: Array<{
    id: string;
    is_number: string;
    title: string;
    year?: number | null;
    status: string;
    category?: string | null;
    industry?: string | null;
    committee?: string | null;
    source_url?: string | null;
    amendments_count: number;
  }>;
}

export async function searchStandards(
  q?: string,
  category?: string,
  industry?: string,
  status?: string,
  limit: number = 20,
  offset: number = 0
): Promise<StandardsSearchResult> {
  const params = new URLSearchParams();
  if (q) params.append('q', q);
  if (category) params.append('category', category);
  if (industry) params.append('industry', industry);
  if (status) params.append('status', status);
  params.append('limit', limit.toString());
  params.append('offset', offset.toString());

  return apiClient<StandardsSearchResult>(`/api/standards/search?${params.toString()}`);
}

export async function getStandardById(idOrIsNumber: string): Promise<StandardDetail> {
  const encoded = encodeURIComponent(idOrIsNumber);
  return apiClient<StandardDetail>(`/api/standards/${encoded}`);
}
