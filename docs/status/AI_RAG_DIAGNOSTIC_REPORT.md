# SIH26107 — Phase 3.5 Pre-Optimization AI/RAG Diagnostic Audit Report

## 1. Executive Summary
This document presents the formal **Pre-Optimization Diagnostic Audit** for the AI/RAG engine of **SIH26107 — AI-Powered Intelligent Assistant for Indian Standards & BIS Services**.

In accordance with Phase 3.5 mandates, this audit **observes, measures, and diagnoses** the current system behavior across 25 baseline queries without masking defects, altering thresholds, or artificially inflating confidence.

The baseline evaluation achieved an overall pass rate of **76.0% (19/25)**, identifying **two major architectural failure modes** that must be resolved in Prompt C:
1. **General/Conceptual BIS Knowledge Collapse**: General questions (*"What is BIS certification?", "What is a QCO?"*) fail completely (0% pass rate) because the pipeline equates "no specific product standard found" with "no answer available."
2. **Ambiguity Substring False Positives**: Substring matching in `vague_templates` erroneously triggers clarification on detailed queries that contain substrings like `"what bis certification do i need"`.

---

## 2. Section A: Current System Architecture

```
User Query
    ↓
Query Processing (QueryParser + IntentClassifier)
    ├── Extracts Product, Material, User Role, IS Number, Constraints
    └── Ambiguity Check (vague_templates substring match)
    ↓
[If Ambiguous] ─── (Early Exit) ───> Return Clarification Prompt (LOW Confidence)
    ↓
Hybrid Retrieval Layer
    ├── Qdrant Semantic Search (384-dim COSINE)
    ├── BM25 Keyword Search (DocumentChunks corpus)
    └── Reciprocal Rank Fusion (RRF Score Combination)
    ↓
Heuristic Reranker
    └── Score Boosts: Exact IS (+0.35), Product (+0.25), Material (+0.15), Clause (+0.30)
    ↓
Relevance Threshold Filtering (reranked_score ≥ 0.15 OR fused_score ≥ 0.035)
    ↓
Regulatory & Compliance Resolver (PostgreSQL / SQLite)
    ├── Maps Standards → Mandatory QCOs (DPIIT/Ministry orders)
    ├── Maps Standards → Certification Schemes (Scheme-I, Scheme-II CRS, FMCS)
    └── Maps Standards → Active Amendments
    ↓
Evidence Pack Constructor
    └── Bounded JSON: { standards, qcos, certification_schemes, document_excerpts, sources }
    ↓
Confidence & Citation Scorer
    ├── Confidence: HIGH (Standard + Clauses + QCO), MEDIUM (Standard OR Clauses), LOW
    └── Citations: Exact Standard, Clause, Section, Page, Portal URL
    ↓
LLM / Generator Abstraction
    ├── OpenAI / Ollama (if configured with API key)
    └── Grounded Deterministic Synthesizer (Demo / Offline fallback)
    ↓
Pydantic Schema Validation & Final JSON Response
```

---

## 3. Section B: Query Classification Audit

The current system observes 9 distinct query categories:

| Category | Description | Current Classifier Mapping | Observed Behavior |
| :--- | :--- | :--- | :--- |
| **A. General BIS Knowledge** | Conceptual questions on BIS Act, roles, definitions | `GENERAL_BIS_SERVICE` | ❌ **Collapsed to Fallback** |
| **B. Standard Discovery** | Natural language queries to find standard | `STANDARD_LOOKUP` | ✅ **100% Accurate** |
| **C. Exact Standard Lookup** | Queries specifying exact IS number | `STANDARD_LOOKUP` | ✅ **100% Accurate** |
| **D. Clause Lookup** | Queries targeting specific clause numbers | `COMPLIANCE` | ✅ **100% Accurate** |
| **E. Product Compliance** | Manufacturer questions on testing & roadmaps | `CERTIFICATION` | ⚠️ **50% (Q14 false clarification)** |
| **F. Regulatory / QCO** | Inquiries about gazette notifications & ministries | `QCO` | ⚠️ **66.7% (Q18 false clarification)** |
| **G. Consumer Queries** | Citizen safety and ISI verification | `STANDARD_LOOKUP` | ✅ **100% Accurate** |
| **H. Clarification-Required**| Underspecified queries missing context | `STANDARD_LOOKUP` | ⚠️ **50% (Q22 missed template)** |
| **I. Out-of-Scope / Fake** | Non-existent standards or unrelated topics | `STANDARD_LOOKUP` | ✅ **100% Zero-Hallucination** |

---

## 4. Section C: Retrieval & Indexing Telemetry

| Parameter | Current Configuration | Diagnostic Evaluation |
| :--- | :--- | :--- |
| **Embedding Model** | Fixed 384-dimensional dense semantic projection (`Embedder`) | Consistent cosine space; fast in-memory/local execution |
| **Vector DB** | Qdrant `1.19.0` with `Distance.COSINE` | Shared singleton client; collection `bis_standards_chunks` |
| **Chunking Strategy** | Structure-Aware Clause Hierarchy (`StructureAwareChunker`) | Preserves `IS`, `Clause`, `Section`, `Page`, `Title` |
| **Keyword Search** | `rank_bm25` (BM25Okapi) | Tokenized over standard + clause + content |
| **Fusion Metric** | Reciprocal Rank Fusion ($k=60$) | $RRF = 0.5 \times \frac{1}{60 + \text{rank}_{sem}} + 0.5 \times \frac{1}{60 + \text{rank}_{bm25}}$ |
| **Reranking** | Cross-feature heuristic (`Reranker`) | Boosts exact IS and product matches |
| **Relevance Threshold**| `reranked_score >= 0.15` OR `fused_score >= 0.035` | Filters noise cleanly for product queries |
| **Query Rewriting** | **None** (Original string passed directly to retriever) | Missing query decomposition for complex questions |

---

## 5. Section D: Deep-Dive Failure Analysis

### 1. The Conceptual / General BIS Question Failure (Q01, Q02, Q03)
**Failing Queries**:
- `Q01`: *"What is BIS certification and when is it required for a product in India?"*
- `Q02`: *"What is the difference between an Indian Standard (IS) and a BIS certification scheme?"*
- `Q03`: *"What is a Quality Control Order (QCO) and which ministry issues it?"*

**Observed Response**:
> *"No authoritative Indian Standard or Quality Control Order (QCO) was found matching 'What is BIS certification...' Please verify the product name or standard number against the official e-BIS portal."*

#### Exact Root Cause Breakdown:
1. **Forced Document Chunk Retrieval**: The system assumes **every non-ambiguous query is a specific product-standard lookup**.
2. **Missing General Regulatory Knowledge Chunks**: Ingestion indexed only product standard clauses (`IS 2347`, `IS 302`, `IS 1293`, etc.). It did not index general regulatory overview chunks (e.g. BIS Act 2016 overview, Scheme-I / Scheme-II operational guidelines, QCO Section 16 statutory framework).
3. **Equating "No Product Standard" with "No Answer"**: Line 83 of `generator.py` states:
   ```python
   if not evidence.standards and not evidence.document_excerpts:
       return StructuredResponse(
           answer="No authoritative Indian Standard or Quality Control Order (QCO) was found...",
           confidence=ConfidenceLevel.LOW,
       )
   ```
   Because no product standard was matched, the generator aborts, even though `CertificationScheme` and `Source` data exist in the database.

---

### 2. Substring Ambiguity False Positives (Q14, Q18)
**Failing Queries**:
- `Q14`: *"I manufacture stainless steel pressure cookers for domestic use. **What BIS certification do I need** and what are the proof pressure requirements?"*
- `Q18`: *"Is BIS certification mandatory for PVC insulated cables in India?"*

#### Exact Root Cause:
In `query_parser.py`, `vague_templates` performs a substring match:
```python
is_generic_query = any(vt in lower_q for vt in vague_templates)
```
Because the phrase `"what bis certification do i need"` is contained within Q14, the parser triggered `needs_clarification = True` despite the query already specifying **stainless steel pressure cookers** and **proof pressure requirements**.

---

### 3. Missing Ambiguity Pattern (Q22)
**Query**: *"How do I apply for a license?"*
- `needs_clarification` evaluated to `False` because the phrase was not in `vague_templates`. It executed retrieval, found no documents, and returned "No standard found" instead of an interactive clarification request.

---

## 6. Section E: Successful Cases
The current system excels in the following areas (100% pass rate):
- **Exact IS Lookup**: Queries like `"IS 2347:2017"` or `"What does IS 1293:2019 cover?"` immediately retrieve title, scope, committee, clauses, amendments, and QCOs.
- **Clause-Level Precision**: Queries asking for specific clause parameters (e.g. `"Clause 5.2 of IS 2347"`, `"Clause 13.2 of IS 302-2-3"`, `"Clause 10.1 of IS 1293"`) return verbatim technical specifications and exact page numbers.
- **Consumer vs Industry Tailoring**: Industry queries receive STI checklists and testing parameters; Consumer queries receive plain-language ISI verification steps and BIS CARE app instructions.
- **Zero Hallucination Guardrails**: Queries on fake standards (`IS 99999:2099`) and non-existent products (`flying hoverboards on Mars`) are cleanly rejected with `LOW` confidence and zero invented standard numbers.

---

## 7. Section F: Unsupported Cases
- **Standards Not in Seed Knowledge**: Products outside the 6 seed standards (e.g. automotive glass, helmets, gold hallmarking) correctly return "No standard found in local records."
- **Lab Accreditation Details**: Specific NABL/BIS laboratory directory searches are not yet indexed in vector storage.

---

## 8. Section G: Hallucination Risks
- **Risk Level: LOW (0.0% observed hallucination rate)**.
- Anti-hallucination guardrails in `generator.py` and strict citation extraction directly from `DocumentChunk` records prevent the LLM from fabricating standards, clauses, or QCO dates.

---

## 9. Section H: Confidence Scorer Audit

### Current Confidence Logic:
- **`HIGH`**: When `len(evidence.standards) > 0` AND `len(evidence.document_excerpts) > 0` AND (`has_qco` OR `is_exact_is_query`).
- **`MEDIUM`**: When `len(evidence.standards) > 0` OR `len(evidence.document_excerpts) > 0`.
- **`LOW`**: When no standards and no excerpts are available, or when `needs_clarification = True`.

### Finding:
The confidence mechanism is **sound and defensible**—it is grounded strictly in evidence availability and retrieval quality, never in LLM fluency.

---

## 10. Summary of Recommendations for Prompt C (Optimization Phase)

1. **Intent-Based Query Routing**:
   - Introduce an **Intent Router** that distinguishes `CONCEPTUAL_KNOWLEDGE` queries from `PRODUCT_STANDARD_LOOKUP` queries.
   - Conceptual queries must be answered from general regulatory knowledge without requiring a product-specific standard match.
2. **Expand Knowledge Base with General BIS Overviews**:
   - Ingest and index core BIS structural documents: BIS Act 2016 overview, Section 16 QCO statutory powers, Scheme-I (ISI Mark) process, Scheme-II (CRS) process, FMCS overview.
3. **Fix Ambiguity Detection Logic**:
   - Check `needs_clarification` only if **`parsed.product is None` AND `parsed.is_number is None`**. Substring templates must not override explicit product entities.
4. **Query Rewriting & Normalization**:
   - Add query decomposition/rewriting before vector retrieval to improve recall for complex multi-part queries.
