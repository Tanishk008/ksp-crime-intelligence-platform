# Enterprise System Architecture & Technical Blueprint
## Challenge 01 — Intelligent Conversational AI for the Karnataka State Police Crime Database

**Prepared by:** Executive Enterprise Architecture Review Board (building on all prior phases — Strategic Capability Formulation, Product Vision, Product Specification Catalogue, and Cognitive Intelligence Specification)
**Status:** Enterprise architecture and technical blueprint — this document specifies how to build the platform
**Date:** June 2026

---

## 1. Executive Architecture Philosophy

Architecture must serve requirements, not precede them. This board began not with a preferred technology stack but with the complete constraint set derived from seven prior documents, and derived the architecture from those constraints. Every major decision in this blueprint follows the same structure: the engineering problem, alternatives considered, trade-offs evaluated, and the recommendation with its justification.

Three principles governed every architecture decision and are restated here as a standing check against future drift.

**Data sovereignty before performance.** <cite index="9-1">MeitY's empanelment framework requires all government cloud data to reside in India, with annual STQC audits against ISO 27001/27017/27018</cite>. For sensitive criminal-justice data, this is not just a compliance requirement — it is an absolute boundary. Every architecture option that required data to leave India's borders was eliminated before any performance comparison.

**Governance substrate is structural, not a layer.** The Cognitive Intelligence Specification (Phase 7) confirmed what the Strategic Capability Formulation Report first established: the governance substrate (confidence annotation, audit logging, access control, boundary enforcement) must be a passthrough that every capability's output traverses, not a module added afterward. This shapes the entire service interaction pattern described in Section 7.

**The platform is a reasoning layer over CCTNS, not a replacement.** The CCTNS/ICJS backbone already exists and must not be duplicated. This platform reads from CCTNS, enhances reasoning over its data, and writes back nothing to CCTNS except through formally approved integration channels. Any architecture that implied ownership of primary criminal-justice records was eliminated immediately.

---

## 2. Architectural Context & Constraints

Derived from all prior phases. These are not assumptions — they are fixed constraints that no architecture decision may override.

### 2.1 Operational context

| Constraint | Value | Source |
|---|---|---|
| Number of police stations | 1,100+ | Phase 1, Challenge 01 |
| Primary language of case narratives | Kannada (regional) and English | Phase 1, 2, 5 |
| Voice interaction required | Yes — field conditions | Phase 5, Challenge 01 |
| Data sensitivity | Highest — active criminal-justice records | Phase 1, 6 |
| Data residency | India only — MeitY/DPDPA compliance | This phase's research |
| Deployment model | Karnataka State Data Centre primary + NIC DR | SDC national pattern (per MeitY guidelines) |
| Integration upstream | CCTNS (read-only from this platform) via ICJS APIs | Phase 1, 6 |
| Connectivity profile | Variable — urban stations reliable, rural potentially intermittent | Phase 1 |
| Hard exclusions | No person-level risk scoring; no demographic-correlated inference | Phases 4, 5, 6, 7 |
| Governance substrate | Structural passthrough on every output — not optional | Phases 4, 5, 6, 7 |
| Habitual Offenders Act exposure | Karnataka-specific legal constraint on Domains 3 modules | Phase 4, 5 |

### 2.2 Scale assumptions

| Parameter | Estimate | Basis |
|---|---|---|
| Total potential users | ~15,000–25,000 | ~1,100 stations × 10–15 officers/station + specialist units |
| Peak concurrent users | ~500–2,000 | Government shift-pattern usage; not consumer-scale traffic |
| Data volume (CCTNS read replica) | Hundreds of millions of records, growing | Phase 1's ~28 crore+ national CCTNS record estimate; state share estimated |
| AI inference requests per day | Tens of thousands | Moderate — not consumer scale |
| Audit log retention | Minimum 7 years, preferably indefinite | Criminal-justice evidentiary standards |

**Key scale insight:** This is government-scale, not consumer-scale. The architecture need not be engineered for millions of concurrent users. It must be engineered for *guaranteed availability* (officers working critical investigations cannot tolerate platform downtime) and *data integrity* (audit logs must be tamper-evident).

### 2.3 Quality attributes (prioritized)

| Priority | Attribute | Architectural implication |
|---|---|---|
| 1 | Security & data sovereignty | On-premises or SDC-resident deployment; encryption at rest and in transit; strict RBAC |
| 2 | Auditability & tamper-evidence | Append-only event store; cryptographic log integrity; audit access independent of the application itself |
| 3 | Availability | Active-passive HA at minimum; RTO < 4 hours; RPO < 1 hour |
| 4 | Correctness & traceability | Every factual claim carries a source; confidence is computed, not asserted |
| 5 | Bilingual accuracy parity | Kannada NLP performance must be independently evaluated, not assumed from benchmark data |
| 6 | Explainability | Reasoning traces must be reconstructable from stored intermediate states |
| 7 | Performance / latency | Conversational responses within 3–5 seconds for typical queries; complex multi-stage reasoning may be asynchronous |
| 8 | Scalability | Must scale to 3× current user base without rearchitecting |
| 9 | Maintainability | Government deployment — the team maintaining this in year 5 may not have built year 1 |
| 10 | Extensibility | Must absorb new ICJS pillars and new capabilities without architectural surgery |

---

## 3. Functional & Non-Functional Requirements Summary

Derived from all prior phases and not repeated in full (per the brief's own instruction). The architecturally significant ones that drive major structural decisions:

**Functional:**
- Natural-language query understanding in English and Kannada, text and voice
- 20-stage reasoning pipeline (Phase 7, Section 3) — must be orchestratable, inspectable, and stoppable at any stage
- Nine distinct memory types (Phase 7, Section 5) with different lifespans, access scopes, and isolation requirements
- Multi-hypothesis management — the system must hold competing hypotheses simultaneously, never collapse to one prematurely
- Evidence-grounded answer composition with inline source attribution
- Network visualization, timeline visualization, spatial hotspot visualization
- PDF export — structured, source-carrying
- Hard exclusion enforcement: demographic/person-level outputs must be architecturally impossible, not just policy-blocked

**Non-Functional:**
- All data must remain within India; no data may transit or rest outside Indian territory
- Audit logs must be immutable, independently accessible to Auditors without application-layer involvement
- The governance substrate must be a structural passthrough, not a service option
- RBAC must mirror the police organizational hierarchy established in the Product Specification Catalogue
- The platform must remain operational during CCTNS connectivity degradation (graceful degradation to cached/replicated data, not complete failure)

---

## 4. Architectural Principles

Eight principles, each derived from the constraint and requirements analysis above.

1. **Data sovereignty first.** No architectural pattern that requires data to leave Indian infrastructure is acceptable regardless of performance advantage. Every AI model inference, every vector search, every log aggregation must occur on India-resident infrastructure.

2. **CCTNS is the system of record — this platform never is.** The platform holds derived, replicated, and enriched data. It never directly modifies source records. All CCTNS interactions are read-only from this platform's perspective.

3. **Governance substrate is a mandatory passthrough, implemented as infrastructure, not code.** The confidence annotation, audit logging, and access control functions are implemented at the infrastructure/platform level — meaning they apply to all traffic by construction, not because each service remembered to call them.

4. **Event sourcing for all investigative state changes.** Every hypothesis update, every confidence revision, every investigator override is an immutable event, not a state overwrite. This is the only architecture that satisfies simultaneous requirements for auditability, reasoning-trace reconstruction, and belief-revision visibility (Phase 7, Section 4.10).

5. **Asynchronous orchestration for multi-stage reasoning; synchronous retrieval for simple lookups.** The 20-stage reasoning pipeline cannot always complete in one round-trip. The architecture must support both patterns gracefully.

6. **Fail operational, not fail closed.** When the AI reasoning layer is degraded, basic record retrieval should remain available. Investigators must not be blocked from core search functions because an AI inference service is temporarily unavailable.

7. **Modular services with shared platform capabilities.** The four Domains (Conversational Intelligence, Investigative Reasoning, Aggregate Pattern & Context, Governance) map to service groupings. Shared capabilities (confidence scoring, entity resolution, audit logging) are platform services consumed by all, not reimplemented per domain.

8. **Design for the team that maintains this in year 5.** Avoid clever or exotic patterns where a well-understood alternative exists. Prioritize operational simplicity, clear service boundaries, and comprehensive observability over architectural elegance.

---

## 5. Enterprise Architecture Overview

### 5.1 Logical architecture — the seven-layer stack

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 7 — CLIENT LAYER                                         │
│  Web Application · Mobile Application · Voice Client           │
│  (Progressive Web App + REST/WebSocket; voice via browser/app)  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS / WSS
┌────────────────────────────▼────────────────────────────────────┐
│  LAYER 6 — API GATEWAY & EDGE                                   │
│  Authentication · Rate Limiting · TLS Termination               │
│  Request Routing · API Versioning                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  LAYER 5 — GOVERNANCE SUBSTRATE (HORIZONTAL PASSTHROUGH)        │
│  Every request/response must pass through this layer            │
│  RBAC Enforcement · Boundary-Violation Detection                │
│  Confidence Annotation · Audit Event Emission                   │
└──────┬──────────────┬───────────────────┬───────────────────────┘
       │              │                   │
┌──────▼──────┐ ┌─────▼────────┐ ┌───────▼──────────────────────┐
│ LAYER 4a    │ │  LAYER 4b    │ │  LAYER 4c                    │
│ DOMAIN      │ │  DOMAIN      │ │  DOMAIN SERVICES             │
│ SERVICES:   │ │  SERVICES:   │ │  Aggregate Pattern           │
│ Conversa-   │ │  Investigative│ │  & Context Intelligence      │
│ tional      │ │  Reasoning   │ │  (Domains 3.1 + 3.2)         │
│ Intelligence│ │  (Domains    │ │                              │
│ (Domain 1)  │ │  2.1+2.2+2.3)│ │                              │
└──────┬──────┘ └─────┬────────┘ └───────┬──────────────────────┘
       │              │                   │
┌──────▼──────────────▼───────────────────▼──────────────────────┐
│  LAYER 3 — AI SERVICES PLATFORM                                 │
│  LLM Inference Engine · ASR/TTS Engine                         │
│  Embedding/Similarity Engine · Entity Resolution Engine         │
│  Reasoning Pipeline Orchestrator                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  LAYER 2 — DATA PLATFORM                                        │
│  Knowledge Graph · Vector Store · Relational Store              │
│  Spatial/Temporal Store · Document Store                        │
│  Event Store (append-only) · Cache                              │
│  CCTNS Read Replica Sync                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  LAYER 1 — INFRASTRUCTURE                                       │
│  Karnataka SDC (primary) · NIC DR Node (secondary)             │
│  SWAN connectivity to police stations                           │
│  Private container orchestration platform                       │
│  Encrypted storage · HSM-backed key management                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Why this layering

The Governance Substrate (Layer 5) is drawn as a horizontal passthrough between the API Gateway and the Domain Services, not as a peer Domain Service, for exactly the reason established in the Product Specification Catalogue (Section 14.2): if governance is drawn as one optional service, it can be skipped. Drawn as a mandatory passthrough layer, it cannot be bypassed without bypassing the entire platform routing, making it structurally enforced rather than policy-enforced.

The Domain Services (Layer 4) map directly onto the Product Specification Catalogue's four Domains. They do not share databases directly — they communicate through the AI Services Platform (Layer 3) for AI-assisted operations and through well-defined platform APIs for shared capabilities, preserving the module boundaries established in the Product Specification Catalogue.

---

## 6. Information Architecture & Data Flows

### 6.1 The end-to-end investigator request lifecycle

```
[1] Investigator submits query (text/voice, EN/Kannada)
        │
        ▼
[2] Client Layer: TLS-encrypted transport; voice converted to text client-side or at edge
        │
        ▼
[3] API Gateway: authenticate; rate-limit; route to Conversational Intelligence service
        │
        ▼
[4] Governance Substrate:
        ├── RBAC check: does this user/role have access to the requested scope?
        ├── Boundary-Violation pre-check: does the query pattern match an excluded category?
        └── Request audit event emitted (immutable, pre-processing)
        │
        ▼
[5] Conversational Intelligence (Domain 1):
        ├── Intent classification: retrieval or reasoning?
        ├── Language detection: English or Kannada?
        ├── Context recovery: what case/session is active?
        └── Route to: (a) simple retrieval path [→ step 7] or (b) full reasoning pipeline [→ step 6]
        │
        ▼ (for reasoning path)
[6] Reasoning Pipeline Orchestrator (AI Services, Layer 3):
        ├── Stages 1–8 (Intent → Entity Resolution): may run partly in parallel
        ├── Stages 9–12 (Timeline, Network, Behavioral, Pattern): run in parallel where no dependencies exist
        ├── Stages 13–17 (Hypothesis Gen → Alt Explanation): sequential with interdependencies per Phase 7 Section 4.2
        └── Stage 18 (Recommendation Formulation): conditional on diagnosticity gap detected
        │
        ▼
[7] Answer Composition (Domain 1):
        ├── Assemble sourced facts into structured answer
        ├── Conflict Surfacing: flag contradictions found during pipeline
        └── Select appropriate confidence language tier
        │
        ▼
[8] Governance Substrate (second pass — every output annotated before delivery):
        ├── Confidence annotation attached
        ├── Source attribution verified complete
        ├── Boundary-Violation post-check: could this output reconstruct an excluded category?
        ├── Response audit event emitted (immutable, including full answer content)
        └── Access-scope filter: strip any fields the requesting role should not see
        │
        ▼
[9] Response delivered to investigator (API → Client Layer)
        │
        ▼
[10] Investigation Memory Update: new entities, relationships, and reasoning trace persisted
```

### 6.2 Data sensitivity classification

| Data category | Classification | Storage location | Access |
|---|---|---|---|
| Active criminal-justice case records | Restricted — highest sensitivity | Karnataka SDC only | Role-scoped via RBAC |
| CCTNS read replica | Restricted | Karnataka SDC only | Read-only; platform-internal only |
| Entity/relationship graph | Restricted | Karnataka SDC only | Role-scoped |
| Audit logs | Restricted, tamper-evident | Separate append-only store, Karnataka SDC + NIC DR copy | Auditor role + System Administrator only |
| AI model weights (hosted) | Sensitive | Karnataka SDC AI serving infrastructure | AI services layer only |
| Aggregate hotspot data | Sensitive but less restricted | Karnataka SDC | District Supervisor+ role |
| Session/conversation state | Sensitive | Encrypted, TTL-bound cache | Scoped to the active user's session |
| User preference data | Internal | Application database | Scoped to the individual user |

---

## 7. Data Architecture

### 7.1 Data stores — the right tool for each data type

**Problem with a single-database approach:** The nine memory types from Phase 7 have fundamentally different query patterns, lifespan requirements, and consistency models. A single relational database would satisfy none of them well. The architecture uses purpose-specific stores, accessed through well-defined platform APIs, not directly from Domain services.

| Store type | What it holds | Why this store type | Access pattern |
|---|---|---|---|
| Relational database (CCTNS read replica) | FIR/case diary/chargesheet structured fields | Strong schema consistency; ACID transactions; SQL query familiarity for SCRB analysts | Read-heavy; refreshed from CCTNS on a defined sync schedule |
| Document store | Case narrative text, witness statements, unstructured exhibits | Flexible schema for narratively-structured documents; full-text indexing | Read-heavy; ingest from CCTNS and digital-evidence sources |
| Knowledge graph | Entity nodes, relationship edges, aliases, network structure | The natural representation for Entity Memory and Relationship Memory — a relational database requires joins across many tables to express what a graph stores natively | Complex traversal queries; entity resolution; network analysis |
| Vector store | Semantic embeddings of case narratives, MO descriptions, behavioral features | Approximate nearest-neighbor search for similarity — the backbone of Cross-Case Pattern Matching and MO Linkage | High-throughput similarity queries; updated as new cases are indexed |
| Spatial/temporal store | Incident locations, timestamps, hotspot aggregates | Purpose-built for spatial index operations (bounding-box, radius, temporal aggregation) that relational databases handle poorly at scale | Geospatial queries; time-series aggregation |
| Event store (append-only) | Every state change in the reasoning pipeline; every investigator action; all audit events | Immutability is a design property of event sourcing, not an access-control add-on — an audit log in a mutable relational table can always be tampered with, however good the access controls | Sequential write; temporal range read; never delete |
| Cache (TTL-bounded) | Session context; frequently-accessed entity lookups; recent query results | Latency reduction for conversational continuity; conversation context must be retrievable in under 100ms | Read/write with defined TTL; scoped to session |
| Key-value store | User preferences; RBAC role assignments; system configuration | Simple, fast, highly available for non-relational state | Low-latency reads; infrequent writes |

### 7.2 Data flow — CCTNS integration

The platform does not replicate all of CCTNS — only the subsets needed for its defined capabilities. This is a deliberate scoping decision: a full replica would double the data-governance surface, while a selective replica keeps the platform focused on what it actually needs.

```
CCTNS (State) ──[read-only, authenticated API or database replication]──▶
        │
        ▼
Data Ingestion Service (see Section 12):
        ├── Schema validation
        ├── PII field classification (which fields are restricted to which roles)
        ├── Entity extraction: persons, vehicles, organizations, locations → Knowledge Graph ingest
        ├── Narrative text → Document Store + Vector embedding pipeline
        └── Structured fields → Relational read replica

Data is never written back to CCTNS from this platform.
If an SCRB Analyst needs to correct a data-quality issue, they are directed to CCTNS's own
correction workflow — this platform surfaces the discrepancy, the correction happens upstream.
```

### 7.3 Event sourcing — why and how

Every mutation to investigative state (a new hypothesis added, a confidence level revised, an investigator override, a boundary-violation flag) is written as an immutable event to the event store. The current state of any investigation can always be reconstructed by replaying its event stream. This satisfies three requirements simultaneously:
- **Auditability**: a complete, tamper-evident history of every state change
- **Reasoning-trace reconstruction**: Phase 7's requirement that intermediate reasoning states be reconstructable for audit
- **Belief-revision visibility**: Phase 7's requirement that a revision is shown as a logged event, never a silent overwrite

The event store is the single most governance-critical component in the entire architecture. It receives its own physical separation (a dedicated storage volume, separately backed up) as a result.

---

## 8. Knowledge Architecture

### 8.1 The knowledge graph — central design decisions

The knowledge graph is the runtime representation of Entity Memory and Relationship Memory from Phase 7's memory model. It is not an add-on to the platform — it is the data structure that makes cross-case entity resolution and network analysis possible at all.

**Key design decisions:**

*Node types:* Person (with normalized aliases), Organization, Location, Vehicle, Case, Exhibit, Phone Number, Financial Account, Modus Operandi. Each node type has a defined set of attributes and a set of allowed relationship types to other node types, governed by an ontology.

*Edge types:* Typed relationships (ASSOCIATE_OF, ACCUSED_IN, LINKED_TO_CASE, SHARES_PHONE, EXHIBITS_MO, etc.). Every edge carries a confidence score and a provenance — the source case(s) that caused this relationship to be asserted.

*Alias handling:* A Person node may have many name-string variants (spellings, transliterations, aliases). The node itself holds the canonical identity; aliases are stored as edges to a dedicated name-string node type. Entity resolution (Phase 7's Stage 8) works by querying this structure, not by fuzzy-matching free text every time.

*The governance boundary:* No node or edge in the knowledge graph may carry a demographic-risk annotation. The graph stores identity facts and relationships — not risk characterizations. This is a schema-level enforcement, not a query-time filter.

### 8.2 Domain ontology

The ontology defines what exists in this domain and how things relate — it is the formal specification that makes the knowledge graph's structure governed rather than ad-hoc. The ontology is maintained as a versioned, reviewed artifact, with changes requiring the same review gate as a schema migration. This directly implements Phase 7's Knowledge Memory principle: "changes here should be a reviewed event, not an automatic byproduct of routine use."

### 8.3 Knowledge Memory updates vs. Entity/Relationship Memory updates

Per Phase 7: Entity and Relationship Memory are updated continuously as new cases are processed. Knowledge Memory (MO taxonomies, crime-type categories, behavioral feature definitions) is updated only through a deliberate, reviewed process. The architecture implements this distinction by separating the write path: continuous entity/relationship updates flow through the standard data ingestion pipeline; knowledge-level updates require an explicit schema/ontology change process with approval gates.

---

## 9. AI & Machine Learning Architecture

### 9.1 The core AI services — what each does

**Large Language Model (LLM) Inference Service**

*Problem it solves:* Bilingual intent classification, context-aware answer composition, conflict surfacing in natural language, recommendation formulation.

*Architecture decision:* The LLM runs on India-resident infrastructure (Karnataka SDC AI serving infrastructure). Per Architectural Principle 1, no inference call may route to a third-party API whose underlying compute is outside India. This has a direct model selection implication: the LLM used must either have an India-resident deployment option (several major models do, via MeitY-empanelled providers) or be deployed as a self-hosted model on SDC infrastructure. **This board does not select a specific model or vendor** — that decision belongs to the implementation phase — but we constrain it to models deployable on India-resident infrastructure with the Kannada language performance verified through independent evaluation.

*Justification for independence from vendor:* Coupling the architecture to a single LLM vendor at this stage would make the platform brittle to pricing changes, vendor availability, or performance regressions. The AI services layer is designed with a vendor-abstraction interface so the underlying model can be swapped without changing Domain service code.

**ASR/TTS Service (Automatic Speech Recognition / Text-to-Speech)**

*Problem it solves:* Voice interaction — converting spoken queries to text and spoken answers back.

*Architecture decision:* Voice processing must support Kannada with sufficient accuracy for police-domain vocabulary (specialized legal/police terminology in regional language is harder than conversational Kannada). A dedicated ASR/TTS service, with a Kannada-specific fine-tuning option, is preferable to relying on the LLM's own voice capabilities, because ASR accuracy and LLM reasoning accuracy need to be independently evaluated and improved.

**Embedding/Similarity Engine**

*Problem it solves:* Converting case narrative text, MO descriptions, and behavioral features into vector representations for similarity search (Cross-Case Pattern Matching, Behavioral/MO Linkage).

*Architecture decision:* A dedicated embedding service, separate from the LLM, for two reasons. First, embedding performance and LLM reasoning performance are different optimization targets — separating them allows each to be tuned independently. Second, embeddings need to be recomputed in batch when new cases arrive (for the vector store), an operation that should not compete with live inference.

**Entity Resolution Engine**

*Problem it solves:* Alias/spelling variant normalization — the #1-ranked operational pain point across this entire research program.

*Architecture decision:* A dedicated, specialized service rather than LLM-based entity resolution, because the specific challenge (Indian name transliteration variance from Kannada/other regional scripts to Latin characters) benefits from domain-specific training that a general-purpose LLM is unlikely to have in sufficient depth. This service maintains and queries the canonical identity layer of the knowledge graph.

**Reasoning Pipeline Orchestrator**

*Problem it solves:* Coordinating the 20 stages in Phase 7's reasoning framework, managing parallel vs. sequential execution, propagating intermediate state, and implementing Phase 7's sequencing correction (Evidence Validation before Confidence Assessment).

*Architecture decision:* A purpose-built orchestration service that treats the reasoning pipeline as a directed acyclic graph of stages, where each stage declares its inputs, outputs, and dependencies. This allows the orchestrator to:
- Run independent stages in parallel (Stages 9–12)
- Enforce mandatory preconditions (Evidence Validation before Confidence Assessment, per Phase 7 Section 4.2)
- Emit intermediate stage outputs to the event store (supporting reasoning-trace reconstruction)
- Implement graceful degradation: if one stage fails, the orchestrator can return a partial answer with explicit gaps rather than failing the entire pipeline

### 9.2 AI Model Lifecycle

```
[Data Preparation]
CCTNS-derived training data → anonymized, governed preparation
        ↓
[Model Development]
Fine-tuning on Kannada police-domain vocabulary
Behavioral linkage model training on validated case-similarity data
        ↓
[Evaluation Gate]
Kannada accuracy parity evaluation (mandatory before any model update ships)
Behavioral linkage statistical validation (mandatory before Capability E is activated)
Demographic-exclusion probe set: a deliberate test suite that attempts to elicit excluded outputs
        ↓
[Staging Deployment]
Shadow mode: new model runs alongside production, outputs compared
        ↓
[Production Deployment]
Blue-green deployment with instant rollback capability
        ↓
[Production Monitoring]
Confidence calibration drift detection
Kannada accuracy continuous monitoring
Boundary-violation attempt monitoring
        ↓
[Retraining triggers]
Calibration drift beyond defined threshold
New CCTNS data distribution shift
Significant change in Kannada query volume or vocabulary
```

### 9.3 The MLOps architecture — key principles

- No model update ships without passing the Demographic-Exclusion probe set. This is a release gate, not a post-deployment audit.
- Every model version is immutable once deployed — the model artifact is hashed and stored with the audit log entry for the deployment event.
- A model rollback can be completed in under 30 minutes, returning to any prior version with its known performance characteristics.
- The Kannada accuracy evaluation is independent of the LLM vendor's own benchmarks — it uses a KSP-specific evaluation set.

---

## 10. Backend Architecture

### 10.1 Service decomposition

The Domain Services layer (Layer 4) maps to four backend service groups, each with one clearly-bounded responsibility.

**Conversational Intelligence Service (Domain 1)**
Owns the investigator-facing dialogue: intent classification, context management, answer composition, conflict surfacing, export generation, and visualization routing. It is the only service with a direct user-facing interface. It does not hold its own persistent data — it queries the AI Services Layer and the Data Platform, and delegates memory persistence to the appropriate store. This makes it stateless between requests (session state lives in the cache layer), which is essential for horizontal scaling.

**Investigative Reasoning Service (Domain 2)**
Manages cross-case resolution, network reasoning, and behavioral linkage. These are typically invoked by the Conversational Intelligence Service in response to a reasoning-type query, not directly by the user. Returns structured outputs (candidate matches, network structure, similarity scores) to the Conversational Intelligence Service for composition. All outputs are passed through the Governance Substrate before delivery.

**Aggregate Intelligence Service (Domain 3)**
Handles spatial-temporal pattern aggregation, graduated threshold monitoring, and structural correlation. Critically, this service's data access layer is architecturally isolated from individual-level data: it is the only service that the Exclusion Filter component is permanently engaged on, at the data access layer, not just the output layer.

**Governance Service (Domain 4)**
Implements the Governance Substrate layer. Every other service's outbound traffic passes through it. It runs confidence annotation, audit event emission, boundary-violation detection, and access-scope filtering as a pipeline applied to every response before it returns through the API gateway. This is not a traditional "authentication service" — it is a mandatory response envelope that every other service's output must traverse.

### 10.2 Why not microservices from day one

**Problem with full microservices at launch:** For a government deployment at this scale and with this team-size profile, fully independent microservices add significant operational complexity (service mesh, distributed tracing, inter-service authentication, independent deployment pipelines) before the platform has validated its own data model and usage patterns.

**Recommended approach:** Begin with a well-structured modular monolith organized into the four Domain service groups, with clear internal module boundaries and no direct cross-Domain database access. The internal module boundaries are designed to allow selective extraction into independent services as scale or team-size demands it — without the launch-day complexity of a fully distributed system.

**Decision boundary:** The Governance Service is the one exception — it should run as an independent service from day one, precisely because it must be independently deployable, independently monitored, and independently auditable without touching the application code of any Domain service.

### 10.3 API design

**Problem it solves:** Multiple clients (web, mobile, voice-capable devices) need consistent access to the same backend capabilities.

**Architecture decision:** RESTful APIs for standard query/response interactions; WebSocket connections for streaming conversational responses (where latency matters) and for push-based early-warning alerts. All APIs are versioned from the first release.

**Internal service communication:** Synchronous REST/gRPC for low-latency, request-scoped calls; asynchronous message queue for the reasoning pipeline's multi-stage orchestration, where stages may take time and the caller should not block.

---

## 11. Frontend & UX Architecture

**Design constraint:** The platform must feel like one conversation, not a set of tools. The frontend architecture follows the Product Vision report's "hub-and-spoke" principle: one conversational interface; visualizations emerge from within it.

### 11.1 Client architecture

**Web application:** Progressive Web App (PWA), enabling offline caching of frequently used reference data and basic functionality degradation during connectivity loss — directly addressing Phase 1's finding that some stations have intermittent connectivity. The PWA runs in a browser; no OS-specific installation is required for the web version, reducing the deployment and update burden across 1,100+ stations.

**Mobile application:** Native or hybrid mobile app for field use, primarily for voice interaction. Shares the same API layer as the web application — there is no separate "mobile backend."

**Voice integration:** ASR is invoked client-side (where device capability allows) or server-side at the edge service, before the text reaches the Conversational Intelligence Service. The response text is converted to speech either by a TTS service call or by the client's built-in synthesis. The important constraint: the text of the answer — including its source and confidence annotation — must be available in both text and spoken form. The spoken version should convey the key confidence signal, not skip it.

### 11.2 State management

The client maintains minimal state: the current session identifier (which maps to session context held server-side in the cache), the user's role (from the authentication token), and UI preferences. No investigative data is stored client-side beyond the current conversation view — this is a security constraint, not only a design preference.

### 11.3 Accessibility and connectivity resilience

The PWA service worker caches a set of reference data (the most recently active case's basic facts, recently used entity lookups) for offline read-only access during brief connectivity gaps. Write operations (new queries, responses) queue locally and sync when connectivity is restored. This is not a substitute for connectivity — it is a graceful degradation strategy specifically for the intermittent-connectivity rural-station use case Phase 1 documented.

---

## 12. Data Ingestion & Processing Architecture

```
SOURCE: CCTNS (via official API or scheduled extract — integration method defined by KSP IT)
        │
        ▼
Ingestion Service:
├── Schema validation: does this record conform to the expected CCTNS field model?
├── Change detection: has this record changed since last ingestion? (incremental ingestion)
├── PII field classification: which fields require restricted access?
├── Sensitive data handling: fields required for certain roles only are tagged at ingestion
└── Error quarantine: malformed records go to a quarantine queue, not dropped silently
        │
        ▼
Processing Pipeline (parallel tracks):
│
├── [Track A] Structured fields → Relational read replica (for SQL-style queries)
│
├── [Track B] Narrative text → Document Store
│              └──── Async embedding pipeline → Vector Store
│                    (batch; runs on a schedule, not blocking ingestion)
│
├── [Track C] Entity extraction:
│              ├── Person, vehicle, location, organization, phone entities extracted
│              ├── Entity resolution: match against existing knowledge graph nodes
│              │       (existing node? add alias. new entity? create node.)
│              └── Relationship extraction: link entities to their cases and to each other
│                   └──────▶ Knowledge Graph (incremental update)
│
└── [Track D] Spatial/temporal: incident location + time → Spatial/Temporal Store
              (aggregate update; never individual-level hotspot prediction until Domain 3 is live)
        │
        ▼
Ingestion audit event emitted: every record processed, every error quarantined, logged immutably
```

**Key principle:** Ingestion is idempotent — reprocessing the same record twice produces the same result. This is essential for the "fail operational" principle: if a processing stage fails, records can be re-ingested without producing duplicate entities or double-counting.

---

## 13. Security Architecture

### 13.1 Security principles

**Security by design, not by policy.** Every sensitivity boundary in this architecture is enforced structurally — at the data layer (schema-level exclusions for demographic fields), at the service layer (the Governance Substrate as a mandatory passthrough), and at the network layer (service mesh mutual TLS). Relying on policy alone to enforce security would reproduce the exact failure pattern — available safeguards skipped under pressure — that Phase 3's intelligence-failure research documented.

### 13.2 Authentication & authorization

**Authentication:** Every user authenticates through the API gateway before any request reaches a Domain service. The authentication mechanism should integrate with KSP's existing identity management infrastructure rather than creating a parallel identity system — reducing administrative overhead and ensuring personnel directory changes (transfers, retirements) automatically revoke access.

**Authorization (RBAC):** The RBAC model mirrors the police organizational hierarchy documented in the Product Specification Catalogue (Section 7). Role assignments are stored in the key-value store and are read by the Governance Service on every request. Role changes (transfers, promotions) must propagate to the RBAC store within a defined SLA (recommended: 4 hours maximum lag from HR system event to access change).

**Least-privilege principle:** Each service has exactly the data-store permissions it needs, not more. The Conversational Intelligence Service, for example, cannot directly query the event store (audit logs) — that access belongs to the Governance Service only.

### 13.3 Network security

```
External users (police stations over SWAN)
        │
        │ HTTPS/TLS 1.3 (minimum)
        ▼
API Gateway (TLS termination) — DMZ
        │
        │ mTLS (service-to-service mutual authentication)
        ▼
Internal service mesh — private network segment
        │
        ▼
Data platform — separate, more restricted network segment
        │
        ▼
AI model serving infrastructure — isolated segment
        (no direct external access; AI services reachable only from Domain services)
```

**Critical isolation:** The AI model serving infrastructure has no direct network path from external clients. All inference requests route through the Domain services, which have passed through the Governance Substrate first. This architectural isolation prevents a class of attacks where a malicious or manipulated query attempts to extract training data or cause model misbehavior by bypassing application-layer controls.

### 13.4 Encryption

- **In transit:** TLS 1.3 minimum on all external connections; mTLS on all internal service-to-service connections.
- **At rest:** All data stores encrypted. Encryption keys managed by a Hardware Security Module (HSM) at the Karnataka SDC — keys never leave the HSM in plaintext.
- **Audit logs:** Cryptographically signed (HMAC chain) so any tampering with the log sequence is detectable. The signing keys are held separately from the application keys.

### 13.5 Vulnerability management and secure development

- Dependency scanning in the CI/CD pipeline — no build passes if a critical vulnerability is detected in a direct dependency.
- Static application security testing (SAST) as a mandatory CI check.
- Penetration testing before each major release (Version 1, Version 2, Version 3 per the capability roadmap).
- Security incident response plan with defined escalation paths, maintained as a living document by the System Administrator team.

---

## 14. Explainability & Audit Architecture

This section specifies how the Governance Service implements its responsibilities technically. It translates the Cognitive Intelligence Specification's requirements for explainability and auditability into concrete architectural behavior.

### 14.1 Confidence annotation pipeline

Every response from every Domain service passes through the following annotation steps before being returned:

1. **Confidence tier assignment:** Based on the reasoning pipeline's Confidence Assessment stage output (Phase 7, Stage 15), the response is assigned a confidence tier using the standardized language scale.
2. **Source attribution verification:** The composition stage's source list is checked for completeness — every factual claim must map to at least one source. A response with unmapped claims is flagged and the un-sourced claims are either sourced or removed before delivery.
3. **Basis summary attachment:** The one-line basis for the confidence level is appended to the response, per Phase 7's requirement that "a confidence figure without its basis is a specification violation."

### 14.2 Audit event schema

Every audit event contains, at minimum:

| Field | Description |
|---|---|
| event_id | Globally unique, immutable identifier |
| timestamp | UTC timestamp with millisecond precision |
| user_id | Authenticated user identifier |
| user_role | Role at time of event |
| session_id | Active session |
| event_type | QUERY / RESPONSE / OVERRIDE / BOUNDARY_VIOLATION_FLAG / ACCESS_DENIED / MODEL_UPDATE / etc. |
| event_content | Full query text or full response content (for QUERY/RESPONSE types) |
| sources_cited | All source identifiers cited in this response |
| confidence_tier | Assigned confidence level |
| reasoning_trace_id | Pointer to the full reasoning trace stored separately |
| hmac_chain_value | Cryptographic integrity value linking this event to the previous event in the log |

**Why full content is stored:** An audit log that stores only metadata (query type, user, timestamp) cannot satisfy the Auditor persona's requirement to "independently verify, not just be told, that the platform stayed within its designed boundaries." Full query and response content is necessary for this independent verification.

### 14.3 Boundary-violation detection

The Governance Service maintains a probe set — a curated collection of query and response patterns associated with the hard-exclusion categories — which runs as a continuous matching step against all traffic. A match produces a BOUNDARY_VIOLATION_FLAG event, which:
- Is immediately visible to the System Administrator
- Does not suppress the response (a false-positive flag should not disrupt a legitimate investigation)
- Does trigger a human review workflow, completing within 24 hours per SLA

High-severity matches (e.g., a response that appears to include person-level risk scores) also trigger immediate response suppression before delivery, pending human review.

---

## 15. Infrastructure & Deployment Architecture

### 15.1 Physical deployment — Karnataka SDC primary

The primary deployment is on Karnataka State Data Centre infrastructure, consistent with the national pattern established by MeitY/NIC for state-level sensitive government workloads. <cite index="11-1">State Data Centres must comply with essential requirements around physical security, access mechanism, data protection and security, confidentiality, privacy issues, and business continuity plans, particularly given the sovereignty and sensitivity of the databases and applications they host.</cite>

```
Karnataka SDC (Primary)
├── Compute cluster (container orchestration)
│   ├── Application workloads (Domain services, API gateway, Governance service)
│   ├── AI serving workloads (LLM inference, ASR/TTS, embeddings) — GPU-capable nodes
│   └── Data processing workloads (ingestion, indexing)
├── Storage tier
│   ├── Relational database (primary + standby)
│   ├── Knowledge graph database
│   ├── Vector store
│   ├── Document store
│   ├── Spatial/temporal store
│   ├── Event store (append-only, separately provisioned volume)
│   └── Cache cluster
├── Network
│   ├── Connectivity to SWAN (police station network)
│   ├── Internal service mesh (mTLS)
│   └── HSM (Hardware Security Module) for key management
└── Observability stack
    ├── Metrics collection and alerting
    ├── Log aggregation (non-audit operational logs)
    └── Distributed tracing
```

### 15.2 Disaster recovery — NIC DR node

<cite index="11-1">NIC is in the process of establishing National Data Centres, and these centres will have capacity to be used as DR (Disaster Recovery) facilities for State Data Centres on a regional basis.</cite>

The DR deployment at NIC replicates: the event store (continuous, near-real-time replication — this is the highest-priority replication target given its audit significance), the relational read replica, and the knowledge graph. AI model weights and the vector store are replicated on a daily schedule — they can be rebuilt from the primary if needed, but a copy accelerates recovery. AI serving infrastructure at the DR site runs in cold-standby; warming it up is part of the disaster recovery run book.

**RTO target: 4 hours. RPO target: 1 hour for all data stores.** These are derived from the criminal-justice context — a multi-day outage during an active investigation would be operationally significant; an hour of data loss on the read replica would typically be recoverable by re-querying CCTNS.

### 15.3 High availability

**Within the SDC:** Active-passive configuration for stateful components (databases); active-active (load-balanced) for stateless application workloads (Domain services, API gateway). A node failure in the application tier should be invisible to users; a database primary failure should complete automated failover within 2 minutes.

**Connectivity resilience:** The PWA client-side caching described in Section 11 provides the graceful degradation path when the station's connection to the SDC is intermittent. This is not HA in the infrastructure sense — it is a user-experience resilience mechanism for a known, documented connectivity profile.

---

## 16. Monitoring, Logging & Observability

### 16.1 Three observability pillars, each with a distinct purpose

| Pillar | What it covers | Who consumes it |
|---|---|---|
| Metrics | Service health, latency, error rates, AI inference performance, confidence calibration drift | Platform operations team; automatic alerting |
| Traces (distributed) | End-to-end request journey across services; reasoning pipeline stage latencies; where slow requests are spending their time | Engineering and operations for performance analysis |
| Operational logs | Application events, errors, warnings — separate from audit logs (which are governance artifacts, not operational ones) | Engineering and operations |

### 16.2 AI-specific monitoring

Standard infrastructure monitoring is insufficient for an AI-serving platform. Required additional monitoring:

- **Confidence calibration drift:** Are stated confidence levels still tracking actual accuracy over time? This is checked by comparing stated confidence tiers against retrospective ground-truth outcomes on a sample basis.
- **Kannada accuracy monitoring:** Is the Kannada NLP performance maintaining the launch-day parity target?
- **Boundary-violation attempt rate:** Not to block investigations, but to detect sustained patterns that might indicate misuse or a model behavior regression.
- **Reasoning pipeline stage latency:** Which of the 20 stages is contributing most to slow responses? This is essential for identifying where to optimize without guessing.

### 16.3 Alerting and escalation

| Condition | Severity | Response |
|---|---|---|
| Any service unavailable | Critical | Automated failover attempt + PagerDuty-equivalent escalation within 5 minutes |
| Audit log chain verification failure | Critical | Immediate escalation to security team; service continues but flagged |
| Boundary-violation high-severity match | High | Response suppression + human review SLA triggered |
| Confidence calibration drift > defined threshold | High | MLOps team review; potential model update pipeline triggered |
| Kannada accuracy degradation | Medium | Investigation within 24 hours; potential hotfix if critical vocabulary affected |

---

## 17. Engineering Organization & Development Workflow

### 17.1 Team structure

Five focused engineering domains, each owning a clear scope, able to work independently within their boundaries and communicating through defined interfaces:

| Team | Owns | Needs |
|---|---|---|
| Platform & Infrastructure | Karnataka SDC deployment, container orchestration, networking, storage provisioning, CI/CD | All other teams' deployment requirements |
| AI Engineering | LLM integration, ASR/TTS, embedding service, entity resolution, reasoning orchestrator | Data platform access; MLOps pipeline |
| Data Engineering | Ingestion, knowledge graph, vector store, relational replica, spatial store, event store | CCTNS integration spec; ingestion schema |
| Backend Engineering | Domain services (Domains 1–4), API gateway, Governance Service | AI service contracts; data platform APIs |
| Frontend Engineering | Web app (PWA), mobile app, visualization components | Backend API specification |

A cross-cutting **Security & Governance Engineering** function is embedded rather than siloed — each team has a security-focused engineer responsible for applying security principles within that team's scope, with a central security lead coordinating platform-wide security posture.

### 17.2 CI/CD pipeline

```
Developer pushes code
        ↓
Automated: unit tests → integration tests → SAST scan → dependency vulnerability scan
        ↓
Gate: all tests pass + no critical vulnerabilities
        ↓
Automated: build artifact → container image → sign and push to artifact registry
        ↓
Automated: deploy to staging environment
        ↓
Automated: smoke tests + AI model regression tests (including Demographic-Exclusion probe set)
        ↓
Gate: staging tests pass
        ↓
Manual approval (for production deployments)
        ↓
Automated: blue-green production deployment
        ↓
Automated: canary health checks → full traffic switch or automatic rollback
```

### 17.3 Testing strategy

| Test type | What it covers | When it runs |
|---|---|---|
| Unit tests | Individual service functions and components | On every commit |
| Integration tests | Service-to-service interactions; database interactions | On every commit |
| End-to-end tests | Full investigator request journeys through all layers | On pull request to main branch |
| Demographic-exclusion probe set | Attempts to elicit hard-excluded outputs from every release | On every staging deployment — a release gate |
| Kannada accuracy evaluation | NLP performance on KSP-specific Kannada vocabulary | On every model update |
| Performance tests | Response latency under expected concurrent load | Before every major release |
| Security penetration test | External-facing attack surface | Before Version 1, 2, 3 releases |
| Disaster recovery drill | Recovery from SDC primary failure against RTO/RPO targets | Quarterly |

---

## 18. Incremental Build Roadmap

Mapping the capability roadmap established in Phase 4 onto concrete engineering priorities:

### Version 1 — Foundation & Core Conversation (Governance + Domain 1 + Domain 2.1)

**Must exist at Version 1 launch:**
- Karnataka SDC deployment infrastructure (container orchestration, networking, storage provisioning)
- API gateway with authentication and TLS
- Governance Service (as an independent service from day one — see Section 10.2)
- Event store with cryptographic HMAC chain (audit integrity from the first production event)
- CCTNS read integration (RBAC-scoped, read-only)
- RBAC aligned to police hierarchy
- Conversational Intelligence Service (Domain 1) with English and Kannada NLP
- Voice interface (ASR/TTS)
- Cross-case entity resolution (Domain 2.1 — the #1-ranked pain point from Phase 1)
- Basic knowledge graph (entities from initial CCTNS data load)
- PDF export

**Must NOT be in Version 1 (regardless of technical readiness):**
- Domain 3 (hotspot/structural context) — requires demonstrated Version 1 governance maturity first
- Behavioral linkage (Domain 2.3) — requires statistical validation on Karnataka case data first
- Network visualization (Domain 2.2) — requires sufficient relational data, reviewed for readiness post-V1

### Version 2 — Investigative Reasoning Depth (Domain 2 complete)

- Network reasoning and visualization (Domain 2.2) — enabled once V1 has established data maturity
- Behavioral/MO linkage (Domain 2.3) — enabled only after statistical validation release gate is satisfied
- Full 20-stage reasoning pipeline with parallel orchestration
- Enhanced knowledge graph (richer relationship types, temporal network structure)

### Version 3 — Aggregate Intelligence (Domain 3, after external review gates)

- Spatial-temporal hotspot forecasting (Domain 3.1) — place/time only
- Graduated early-warning threshold monitoring
- Structural context layer (Domain 3.2) — only after mandatory external legal/ethics review

---

## 19. Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation | Residual risk |
|---|---|---|---|---|
| Kannada NLP performance insufficient for police-domain vocabulary at launch | Medium-high | High (undermines the platform's stated language parity commitment) | Independent evaluation before launch; dedicated Kannada fine-tuning; fallback to English query restatement with clear UX signaling | Medium — fine-tuning quality is inherently uncertain before evaluation |
| AI inference latency too high for conversational use on SDC hardware | Medium | High | GPU-capable hardware provisioning confirmed before model selection; performance testing under expected load before launch | Low-medium if provisioning is confirmed early |
| CCTNS integration complexity/access delays launch | Medium | High | Treat CCTNS integration as the longest-lead-time dependency; initiate formal KSP IT integration request as early in the implementation phase as possible | Medium — government IT integration timelines are outside this team's control |
| Governance substrate bypassed under deadline pressure | Medium (Phase 3's most-documented failure pattern) | Severe | Structural enforcement (mandatory passthrough, not a service call); independent Governance Service; CI/CD gate that tests governance behavior explicitly | Medium-low with structural enforcement; cannot reach zero |
| Demographic-exclusion boundary violated by a model update | Low (with probe-set gate) | Severe (Karnataka legal/constitutional exposure) | Demographic-exclusion probe set as a non-negotiable CI/CD gate; no model update ships without passing it | Low if the gate is maintained; the risk is not the architecture, it is the discipline to maintain the gate over years |
| Event store integrity compromised | Low | Severe | HMAC chain; physically separate storage; NIC DR copy; access restricted to Governance Service only | Low |
| CCTNS data quality problems inherited by this platform | High | Medium-high | Cannot be solved architecturally; surfaces data-quality issues to SCRB Analysts (per the Product Vision report's persona success criteria) but cannot fix upstream problems | High — this is a pre-existing condition |

---

## 20. Future Expansion Strategy

The architecture is designed to absorb future growth in three dimensions without requiring a fundamental rearchitecting:

**New ICJS pillars:** The data ingestion pipeline is designed to accept new source schemas. Adding e-Courts or e-Prosecution data as an additional ingestion track requires a new ingestion connector and schema mapping, not changes to the knowledge graph schema or the Domain services.

**New capabilities (Capability H — Institutional Memory):** Domain 5 is architecturally reserved — no other service owns the namespace it would occupy — but not yet deployed. When its governance preconditions are met, it can be added as a new Domain service consuming existing platform capabilities (event store for reasoning traces, Governance Service for access control) without changing Version 1–3 services.

**Scale growth:** The stateless Domain services and the AI serving layer are horizontally scalable within the container orchestration platform. Database scaling (knowledge graph, vector store) follows each product's established scaling path. The estimated 3× user-base growth target (Section 2.2's quality attribute) is achievable through horizontal compute scaling and read replica addition, without schema changes.

---

## 21. Enterprise Architecture Summary

**What has been specified:** A seven-layer enterprise architecture on Karnataka SDC infrastructure that is production-ready, government-scale, secure by design, and AI-native. It organizes around four Domain service groups aligned exactly to the Product Specification Catalogue; deploys a Governance Service as a mandatory, independent passthrough rather than an optional feature; uses purpose-specific data stores for each of Phase 7's nine memory types; and delivers the 20-stage reasoning pipeline as an orchestrated, event-sourced, independently auditable process.

**What makes it different from a simpler approach:** The Governance Substrate as structural infrastructure (not a service call some developer might forget to make), the event store's cryptographic HMAC chain (not a relational audit table that can be overwritten), the demographic-exclusion probe set as a CI/CD release gate (not a post-deployment promise), and the deliberate sequencing of Domain 3's deployment behind demonstrated governance maturity.

**What is still to be determined in the implementation phase:** LLM vendor selection (constrained to India-resident deployment with Kannada performance verification), specific database product selection within each store-type category, and the exact CCTNS integration API mechanism (dependent on KSP IT's current CCTNS API exposure).

---

## 22. Executive Recommendations

1. **Confirm Karnataka SDC GPU capacity for AI serving as the first procurement action.** Model selection and deployment architecture depend on this capacity being confirmed; a software design that assumes hardware that turns out to be unavailable wastes the most time of any execution risk here.

2. **Initiate CCTNS integration access formally, early, and in parallel with software development.** Government API access is typically the longest-lead-time dependency in a programme like this. Start it as soon as the implementation phase begins, not when code is ready to test against it.

3. **Build and run the Demographic-Exclusion probe set before any other testing begins.** It takes less time to build a probe set than to defend a released product that violated the Karnataka Habitual Offenders Act constraint. The probe set should exist as a code artifact in the repository from sprint one.

4. **Staff the Governance Service team with engineers who understand both security and the specific regulatory risk context.** The Governance Service is not a standard authentication service — it is the architectural embodiment of every hard exclusion and governance commitment in this programme. It deserves engineering ownership proportional to its criticality.

5. **Do not attempt Domain 3 development in parallel with Version 1 development**, however tempting the schedule pressure. The governance precondition for Domain 3's release is not bureaucratic — it is the documented finding from Phase 3 that available safeguards are routinely bypassed under deadline pressure. Domain 3 is exactly the kind of capability that should not exist in a deployable state before its governance infrastructure has been proven in production.

---

## Closing Note

This blueprint emerged from constraints, not from technology preferences. Every major structural decision — the Governance Service as an independent passthrough, the event store's HMAC chain, the demographic-exclusion probe set as a release gate, the Karnataka SDC + NIC DR deployment topology, the modular-monolith-first approach — is traceable to a specific requirement established in one of the seven prior documents. Future implementation teams should treat those traceability links as active constraints, not retrospective justifications: if a technical constraint makes one of these architectural decisions look inconvenient, the right response is to escalate the constraint for review, not to quietly discard the architectural decision that was derived from it.

*This blueprint draws on MeitY's MeghRaj empanelment framework, India's Digital Personal Data Protection Act 2023 and draft rules (January 2025), and MeitY/NIC guidance on State Data Centre deployment patterns, in addition to the full chain of prior documents in this research and design programme. All data-residency and compliance positions should be verified against the current regulatory position at the time of implementation, as this landscape is actively evolving.*
