# W4 Evidence Pack

---

# 1. Cover

## Group Information

- Group Number: 2
- Members:
  - Ngô Hũu Tài
  - Mai Phước Khoa
  - Nguyễn Tiến Hoàng Thịnh
  - Đặng Thị Ngọc Thảo
  - Nguyễn Phú Triệu
  - Nguyễn Hưng Thịnh
  - Huỳnh Bá Huân
  - Nguyễn Văn Tuấn Anh
  - Lê Hoàng Việt
  - Hoàng Công Trí Dũng

- LLM:
  - Claude Sonnet via AWS Bedrock

- Framework:
  - Custom orchestration using Python + FastAPI

- Repository:
  - (paste GitHub link)

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

## System Components

### Bedrock Knowledge Base

Used for:
- semantic retrieval
- vector search
- grounding LLM responses

Documents are stored in:
- Amazon S3

Embeddings generated using:
- Amazon Titan Embeddings v2

Vector search backend:
- OpenSearch Serverless

---

### Monitoring API

Provides:
- service health
- incident history
- operational metrics

Integrated as:
- external tool layer

---

### SQLite Database

Stores:
- monthly infrastructure costs
- SLA metrics
- operational analytics

Used for:
- numerical grounding
- exact analytics queries

---

### Orchestrator

Responsibilities:
- route queries
- invoke tools
- combine retrieval results
- structure prompts

Implemented using:
- custom Python orchestration

---

### Memory Layer

Maintains:
- multi-turn context
- conversation history
- pronoun resolution

Implemented using:
- bounded window memory

---

# 3. Data Flow

1. User submits question
2. FastAPI or CLI receives query
3. Query enters orchestrator
4. Orchestrator performs:
   - Bedrock KB retrieval
   - tool routing
   - SQL execution
   - monitoring API calls
5. Results combined into grounded prompt
6. Claude Sonnet generates answer
7. Memory updated
8. Session logged

---

# 4. Decision Log

## Decision 1 — Bedrock KB instead of fully custom RAG

We selected Bedrock Knowledge Base because:
- it simplified infrastructure management
- integrated directly with OpenSearch
- accelerated development

Learned:
- managed retrieval systems significantly reduce operational complexity.

---

## Decision 2 — SQLite instead of PostgreSQL

SQLite was selected because:
- setup was lightweight
- local debugging was simpler
- assignment scale did not require distributed databases

Learned:
- SQLite is sufficient for lightweight analytics workloads.

---

## Decision 3 — Custom Orchestrator instead of LangChain

We implemented our own orchestration layer because:
- it improved observability
- easier debugging
- full visibility into retrieval and tool execution

Learned:
- custom orchestration improves understanding of AI system internals.

---

## Decision 4 — Window Memory Strategy

We implemented bounded memory instead of full persistent memory because:
- it reduced prompt growth
- improved predictability
- simplified context management

Learned:
- window memory is effective for short multi-turn conversations.

---

# 5. Level-by-Level Evidence

---

# L1 — Retrieval

## Goal

Answer grounded factual questions using Bedrock KB retrieval.

---

## Example Question

```txt
Who is Team Platform lead?
```

---

## Result

```txt
Alex Chen
```

---

## Evidence

System successfully:
- retrieved relevant document
- grounded response
- cited source

Retrieved source:
- `team_platform.md`

---

## Retrieval Logs

```txt
[RETRIEVAL] USER QUERY
Who is Team Platform lead?

[RETRIEVAL] RETRIEVED DOCUMENTS
- team_platform.md
```

---

## Screenshot

(paste screenshot here)

---

# L2 — Multi-Source Retrieval

## Goal

Combine information across multiple documents and resolve conflicts.

---

## Example Question

```txt
Why did PaymentGW reliability drop?
```

---

## Result

System combined:
- incident postmortems
- quarterly reviews
- architecture reviews
- optimization documents

The system identified:
- database connection exhaustion
- circuit breaker failures
- operational overload

---

## Conflict Resolution Example

```txt
What is PaymentGW API rate limit?
```

---

## Result

System identified:
- archived v1 limit = 500 req/min
- current v2 limit = 1000 req/min

System correctly preferred:
- current v2 configuration

---

## Evidence

Retrieved documents:
- `paymentgw_api_v1.md`
- `paymentgw_api_v2.md`

---

## Screenshot

(paste screenshot here)

---

# L3 — Retrieval + Tools

## Goal

Use tools for operational reasoning and exact numerical grounding.

---

## Example Question

```txt
Why did PaymentGW reliability drop and how much infrastructure cost did it incur in Q1 2026?
```

---

## Result

System:
- retrieved KB documents
- queried incident history
- executed SQL analytics query
- combined all results into grounded answer

Exact grounded result:
- Q1 infrastructure cost = $16,500

---

## Tool Logs

```txt
[TOOL] INCIDENT HISTORY

[TOOL] DATABASE QUERY

SELECT SUM(total_cost)
FROM monthly_costs
...
```

---

## Evidence

Tools used:
- Monitoring API
- SQLite analytics tool

---

## Screenshot

(paste screenshot here)

---

# L4 — Multi-Turn Memory

## Goal

Maintain conversational context across multiple turns.

---

## Example Conversation

### Turn 1

```txt
Which service had highest infrastructure cost?
```

### Turn 2

```txt
Why did its costs spike?
```

### Turn 3

```txt
Which team owns it?
```

---

## Result

System correctly resolved:
- "its"
- "it"

The assistant maintained context across turns.

---

## Evidence

Memory implementation:
- bounded window memory
- conversation history tracking

---

## Screenshot

(paste screenshot here)

---

# 6. Observability & Logging

Implemented observability features:

- retrieval tracing
- tool invocation logs
- database query logs
- session logging

Example:

```txt
[RETRIEVAL] RETRIEVED DOCUMENTS
[TOOL] DATABASE QUERY
[TOOL] INCIDENT HISTORY
```

Session logs stored in:

```txt
logs/session.log
```

Purpose:
- debugging
- observability
- auditing
- evidence tracking

---

# 7. Reflection

## Hardest Component

The hardest component was:
- multi-tool orchestration

because:
- retrieval
- SQL grounding
- API integration
- memory
- prompt engineering

all had to work together reliably.

---

## Key Lessons Learned

We learned:
- retrieval quality strongly impacts reasoning quality
- observability is critical for debugging AI systems
- numerical grounding reduces hallucinations
- orchestration is more important than model size alone

---

## Future Improvements

Given more time we would add:
- persistent memory
- streaming responses
- real function calling
- frontend dashboard
- vectorized conversation memory
- authentication and RBAC

---

# 8. Final System Capabilities

The final system supports:

- semantic retrieval
- multi-source reasoning
- conflict resolution
- monitoring analysis
- SQL analytics
- numerical grounding
- conversational memory
- observability logging
- API-based access
- production-style orchestration

---
