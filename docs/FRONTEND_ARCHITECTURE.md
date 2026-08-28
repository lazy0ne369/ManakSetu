# SIH26107 — Frontend Architecture & Backend Mapping

## 1. Overview
The **SIH26107 Frontend** is a modern, responsive, highly accessible React 18 / TypeScript single-page application built with **Vite** and styled using **Tailwind CSS**. It is architected specifically for dense regulatory and compliance workflows, featuring dual-pane layout on desktop and bottom-sheet drawers on mobile.

---

## 2. UI Component to Backend Mapping Matrix

| UI Component | Purpose | Backend Endpoint | Method | Payload / Response Schema |
| :--- | :--- | :--- | :--- | :--- |
| **`ChatInput`** / **`ChatArea`** | Main conversational assistant | `/api/chat` | `POST` | `ChatRequest` → `StructuredResponse` |
| **`StandardsPanel`** | Standards search & browse | `/api/standards/search` | `GET` | Params: `q`, `category`, `industry` → `StandardsList` |
| **`StandardCard`** (Detail view) | Clause breakdown & amendments | `/api/standards/{id}` | `GET` | Path: `id` (IS Number/UUID) → `StandardDetail` |
| **`CompliancePanel`** | QCO orders & Scheme roadmap | `/api/compliance/{product}` | `GET` | Path: `product` → `ComplianceDetail` |
| **`EvidenceDrawer`** | Source verification modal | `/api/sources/{id}` | `GET` | Path: `id` → `SourceDetail` |
| **`Sidebar`** (History) | Past conversation threads | `/api/history` | `GET` | Params: `limit`, `session_id` → `QueryLog[]` |
| **`MessageBubble`** (Feedback) | Thumbs up/down rating | `/api/feedback` | `POST` | `FeedbackRequest` → `FeedbackResponse` |
| **`Header`** (Status Badge) | Backend connectivity check | `/api/health` | `GET` | → `{ status: "healthy", ... }` |

---

## 3. Data Flow & Layout Architecture

```
                                    ┌───────────────────────┐
                                    │    Header Component   │
                                    │ (Persona Mode Switch) │
                                    └───────────┬───────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 │                                                             │
                 ▼                                                             ▼
    ┌─────────────────────────┐                                   ┌─────────────────────────┐
    │     Primary Pane        │                                   │     Secondary Pane      │
    │  (Conversational UI)    │                                   │   (Dynamic Inspector)   │
    ├─────────────────────────┤                                   ├─────────────────────────┤
    │ • MessageList Stream    │ ─── (Click Standard Card) ──────> │ • StandardsPanel        │
    │ • Markdown & Checklists │ ─── (Click QCO Badge)     ──────> │ • CompliancePanel       │
    │ • Clarification Prompts │ ─── (Click Citation)      ──────> │ • Evidence Drawer Modal │
    │ • ChatInput & Prompts   │                                   │ • Scheme STI Checklist  │
    └─────────────────────────┘                                   └─────────────────────────┘
```

---

## 4. State Management (AssistantContext)
The application state is managed via React Context (`AssistantContext`) with strict TypeScript types:
- `messages`: Active conversation messages array.
- `userRole`: `'consumer' | 'industry'` (controls prompt framing and UI complexity).
- `selectedStandard`: Indian Standard currently opened in the inspector panel.
- `activeCitation`: Citation excerpt opened in the evidence drawer.
- `isLoading`: Query generation and retrieval state.
- `activeTab`: Active tab in secondary pane (`'standards' | 'compliance' | 'evidence'`).

---

## 5. Persona Modes

### Consumer Mode
- **Goal**: Help citizens quickly check product safety and verify ISI marks.
- **UI Presentation**: Plain language explanations, prominent "Look for ISI Mark" checklist, hidden internal committee jargon, verification via BIS CARE app guide.

### Industry / Professional Mode
- **Goal**: Enable manufacturers, importers, and auditors to navigate compliance and testing.
- **UI Presentation**: Full IS clause references (e.g. proof pressure, leakage current limits), DPIIT QCO gazette notification numbers, Scheme-I vs Scheme-II requirements, Scheme of Testing & Inspection (STI) steps.

---

## 6. Runtime Schema Validation (Zod)
Every API response is parsed through Zod schemas in `src/types/schemas.ts` before reaching UI state, ensuring resilience against malformed data.
