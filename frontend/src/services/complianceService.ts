import { apiClient } from './apiConfig';
import { ApplicableStandardItem, QCOItem } from '../types/api';

export interface ComplianceProductResult {
  product: string;
  certification_status: string;
  applicable_standards: ApplicableStandardItem[];
  qcos: QCOItem[];
  certification_schemes: Array<{
    scheme_id: string;
    scheme_name: string;
    description?: string;
    requirements?: string;
    testing_info?: string;
  }>;
  amendments: Array<{
    is_number: string;
    amendment_number: string;
    title?: string;
    effective_date?: string;
    notes?: string;
  }>;
}

export async function getComplianceByProduct(product: string): Promise<ComplianceProductResult> {
  const encoded = encodeURIComponent(product);
  return apiClient<ComplianceProductResult>(`/api/compliance/${encoded}`);
}
