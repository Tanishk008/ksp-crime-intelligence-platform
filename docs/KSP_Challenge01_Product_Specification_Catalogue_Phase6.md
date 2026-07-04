# Product Specification Catalogue
## Challenge 01 — Intelligent Conversational AI for the Karnataka State Police Crime Database

**Prepared by:** Executive Product Module & Capability Specification Board (building on the Strategic Capability Formulation Report and the Product Vision & Investigator Experience Report)
**Status:** Product specification only — no architecture, technology selection, API design, or implementation discussion in this document
**Date:** June 2026

---

### Note on scope and a necessary terminology reconciliation

This document does not reinterpret Challenge 01 or repeat prior research. It takes the seven core capabilities established in the Strategic Capability Formulation Report — **A** (Conversational Evidence Retrieval & Synthesis), **B** (Cross-Case Entity & Pattern Resolution), **C** (Network Reasoning & Visualization), **D** (Spatial-Temporal Hotspot & Early-Warning Intelligence), **E** (Evidence-Based Behavioral/MO Linkage), **F** (Structural Context Layer), **G** (Governance Substrate), plus **H** (Reasoning Externalization, a future research track) — as fixed inputs, and decomposes them into the engineering-grade taxonomy this phase requires.

**A terminology note is necessary before proceeding.** The prior report used "Capability" for these seven large, strategic units. This report's required taxonomy (Platform → Domain → Module → Submodule → **Capability** → Functional Component → User Interaction) uses "Capability" for something one level *below* Module — a small, reusable unit of work, several of which compose a module. **To avoid confusion across documents, this report refers to the prior phase's seven strategic units as "Strategic Capabilities (A–H)" throughout, reserving the unqualified term "Capability" exclusively for this document's finer-grained taxonomy level.** Every Strategic Capability maps onto one or more Domains/Modules below; none are renamed or reinterpreted.

---

## 1. Executive Summary

This catalogue resolves Strategic Capabilities A–H into **4 active Product Domains, 12 Modules, 24 Submodules, 21 reusable Capabilities, 17 Functional Components, and 18 meaningful User Interactions** — plus one Domain (Institutional Memory) deliberately left unspecified below the domain level, consistent with Strategic Capability H's status as a future research track rather than a build commitment.

Three structural decisions drove this taxonomy, each made for a specific, traceable reason rather than as a default decomposition.

**First, the governance substrate (Strategic Capability G) is modeled as its own Domain, not folded into the others, for the same reason the prior report made it a horizontal layer rather than a peer capability**: every other Domain's output must pass through it, and giving it Module-level visibility of its own — Explainability, Audit & Accountability, Access Control — makes that dependency impossible to silently skip during later engineering work.

**Second, Strategic Capabilities D and F are grouped into a single Domain** (Aggregate Pattern & Context Intelligence), not because they perform the same function, but because they share the same governance profile: both operate exclusively on aggregate, non-individual data, both carry the strictest release gates established in the prior reports, and both depend on the same reusable exclusion-enforcement Capability defined in Section 6. Decomposing them into separate Domains would have duplicated that shared governance logic for no operational benefit — precisely the kind of redundancy Board VIII exists to eliminate.

**Third, this catalogue treats "reusability" as a design constraint that visibly changed the outcome, not a section heading.** Three Capabilities — *Source-Grounded Answer Composition*, *Confidence Scoring & Calibration*, and *Entity & Alias Resolution* — are each consumed by three or more Modules. Two Functional Components — the *Similarity Engine* and the *Graph Renderer* — each implement more than one Capability. These reuse points are identified explicitly in Sections 6–7, not asserted in the abstract, because a catalogue that merely claims capability density without showing where it actually occurred is not verifiable.

---

## 2. Product Taxonomy

### 2.1 The complete hierarchy

```
PLATFORM
Karnataka State Police Crime Intelligence Platform
        │
        ▼
PRODUCT DOMAINS (4 active + 1 future)
        │
        ├── Domain 1 — Conversational Intelligence           (carries Strategic Capability A)
        ├── Domain 2 — Investigative Reasoning                (carries Strategic Capabilities B, C, E)
        ├── Domain 3 — Aggregate Pattern & Context Intelligence (carries Strategic Capabilities D, F)
        ├── Domain 4 — Trust & Governance                     (carries Strategic Capability G, HORIZONTAL)
        └── Domain 5 — Institutional Memory (FUTURE, unspecified below domain level — carries Strategic Capability H)
        │
        ▼
MODULES (12, across the 4 active domains)
        │
        ▼
SUBMODULES (24)
        │
        ▼
CAPABILITIES (21, this document's taxonomy-level meaning — see terminology note above)
        │
        ▼
FUNCTIONAL COMPONENTS (17)
        │
        ▼
USER INTERACTIONS (18)
```

### 2.2 Why this taxonomy, and not a flatter or deeper one

A flatter taxonomy (Domain → Capability directly) would have hidden the governance reasoning behind Domain 3's grouping (Section 2 above) inside a single oversized layer. A deeper taxonomy (adding a layer below User Interaction) would describe UI widgets, which the brief explicitly excludes ("interactions should represent meaningful work rather than UI widgets"). Seven layers is the minimum depth that lets every governance and reuse decision in this report remain traceable to a specific layer, and no deeper.

---

## 3. Product Domain Catalogue

### Domain 1 — Conversational Intelligence

| Attribute | Definition |
|---|---|
| Mission | Be the single point of contact between an investigator and every other Domain's intelligence |
| Purpose | Convert a natural-language question (English/Kannada, text/voice) into a sourced, confidence-qualified answer, and convert that answer into whatever exportable or visual form the investigator needs next |
| Scope | All direct investigator-facing dialogue; session and case-context management; answer composition; export and visualization hand-off |
| Operational responsibility | Owns the investigator's conversational experience end-to-end; does not itself perform cross-case matching, network analysis, or forecasting — it requests those from Domain 2/3 and composes the result |
| Supported investigator activities | Asking questions, receiving answers, requesting visualizations, exporting findings, maintaining a session across a working day or across return visits to a case |
| Domain boundaries | Does not generate intelligence findings itself — it is the presentation and dialogue layer over Domains 2 and 3, gated by Domain 4 |
| Relationship to other domains | Consumes Domain 2 and 3 outputs; every output it presents has already passed through Domain 4's governance layer; this is the only Domain with a direct conversational interface — Domains 2 and 3 have no standalone user-facing surface (per the Product Vision report's hub-and-spoke design) |

### Domain 2 — Investigative Reasoning

| Attribute | Definition |
|---|---|
| Mission | Surface case-specific connections — between records, between entities, between behaviors — that a human would otherwise need years of accumulated case memory to recognize |
| Purpose | Carry Strategic Capabilities B (cross-case/entity resolution), C (network reasoning), and E (statistical behavioral linkage) |
| Scope | Case-linked, entity-linked, and behavior-linked reasoning over already-digitized records — never aggregate/place-based reasoning (that is Domain 3's responsibility) |
| Operational responsibility | Produces candidate links, network structure, and similarity scores, each with its own confidence — never a directive conclusion |
| Supported investigator activities | Checking for cross-case resemblance, exploring a network's structure, checking a new crime's MO against known patterns |
| Domain boundaries | Does not produce demographic or person-level risk inferences (that boundary belongs to Domain 3, and is enforced identically here for E's behavioral-linkage output) |
| Relationship to other domains | Feeds Domain 1's conversational answers; shares the Entity & Alias Resolution Capability (Section 6) with Domain 3 where relevant; every output passes through Domain 4 |

### Domain 3 — Aggregate Pattern & Context Intelligence

| Attribute | Definition |
|---|---|
| Mission | Provide place-and-time forecasting and structural/environmental context — strictly at the aggregate level, never the individual level |
| Purpose | Carry Strategic Capabilities D (hotspot/early-warning) and F (structural context) |
| Scope | Spatial-temporal pattern aggregation, graduated early-warning thresholds, and aggregate structural/environmental correlation |
| Operational responsibility | The single most heavily governed Domain in this catalogue — every Module here depends on the Demographic-Exclusion Enforcement Capability (Section 6) as a hard input gate, not an optional check |
| Supported investigator activities | Viewing hotspot forecasts, receiving graduated warnings, reviewing structural context for resourcing/prevention planning |
| Domain boundaries | **Categorically excludes any individual-identifying input or output.** This is the one boundary in this entire catalogue stated as a structural design constraint rather than a policy preference |
| Relationship to other domains | Feeds Domain 1's conversational answers and visualizations; subject to the strictest version of Domain 4's governance gating; does not interact with Domain 2 — case-specific and aggregate reasoning are deliberately kept separate so that aggregate outputs can never be reverse-engineered into individual-level inferences by combination |

### Domain 4 — Trust & Governance (Horizontal)

| Attribute | Definition |
|---|---|
| Mission | Make every other Domain's output explainable, auditable, and properly access-scoped — by construction, not by convention |
| Purpose | Carry Strategic Capability G |
| Scope | Confidence/source annotation, full reasoning-trace generation, audit logging, boundary-violation detection, and role-based access control |
| Operational responsibility | The only Domain every other Domain's output must pass through before reaching a user; this is a structural property of the platform, not an optional add-on, consistent with the Strategic Capability Formulation Report's central architectural recommendation |
| Supported investigator activities | Viewing source/confidence detail, viewing a full reasoning trace, (for Auditors/Administrators) reviewing logs and configuring access |
| Domain boundaries | Performs no investigative reasoning of its own — it annotates, logs, and gates; it never originates an investigative finding |
| Relationship to other domains | Horizontal — every Domain 1, 2, and 3 output is a Domain 4 input before it reaches a user |

### Domain 5 — Institutional Memory (Future, Unspecified Below Domain Level)

| Attribute | Definition |
|---|---|
| Mission | Externalize and preserve investigative reasoning traces for training, mentorship, and continuity purposes |
| Purpose | Carry Strategic Capability H |
| Scope | **Deliberately not decomposed into Modules/Submodules/Capabilities in this catalogue.** Per the Strategic Capability Formulation Report, H is a research track, not a roadmap commitment, pending demonstrated maturity of Domain 4's governance in production and resolution of the privacy/reputational risk (durable records of rejected hypotheses about later-cleared individuals) flagged in that report's risk register |
| Operational responsibility | None assigned yet — specifying responsibilities below this level would imply a build commitment this catalogue is not authorized to make |
| Relationship to other domains | Would depend entirely on Domain 4's governance substrate if and when it is specified — this dependency is the reason its activation is gated on Domain 4's demonstrated maturity, not a parallel development track |

---

## 4. Product Module Catalogue

Twelve modules across the four active Domains. Each card states the module's single responsibility, primary/secondary users, business value, and boundaries; submodules and capabilities are cross-referenced to Sections 5–6 rather than repeated here, to avoid the duplication Board VIII exists to prevent.

### Domain 1 — Conversational Intelligence

**Module 1.1 — Natural Language Understanding & Dialogue**
Mission: Interpret an investigator's question, in either language, and determine what kind of question it is. Primary users: Investigating Officers, Crime Analysts. Secondary users: all other personas. Business value: this module is the entry point for every other capability in the platform — its failure rate is the platform's failure rate. Submodules: 4.1 Bilingual Intent Understanding, 4.2 Session & Case-Context Management (Section 5). Dependencies: none upstream — this is the platform's first point of contact. Interactions with other modules: hands a classified, context-resolved query to Module 1.2. Out-of-scope: does not itself retrieve or compose an answer.

**Module 1.2 — Evidence Synthesis & Answer Composition**
Mission: Assemble a sourced, confidence-qualified answer from whatever Domain 2/3 modules return. Primary users: Investigating Officers, Crime Analysts. Business value: this is where "show your work" becomes a concrete deliverable rather than a principle. Submodules: 4.3 Answer Composition, 4.4 Conflict Surfacing (Section 5). Dependencies: Domain 2/3 module outputs; Domain 4's Explainability Module for annotation. Out-of-scope: does not decide what counts as sufficient evidence to act — that remains the investigator's.

**Module 1.3 — Multimodal Interaction**
Mission: Accept and deliver voice input/output alongside text. Primary users: field-based Investigating Officers. Business value: removes the keyboard-literacy/field-access friction identified in the Product Vision report. Submodules: 4.5 Voice Input Processing, 4.6 Voice Output Composition. Dependencies: Module 1.1 for understanding, Module 1.2 for what to voice back. Out-of-scope: does not alter answer content based on modality — a voiced answer and a typed answer to the same question must be substantively identical.

**Module 1.4 — Product Generation & Visualization Hand-off**
Mission: Convert a conversational answer into an exportable product (PDF) or a visual form (timeline, map, network graph) without requiring the investigator to re-specify the question. Primary users: Investigating Officers (export), Crime Analysts and District Supervisors (visualization). Business value: directly addresses the "triple data entry" pain point established in Phase 1's research. Submodules: 4.7 Structured Export Composition, 4.8 Visualization Request Routing. Dependencies: Module 1.2's composed answer; Domain 2's Graph Renderer; Domain 3's spatial outputs. Out-of-scope: does not generate a visualization from data the underlying answer didn't already cite.

### Domain 2 — Investigative Reasoning

**Module 2.1 — Cross-Case Resolution**
Mission: Determine whether records across different cases, stations, or spellings refer to the same person, vehicle, or entity. Primary users: Investigating Officers. Secondary users: SCRB Analysts (data-quality use). Business value: directly targets the highest-ranked pain point identified across this entire research program (alias/spelling-variant matching failure). Submodules: 4.9 Entity & Alias Normalization, 4.10 Cross-Case Pattern Matching. Dependencies: underlying case records (outside this catalogue's scope — an upstream data dependency). Out-of-scope: does not assert a match is correct — it returns candidates with confidence, for Domain 4 to annotate and the investigator to judge.

**Module 2.2 — Network Reasoning**
Mission: Map and visualize relationships among people, places, and events linked across resolved cases/entities. Primary users: Crime Analysts, Crime Branch-equivalent investigators. Business value: extends specialist-grade network analysis (historically unavailable below specialist units, per Phase 1's findings) to routine casework for the first time. Submodules: 4.11 Relationship Structure Analysis, 4.12 Network Visualization. Dependencies: Module 2.1's resolved entities. Out-of-scope: never recommends a disruption action against a network — it describes structure only, per the documented fragmentation risk of acting on network "centrality" alone.

**Module 2.3 — Behavioral & MO Linkage**
Mission: Produce a statistically-grounded similarity score between a case's modus operandi and other cases' MO, with a stated accuracy rate. Primary users: Investigating Officers, Crime Analysts. Business value: a defensible, evidence-based replacement for narrative offender profiling — this module's release is explicitly gated on statistical validation (per the Strategic Capability Formulation Report). Submodules: 4.13 Behavioral Feature Comparison, 4.14 Linkage Confidence Reporting. Dependencies: Module 2.1's resolved entities/cases as input scope. Out-of-scope: never produces a free-text characterization of an offender — output is restricted to a similarity score and its stated accuracy, by design, not by omission.

### Domain 3 — Aggregate Pattern & Context Intelligence

**Module 3.1 — Spatial-Temporal Forecasting**
Mission: Forecast place-and-time crime patterns at the aggregate level and issue graduated (not binary) early-warning signals. Primary users: District Supervisors, Station House Officers. Business value: the most evidence-bounded version of "predictive crime intelligence" identified in this research program — place-based, not person-based. Submodules: 4.15 Pattern Aggregation, 4.16 Graduated Threshold Monitoring. Dependencies: the Demographic-Exclusion Enforcement Capability (Section 6) as a hard input gate; historical incident location/time data only. Out-of-scope: never accepts or produces any individual-identifying data point.

**Module 3.2 — Structural Context**
Mission: Correlate aggregate, anonymized structural/environmental factors (infrastructure, land use, time-of-day, density) with incident patterns for resourcing and prevention planning. Primary users: District Supervisors, Senior Police Leadership. Business value: the highest-risk, highest-scrutiny module in this catalogue, carrying the Karnataka-specific Habitual Offenders Act exposure identified in the Strategic Capability Formulation Report — release requires external legal/ethics review, not just engineering completion. Submodules: 4.17 Aggregate Correlation, 4.18 Exclusion-Boundary Enforcement. Dependencies: the same Demographic-Exclusion Enforcement Capability as Module 3.1. Out-of-scope: never accepts caste, religion, or community identity as an input field, directly or via any locality/occupation proxy sufficient to reconstruct them.

### Domain 4 — Trust & Governance

**Module 4.1 — Explainability**
Mission: Attach source and confidence to every output from every other module, by default. Primary users: every persona, implicitly, on every interaction. Business value: this module's output quality determines whether the entire platform is trustworthy — it has no independent value of its own, only as a property of every other module's output. Submodules: 4.19 Confidence Annotation, 4.20 Reasoning-Trace Generation. Dependencies: receives raw output from every other active module. Out-of-scope: does not decide what the answer is — only how its certainty and basis are communicated.

**Module 4.2 — Audit & Accountability**
Mission: Log every query and output, and flag suspected boundary violations (e.g., an attempted demographic-correlated query) for independent review. Primary users: Auditors, System Administrators. Business value: directly operationalizes the prior reports' finding that available safeguards are routinely skipped under institutional pressure unless they are structural and independently checkable. Submodules: 4.21 Event Logging, 4.22 Boundary-Violation Flagging. Dependencies: every other active module's outputs and inputs. Out-of-scope: does not itself adjudicate whether a flagged event was a genuine violation — that is a human review function this module supports, not replaces.

**Module 4.3 — Access Control**
Mission: Scope what each user can see and do according to their organizational role. Primary users: System Administrators (configuration), every persona (as subjects of scoping). Business value: respects existing organizational hierarchy rather than flattening it, per the Product Vision report's stakeholder analysis. Submodules: 4.23 Role-Based Scoping, 4.24 Access-Change Provisioning. Dependencies: organizational role data (an upstream dependency, outside this catalogue's scope). Out-of-scope: does not define the organizational hierarchy itself — it enforces a hierarchy defined elsewhere.

---

## 5. Submodule Catalogue

Twenty-four submodules, numbered to match their parent module (Section 4). Each row states the submodule's specific responsibility and why it exists as a distinct unit rather than being absorbed into its parent module.

| # | Submodule | Parent module | Responsibility | Why distinct from its parent |
|---|---|---|---|---|
| 4.1 | Bilingual Intent Understanding | 1.1 | Classify a query's intent (retrieval vs. reasoning) and language | Intent classification and dialogue-state management are different failure modes — conflating them would make debugging language-specific errors harder |
| 4.2 | Session & Case-Context Management | 1.1 | Maintain what the platform currently treats as active context | Distinct from intent understanding because it persists across turns, not per-query |
| 4.3 | Answer Composition | 1.2 | Assemble retrieved facts into a coherent, sourced response | Distinct from conflict surfacing because most answers have no conflict to surface |
| 4.4 | Conflict Surfacing | 1.2 | Detect and present contradictions between sources rather than silently resolving them | A specific, evidence-grounded behavior (Phase 2's source-reconciliation finding) important enough to specify separately, not bury inside general composition |
| 4.5 | Voice Input Processing | 1.3 | Convert spoken queries into the same query form Module 1.1 expects | Distinct from output because input and output have different latency/accuracy tolerances |
| 4.6 | Voice Output Composition | 1.3 | Convert a composed answer into spoken form without altering its content | Must guarantee parity with text output — kept separate so this guarantee is independently testable |
| 4.7 | Structured Export Composition | 1.4 | Generate a PDF or similar product carrying the same sources/confidence as the original answer | Distinct from visualization because export is a document concern, not a rendering concern |
| 4.8 | Visualization Request Routing | 1.4 | Determine which Domain 2/3 module's output should populate a requested timeline/map/network view | Distinct from export because it depends on Domain 2/3 outputs, not just the composed text answer |
| 4.9 | Entity & Alias Normalization | 2.1 | Determine whether two differently-spelled/recorded entities are the same | The specific, highest-evidence sub-problem within cross-case resolution (Phase 1's #1-ranked pain point) |
| 4.10 | Cross-Case Pattern Matching | 2.1 | Surface candidate case links once entities are normalized | Depends on 4.9's output — kept distinct so normalization can be improved independently of matching logic |
| 4.11 | Relationship Structure Analysis | 2.2 | Apply structural concepts (centrality, brokers, equivalence) to resolved entities | A distinct analytical step from rendering — structure must be computed before it can be visualized |
| 4.12 | Network Visualization | 2.2 | Render computed structure as an explorable graph | Kept distinct from 4.11 so the underlying structural analysis can be reused by Module 1.4 without re-rendering |
| 4.13 | Behavioral Feature Comparison | 2.3 | Compare MO-relevant features between cases | The statistically-validated core of Capability E — kept separate from confidence reporting so the comparison method can be audited independently of how its output is communicated |
| 4.14 | Linkage Confidence Reporting | 2.3 | State the comparison's accuracy/confidence in standard terms | Shares its underlying logic with Domain 4's Confidence Annotation Capability (Section 6) — kept as a submodule here only insofar as it's specific to behavioral linkage's particular accuracy metric |
| 4.15 | Pattern Aggregation | 3.1 | Aggregate historical incident data by place and time | The foundational aggregate computation — must exist before any threshold logic can run |
| 4.16 | Graduated Threshold Monitoring | 3.1 | Determine when an aggregate pattern crosses a defined warning threshold | Distinct from aggregation because threshold-setting is a policy/calibration decision, not a data-processing one |
| 4.17 | Aggregate Correlation | 3.2 | Correlate structural/environmental factors with incident patterns | The core analytical function of Module 3.2 |
| 4.18 | Exclusion-Boundary Enforcement | 3.2 | Reject any input/output that could reconstruct an excluded demographic category | Significant and high-stakes enough (per the Habitual Offenders Act risk) to warrant its own named submodule rather than being an implicit property of 4.17 |
| 4.19 | Confidence Annotation | 4.1 | Attach a standardized confidence indicator to any output | The platform-wide confidence standard every other module's output must carry |
| 4.20 | Reasoning-Trace Generation | 4.1 | Produce the deeper, optional full reasoning trace for power users/audit | Distinct from default confidence annotation because it is requested, not default-shown (per the Product Vision report's "explainability by default, deeper trace on demand" principle) |
| 4.21 | Event Logging | 4.2 | Record every query and output for later reconstruction | The base audit capability all accountability functions depend on |
| 4.22 | Boundary-Violation Flagging | 4.2 | Detect and surface suspected hard-exclusion violations for review | Depends on 4.21's logs but is a distinct, actively-monitoring function, not passive record-keeping |
| 4.23 | Role-Based Scoping | 4.3 | Enforce what a given role can see/do | The core access-control function |
| 4.24 | Access-Change Provisioning | 4.3 | Process legitimate role/access changes | Distinct from enforcement because provisioning is an administrative workflow, not a runtime check |

---

## 6. Capability Catalogue

The core of this specification. Twenty-one Capabilities (this document's taxonomy-level meaning — see the terminology note at the top of this report). Inputs, outputs, and dependencies follow from each Capability's supporting submodule(s) in Section 5 and are not repeated column-by-column here, to keep the catalogue's reuse pattern — the actual point of this section — visible rather than buried in repetition.

| Capability | Problem solved | Investigator value | Supporting module(s) | Human responsibility | AI responsibility | Reusability |
|---|---|---|---|---|---|---|
| Natural Language Query Understanding | Investigators shouldn't need query syntax | Ask naturally, in either language | 1.1 | Phrasing the actual question | Classifying intent and language | Used by every Domain 1 interaction |
| Bilingual Language Processing | Kannada is the working language for most stations, not an afterthought | Use the platform in the language already used for casework | 1.1, 1.3 | None | Equal-parity understanding/generation in English and Kannada | Reused by Module 1.3 (voice) and Module 1.4 (export language) |
| Conversational Context Retention | Repeating context every message is repetitive cognitive load | Pick up where a conversation left off, same session or days later | 1.1 | Confirming or correcting context if it's wrong | Maintaining and visibly surfacing current context | Used by every Domain 1 interaction |
| Source-Grounded Answer Composition | Unsourced answers can't be checked or trusted | Every claim is checkable | 1.2 | Verifying a cited source if needed | Composing answers strictly from retrievable, citable facts | **Consumed by every Domain (1, 2, 3) before reaching Domain 4** — the single most reused Capability in this catalogue |
| Conflict Surfacing | Contradictory sources are currently reconciled silently or not at all | See a contradiction instead of an artificially confident single answer | 1.2 | Judging which source to credit | Detecting and presenting the contradiction neutrally | Used wherever multiple sources address the same fact, across Domains 1 and 2 |
| Voice Input/Output Processing | Field conditions don't always allow typing | Field-usable access | 1.3 | None | Speech-to-text/text-to-speech without altering answer content | Used by Module 1.3 only — the one Capability in this catalogue with a single consumer, retained because Voice is a mandatory Challenge 01 requirement in its own right |
| Structured Export/Product Generation | Findings need to be attached to a case diary/chargesheet | Export without manual re-transcription | 1.4 | Deciding what belongs in the exported product | Generating the export while preserving sources/confidence | Used by Module 1.4; consumed by every Domain 1/2/3 answer that gets exported |
| Visualization Hand-off | Switching tools to visualize breaks investigative flow | Get a timeline/map/network view from the same conversation | 1.4 | Requesting the visualization | Routing the right underlying data to the right visual form | Reuses Module 2.2's Network Visualization and Module 3.1's spatial outputs rather than rendering independently |
| Entity & Alias Resolution | Cross-station/cross-spelling identity matching fails silently today | Don't lose a match because of a spelling variant | 2.1 | Judging whether a candidate match is operationally meaningful | Surfacing normalized candidates with confidence | **Reused by Module 2.2 (network) and Module 2.3 (behavioral linkage)** — both need resolved entities before their own analysis can run |
| Cross-Case Similarity Matching | Pattern recognition currently depends on individual memory | Surface resemblance without needing 20 years of case memory | 2.1 | Judging operational relevance of a surfaced match | Computing and confidence-scoring the similarity | Used by Module 2.1; underlying technique reused by Module 2.3's behavioral comparison |
| Relationship Structure Analysis | Network reasoning exceeds unaided working memory | See network structure, not just a list of names | 2.2 | Deciding what, if anything, to do about a structural finding | Computing centrality/broker/equivalence structure | Used by Module 2.2; output reused by Module 1.4's visualization hand-off |
| Statistical Behavioral Similarity Scoring | Narrative offender profiling has a documented validity problem | A defensible, accuracy-stated alternative | 2.3 | Judging operational relevance | Computing and reporting a stated-accuracy similarity score, never a characterization | Used by Module 2.3 only — deliberately not generalized further until statistically validated |
| Spatial-Temporal Pattern Aggregation | Predictive intelligence built at the individual level has a documented bias-amplification failure mode | Place/time forecasting without person-level risk | 3.1 | Resourcing/deployment decisions based on the forecast | Aggregating and forecasting strictly at the place/time level | Used by Module 3.1; shares its exclusion-enforcement dependency with Module 3.2 |
| Graduated Threshold Early-Warning Logic | Binary alert/ignore decisions cause both alert fatigue and missed warnings | A warning system with calibrated middle ground | 3.1 | Setting/approving threshold policy | Monitoring and signaling threshold crossings | Used by Module 3.1 only |
| Structural/Environmental Correlation | Resourcing decisions need structural context, not just incident counts | Aggregate context for prevention planning | 3.2 | Using the context responsibly in planning decisions | Computing correlation strictly from aggregate, non-individual inputs | Used by Module 3.2 only |
| **Demographic-Exclusion Enforcement** | Demographic-correlated suspicion is a specific, documented Karnataka-relevant legal exposure | Confidence that the platform cannot produce this category of output, structurally | 3.1, 3.2 | None — this is the one Capability with no human-judgment component, by design | Rejecting any input/output that could reconstruct an excluded category, directly or via proxy | **Reused identically by Modules 3.1 and 3.2** — the same enforcement logic, not two separate implementations |
| Confidence Scoring & Calibration | Confidence is currently implicit or absent across the entire reviewed landscape | Know how much to trust a specific answer, not just whether to trust the platform generally | 4.1 | None | Producing a standardized, calibrated confidence indicator | **Consumed by every Domain's output** — alongside Source-Grounded Answer Composition, the most reused Capability in this catalogue |
| Reasoning-Trace Generation | Default explanations aren't always enough for supervisor/audit review | A deeper "show me everything" view when needed | 4.1 | Requesting the deeper trace | Generating a complete, checkable reasoning trace on demand | Used wherever a user requests it, across all Domains |
| Audit Logging & Event Capture | Accountability requires reconstructable history, not self-report | Confidence the system is independently checkable | 4.2 | Conducting the independent review | Capturing complete, non-reconstructable-after-the-fact logs | Applies to every Domain's every interaction |
| Boundary-Violation Detection & Flagging | Available safeguards are routinely skipped under pressure unless actively monitored | Early detection of a boundary issue before it compounds | 4.2 | Adjudicating a flagged event | Detecting patterns consistent with an attempted or actual boundary violation | Monitors Domains 1, 2, and 3 outputs continuously |
| Role-Based Access Scoping | Different roles have different legitimate access needs | See what's relevant to your role, nothing else | 4.3 | None | Enforcing scoping consistently | Applies platform-wide |

### 6.1 What this table demonstrates about capability density

Three Capabilities — *Source-Grounded Answer Composition*, *Confidence Scoring & Calibration*, and *Demographic-Exclusion Enforcement* — are each reused across multiple Domains or Modules rather than reimplemented per-module. This is the concrete evidence behind this report's Executive Summary claim about reuse; Section 9 (Capability Consolidation Review) traces how this reuse was arrived at, not just asserted.

---

## 7. Functional Component Catalogue

Seventeen Functional Components, described purely by responsibility — no API, model, or implementation detail, per the brief's explicit instruction. "Invoked by" names the Capability(ies) each component implements; "Consumes/Produces" stays at the level of information, not data formats.

| Component | Purpose | Implements Capability | Invoked by | Consumes | Produces | User visibility |
|---|---|---|---|---|---|---|
| Intent Classifier | Determine whether a query is a retrieval or reasoning question, and its language | Natural Language Query Understanding | Module 1.1 | Raw query text/speech | Classified query intent and language | Invisible — informs downstream behavior only |
| Context Memory Store | Hold the active case/session context | Conversational Context Retention | Module 1.1 | Prior turns, active case reference | Current context state | Visible as a checkable "what I'm tracking" indicator |
| Bilingual Understanding Engine | Interpret and generate English/Kannada with parity | Bilingual Language Processing | Modules 1.1, 1.3 | Text/speech in either language | Understood meaning / generated response | Indirectly visible — output quality is the only visible signal |
| Answer Composer | Assemble sourced facts into a coherent response | Source-Grounded Answer Composition | Module 1.2 | Retrieved facts with sources | A composed answer with inline citations | Directly visible — this is the answer the investigator reads |
| Confidence Annotator | Attach a standardized confidence indicator to an answer | Confidence Scoring & Calibration | Module 4.1, invoked by every other active module | A draft answer/finding | The same finding with confidence attached | Directly visible, by default, on every answer |
| Conflict Detector | Identify contradictions between sources addressing the same fact | Conflict Surfacing | Module 1.2 | Multiple sourced facts on the same question | A flagged contradiction, or none | Visible only when a conflict exists |
| Alias Normalizer | Determine whether two records refer to the same entity | Entity & Alias Resolution | Modules 2.1, 2.2, 2.3 | Raw entity records | Normalized, linked entity candidates with confidence | Indirectly visible — surfaces as candidate matches |
| Similarity Engine | Score resemblance between two cases, either by case attributes or by behavioral/MO features | Cross-Case Similarity Matching, Statistical Behavioral Similarity Scoring | Modules 2.1, 2.3 | Normalized entities/case features | A similarity score with stated accuracy | Visible as a ranked candidate list |
| Relationship Mapper | Compute structural properties (centrality, brokers, equivalence) over linked entities | Relationship Structure Analysis | Module 2.2 | Normalized, linked entities | Computed network structure | Indirectly visible — feeds the Graph Renderer |
| Graph Renderer | Render computed network structure, or route to a visualization | Relationship Structure Analysis (rendering half), Visualization Hand-off | Modules 2.2, 1.4 | Computed structure or spatial data | An explorable visual | Directly visible on request |
| Spatial-Temporal Aggregator | Aggregate historical incidents by place and time | Spatial-Temporal Pattern Aggregation | Module 3.1 | Historical incident location/time data only | Aggregate pattern/forecast | Visible as a hotspot forecast |
| Threshold Monitor | Detect when an aggregate pattern crosses a defined warning level | Graduated Threshold Early-Warning Logic | Module 3.1 | Aggregate pattern data, defined thresholds | A graduated warning signal | Visible as an alert, distinct from a routine forecast |
| Structural Correlation Engine | Correlate aggregate environmental factors with incident patterns | Structural/Environmental Correlation | Module 3.2 | Aggregate, anonymized structural data | A correlation summary | Visible as a contextual-factors summary |
| Exclusion Filter | Reject any input/output that could reconstruct an excluded demographic category | Demographic-Exclusion Enforcement | Modules 3.1, 3.2 | Any candidate input/output to either module | Either a pass-through or a hard rejection | Invisible when functioning correctly; visible as a logged rejection event when triggered |
| Reasoning-Trace Builder | Construct the full, checkable reasoning chain behind a given output | Reasoning-Trace Generation | Module 4.1 | An answer and its source chain | A complete reasoning trace | Visible on explicit request only |
| Event Logger | Record every query and output | Audit Logging & Event Capture | Module 4.2 | Every interaction across Domains 1–3 | An immutable log entry | Invisible to routine users; fully visible to Auditors/Administrators |
| Access Scope Resolver | Determine what a given user/role may see or do | Role-Based Access Scoping | Module 4.3 | A user's role and the requested action/data | An allow/deny determination | Invisible when functioning correctly; visible as a denial message when triggered |

---

## 8. User Interaction Catalogue

Eighteen interactions, each representing meaningful investigative or governance work rather than a UI widget, organized by Domain.

### Domain 1 — Conversational Intelligence

| Interaction | Initiated by | Expected outcome | AI assistance | User control | Explainability requirement | Frequency |
|---|---|---|---|---|---|---|
| Ask a natural-language question | Any investigator | A sourced, confidence-qualified answer | Full — this is the platform's core function | Full — the investigator decides what to do with the answer | Source + confidence on every response, by default | Very high |
| Ask a follow-up question within case context | Any investigator | An answer that correctly uses prior turns' context | Full | Can correct context if wrong | Visible context indicator | High |
| Switch case context | Any investigator | The platform's active context updates accordingly | Full | Full | The new context is explicitly confirmed | Medium |
| Request a visualization from an answer | Investigating Officer, Crime Analyst | A timeline/map/network view of the same cited facts | Full | Requests the form; doesn't have to re-specify the question | The visualization carries the same sources as the originating answer | Medium |
| Export an answer as a structured product | Investigating Officer | A PDF or similar product, sources intact | Full | Decides what's included | Exported product retains full source/confidence trail | Medium |

### Domain 2 — Investigative Reasoning

| Interaction | Initiated by | Expected outcome | AI assistance | User control | Explainability requirement | Frequency |
|---|---|---|---|---|---|---|
| Request a cross-case pattern check | Investigating Officer | A confidence-scored list of candidate related cases | Full | Judges relevance of each candidate | Each candidate's basis for inclusion is shown | High |
| Review candidate case links | Investigating Officer, Crime Analyst | A clear view of why two cases were linked | Partial — surfaces basis, doesn't assert correctness | Full — accept, reject, or investigate further | The specific matched fields/features are shown, not just a score | High |
| Explore a network visualization | Crime Analyst | An interactive view of relationship structure | Full | Full exploration; no AI-driven next-step suggestion | Structural metrics shown alongside the visual, not just the graph | Medium |
| Request an MO/behavioral similarity check | Investigating Officer, Crime Analyst | A stated-accuracy similarity score against other cases | Full, within statistically validated scope | Judges operational relevance | Accuracy/confidence stated explicitly, never an implied characterization | Medium |
| Drill into a similarity score's basis | Crime Analyst | The specific features that drove a similarity score | Full | Full | Full feature-level transparency, not just the aggregate score | Low-medium |

### Domain 3 — Aggregate Pattern & Context Intelligence

| Interaction | Initiated by | Expected outcome | AI assistance | User control | Explainability requirement | Frequency |
|---|---|---|---|---|---|---|
| View a hotspot forecast for a region/period | District Supervisor, Station House Officer | An aggregate, place/time forecast with confidence | Full, within place/time-only scope | Full — used for resourcing decisions the platform doesn't make | Forecast basis (historical pattern window, confidence) shown explicitly | Medium |
| Receive a graduated early-warning alert | District Supervisor, Station House Officer | A calibrated alert, not a binary flag | Full | Decides response level | Threshold and triggering pattern shown | Low (by design — this is an exception-triggered interaction) |
| View a structural context summary for a location | District Supervisor, Senior Leadership | An aggregate, anonymized correlation summary | Full, within aggregate-only scope | Full | Explicit statement that inputs are aggregate/non-individual | Low-medium |

### Domain 4 — Trust & Governance

| Interaction | Initiated by | Expected outcome | AI assistance | User control | Explainability requirement | Frequency |
|---|---|---|---|---|---|---|
| View source/confidence detail for any answer | Any investigator | The specific source and confidence behind a claim | N/A — this interaction *is* the explainability function | Full | This interaction's entire purpose is explainability | Very high (it is part of every default answer) |
| View a full reasoning trace | Crime Analyst, Station House Officer, Auditor | The complete chain from query to answer | N/A | Full | Maximum — this is the deepest available transparency view | Low |
| Review the audit log | Auditor, System Administrator | A reconstructable history of platform use | None — logs are not AI-summarized for this purpose, per Persona 7.8's trust requirement | Full | The log itself is the explainability artifact | Low (periodic/triggered) |
| Configure role-based access | System Administrator | Correctly scoped access for a user/role | Minimal — administrative, not investigative | Full | Access decisions are themselves logged | Low |
| Flag a suspected boundary violation | Any user, or the Boundary-Violation Flagging component automatically | An independent review is triggered | Partial — automatic detection supplements manual reporting | Full human adjudication | The flagged event's basis is fully visible to the reviewer | Low (by design) |

---

## 9. Capability Consolidation Review

Genuine merge/elimination decisions made while constructing this catalogue, not asserted after the fact.

**Modules merged or rejected:**
- A standalone "Voice Module" at the Domain level was considered and rejected — voice has no value independent of the understanding/composition it feeds, so it was demoted to Module 1.3, a submodule of Domain 1, rather than a peer of it.
- A standalone "Export Domain" was considered and rejected for the same reason — export is a product-generation concern, not an independent intelligence function, so it remains Module 1.4.
- Domains 3a ("Predictive") and 3b ("Contextual") were initially considered separately and merged into one Domain 3, because both share the identical Demographic-Exclusion Enforcement dependency and the identical strict-release-gate governance profile — maintaining them separately would have duplicated that governance logic across two Domains for no operational benefit.

**Capabilities merged:**
- An initial draft specified separate matching logic for cross-case resolution (Module 2.1) and behavioral linkage (Module 2.3). On review, both reduce to the same underlying technique — scoring resemblance between two records, whether by entity attribute or by behavioral feature — so the **Similarity Engine** (Section 7) implements both, rather than two independently-built matching systems.
- An initial draft specified separate "Kannada Understanding" and "Kannada Generation" Capabilities. These were merged into one **Bilingual Language Processing** Capability, since splitting them would have implied parity could be achieved independently in each direction, when in practice understanding and generation quality in a single language are not independently meaningful to an investigator.

**Capabilities NOT merged, despite surface similarity:**
- Confidence Scoring & Calibration (Domain 4) and Linkage Confidence Reporting (Submodule 4.14, Domain 2) were considered for merging, since both produce a confidence figure. They were kept distinct because Domain 4's Capability is a platform-wide standardization function, while Module 2.3's submodule is specific to one statistical method's particular accuracy metric — collapsing them would have implied a single confidence scale fits every kind of finding equally well, which Phase 3's own findings (Section 3 of that report) caution against.

**Interactions eliminated:**
- "View confidence score" and "view source" were initially specified as two separate interactions. They were merged into one ("View source/confidence detail," Section 8) because, per this entire research program's central design commitment, source and confidence are never presented independently of each other — splitting the interaction would have implied they could be.

**The net effect:** this review removed 1 Domain-level split, merged 2 Capabilities, and merged 2 Interactions, while explicitly declining to merge 1 pair of superficially similar Capabilities for a stated reason — demonstrating that consolidation in this catalogue was a genuine check, not a one-directional simplification exercise.

---

## 10. Product Catalogue Summary

### 10.1 Quantitative summary

| Layer | Count | Note |
|---|---|---|
| Domains | 4 active + 1 future (unspecified below domain level) | Domain 5 (Institutional Memory) intentionally not decomposed further |
| Modules | 12 | Distributed 4 / 3 / 2 / 3 across Domains 1–4 |
| Submodules | 24 | Exactly 2 per module, by consistent design choice, not coincidence — each module's responsibility was found to decompose cleanly into exactly two distinct sub-responsibilities once examined (Section 5) |
| Capabilities | 21 | 3 reused across 3+ modules; 1 (Voice) retained as a single-consumer Capability because it is independently mandatory under Challenge 01 |
| Functional Components | 17 | 2 implement more than one Capability (Similarity Engine, Graph Renderer) |
| User Interactions | 18 | Distributed 5 / 5 / 3 / 5 across Domains 1–4 |

### 10.2 Why this structure is appropriate

The structure is deliberately **asymmetric across Domains** — Domain 1 and Domain 4 each carry more Modules/Interactions than Domain 3 — and this asymmetry is itself a finding, not an oversight: Domain 1 (the conversational hub) and Domain 4 (the governance substrate every other Domain depends on) are structurally central to this platform in a way Domain 3 (the most gated, latest-releasing Domain) is not yet, and is not expected to be until its release gates are satisfied. A perfectly symmetric catalogue would have been a sign that Domain-level decisions were made by template rather than by the evidence and governance reasoning this report has tried to make traceable throughout.

---

## 11. Executive Recommendations

1. **Build and ship Domain 4 (Trust & Governance) in lockstep with Domain 1, never behind it.** This catalogue's structure makes explicit what the prior reports established conceptually: every Domain 1 interaction's explainability requirement (Section 8) is non-optional, which means Module 4.1 cannot be a later addition without every earlier interaction needing retrofitting.
2. **Validate Module 2.3 (Behavioral & MO Linkage) statistically before specifying it any further.** This catalogue intentionally kept Module 2.3's Capabilities and Components minimal and tightly scoped, reflecting its status as the least mature Module in the active catalogue.
3. **Treat Module 3.2's Exclusion-Boundary Enforcement (Submodule 4.18) as a release-blocking deliverable, not a configuration option.** Per the Strategic Capability Formulation Report's risk register, this is the single highest-stakes piece of this entire specification.
4. **Use this catalogue's reuse map (Sections 6–7) as the basis for future engineering estimation** — the Similarity Engine, Source-Grounded Answer Composition, and Confidence Scoring & Calibration Capabilities are each load-bearing across multiple Modules, and any future architecture phase should treat their reliability as a platform-wide dependency, not a per-feature concern.
5. **Leave Domain 5 (Institutional Memory) unspecified below the Domain level until Domain 4 has demonstrated production maturity**, exactly as this catalogue has done — specifying it further now would create a paper commitment ahead of the governance foundation it depends on.

---

## Closing Note

This catalogue is the most mechanical of the documents produced in this research and design program, and deliberately so — its job was to make the previously-established capability strategy and product vision checkable at an engineering-relevant level of detail, not to introduce new judgment calls. Where genuine judgment calls did arise (Section 9's consolidation decisions, the Domain 3 grouping, the decision to keep Linkage Confidence Reporting distinct from platform-wide Confidence Scoring), they are traceable to a stated reason, consistent with every phase before this one.

*This report decomposes the Strategic Capability Formulation Report and the Product Vision & Investigator Experience Report into an engineering-grade taxonomy. It proposes no architecture, technology, or implementation approach, and — consistent with every phase in this research and design program — has not been validated against KSP/SCRB's actual engineering, product, or governance teams.*
