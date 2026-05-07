# W4 Evidence Pack

---

# 1. Cover

## Group Information

- Group Number:
- Members:
- LLM:
  - Claude Sonnet via AWS Bedrock
- Framework:
  - Custom orchestration using Python + FastAPI
- Repository:
  - (paste repo link)

---

# 2. Architecture Overview

## Architecture Diagram

```txt
User
 ↓
FastAPI / CLI
 ↓
Conversation Memory
 ↓
Orchestrator
 ├── Bedrock KB
 │    ↓
 │ OpenSearch Vector Store
 │
 ├── Monitoring API
 │
 ├── SQLite Database
 │
 └── Claude Sonnet (Bedrock)
      ↓
Grounded Response
```

---

## Components

### Bedrock Knowledge Base

- Semantic retrieval
- Vector search
- Knowledge grounding

### OpenSearch

- Stores embeddings
- Semantic similarity retrieval

### Monitoring API

- Current service metrics
- Incident history
- Service status

### SQLite

- Historical cost data
- SLA data
- Daily metrics

### Orchestrator

- Routes queries
- Selects tools
- Combines results

### Memory Layer

- Maintains conversation history
- Enables pronoun resolution

---

## Data Flow

1. User submits question
2. Query enters orchestrator
3. Retrieval executes against Bedrock KB
4. Tool routing determines:
   - Monitoring API usage
   - SQLite usage
5. Results combined into prompt
6. Claude generates grounded answer
7. Memory updated

---

# 3. Decision Log

## Decision 1 — Bedrock KB instead of fully custom RAG

We used Bedrock KB because it reduced infrastructure complexity and allowed rapid experimentation.

Learned:
- Managed retrieval accelerates development significantly.

---

## Decision 2 — SQLite instead of PostgreSQL

SQLite was selected for faster local development and easier debugging.

Learned:
- SQLite was sufficient for analytics queries.

---

## Decision 3 — Custom orchestrator instead of LangChain

We implemented our own orchestration layer for better visibility into retrieval and tool routing.

Learned:
- Custom orchestration improved debugging and observability.

---

# 4. Per-Level Evidence

## L1 — Retrieval

### Question

Who is Team Platform lead?

### Result

Alex Chen

### Evidence

- Retrieval logs
- Retrieved chunk from `team_platform.md`

(paste screenshot)

---

## L2 — Multi-Source Retrieval

### Question

Why did PaymentGW costs spike?

### Result

System combined:
- incident postmortems
- quarterly review
- optimization documents

### Evidence

(paste screenshot)

---

## L3 — Retrieval + Tools

### Question

What was PaymentGW total infrastructure cost in Q1 2026?

### Result

$16,500

### Evidence

- Database tool invocation
- SQL query execution logs

(paste screenshot)

---

## L4 — Memory

### Multi-turn Conversation

Turn 1:
Which service had highest infrastructure cost?

Turn 2:
Why did its costs spike?

Turn 3:
Which team owns it?

### Result

System correctly resolved:
- "its"
- "it"

### Evidence

(paste screenshot)

---

# 5. Reflection

## Hardest Level

L3 was the hardest because:
- tool orchestration
- SQL grounding
- API integration
- numerical correctness

required coordination across multiple systems.

---

## What We Would Improve

Given more time:
- implement real function calling
- add streaming responses
- improve persistent memory
- build dashboard UI
