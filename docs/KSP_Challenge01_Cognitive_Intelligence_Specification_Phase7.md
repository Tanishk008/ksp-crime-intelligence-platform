# Cognitive Intelligence Specification
## Challenge 01 — Intelligent Conversational AI for the Karnataka State Police Crime Database

**Prepared by:** Executive Cognitive Intelligence & Reasoning Specification Board (building on the Strategic Capability Formulation Report, the Product Vision & Investigator Experience Report, and the Product Specification Catalogue)
**Status:** Cognitive behavior specification only — no software architecture, AI models, frameworks, databases, or implementation technology discussed in this document
**Date:** June 2026

---

### Note on scope

This document specifies how the platform's intelligence should think, not what it is built from. It takes the Product Specification Catalogue's Domains and Modules as fixed and answers a different question for each one: when a Module like Cross-Case Resolution (2.1) or Behavioral & MO Linkage (2.3) actually runs, what cognitive process should be happening inside it, what should it remember, how should it handle disagreement with itself across hypotheses, and how should it explain what it did? This document draws directly on the investigative-cognition and intelligence-tradecraft research that opened this entire research program — hypothesis generation, tunnel vision, calibration, the Analysis of Competing Hypotheses, working-memory limits on relational reasoning — and treats it as the specification's primary evidence base, alongside two further bodies of research introduced specifically for this phase: **case-based reasoning** (Kolodner; Aamodt & Plaza's Retrieve-Reuse-Revise-Retain cycle), which maps closely onto how an investigation should be represented and how the system should learn from closed cases, and **appropriate reliance / calibrated trust research** (Lee & See, 2004; Bansal et al., 2021), which directly informs how explanations should be designed — not to be convincing, but to be informative enough for an investigator to independently judge whether to rely on them.

---

## 1. Executive Summary

Four commitments define this specification.

**First, the system's job is to make multiple hypotheses visible and comparable, never to collapse them into one answer prematurely.** This is the most consequential design decision in this document, and it is justified by the single best-evidenced finding in this entire research program: premature narrowing onto one explanation, and the subsequent filtering of all new evidence through that explanation, is the best-documented cognitive failure mode in criminal investigation and intelligence analysis alike. The cognitive architecture specified here makes generating and maintaining more than one hypothesis the default behavior, not an optional deep-dive.

**Second, calibrated trust — not maximized trust — is the explicit design target.** Foundational human-automation research (Lee & See, 2004) established that the goal of a decision-support system is not to make people trust it more; it's to make their trust track its actual reliability. More recent research (Bansal et al., 2021) found something sharper and directly load-bearing for this specification: explanations engineered to be *persuasive* measurably hurt human-AI team performance compared to explanations engineered to be *informative* — even when the persuasive version is more pleasant to read. Every explainability principle in Section 9 follows from choosing informativeness over persuasiveness, deliberately, even where that means a less confident-sounding answer.

**Third, the system should learn the way an experienced investigator does — by retaining and retrieving cases, not by treating each query as independent.** Case-based reasoning's well-established cycle (retrieve a similar past case, reuse what's transferable, revise it for the current situation, retain the outcome for next time) gives this specification a real, research-grounded structure for what was, in Phase 2 of the original research program, identified as the least-supported cognitive activity in policing: the years-long, informally-built "case library" that separates an experienced investigator from a novice. This specification's reasoning framework (Section 3) and memory model (Section 5) are built to make that library available to every investigator, immediately — without pretending the system has replaced the judgment that library supports.

**Fourth, every hard exclusion and governance principle established in the prior three reports is carried forward unchanged, now specified at the level of cognitive behavior rather than capability or product design.** This document does not revisit whether the platform should produce person-level risk scores, narrative offender profiles, or demographic-correlated inferences — it specifies, in Sections 3, 6, and 9, exactly how the reasoning process itself refuses to produce them, as a property of how hypotheses are generated and evidence is weighed, not as a filter applied after the fact.

---

## 2. Cognitive Philosophy

### 2.1 How the intelligence perceives an investigation

Not as a static record to be queried, but as **an evolving case** in the case-based-reasoning sense: a contextualized episode with a goal, a growing and sometimes contradictory evidence base, and — critically — open questions that have not yet been answered. Perceiving an investigation well means continuously asking "what is this most similar to, and specifically how does it differ" (the CBR retrieval-and-adaptation move), not matching keywords against a static store.

### 2.2 How investigations are represented internally

As a structured case representation analogous to a CBR case: known facts (each with a source), a set of live hypotheses (each with its own supporting evidence, disconfirming evidence, and confidence level), explicitly flagged contradictions, and — for each live hypothesis — an explicit marker of what evidence would most change its standing. This is a deliberately richer representation than a single best-guess answer, because a single best-guess answer is precisely the representation that produces premature closure.

### 2.3 How problems are decomposed

Using the same cognitive chain documented in the foundational investigative-cognition research this program is built on (observation → pattern recognition → hypothesis generation → evidence evaluation → belief revision, and onward) — not an arbitrary computational pipeline invented for this platform. This is a deliberate choice: an investigator should be able to recognize the system's reasoning stages as a more rigorous, externalized version of their own mental process, not as an alien procedure they must learn to interpret.

### 2.4 How reasoning is organized

Around explicit, separable hypotheses, evaluated against each other using **diagnosticity** — whether a piece of evidence actually discriminates between live hypotheses, not merely whether it's consistent with one of them. This is the same standard the Analysis of Competing Hypotheses method exists to enforce, and it is treated here as a structural property of the reasoning process, not an optional technique an investigator must remember to request.

### 2.5 How uncertainty is handled

Never collapsed into false certainty, and never expressed as vague hedging either. Every stage of reasoning that produces a confidence judgment expresses it in standardized, consistent terms — the same Words-of-Estimative-Probability discipline (Kent, 1964; operationalized today in standards like ICD 203) that intelligence tradecraft has used for exactly this purpose since the 1960s, chosen over free-text hedging specifically because free-text confidence language is well-documented to be interpreted inconsistently by different readers.

### 2.6 How incomplete information influences reasoning

The system represents what it does not know as a first-class part of its internal state, not an omission. Three distinct epistemic states are kept distinct, never collapsed into one: **"no evidence exists on this point,"** **"evidence exists but is inconclusive,"** and **"this has not yet been investigated."** Conflating these — a common failure in naive systems — would make an unexplored question look the same as a settled absence, which is exactly the kind of false confidence Section 9 is designed to prevent.

### 2.7 How multiple hypotheses coexist

By default, not as an advanced mode. Per the Analysis of Competing Hypotheses' own logic, every hypothesis the system holds is evaluated against the same evidence matrix as its competitors, and the system does not silently prune a hypothesis to one before presenting the set to the investigator — pruning is the investigator's decision, informed by what the system surfaces, not a decision the system makes on the investigator's behalf.

### 2.8 How intelligence supports rather than replaces investigators

By exposing its internal reasoning state, always — never just its conclusion. This is where the appropriate-reliance research becomes a design principle rather than a citation: the system is specifically not designed to maximize how confident or persuasive it sounds. It is designed so that an investigator's trust in any given answer tracks how well-evidenced that answer actually is — which means the system must be equally willing to say "this is weakly supported" as "this is well supported," even though the former is less satisfying to receive. A system optimized to sound consistently confident would, by the cited research's own finding, produce *worse* investigative outcomes than one that is honestly uneven.

---

## 3. Investigative Reasoning Framework

### 3.1 The complete reasoning lifecycle

```
Intent Understanding → Investigation Goal Identification → Context Recovery
        ↓
Information Need Assessment → Knowledge Discovery (CBR: Retrieve)
        ↓
Evidence Correlation → Cross-Case Correlation → Entity Resolution
        ↓
Timeline Construction ⟷ Network Expansion ⟷ Behavioural Reasoning   (these three
        ↓                                                            may run in
Pattern Recognition                                                  parallel —
        ↓                                                            see Section 4)
Hypothesis Generation
        ↓
Hypothesis Evaluation ⟷ Confidence Assessment ⟷ Evidence Validation  (interdependent —
        ↓                                                            see Section 4's
Alternative Explanation Generation                                   sequencing note)
        ↓
Recommendation Formulation
        ↓
Explainable Response Composition
        ↓
Investigation Memory Update (CBR: Retain)
```

### 3.2 Why each stage exists, and what it contributes to investigative quality

| # | Stage | Why this stage exists | Contribution to investigative quality |
|---|---|---|---|
| 1 | Intent Understanding | A question's surface form doesn't reveal whether it needs retrieval or reasoning | Calibrates how much downstream reasoning depth is actually warranted — prevents both over-processing simple lookups and under-processing complex ones |
| 2 | Investigation Goal Identification | "Find a fact," "check a pattern," and "build a case" carry different evidentiary thresholds | Sets the diagnosticity bar appropriate to what's actually being asked |
| 3 | Context Recovery | A question is rarely self-contained — it depends on the active case or session | Preserves investigation continuity across a session or across days, without requiring the investigator to re-establish context |
| 4 | Information Need Assessment | A single question often implies several distinct underlying needs (e.g., "is this connected" implies both entity resolution *and* MO comparison) | Prevents a shallow, single-pass answer to a question that actually required several kinds of evidence |
| 5 | Knowledge Discovery | The CBR "Retrieve" step — finding the cases, records, and entities most relevant by analogy to the current situation | Makes the years-long "case library" experienced investigators build informally available immediately, regardless of the requesting investigator's tenure |
| 6 | Evidence Correlation | Raw retrieved facts must be checked against each other before they're used | Surfaces contradictions early, before they propagate into a hypothesis built on unreconciled sources |
| 7 | Cross-Case Correlation | The highest-evidence operational pain point identified across this entire research program | Directly targets cross-station/cross-case pattern blindness |
| 8 | Entity Resolution | The single most failure-prone judgment within cross-case correlation (spelling/transliteration variance) | Kept as its own stage because its failure mode is specific and well-documented enough to need dedicated handling, not folded into general correlation |
| 9 | Timeline Construction | Reconciling multiple partial, conflicting time-stamped sources exceeds unaided working memory | Externalizes sequencing explicitly rather than relying on the investigator to mentally track it |
| 10 | Network Expansion | Relational reasoning exceeds working-memory capacity faster than almost any other task (estimated at roughly four variables held reliably at once) | Makes relationship structure explicit and explorable rather than dependent on memory |
| 11 | Behavioural Reasoning | MO and behavioral "signature" are functionally and psychologically distinct, and only the statistically-testable version of behavioral similarity has a defensible evidence base | Provides a defensible alternative to narrative offender profiling, scoped to similarity scoring only |
| 12 | Pattern Recognition | Cross-case/cross-incident pattern recognition normally takes years of accumulated exposure to build | Extends pattern recognition to every investigator, not only the most experienced |
| 13 | Hypothesis Generation | The single most consequential, most bias-vulnerable stage identified anywhere in this research program | Defaults to generating multiple candidate explanations, directly countering premature closure at its source |
| 14 | Hypothesis Evaluation | Evidence must be judged by whether it discriminates between hypotheses, not by how much of it exists | Prevents the documented failure of treating evidence volume as if it were evidence diagnosticity |
| 15 | Confidence Assessment | Calibration is a distinct, separately trainable skill, not a byproduct of good analysis | Ensures stated confidence is a deliberate computation, not an implicit impression carried over from fluent-sounding prose |
| 16 | Evidence Validation | Even "objective" evidence can be contextually contaminated, as documented in forensic-science bias research | Checks evidence quality and provenance before it's used to support a hypothesis, not only after a conclusion is challenged |
| 17 | Alternative Explanation Generation | Structured techniques (devil's advocacy, key-assumptions checks) exist specifically because the strongest case against the leading hypothesis is rarely generated spontaneously | Surfaces the strongest competing explanation explicitly, even when not directly requested |
| 18 | Recommendation Formulation | Investigative next-step suggestions are valuable; conclusions about guilt are not this system's role | Restricted, by design, to suggesting what evidence would most efficiently discriminate between live hypotheses — never a charge, arrest, or verdict |
| 19 | Explainable Response Composition | An answer's explanatory framing measurably affects whether reliance on it is appropriate | Composes the response to be informative rather than persuasive, per Section 9's central design principle |
| 20 | Investigation Memory Update | The CBR "Retain" step — without it, every investigation starts the system's pattern-recognition from zero | Closes the learning loop so Stage 5 and Stage 12 improve over time, across investigators, not just within one session |

---

## 4. Intelligence Orchestration Model

### 4.1 Sequential vs. parallel reasoning

Some stages have a hard dependency order: Entity Resolution (8) must complete before Network Expansion (10) can operate on resolved entities, and before Behavioural Reasoning (11) can compare MO features across confirmed-distinct cases. Others do not: Timeline Construction (9), Network Expansion (10), and Behavioural Reasoning (11) depend on the same upstream correlation stages but not on each other, and should run in parallel — there is no investigative-quality reason to force a network analysis to wait for a timeline that addresses an unrelated question.

### 4.2 A sequencing correction identified during specification

The stage list as given does not explicitly order Hypothesis Evaluation (14), Confidence Assessment (15), and Evidence Validation (16) relative to each other. This specification corrects that: **Evidence Validation must precede Confidence Assessment**, because assessing confidence in a hypothesis before checking whether the evidence supporting it is itself sound (per the forensic contextual-bias research underlying Stage 16) would produce a confidence figure built on potentially contaminated input. Hypothesis Evaluation and Confidence Assessment are interdependent and iterate together, but Evidence Validation is a precondition for both, not a peer.

### 4.3 Context-driven reasoning

Which stages actually run depends on Investigation Goal Identification (Stage 2). A simple retrieval question ("what is the status of exhibit #4471") does not need Hypothesis Generation, Hypothesis Evaluation, or Alternative Explanation Generation at all — running them anyway would not improve the answer, and would simply consume time and obscure a simple answer behind unnecessary apparatus. Reasoning depth is matched to the question, not maximized by default.

### 4.4 Iterative reasoning and progressive refinement

Confidence at any given point is provisional. New evidence discovered during Evidence Correlation (6) after Hypothesis Generation (13) has already run should trigger a return to Hypothesis Generation, not a patch applied only to Confidence Assessment — a structural enforcement of the belief-revision principle this entire research program has emphasized: revision should happen at the level where the new evidence is actually relevant, not be absorbed only at the surface.

### 4.5 Continuous evidence integration

A still-open investigation should be capable of triggering re-evaluation when new evidence enters the system independent of any new query — a forensic report returning, a new case being filed with a matching MO. This is the orchestration-level expression of the same principle: investigative reasoning should not be a one-shot response to a query, but a standing relationship between the system and an open case.

### 4.6 Dynamic investigation adaptation

An investigation's reasoning needs change over its life. Early in a case, breadth matters most — Hypothesis Generation should err toward more candidates. Late in a case, when most alternatives have been evaluated and discarded, the emphasis shifts toward confirmation-checking and Evidence Validation against the surviving hypothesis. Orchestration should adapt which stages receive the most reasoning effort based on the investigation's maturity, not apply uniform effort throughout.

### 4.7 Branching and merging

Reasoning pipelines **branch** when Hypothesis Generation produces more than one credible candidate — each candidate's Evidence Validation and Confidence Assessment proceeds as its own path. They **merge** when separate branches converge on evidence bearing on the same underlying fact (e.g., two hypotheses both depend on whether a specific timeline is accurate) — at that point, the shared evidence's validation should not be duplicated across branches, and the result feeds back into both.

### 4.8 How uncertainty propagates — the weakest-link principle

A downstream stage's confidence should never exceed the confidence of its weakest necessary input. This directly guards against a documented historical failure pattern (from the original intelligence-tradecraft research underlying this program): compressing a chain of individually uncertain judgments into a single, more confident-sounding conclusion at the point of communication. If Hypothesis Evaluation depends on a piece of evidence Evidence Validation rated as only weakly corroborated, the resulting confidence in that hypothesis cannot be stated as high regardless of how many other strong facts surround it.

### 4.9 How confidence evolves

Confidence increases only with new, **independent** corroborating evidence — never with repetition or restatement of the same underlying source in a different form. Two case-file mentions of the same witness's single observation are one piece of evidence, not two, for confidence purposes. This distinction is easy to lose and is treated here as a structural rule, not a judgment call left to be applied inconsistently.

### 4.10 How intelligence revises earlier conclusions

Explicitly and visibly. A revision is itself a logged event, shown to the investigator with what changed and why — never a silent overwrite of a previous answer. This directly extends the Conflict Surfacing principle established in the Product Vision report into the orchestration layer: revision is a visible event in the investigation's history, not an erasure of one.

---

## 5. Cognitive Memory & Context Model

### 5.1 The nine memory types

| Memory type | What it holds | Lifespan | Key boundary |
|---|---|---|---|
| Conversation Memory | The current session's dialogue turns | Scoped to the active session | Never leaks into Entity/Relationship Memory's substantive content |
| Case Memory | Everything tied to a specific case file | As long as the case is open, and thereafter per applicable records-retention rules (an upstream legal dependency this specification does not set) | Scoped to one case; a cross-case analytic question does not inherit any single case's Case Memory |
| Investigation Memory | The reasoning trace — hypotheses considered, evidence evaluated, confidence assigned — for a specific investigation | Tied to Case Memory's lifespan | This is the Reasoning Externalization capability flagged as a future research track in the Strategic Capability Formulation Report — full specification here is intentionally deferred for the same reason |
| Evidence Memory | The corpus of evidence/exhibits across cases, with provenance | Indefinite, subject to records-retention rules | Provenance is never separable from the evidence itself — no evidence entry exists without its source attached |
| Entity Memory | Resolved entity identities and their normalized aliases | Persists across cases — the same person may recur in unrelated cases over years | Holds identity facts only — never a risk score or characterization attached to an entity |
| Relationship Memory | Network structure derived from Entity Memory and case linkages | Persists across cases | Holds structural facts only (who is connected to whom, and how) — never an inferred "risk" annotation on a relationship |
| Knowledge Memory | Stable domain knowledge — legal codes, MO taxonomies, statistical baselines for behavioral linkage | Updated deliberately, not continuously | Changes here should be a reviewed event, not an automatic byproduct of routine use |
| Organizational Memory | Role/hierarchy/access information | Tied to the organizational structure it reflects | Owned by the governance function; not freely mutable through ordinary investigative use |
| User Preference Memory | An individual investigator's stated interface preferences (language, explanation detail level) | Tied to the user's account | **Scoped strictly to interface preference.** Never used to infer or record anything about an investigator's competence, judgment, or behavior — this boundary exists specifically so the system never becomes a system that profiles the investigator instead of the case |

### 5.2 What should never be remembered

- Anything that would reconstruct an excluded demographic category, directly or by proxy — carried forward unchanged from every prior report in this program.
- A discarded hypothesis re-surfacing in a later, unrelated case as if it were evidence. The hypothesis's *existence* is preserved in Investigation Memory's audit trail, but it must never silently re-enter a different case's reasoning — this is a memory-hygiene principle that prevents tunnel vision from propagating across cases via the system's own memory.
- Any biometric or identifying data beyond what Entity Resolution specifically requires to confirm a match.

### 5.3 Context inheritance and switching

A question asked within an active case inherits that case's Context Memory. A cross-case analytic question (the Crime Analyst persona's typical use) explicitly does **not** inherit any single case's context, specifically to prevent one case's assumptions from contaminating a broad pattern search. Every context switch is visible to the investigator, never silent — consistent with the Conversational Context Retention principle established in the Product Vision report.

### 5.4 Context recovery

Resuming a case after time has passed recovers the case's accumulated context with an explicit recap that distinguishes **what was concluded** from **what remained an open, unresolved hypothesis** — this distinction matters more, not less, as time passes, since an investigator returning to a case after a gap is at higher risk of misremembering which was which.

### 5.5 Memory consistency and validation

If two memory entries conflict (Entity Memory states one thing; a newly entered case record states otherwise), this surfaces as a Conflict per Section 3's Evidence Correlation stage — it is never silently resolved by preferring whichever entry is more recent. Entity Memory and Relationship Memory specifically should be subject to the same data-quality review discipline already established for SCRB Analysts in the Product Vision report, rather than a new, separate review process invented for this purpose.

### 5.6 Context compression and prioritization

When a long case history must be compressed for a quick answer, compression must preserve confidence and uncertainty markers, not just facts. A long history compressed to "no major findings" is a different statement from "an open hypothesis nobody has yet followed up on," and a compression process that cannot tell these apart is a memory-design failure, not a minor simplification. When multiple pieces of context compete for relevance in a given moment, prioritization follows diagnosticity to the current question, not recency alone.

### 5.7 Memory boundaries — the central design constraint

Conversation Memory and User Preference Memory are categorically separate from Entity, Relationship, and Case Memory. How an investigator phrases questions or prefers explanations to be delivered must never influence what the system treats as fact about a case. This boundary exists because conflating the two would let an investigator's own communication style — entirely irrelevant to the case — subtly bias what the system surfaces as evidence.

---

## 6. Hypothesis & Decision Intelligence

### 6.1 How hypotheses are created

Seeded by Pattern Recognition and Knowledge Discovery (the CBR retrieval step), but subject to one structural rule that exists specifically to counter confirmation bias at its origin: **if an investigator's own question implies a specific hypothesis** ("is X the suspect"), **the system must generate at least one credible alternative**, not only answer about X. This directly prevents the query's own framing from becoming the system's only frame.

### 6.2 How competing hypotheses coexist

Each hypothesis carries, as a structural property, its own supporting evidence, its own disconfirming evidence, its own confidence level, and an explicit marker of what evidence would most change its standing. These are displayed side by side by default — never collapsed to a single ranked answer unless the investigator explicitly asks only for the top candidate, in which case the system still discloses that alternatives exist and were not shown in full.

### 6.3 How conflicting evidence is managed

Surfaced explicitly as a Conflict, with both sides' sourcing shown — never silently dropped, never averaged into a blended account that no single source actually stated.

### 6.4 How confidence changes

Only through new, independent evidence (Section 4.9's rule) — never through mere accumulation of restated or low-diagnosticity facts. A hypothesis is not "more confident" because more text discusses it; it is more confident only because something that could have discriminated against it failed to.

### 6.5 How investigators compare hypotheses

Through identical structure for every hypothesis under consideration — the same four properties (supporting evidence, disconfirming evidence, confidence, what-would-change-this) for each — so that comparison is a like-for-like judgment the investigator makes, not a narrative that has already implicitly favored one candidate through how it was written.

### 6.6 How uncertainty is communicated

Through the same standardized confidence language specified in Section 2.5, applied consistently across every hypothesis under comparison, not just the leading one.

### 6.7 How recommendations are generated

Restricted to investigatory next-steps, and specifically to **closing the largest diagnosticity gap** between the current leading hypotheses — "what evidence would most efficiently distinguish your top two explanations" — never a recommendation to arrest, charge, or conclude. This is the same hard boundary established in every prior report in this program, now expressed as the literal logic by which a recommendation is generated, not just a content restriction applied afterward.

### 6.8 How recommendations are revised

When new evidence changes which hypothesis is best-supported, or changes what would most efficiently discriminate between the survivors, the recommendation updates — visibly, with the change logged, never silently.

### 6.9 How decisions remain explainable

Every recommendation traces to the specific hypotheses and the specific diagnosticity gap it was generated to close. A recommendation with no traceable hypothesis behind it is, by this specification's standard, not a valid output state.

---

## 7. Proactive Intelligence Model

### 7.1 The non-intrusiveness principle, stated as a structural rule

Every proactive (unprompted) output must be visually and structurally distinguishable from a direct answer to an asked question, and must be dismissible without the system re-surfacing the same suggestion repeatedly. An investigator who declines a suggestion once should not see it again in the same form — repetition after a decline is what separates "informative" from "intrusive," and this specification treats that line as a hard one, not a matter of degree.

### 7.2 When the system should remain passive

When a question is fully specified and directly answerable. Routine retrieval does not need an unsolicited suggestion attached to it — adding one where none is warranted is itself a violation of Section 7.1's principle, since it trains the investigator to expect noise alongside every answer.

### 7.3 When the system should recommend

When Hypothesis Evaluation (Section 3, Stage 14) identifies a diagnosticity gap the investigator's question did not address — the system recommends the action that would close that specific gap, per Section 6.7's logic, not a generic prompt to "investigate further."

### 7.4 When the system should ask clarifying questions

Only when the ambiguity would materially change the answer — the same threshold established in the Product Vision report, restated here as the formal trigger condition governing this cognitive behavior specifically, not merely a UX preference.

### 7.5 When the system should detect investigative opportunities, suggest related cases, suggest emerging patterns, or highlight behavioural similarities

Only above a deliberately conservative confidence threshold, and always presented as a clearly labeled, separate suggestion the investigator can distinguish from what they directly asked for. This threshold is set deliberately high because the appropriate-reliance research (Bansal et al., 2021) found that explanations and suggestions designed to maximize apparent usefulness — rather than calibrated to actual evidentiary strength — measurably degrade human-AI team performance. An unsolicited, low-confidence suggestion is exactly this failure mode in miniature.

### 7.6 When the system should recommend additional evidence

Only when doing so resolves a specific, named diagnosticity gap between two live hypotheses — never a generic "gather more evidence" prompt, which would carry no information the investigator doesn't already have.

### 7.7 When the system should recommend next investigative actions

Framed only as informational precedent ("in similar past cases, this was a commonly useful next step"), never as an instruction — the same distinction established in the Product Vision report, restated here as the literal content restriction governing Recommendation Formulation (Section 3, Stage 18).

---

## 8. Human–AI Collaboration Framework

### 8.1 Responsibility allocation

| Always human | Shared | Always system |
|---|---|---|
| Deciding what to investigate next | Identifying which hypotheses are worth pursuing (system proposes, investigator selects) | Retrieving, correlating, and cross-referencing records |
| Judging witness credibility in person | Assessing whether a recommendation's diagnosticity logic is sound (system computes it, investigator can challenge it) | Computing and reporting confidence/diagnosticity scores |
| Forming and revising belief about what happened | Reconciling a surfaced conflict (system presents both sides, investigator weighs them) | Surfacing contradictions and maintaining the evidence-to-hypothesis matrix |
| Deciding when evidence is sufficient to act | — | Maintaining memory and context continuity across a session and across time |
| Signing the chargesheet | — | Generating an explainable trace for every output |

### 8.2 Decision ownership and escalation

The system never owns a decision — it owns the quality and traceability of the information a decision is based on. Escalation (e.g., a Station House Officer being notified of a flagged conflict in a high-priority case) is a notification function, not a decision-making one: the system surfaces that something needs human attention; it does not determine what should be done about it.

### 8.3 Investigator override

Any investigator may discard a system-generated hypothesis, override a confidence assessment in their own working notes, or proceed against a system recommendation. The system's response to an override is to log it neutrally (Section 9's auditability principle) — never to repeat the original assessment with escalating emphasis, and never to silently relabel the overridden hypothesis as "rejected" in a way that would make it harder to reconsider later if circumstances change.

### 8.4 Trust calibration as an ongoing process, not a one-time onboarding step

Per Lee & See's foundational framing, trust should track demonstrated reliability over time, differentiated by capability — an investigator's trust in cross-case retrieval (very well-evidenced) should be allowed to be higher than their trust in behavioral-linkage scoring (a newer, statistically-validated-but-narrower capability) without the system trying to equalize that difference through presentation. Section 9.3 of the Product Vision report already established this sequencing at the product level; this section confirms it as a cognitive design requirement, not just a rollout schedule.

### 8.5 Confidence communication and evidence presentation

Identical standards apply regardless of audience — a Station House Officer reviewing a case and a Crime Analyst conducting strategic research see the same underlying confidence language, differing only in how much reasoning-trace detail is shown by default (Product Specification Catalogue, Module 4.1), never in how honestly confidence is stated.

### 8.6 Alternative reasoning and human validation

Every multi-hypothesis output includes an explicit prompt structure for the investigator to indicate which alternative they find most credible and why, if they choose to — not required, but available, and when provided, this becomes part of Investigation Memory (Section 5) as a human judgment distinct from, and never overwritten by, the system's own confidence assessment.

### 8.7 Collaborative and team-based investigation support

When multiple investigators work the same case, each sees the same underlying hypothesis set and evidence matrix — but individual annotations (an SI's personal note on a hypothesis) remain attributed to that individual, never merged into the system's own assessment as if the system had independently reached the same conclusion. This boundary prevents a subtle but important failure mode: a human's opinion being laundered into apparent machine-generated confirmation.

### 8.8 Supervisor interaction

A supervisor (Station House Officer, District Supervisor) reviewing a case sees the full hypothesis history, including hypotheses the investigator discarded — framed neutrally, as investigative history, not as a performance evaluation of the investigator's judgment. This framing distinction is deliberate: the same data, presented as "here's what was considered and why" versus "here's what the investigator missed," produces very different organizational incentives, and only the former is consistent with this program's repeated finding that punitive framing degrades the honest reporting any oversight system depends on.

---

## 9. Explainability & Trust Framework

### 9.1 The central design choice: informative, not persuasive

This framework's single governing principle, drawn directly from Bansal et al.'s (2021) controlled finding that persuasively-framed AI explanations measurably degraded human-AI team decision accuracy compared to informative ones: **every explanation in this system is designed to let an investigator independently judge whether to rely on an answer, not to increase the likelihood that they will.** Where these two goals conflict — and they sometimes will, since an honest "this is weakly supported" answer is less satisfying than a confidently-stated one — informativeness wins, without exception.

### 9.2 Evidence attribution and source grounding

Every factual claim traces to a specific, checkable source (case number, exhibit ID, record). This is restated here from the Product Vision report specifically to confirm it as a cognitive-architecture requirement — the reasoning process must retain attribution at every stage (Section 3), not reconstruct it only when composing the final response, because attribution reconstructed after the fact is more vulnerable to error than attribution carried through from the point each fact entered the reasoning chain.

### 9.3 Reasoning transparency

The default answer states its conclusion, its confidence, and its top-line source. The full reasoning trace (every stage of Section 3 the answer actually passed through, and what each stage contributed) is available on request, not hidden — but also not forced into every interaction, consistent with the non-intrusiveness principle (Section 7.1).

### 9.4 Confidence explanation

A stated confidence level is always accompanied by *why* — which evidence supports it, what would raise or lower it — never a bare number or label with no accompanying basis. A confidence figure without its basis is, by Section 9.1's standard, persuasive framing without informative content, and is treated as a specification violation, not a minor omission.

### 9.5 Alternative interpretations

Surfaced by default for any hypothesis-bearing answer (Section 6.2) — not buried behind a separate request, since an answer that shows only the leading hypothesis is, definitionally, less informative than one that shows the competition it survived.

### 9.6 Unknown factors and limitations

Stated explicitly, using the three-way distinction established in Section 2.6 ("no evidence exists," "evidence exists but is inconclusive," "this has not yet been investigated") rather than a generic disclaimer. A generic "this answer may be incomplete" notice attached to every response would, through sheer repetition, stop carrying any real information — the specific kind of gap must be named.

### 9.7 Assumptions

Any assumption load-bearing enough to change the answer if false is stated explicitly as part of the response — directly extending the Key Assumptions Check technique from intelligence tradecraft into ordinary system output, not reserved for a separate analytic exercise.

### 9.8 Recommendation justification

Every recommendation states the specific diagnosticity gap it was generated to close (Section 6.7, 6.9) — a recommendation with no stated justification is treated, by this specification, as an incomplete output, not a terse one.

### 9.9 Auditability

Every reasoning stage's intermediate state (not just the final answer) is retained in a form independently reviewable by an Auditor persona — consistent with the Product Specification Catalogue's Module 4.2, now specified at the cognitive-process level: it is the actual hypothesis set, evidence matrix, and confidence trajectory that must be auditable, not a system-generated summary of them.

### 9.10 The investigator challenge mechanism

An investigator must be able to directly question any specific claim, confidence level, or recommendation, and receive a response that engages with the specific challenge — not a restatement of the original answer in different words. If a challenge reveals a genuine flaw (a misapplied source, an overlooked conflict), this triggers the same revision behavior specified in Section 4.10, visibly logged.

### 9.11 Correction workflow

When an investigator identifies an error (e.g., a misresolved entity match), the correction updates the relevant memory (Section 5) and is itself logged with attribution to the correcting investigator — both so the correction propagates to future reasoning and so a future auditor can see that a human, not the system itself, identified and fixed the error.

### 9.12 Continuous trust calibration

The system does not track or report an aggregate "trust score" for itself — per Section 9.1's principle, the goal is the investigator's trust tracking the system's actual reliability, which is something the investigator judges over time through repeated, honest interactions, not something the system can legitimately self-report. The closest this specification comes to a system-side trust mechanism is the differentiated confidence-by-capability behavior already established in Section 8.4 — allowing trust to vary appropriately by capability, rather than asserting a single trust level for the whole platform.

---

## 10. Cognitive Quality Framework

### 10.1 Qualities, and how each is evaluated

| Quality | What it measures | Evaluation principle |
|---|---|---|
| Reasoning Quality | Whether hypothesis generation, evidence evaluation, and revision actually followed this specification's logic | Reviewable directly from the retained reasoning trace (Section 9.9) against this document's stage definitions (Section 3) — not inferred from output quality alone, since a correct-seeming answer can still result from a flawed process |
| Investigation Support Quality | Whether the system measurably reduced the manual cross-referencing burden documented throughout this research program | Compared against the pre-platform baseline already established in the Product Vision report's success metrics, not an abstract target |
| Evidence Utilization | Whether retrieved evidence was actually used in proportion to its diagnosticity, not just its volume | Checkable by comparing the evidence matrix's diagnosticity ratings against which evidence the final answer actually weighted |
| Context Preservation | Whether Section 5's memory model correctly distinguished what should and shouldn't persist | Tested directly against Section 5.2's "never remembered" list and Section 5.7's boundary rule |
| Consistency | Whether the same question, asked twice with the same available evidence, produces the same hypothesis set and confidence levels | A direct, repeatable test — inconsistency here indicates either a memory fault or an unstable reasoning process, both serious findings |
| Adaptability | Whether reasoning depth correctly scaled to the question (Section 4.3) and to the investigation's maturity (Section 4.6) | Reviewable by checking whether simple questions triggered unnecessary stages, and whether late-stage investigations correctly shifted emphasis toward confirmation-checking |
| Transparency | Whether every output satisfied Section 9's attribution and confidence-explanation requirements | A binary, checkable property per output — present or not, not a matter of degree |
| Reliability | Whether confidence levels, over time and across many cases, actually track real-world accuracy | The calibration question directly — requires retrospective comparison against known outcomes, the same evaluation discipline the Good Judgment Project research (cited in this program's earlier intelligence-tradecraft research) used to validate calibration training generally |
| Investigator Cognitive Load Reduction | Whether the system reduced, rather than added to, the working-memory burden of the tasks it touches (especially timeline and network reasoning) | Measured against the same self-reported and behavioral baseline established in the Product Vision report |
| Operational Value | Whether the system's outputs were actually used in investigative decisions, not just viewed | Distinguishes genuine usefulness from passive engagement |
| Trustworthiness | Whether stated confidence and actual reliability track each other (the calibration property), evaluated separately from how persuasive or polished the explanation reads | Directly testable using the same logic Bansal et al. used: comparing decision accuracy when relying on the system's stated confidence against ground truth, not surveying how convincing investigators found it |
| Human Satisfaction | Investigator-reported experience using the platform | Collected explicitly as a separate measure from Trustworthiness, since Section 9.1 already establishes that these can diverge — a satisfying answer is not automatically a trustworthy one, and tracking only satisfaction risks optimizing for the wrong property |
| Recommendation Effectiveness | Whether system-recommended next steps (Section 6.7) actually closed the diagnosticity gap they targeted | Reviewable retrospectively against case outcomes |
| Knowledge Reuse | Whether closed-case patterns (the CBR "Retain" step) measurably improved Knowledge Discovery (Section 3, Stage 5) for later, similar cases | The clearest test of whether Investigation Memory (Section 5) is functioning as a genuine institutional-memory aid, not just a per-case log |
| Learning Effectiveness | Whether Knowledge Memory updates (Section 5.1) improved performance over time without introducing drift away from this specification's principles | Requires periodic, deliberate review (Section 5.1's "reviewed event, not automatic byproduct" rule) rather than continuous unsupervised adaptation |

### 10.2 Qualitative vs. quantitative evaluation, stated as a principle

Some qualities in this table (Transparency, Context Preservation, Consistency) are directly, mechanically checkable. Others (Trustworthiness, Operational Value, Human Satisfaction) require longitudinal, real-world observation and cannot be meaningfully reduced to a single launch-day metric. **This specification explicitly rejects collapsing all fourteen qualities into one composite score** — doing so would reproduce, at the evaluation layer, the exact false-precision failure mode (Section 9.4) this entire document has been built to avoid at the answer layer.

---

## 11. Cognitive Consolidation Review

### 11.1 Can reasoning be simplified?

Yes, in one specific place identified during this review. The original stage list (Section 3) places Confidence Assessment and Evidence Validation as separate, peer-level stages after Hypothesis Evaluation. This specification reordered them (Section 4.2): Evidence Validation is a precondition for Confidence Assessment, not a peer. This is a genuine simplification — it removes the ambiguity about whether confidence can be assessed before evidence quality is checked, rather than leaving it as an implicit convention. No other reordering was found to be warranted; the remaining sequence has hard dependencies that should not be flattened.

### 11.2 Can cognitive stages be unified?

Timeline Construction (9), Network Expansion (10), and Behavioural Reasoning (11) were considered for unification into a single "Multi-Dimensional Correlation" stage. They were kept separate because they fail differently — a timeline failure (conflicting timestamps) looks nothing like a network failure (a missing entity link), and they need different recovery behaviors. Unifying them would have produced a stage that is harder to diagnose when something goes wrong, not simpler.

### 11.3 Can context management improve?

One clarification was added during review: Section 5.4's context recovery explicitly separates "what was concluded" from "what remained an open, unresolved hypothesis" when resuming a case after a gap. This distinction was implicit in the original brief's context-recovery concept but is load-bearing — an investigator returning to a case after weeks is at precisely the highest risk of misremembering which hypotheses were settled versus which were merely set aside — so it was made explicit here.

### 11.4 Can unnecessary reasoning be removed?

Section 4.3 already specifies that reasoning depth matches the question, not a uniform maximum. The consolidation review confirms this principle is applied consistently throughout: Sections 6 and 7 both define their outputs as conditional on a non-trivial trigger (a diagnosticity gap, a genuine ambiguity, a conservative confidence threshold), not as a default-always output. No stage was found to be running unconditionally when it should be conditional.

### 11.5 Can explainability improve?

One addition was made: Section 9.4 explicitly specifies that a confidence figure without its basis is a specification violation, not a minor omission. This was not stated with that level of force in the initial section structure; the consolidation review added it precisely because the research evidence (Bansal et al.'s finding) is strong enough to warrant a hard rule, not only a preference.

### 11.6 Can investigator effort be further reduced?

One structural redundancy was identified and named: the default answer already carries source and confidence (Section 9.3), and the reasoning-trace view carries everything else. An investigator who wants to understand more never has to leave the existing conversation flow to get it. The consolidation review confirms that no additional investigator effort is required to access explainability — it is present by default and deeper on request, not absent by default and available only after a separate workflow step. This was already the design intent; the consolidation review confirms it is structurally enforced by the stage dependencies in Section 3, not only stated as a preference.

### 11.7 Optimization result

| Optimization target | Assessment |
|---|---|
| Maximum Intelligence Density | Achieved — twenty reasoning stages map without duplication to the specific cognitive bottlenecks identified across the research program; no stage exists for its own sake |
| Minimum Cognitive Complexity | Achieved — depth is conditional (Section 4.3), stages that share a failure mode are kept distinct (Section 11.2), and the single reordering identified (Section 11.1) simplified rather than added a stage |
| Maximum Explainability | Achieved — source, confidence, basis, alternatives, and assumptions are all specified as structural output properties, not optional add-ons; Section 9.1's informativeness-over-persuasiveness principle is stated as a violation boundary, not a preference |
| Maximum Investigator Trust | Structured as calibrated trust, not maximized trust — the honest distinction the appropriate-reliance research draws, carried through consistently |
| Maximum Operational Value | Dependent on deployment and validation — this specification creates the conditions for it, but cannot assert it in advance, consistent with this program's general epistemic discipline about what can be claimed before ground-truth measurement |

---

## 12. Executive Recommendations

1. **Treat Section 3's reasoning lifecycle as the authoritative integration contract between this specification and any future AI architecture phase.** Specifically, every architectural decision should be traceable to one or more named stages in Section 3 — any component that cannot be mapped to a stage in that lifecycle is either a duplicate of something already specified, or something outside this specification's scope that needs a separate justification.

2. **Build the Evidence Validation precondition (Section 4.2) as a structural gate, not a downstream check.** Hypothesis Evaluation must not be able to complete if Evidence Validation has not run against the evidence it depends on — this is the cognitive equivalent of the governance-substrate priority established in the earlier capability and product reports, applied now at the reasoning-process level.

3. **Implement and test the three-way unknown-state distinction (Section 2.6) before any hypothesis-bearing output is considered stable.** The failure mode of conflating "no evidence found" with "not investigated" is documented, consequential, and easy to introduce silently by returning a negative lookup as if it were a confirmed absence.

4. **Maintain Investigation Memory's boundary between what was concluded and what remained open** (Section 5.4) as a first-class test case during any future validation work — specifically test whether a case resumed after a significant time gap correctly shows open hypotheses as open, not as conclusions.

5. **Never collapse the fourteen Cognitive Quality Framework properties into a single aggregate score** (Section 10.2). Operationally, this means quality reviews should report against each property separately, with explicit acknowledgment of which properties require longitudinal data not available at launch.

6. **The proactive intelligence thresholds in Section 7.5 should be calibrated conservatively and reviewed after the first production release cycle** — the appropriate-reliance research warrants caution about low-confidence proactive suggestions specifically, and the right threshold value is an empirical question the specification cannot answer in advance.

7. **Section 8.8's framing distinction for supervisor access** (neutral case history versus performance evaluation) should be validated directly with Station House Officer and District Supervisor personas before release — it is the place in this specification where the gap between the intended framing and the perceived framing is hardest to predict from a design document alone.

---

## Closing Note

This specification is complete as a cognitive-behavior document. It does not specify architecture, models, or implementation — that is the next phase's work. What it does specify is precise enough that a future architecture team should be able to derive requirements from it without ambiguity: every stage in Section 3 implies a specific input-output contract; every memory type in Section 5 has defined boundaries and lifespan rules; every proactive-intelligence trigger in Section 7 has an explicit threshold condition; every quality property in Section 10 has a stated evaluation method. Where the specification is deliberately incomplete — Investigation Memory's full design, Domain 5's specification below domain level — the incompleteness is named and justified, not hidden in vague language.

The same epistemic standard this specification asks of the platform's own outputs — state what is known, state what is uncertain, state what has not yet been investigated, never conflate the three — applies to this document itself.

*This specification builds on the full chain of prior documents in this research and design program, adding case-based reasoning (Kolodner, 1993; Aamodt & Plaza, 1994) and calibrated-trust / appropriate-reliance research (Lee & See, 2004; Bansal, Wu, Vaughan, Wallach, 2021) as new evidence specifically relevant to this phase's cognitive-design questions. It proposes cognitive behavior only — no architecture, AI model, framework, or implementation — and has not been validated against any specific AI engineering team or against KSP/SCRB's actual operational context.*
