<div align="center">

# 🏛️ ManakSetu (मानकसेतु)

### AI-Powered Assistant for Indian Standards, BIS Services & Compliance

<p>
  <b>Helping users navigate Indian Standards, certification requirements, QCOs, and compliance information through evidence-grounded AI.</b>
</p>

<br/>

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_|_TypeScript-61DAFB.svg?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/Styling-TailwindCSS-38B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant-DC2626.svg?style=for-the-badge&logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Evaluation](https://img.shields.io/badge/Evaluation-54%2F54_Passed-10B981.svg?style=for-the-badge)](docs/status/TIER_EVALUATION_REPORT.md)

<br/>

[Features](#-what-is-manaksetu) •
[Architecture](#-system-architecture) •
[Evaluation](#-evaluation) •
[Tech Stack](#️-technology-stack) •
[Setup](#-getting-started) •
[Roadmap](#-roadmap)

</div>

---

## 📌 What is ManakSetu?

**ManakSetu (मानकसेतु)** is an experimental AI-powered assistant for navigating Indian Standards, BIS services, certification requirements, Quality Control Orders (QCOs), and related compliance information.

The project started from a problem statement around making BIS information easier to access, but evolved into a personal exploration of a broader engineering question:

> **How do you build a RAG system that can answer technical and compliance-oriented questions while remaining grounded in evidence and honest about uncertainty?**

Instead of treating the problem as a simple chatbot, ManakSetu combines:

- Query understanding
- Intent and entity extraction
- Hybrid retrieval
- Semantic + keyword search
- Reciprocal Rank Fusion (RRF)
- Reranking
- Compliance resolution
- Evidence extraction
- Citation-aware generation
- Schema validation
- Automated evaluation
- Clarification handling

The goal is not simply to generate an answer.

The goal is to make the path from:

**User Question → Relevant Information → Evidence → Answer**

as explicit and reliable as possible.

---

## 🎯 The Problem

Indian Standards and BIS-related information can be difficult to navigate because the information is distributed across technical standards, clauses, certification schemes, regulatory orders, and related documentation.

A user may know what they manufacture or want to purchase without knowing:

- Which Indian Standard applies
- Whether BIS certification is mandatory
- Whether a QCO applies
- Which certification scheme is relevant
- Which requirements actually matter
- Where a particular requirement appears in the source
- Whether additional information is required before making a determination

For example:

> "I manufacture stainless-steel pressure cookers for household use. What BIS requirements do I need to consider before selling them in India?"

This isn't simply a document search problem.

The system has to understand the product, determine what information is relevant, retrieve supporting evidence, and distinguish between what is known and what remains uncertain.

That is the problem ManakSetu is designed to explore.

---

# ✨ Core Features

## 1. 🧠 Query Intelligence

ManakSetu does not immediately send every question into vector search.

The query is first analyzed for:

- Intent
- Product/entity information
- Standard references
- Compliance-related terminology
- Ambiguity
- Required clarification

This allows the system to distinguish between questions such as:

> "What is BIS certification?"

and:

> "Which BIS standard applies to my electric water heater?"

These questions require different retrieval and reasoning paths.

---

## 2. 🔍 Hybrid Retrieval

The retrieval layer combines two complementary approaches:

### Semantic Retrieval

Uses dense embeddings and Qdrant to find conceptually relevant content.

### Keyword Retrieval

Uses BM25 to preserve exact matches for:

- Standard numbers
- Clause references
- Product terminology
- Technical terms
- Material names

The two result sets are combined using **Reciprocal Rank Fusion (RRF)**.

A heuristic reranking stage then considers additional signals such as exact standard references, product terms, materials, and clause identifiers.

Conceptually:

```text
                 User Query
                     │
                     ▼
             Query Understanding
                     │
              ┌──────┴──────┐
              ▼             ▼
        Semantic Search   BM25 Search
              │             │
              └──────┬──────┘
                     ▼
                 RRF Fusion
                     │
                     ▼
                 Reranking
                     │
                     ▼
              Relevant Evidence
