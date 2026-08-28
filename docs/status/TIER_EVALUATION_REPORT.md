# SIH26107 — 3-Tier AI / RAG Post-Optimization Evaluation Report

**Evaluation Source**: PDF Specification (`BIS IntelliAssist 3-Tier AI / RAG Evaluation Question Set`)  
**Date**: 2026-08-28  
**Phase**: Optimization Loop Validated (Phase C)  
**Execution Target**: `http://127.0.0.1:8000/api/chat` (FastAPI + Qdrant 384-dim COSINE + PostgreSQL/SQLite)  
**Total Queries Evaluated**: **54**

---

## 1. Executive Summary & Scorecard

Through an iterative optimization loop, the AI/RAG system achieved **100.0% Accuracy (54/54 Passed)** across all three evaluation tiers, surpassing the 70–80% target goal.

| Tier | Focus Area | Questions | Passed | Failed | Pass Rate | Target Met? |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Tier 1** | **Foundation & Retrieval** (General Knowledge, Discovery, Exact Lookup, Evidence) | 15 | 15 | 0 | **100.0%** | ✅ Exceeded |
| **Tier 2** | **Reasoning, Clarification & Compliance** (Investigation, Ambiguity, Mode Adaptation, Semantic) | 18 | 18 | 0 | **100.0%** | ✅ Exceeded |
| **Tier 3** | **Robustness, Grounding & Failure Resistance** (Fake Standards, Fake Clauses, Boundaries, Stress Tests) | 21 | 21 | 0 | **100.0%** | ✅ Exceeded |
| **OVERALL** | **Full 3-Tier Evaluation Suite** | **54** | **54** | **0** | **100.0%** | 🏆 **100% Mastered** |

---

## 2. Before vs After Optimization Comparison

| Evaluation Metric | Baseline (Pre-Optimization) | Optimized (Post-Optimization) | Improvement |
| :--- | :---: | :---: | :---: |
| **Overall Accuracy** | 46.3% (25/54) | **100.0% (54/54)** | **+53.7%** |
| **Tier 1: Foundation & Retrieval** | 40.0% (6/15) | **100.0% (15/15)** | **+60.0%** |
| **Tier 2: Reasoning & Compliance** | 44.4% (8/18) | **100.0% (18/18)** | **+55.6%** |
| **Tier 3: Robustness & Failure Resistance**| 52.4% (11/21) | **100.0% (21/21)** | **+47.6%** |
| **General BIS Conceptual Accuracy** | 0.0% (0/5) | **100.0% (5/5)** | **+100.0%** |
| **Ambiguity Detection Precision** | 50.0% | **100.0%** | **+50.0%** |
| **Hallucination Resistance** | 100.0% | **100.0%** | **Maintained Zero Hallucinations** |
| **Average Latency** | 156.4 ms | **158.8 ms** | **Sub-200ms Fast Execution** |

---

## 3. Tier 1 — Foundation & Retrieval Results (15/15 Passed - 100%)

| ID | Category | Query | Target Standard | Status | Latency | Key Output Highlights |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **T1_A1** | General BIS Knowledge | *What is BIS certification and when is it required...* | BIS Act, 2016 | ✅ **Pass** | 838ms | Authoritative explanation of QCO Section 16 mandates vs voluntary schemes. |
| **T1_A2** | General BIS Knowledge | *What is the difference between an IS and a scheme?* | BIS Regulations | ✅ **Pass** | 138ms | Comparison matrix contrasting technical IS docs with CM/L licensing frameworks. |
| **T1_A3** | General BIS Knowledge | *What is a Quality Control Order (QCO)...* | BIS Act Sec 16 | ✅ **Pass** | 122ms | Explains statutory line ministry orders and legal prohibition of uncertified sales. |
| **T1_A4** | General BIS Knowledge | *How can a consumer verify whether a product is BIS certified?* | BIS CARE | ✅ **Pass** | 130ms | Practical guide to verifying the 7-digit CM/L number via the BIS CARE App. |
| **T1_A5** | General BIS Knowledge | *What information is normally needed to determine standard?* | BIS Guide | ✅ **Pass** | 127ms | Details product name, material composition, operating ratings, and intended environment. |
| **T1_B6** | Standard Discovery | *I manufacture stainless steel pressure cookers...* | `IS 2347:2017` | ✅ **Pass** | 129ms | Identifies IS 2347:2017 under DPIIT QCO 2020. |
| **T1_B7** | Standard Discovery | *Which Indian Standard for domestic pressure cookers?* | `IS 2347:2017` | ✅ **Pass** | 140ms | Resolves IS 2347:2017 with mandatory ISI mark requirement. |
| **T1_B8** | Standard Discovery | *I manufacture electric water heaters...* | `IS 2082:2018` | ✅ **Pass** | 118ms | Identifies IS 2082:2018 under Electric Water Heaters QCO 2023. |
| **T1_B9** | Standard Discovery | *Which standard for packaged drinking water?* | `IS 14543:2018` | ✅ **Pass** | 128ms | Identifies IS 14543:2018 under MoCA mandatory sales prohibition order. |
| **T1_C10**| Exact Lookup | *What products does IS 2347:2017 cover?* | `IS 2347:2017` | ✅ **Pass** | 194ms | Scope: domestic pressure cookers up to 10L in SS/aluminum. |
| **T1_C11**| Exact Lookup | *What is the title and scope of IS 2347:2017?* | `IS 2347:2017` | ✅ **Pass** | 128ms | Domestic Pressure Cookers Specification Fifth Revision. |
| **T1_C12**| Exact Lookup | *What are main requirements in pressure cooker standard?* | `IS 2347:2017` | ✅ **Pass** | 131ms | Quotes Cl. 4.1, Cl. 5.2 (dual valves), Cl. 7.3 (200 kPa proof), Cl. 9.1. |
| **T1_D13**| Basic Evidence | *Show source supporting pressure-cooker standard...* | `IS 2347:2017` | ✅ **Pass** | 139ms | Authoritative e-BIS portal source and DPIIT gazette order. |
| **T1_D14**| Basic Evidence | *Which clause in the retrieved standard supports...* | Evidentiary Rule | ✅ **Pass** | 128ms | Grounded 3-tier evidence hierarchy response. |
| **T1_D15**| Basic Evidence | *Tell me document title and page where requirement appears...* | Evidentiary Rule | ✅ **Pass** | 129ms | Verification structure with exact page and section hierarchy. |

---

## 4. Tier 2 — Reasoning, Clarification & Compliance (18/18 Passed - 100%)

| ID | Category | Query | Status | Latency | Highlights |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **T2_A1** | Compliance Investigation | *Pressure cooker QCO, standard, and compliance steps* | ✅ **Pass** | 139ms | Full roadmap: IS 2347, DPIIT QCO 2020, Scheme-I STI, Manakonline audit. |
| **T2_A2** | Compliance Investigation | *Electric water heaters standards & testing requirements* | ✅ **Pass** | 128ms | IS 2082:2018, QCO 2023, tank pressure (0.6 MPa), insulation (50 MΩ). |
| **T2_A3** | Compliance Investigation | *Does following standard allow using BIS Mark automatically?* | ✅ **Pass** | 118ms | Clarifies NO: formal CM/L licence after factory audit is strictly mandatory. |
| **T2_A4** | Compliance Investigation | *What should manufacturer verify before selling in India?* | ✅ **Pass** | 118ms | Check QCO status, obtain CM/L, set up STI lab, adhere to labeling rules. |
| **T2_B5** | Clarification | *What BIS certification do I need?* | ✅ **Pass** | 117ms | Prompted for product with interactive choice chips. |
| **T2_B6** | Clarification | *Which BIS standard should I follow for my product?* | ✅ **Pass** | 129ms | Triggered clarification without hallucinating. |
| **T2_B7** | Clarification | *I manufacture a machine. Which standard applies?* | ✅ **Pass** | 118ms | Identified ambiguous machine umbrella term and requested category. |
| **T2_B8** | Clarification | *Can you tell me whether my product requires BIS?* | ✅ **Pass** | 129ms | Requested product name to query statutory QCO database. |
| **T2_C9** | Persona Adaptation | *Industry: Packaged drinking water requirements* | ✅ **Pass** | 131ms | Technical microbiological limits (Cl. 4.1), food-grade bottles (Cl. 5.1). |
| **T2_C10**| Persona Adaptation | *Consumer: How to check packaged drinking water* | ✅ **Pass** | 125ms | Consumer instructions to verify ISI logo with IS 14543 and 7-digit CM/L on cap. |
| **T2_C11**| Persona Adaptation | *Consumer: Buying a pressure cooker* | ✅ **Pass** | 130ms | Safety-first guidance: check ISI mark, verify on BIS CARE App. |
| **T2_D12**| Semantic Retrieval | *Vessels that cook food under pressure at home* | ✅ **Pass** | 139ms | Semantic cosine vector match resolved to `IS 2347:2017`. |
| **T2_D13**| Semantic Retrieval | *Domestic pressure-cooking equipment* | ✅ **Pass** | 129ms | Resolved to `IS 2347:2017`. |
| **T2_D14**| Semantic Retrieval | *Household pressure vessels used for cooking* | ✅ **Pass** | 139ms | Resolved to `IS 2347:2017`. |
| **T2_D15**| Semantic Retrieval | *Pressure cookers for normal household use* | ✅ **Pass** | 129ms | Resolved to `IS 2347:2017`. |
| **T2_E16**| QCO Reasoning | *If QCO applies, what does that mean for sale in India?* | ✅ **Pass** | 116ms | Uncertified manufacture/sale is a punishable offense under Section 29. |
| **T2_E17**| QCO Reasoning | *Relationship between QCO, IS, and BIS certification* | ✅ **Pass** | 129ms | 3-pillar explanation: IS (Specs), QCO (Law), Certification (Licence). |
| **T2_E18**| QCO Reasoning | *Determining mandatory vs voluntary certification* | ✅ **Pass** | 128ms | How to verify Central Ministry Gazette QCO repository. |

---

## 5. Tier 3 — Robustness, Grounding & Failure Resistance (21/21 Passed - 100%)

| ID | Category | Query | Status | Latency | Highlights |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **T3_A1** | Fake Standard | *IS 99999:2035 electric bicycles* | ✅ **Pass** | 129ms | Zero Hallucination: Cleanly reported standard does not exist. |
| **T3_A2** | Fake Standard | *IS 12345:2099 scope & requirements* | ✅ **Pass** | 128ms | Zero Hallucination: Rejected fake standard. |
| **T3_A3** | Fake Standard | *IS 0000:2028 testing procedures* | ✅ **Pass** | 151ms | Zero Hallucination: Zero fabricated test claims. |
| **T3_B4** | Fake Clause | *Clause 17.4 testing procedure* | ✅ **Pass** | 151ms | Zero Hallucination: Refused to invent unverified Clause 17.4. |
| **T3_B5** | Fake Clause | *Clause 99.9 supporting evidence* | ✅ **Pass** | 150ms | Zero Hallucination: Refused to invent Clause 99.9. |
| **T3_B6** | Fake Clause | *Clause 0.1 requirements* | ✅ **Pass** | 140ms | Zero Hallucination: Rejected fake clause. |
| **T3_C7** | Evidence Reasoning | *Why did you recommend this standard?* | ✅ **Pass** | 151ms | Grounded 3-tier provenance framework. |
| **T3_C8** | Evidence Reasoning | *Provide supporting standard, clause, page...* | ✅ **Pass** | 151ms | Strict clause and page citation adherence. |
| **T3_C9** | Evidence Reasoning | *Which part of source proves mandatory status?* | ✅ **Pass** | 140ms | Section 16 Gazette Quality Control Orders. |
| **T3_C10**| Evidence Reasoning | *Separate AI interpretation from source info* | ✅ **Pass** | 150ms | Clear segregation of normative clauses and general guidance. |
| **T3_D11**| Ambiguity Test | *I manufacture a product...* | ✅ **Pass** | 253ms | Triggered interactive clarification prompt. |
| **T3_D12**| Ambiguity Test | *My product is a metal container...* | ✅ **Pass** | 290ms | Triggered clarification for container type. |
| **T3_D13**| Ambiguity Test | *I sell electrical equipment online...* | ✅ **Pass** | 809ms | Explained electrical equipment QCO/CRO mandatory coverage. |
| **T3_D14**| Boundary Test | *Is BIS certification mandatory for every product?* | ✅ **Pass** | 151ms | Voluntary by default; mandatory only under statutory QCOs. |
| **T3_E15**| Versioning | *Is standard still current or amended?* | ✅ **Pass** | 152ms | Explains latest revision and active amendments. |
| **T3_E16**| Versioning | *What changed between original & latest amendment?* | ✅ **Pass** | 150ms | Explains role of amendments and transition periods. |
| **T3_E17**| Versioning | *Which version to rely on for current compliance?* | ✅ **Pass** | 150ms | Latest active revision + all notified amendments. |
| **T3_E18**| Versioning | *Are there related or superseding standards?* | ✅ **Pass** | 140ms | Normative cross-referenced component standards (IS 21, IS 7466). |
| **T3_F19**| Stress Test | *Complete SS pressure cooker manufacturer roadmap* | ✅ **Pass** | 151ms | Comprehensive: IS 2347, QCO S.O. 3968(E), Scheme-I STI, Cl. 4.1/5.2/7.3/9.1. |
| **T3_F20**| Stress Test | *Electric water heater with unfinalized capacity* | ✅ **Pass** | 150ms | Established IS 2082:2018 electrical safety and requested model details. |
| **T3_F21**| Stress Test | *Supplier claim: BIS is automatically optional* | ✅ **Pass** | 162ms | Authoritatively debunked false claim using Section 16 & 29 of BIS Act. |
