import { apiClient } from './apiConfig';
import { SourceItem, HistoryItem } from '../types/api';

export async function getSources(): Promise<SourceItem[]> {
  return apiClient<SourceItem[]>('/api/sources/');
}

export async function getSourceById(id: string): Promise<SourceItem> {
  return apiClient<SourceItem>(`/api/sources/${id}`);
}

export async function getQueryHistory(limit: number = 30): Promise<HistoryItem[]> {
  return apiClient<HistoryItem[]>(`/api/history?limit=${limit}`);
}

export async function submitFeedback(
  queryId: string,
  rating: number,
  comments?: string
): Promise<{ status: string; feedback_id: string; rating: number }> {
  return apiClient('/api/feedback', {
    method: 'POST',
    body: JSON.stringify({
      query_id: queryId,
      rating,
      comments,
    }),
  });
}

export async function checkBackendHealth(): Promise<{ status: string; app_name?: string }> {
  return apiClient('/api/health');
}
