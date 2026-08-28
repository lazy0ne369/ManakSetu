# SIH26107 — Baseline Evaluation Scorecard

**Evaluation Date**: 2026-08-28  
**Phase**: Pre-Optimization AI/RAG Diagnostic Audit (Phase 3.5)  
**Evaluator**: Automated Baseline Harness (`tests/evaluation/run_diagnostic_audit.py`)  
**Target Backend**: `http://127.0.0.1:8000` (FastAPI + Qdrant 384-dim COSINE + SQLite/PostgreSQL)

---

## 1. Overall System Scorecard

| Metric | Target | Baseline (Observed) | Status | Assessment |
| :--- | :---: | :---: | :---: | :--- |
| **Total Test Queries** | 25 | **25** | ✅ Done | Spans all 9 query categories |
| **Overall Pass Rate** | > 90% | **76.0% (19/25)** | ⚠️ Deficient | Fails on general BIS concepts & substring ambiguity |
| **Standard Discovery Accuracy** | > 90% | **100.0% (4/4)** | ✅ Optimal | Resolves IS 2347, IS 694, IS 302, IS 1293 |
| **Exact Standard Lookup Accuracy**| 100% | **100.0% (3/3)** | ✅ Optimal | Direct IS number match works reliably |
| **Clause-Level Retrieval Accuracy**| > 85% | **100.0% (3/3)** | ✅ Optimal | Retains verbatim clause text & page |
| **Product Compliance Accuracy** | > 85% | **50.0% (1/2)** | ⚠️ Deficient | Q14 false-triggered clarification due to substring check |
| **Regulatory / QCO Accuracy** | > 85% | **66.7% (2/3)** | ⚠️ Deficient | Q18 false-triggered clarification |
| **Consumer Query Accuracy** | > 85% | **100.0% (2/2)** | ✅ Optimal | Generates non-jargon ISI verification steps |
| **Ambiguity / Clarification Detection**| > 85% | **50.0% (1/2)** | ⚠️ Deficient | Q22 returned "No standard found" instead of clarification |
| **General BIS Knowledge Resolution** | > 90% | **0.0% (0/3)** | ❌ Critical Failure | All conceptual queries collapse to "No standard found" |
| **Hallucination Resistance** | 100% | **100.0% (3/3)** | ✅ Optimal | Zero hallucination on fake standards & out-of-scope |
| **Citation Groundedness** | 100% | **100.0%** | ✅ Optimal | Citations strictly generated from retrieved clauses |
| **Average Response Latency** | < 500ms | **156.4 ms** | ✅ Optimal | Ultra-fast local execution |

---

## 2. Category-by-Category Results Breakdown

| Category | Queries Tested | Passed | Failed | Pass Rate | Observed Primary Failure |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **General BIS Knowledge** | 3 | 0 | 3 | **0.0%** | Subsystem forces product lookup; treats 0 standards as total failure |
| **Standard Discovery** | 4 | 4 | 0 | **100.0%** | None |
| **Exact Standard Lookup** | 3 | 3 | 0 | **100.0%** | None |
| **Clause / Requirement Lookup** | 3 | 3 | 0 | **100.0%** | None |
| **Product Compliance Investigation**| 2 | 1 | 1 | **50.0%** | Substring match triggered false clarification on Q14 |
| **Regulatory / QCO Query** | 3 | 2 | 1 | **66.7%** | Substring match triggered false clarification on Q18 |
| **Consumer Queries** | 2 | 2 | 0 | **100.0%** | None |
| **Clarification-Required Queries** | 2 | 1 | 1 | **50.0%** | Q22 ("How do I apply for a license?") missed template |
| **Out-of-Scope / Hallucination Tests**| 3 | 3 | 0 | **100.0%** | None (Zero hallucinated IS numbers) |
| **TOTAL** | **25** | **19** | **6** | **76.0%** | |

---

## 3. Diagnostic System States Observed

| Diagnostic State | Count | Percentage | Description |
| :--- | :---: | :---: | :--- |
| **STATE NORMAL SUCCESS** | 15 | 60.0% | Successfully retrieved standard, resolved QCO, and generated answer |
| **STATE 4 (Question does not require standard doc retrieval)** | 3 | 12.0% | **FAILED**: General BIS concept questions (Q01, Q02, Q03) collapsed to fallback |
| **STATE 5 (Requires clarification)** | 4 | 16.0% | Clarification triggered (2 true positives: Q21, 2 false positives: Q14, Q18) |
| **STATE 6 (Outside system scope / Non-existent)** | 3 | 12.0% | Out-of-scope & hallucination test queries cleanly rejected |
| **STATE 1 (No relevant doc exists in KB)** | 1 | 4.0% | Q22 fell through without clarification |
| **STATE 2 (Doc exists but retrieval failed)** | 0 | 0.0% | Retrieval succeeded whenever standard was indexed |
| **STATE 3 (Content retrieved but insufficient evidence)** | 0 | 0.0% | Handled appropriately by threshold filters |

---

## 4. Latency Telemetry

- **Minimum Latency**: `117.4 ms` (Q16 - QCO lookup)
- **Maximum Latency**: `503.9 ms` (Q01 - Cold start connection)
- **Mean Latency**: `156.4 ms`
- **Median Latency**: `136.9 ms`
- **P95 Latency**: `204.4 ms`
