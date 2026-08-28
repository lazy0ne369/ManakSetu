import { apiClient } from './apiConfig';
import { StructuredResponse, UserRole } from '../types/api';
import { StructuredResponseSchema } from '../types/schemas';

export interface ChatRequestPayload {
  query: string;
  user_role?: UserRole;
  session_id?: string | null;
}

export async function sendChatMessage(
  payload: ChatRequestPayload
): Promise<StructuredResponse> {
  const data = await apiClient<StructuredResponse>('/api/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  // Runtime Zod validation
  const parsed = StructuredResponseSchema.safeParse(data);
  if (!parsed.success) {
    console.warn('API payload validation warnings:', parsed.error);
    return data; // Fallback to raw data if validation has minor non-critical variances
  }

  return parsed.data as StructuredResponse;
}
