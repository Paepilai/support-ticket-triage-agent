# System Architecture & Technical Report

## 1. Architecture Decisions & Design Rationale

The **Support Ticket Triage Agent** is engineered with a clean, decoupled architecture prioritizing modularity, reliability, and type safety:

- **Strict Type Safety with Pydantic V2**: Rather than parsing unstructured text or unstable markdown JSON blocks, the system leverages OpenAI's native Structured Outputs (`beta.chat.completions.parse`). This enforces strict Pydantic schemas for `TriageDecision`, preventing runtime validation exceptions and ensuring reliable downstream execution.
- **Autonomous Tool Execution Loop**: The agent dynamically fetches external context using a 3-tool suite (`check_customer_history`, `lookup_knowledge_base`, and `check_system_status`). Tool execution is managed via a bounded iteration loop (`max_iterations=5`) with `temperature=0.0` to prevent infinite recursion and ensure deterministic execution.
- **Separation of Concerns**: Business logic, database abstractions, tool definitions, prompt guardrails, and runner interfaces reside in distinct files (`models.py`, `tools.py`, `prompts.py`, `agent.py`), making the codebase scalable and easily testable.

---

## 2. Failure Modes & Mitigation Strategies

| Potential Failure Mode                   | Root Cause                                                                             | Technical Mitigation                                                                                                                                                    |
| :--------------------------------------- | :------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Infinite Tool Loop / Recurrent Calls** | Model gets stuck repeatedly calling the same lookup function when results are partial. | Bounded iteration counter (`max_iterations=5`). If threshold is exceeded, default to `NextAction.ESCALATE_TO_HUMAN` with a diagnostic log.                              |
| **Urgency Misclassification**            | Subtle or indirect customer anger/frustration missed by standard zero-shot prompts.    | Prompt rules enforce priority elevation to `CRITICAL` or `HIGH` whenever financial chargebacks, system errors (500), or short client deadlines (<2 hours) are detected. |
| **Hallucinated SLA / Company Policies**  | Model generates inaccurate refund or resolution timelines.                             | System prompt explicitly restricts SLA claims to data returned directly by `check_customer_history` and `lookup_knowledge_base`.                                        |

---

## 3. Extensibility & Scalability for Future Tickets

The architecture is built for long-term extensibility without requiring core rewrites:

1. **Schema Extensibility (Enum-based Typing)**: Adding new issue types (e.g., `ACCOUNT_SECURITY`, `PDPA_PRIVACY`), new routing teams, or new urgency levels requires updating only the Pydantic Enums in `models.py`.
2. **Pluggable Tool Registry**: New tools (e.g., `trigger_password_reset`, `vector_search_db`, `query_billing_api`) are added simply by defining the function and appending it to `TOOLS_SCHEMA` and `TOOL_MAPPING` in `tools.py`. The agent auto-discovers registered tools without modifying `agent.py`.
3. **Production Vector RAG Ready**: The current mock database lookup can be seamlessly replaced with a vector database (e.g., Pinecone, Qdrant, or PostgreSQL `pgvector`) for scaling to tens of thousands of knowledge base articles.

---

## 4. Production Evaluation & Observability Framework

To ensure production reliability without guesswork, the agent is evaluated across three complementary layers:

1. **Offline Evaluation (Golden Benchmark Dataset)**:
   - A regression suite of 200+ annotated tickets covering edge cases (Thai/English code-switching, enterprise outages, billing disputes).
   - Metric targets: **>95% Precision/Recall** on `CRITICAL` urgency classifications and **100% Schema Validity**.

2. **Online LLM-as-a-Judge Validation**:
   - A secondary evaluation LLM scores draft customer replies against four key criteria: _Grounding_, _Tone_, _Safety_, and _Actionability_ (1–5 scale) prior to automated dispatch.

3. **Production Telemetry & Operational Metrics**:
   - **First Response Time (FRT)**: Monitored via API latency metrics (Target: < 3 seconds end-to-end).
   - **Human Override Rate**: Tracks percentage of tickets re-classified by human agents in support tools (e.g., Zendesk), feeding continuous fine-tuning data back into the pipeline.
