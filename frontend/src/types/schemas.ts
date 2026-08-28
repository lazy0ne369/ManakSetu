import { z } from 'zod';

export const ApplicableStandardItemSchema = z.object({
  is_number: z.string(),
  title: z.string(),
  year: z.number().nullable().optional(),
  status: z.string().default('Active'),
  mandatory: z.boolean().default(false),
  qco_number: z.string().nullable().optional(),
  certification_scheme: z.string().nullable().optional(),
  applicability_reason: z.string().nullable().optional(),
  source_url: z.string().nullable().optional(),
});

export const QCOItemSchema = z.object({
  qco_number: z.string(),
  title: z.string(),
  product_name: z.string(),
  is_number: z.string(),
  ministry: z.string().nullable().optional(),
  status: z.string().default('Mandatory'),
  enforcement_date: z.string().nullable().optional(),
  source_url: z.string().nullable().optional(),
});

export const CitationItemSchema = z.object({
  standard: z.string(),
  clause: z.string().nullable().optional(),
  section: z.string().nullable().optional(),
  page: z.number().nullable().optional(),
  source_url: z.string().nullable().optional(),
  excerpt: z.string().nullable().optional(),
});

export const StructuredResponseSchema = z.object({
  answer: z.string(),
  applicable_standards: z.array(ApplicableStandardItemSchema).default([]),
  applicability_reason: z.string().nullable().optional(),
  certification_status: z.string().default('Mandatory'),
  certification_scheme: z.string().nullable().optional(),
  qcos: z.array(QCOItemSchema).default([]),
  key_requirements: z.array(z.string()).default([]),
  compliance_steps: z.array(z.string()).default([]),
  sources: z.array(CitationItemSchema).default([]),
  confidence: z.enum(['high', 'medium', 'low']).default('high'),
  needs_clarification: z.boolean().default(false),
  clarification_question: z.string().nullable().optional(),
});
