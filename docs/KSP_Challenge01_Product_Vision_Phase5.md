# Product Vision & Investigator Experience Report
## Challenge 01 — Intelligent Conversational AI for the Karnataka State Police Crime Database

**Prepared by:** Executive Product Vision & Investigator Experience Board (building on the Strategic Capability Formulation Report and Phases 1–3's research)
**Status:** Product vision and investigator experience only — no architecture, AI model selection, database, or implementation technology is discussed in this document
**Date:** June 2026

---

### Note on scope

This document builds directly on the Strategic Capability Formulation Report's seven core capabilities (A–G, with H as a future research track) and does not re-derive them. Where this document refers to "the platform," it means that capability set, governed by the same hard exclusions established there: no person-level predictive risk scoring, no narrative offender profiling, no demographic-correlated suspicion (a constraint with specific, documented legal weight in Karnataka given Habitual Offenders Act legislation and the Supreme Court's October 2024 observations). This document's job is to answer a narrower, more human question: **what should it feel like for the people who actually use this, every day, under real caseload pressure?**

---

## 1. Executive Summary

Three commitments shape everything in this report.

**First, the product's job is to give time and mental bandwidth back to the investigator, not to give answers to the investigation.** Every prior phase converged on the same finding: the bottleneck is synthesis and trust, not collection, and the cognitive work that actually solves cases — hypothesis generation, diagnosticity judgment, belief revision — is irreducibly human (Phase 2). A product built around this evidence does not try to do that work. It tries to clear away everything that currently prevents an investigator from getting to that work faster, with more of what they need already in front of them.

**Second, trust must be earned through visible, checkable behavior, not asserted through confident language.** The most consistent failure pattern across every intelligence failure and every discontinued predictive-policing program reviewed in this research program was not a lack of capability — it was a system (human or algorithmic) acting more confident than its actual evidentiary basis warranted. This product's defining UX commitment, accordingly, is that **confidence is never implicit.** Every answer states what it knows, how well it knows it, and where that knowledge came from — directly operationalizing both Phase 3's confidence-language research and the established Human-AI Interaction guidelines (Amershi et al., 2019) this report draws on for the conversational design itself.

**Third, the investigator's authority is structural, not aspirational.** It is easy for a product vision to *say* "the human remains in control" while quietly designing an interface that nudges toward AI-suggested conclusions through framing, ordering, or omission. This report treats investigator authority as something the product's actual behavior must demonstrate — in what it refuses to do, in how disagreement is handled, and in what simply never appears as an option — not as a value statement disconnected from the interaction design.

---

## 2. Product Philosophy

### 2.1 Why this product should exist

Not because conversational AI is available, and not because a chatbot is novel. It should exist because three independent research phases converged on the same gap: **the work that actually separates a strong investigation from a weak one — cross-referencing, pattern recognition, network reasoning, calibrated confidence — currently has no tooling support below specialist units, anywhere in the reviewed landscape (global or Indian).** This product exists to close that specific gap, for the specific population (every investigator across 1,100+ stations, not just specialist analysts) the prior research identified as currently unserved.

### 2.2 What investigators should feel while using it

- **"I can check this."** Not relief at being told an answer, but confidence that the answer is verifiable.
- **"It remembers what I just told it."** Not having to re-establish context every message.
- **"It told me clearly when it wasn't sure."** Not vague hedging, not false confidence.
- **"It made the boring part faster and left the thinking part to me."** Not a feeling of being replaced, second-guessed, or judged.

Equally important — what investigators should **not** feel:

- **Surveilled.** Audit trails exist for accountability, not to create a sense of being monitored while thinking out loud. This is a genuine, unresolved design tension — logging every query is necessary for the governance commitments in Section 13, and it is also exactly the kind of visibility that could make an investigator self-censor exploratory questions if the audit trail is ever perceived as evaluative rather than protective. This report does not claim to fully resolve that tension, only to name it as a real cost worth monitoring, not a reason to weaken logging.
- **Talked down to.** A platform that over-explains routine answers or asks unnecessary clarifying questions erodes trust as fast as one that's overconfident — caseload pressure makes both failure modes costly (Phase 2's findings on time-pressured cognition apply to how investigators will tolerate the tool itself).
- **Judged for not knowing something already.** The product's value proposition specifically includes investigators who have not yet built the 15–20 year case-pattern library Phase 2 found experienced investigators rely on — it should never imply that needing to ask is itself a deficiency.

### 2.3 How investigative work should change, and what should never change

**Should change:** The proportion of a working day spent searching versus reasoning. The accessibility of cross-case pattern recognition to a first-year SI, not just a 20-year veteran. The traceability of how a chargesheet's supporting facts were assembled.

**Should never change:** Who decides whether to register a case, who to interview, when to arrest, what to conclude, and who signs the chargesheet. The platform's outputs are inputs to investigator judgment, never substitutes for it — and this is not a values statement, it is a structural commitment carried through every section below.

---

## 3. Vision Statement

A Karnataka where an investigator with one year of service and an investigator with twenty years of service have access to the same depth of cross-referenced evidence and pattern recognition — with the platform never pretending to replace the judgment that experience actually builds, only the manual search labor that experience currently has to substitute for.

---

## 4. Mission Statement

To be the conversational layer between every investigator in Karnataka and the state's crime data — answering questions in the investigator's own language, grounding every answer in checkable evidence, and refusing, structurally rather than just by policy, to generate the categories of output (person-level risk scores, narrative offender characterizations, demographic-correlated suspicion) that the global and Indian-specific evidence in this research program show cause more harm than the operational value they appear to offer.

---

## 5. Product Principles

Six commitments, each stated so it can be checked against actual product behavior, not just intent:

1. **Show your work, always.** Every factual claim in every answer carries a source; every answer carries a confidence indicator. If either is missing, the answer is incomplete, not just unhelpful.
2. **Silence is a valid, sometimes correct, answer.** When there is no grounded evidence for a question, the platform says so, plainly, rather than producing a fluent-sounding guess (directly responding to Phase 3's hallucination/automation-bias findings).
3. **Augment the search, never the verdict.** Retrieval, correlation, pattern-surfacing: yes. Guilt, risk, or characterization of a person: never — this line is drawn the same way, with no exceptions, regardless of how confidently a user phrases their question.
4. **Kannada is not a translation of the default — it is a default.** Parity between English and Kannada is a design requirement, checked the same way accuracy is checked, not an afterthought layered onto an English-first build.
5. **New capabilities earn trust before they earn scope.** Per the capability roadmap already established, the riskiest functions (place/time forecasting, behavioral linkage, structural context) ship later, behind stricter review, regardless of how technically ready they are sooner.
6. **The platform is auditable to the same standard as a paper case diary — never less.** Nothing the platform surfaces should be harder to trace, after the fact, than a handwritten note would have been.

---

## 6. Stakeholder Analysis

This section maps the eight roles named in the brief against the stakeholder evidence already established in Phase 1 (Section 3) and Phase 4, distinguishing investigative roles (which Phase 1 already characterized in depth) from platform-governance roles (System Administrator, Auditor) which are specific to this product and constructed here for the first time.

| Stakeholder | Relationship to the platform | Primary tension this product must resolve for them |
|---|---|---|
| Investigating Officers | Primary daily user | Speed vs. thoroughness — under caseload pressure, the fastest answer and the best-sourced answer must not feel like a trade-off |
| Crime Analysts | Power user, cross-case/strategic use | Depth vs. accessibility — analysts want rigor and method visibility that a frontline IO would find excessive |
| Station House Officers | Supervisory user | Oversight vs. micromanagement — needs a station-level view without the platform feeling like a surveillance layer over their officers |
| District Supervisors | Strategic/reporting user | Real-time accuracy vs. defensibility — numbers used in a public review meeting must be more defensible, not just faster, than current manual compilation |
| SCRB Analysts | Data-quality/admin stakeholder | Consuming vs. improving — the platform should help surface, not just inherit, CCTNS data-quality problems |
| Senior Police Leadership | Institutional risk owner | Capability vs. exposure — leadership bears the legal/reputational consequence if Section 5's hard exclusions are ever violated in practice |
| System Administrators | Platform operations | Access vs. friction — RBAC must be strict without making routine legitimate use cumbersome |
| Auditors | Independent oversight | Completeness vs. usability of logs — an audit trail designed for investigator-facing legibility is not automatically adequate for independent verification, and this product must serve both purposes without compromising either |

---

## 7. Investigator Personas

### 7.1 The Investigating Officer — "I need this to be faster than my own memory, not smarter than my own judgment."

**Responsibilities:** Owns an active caseload from FIR to chargesheet. **Objectives:** Build a case that survives court scrutiny, on time, without sacrificing thoroughness to caseload pressure. **Decision-making:** What to investigate next, who to interview, when evidence is sufficient to act. **Pain points:** Manual cross-referencing by memory or phone call; triple data entry across diary, CCTNS, and chargesheet; language re-coding between Kannada narrative and structured fields (Phase 1, Sections 1.9, 2.3). **Current workflow:** CCTNS terminal, paper case diary, personal phone for informal coordination. **Technology interaction:** Comfortable with a phone, less so with rigid enterprise dashboards. **AI expectations:** Wants confirmation and speed; will distrust anything that feels like it's auditing their competence rather than assisting their task. **Trust requirement:** Must be able to see *why*, in a form quick enough to check without breaking their workflow. **Information needs:** Prior records, similar MO, known associates, exhibit status. **Success criteria:** Less time spent hunting for facts they already half-remember; stronger evidentiary basis for the same time invested.

### 7.2 The Crime Analyst — "I need to see the method, not just the conclusion."

**Responsibilities:** Cross-case and trend analysis, typically at DCRB/SCRB or Crime Branch level. **Objectives:** Surface patterns senior officers can act on with confidence. **Decision-making:** Which patterns are worth escalating. **Pain points:** No structured cross-case tooling reaches this level today outside specialist units (Phase 1, 2, 3's repeated, independent finding). **AI expectations:** Wants rigor over raw speed — comfortable with, and will actively distrust the absence of, explicit confidence/statistical language. **Trust requirement:** The highest scrutiny of any persona toward the platform's actual methodology, not just its output. **Success criteria:** Patterns the analyst would eventually have found anyway, found faster and with a defensible evidence trail attached.

### 7.3 The Station House Officer — "I need to defend anything this surfaces to my superior."

**Responsibilities:** Case allocation, review and sign-off across every case at the station. **Objectives:** Station-level case-clearance health and defensibility. **Pain points:** No consolidated view across many concurrent cases (Phase 1, Section 3.1). **AI expectations:** Wants a station-level synthesis generated conversationally, not a separate reporting tool to learn. **Trust requirement:** Anything surfaced must be something the SHO could stand behind if questioned by a superior. **Success criteria:** Faster, more confident case review without becoming dependent on a tool the SHO can't personally vouch for.

### 7.4 The District Supervisor — "I need numbers I can defend in a public review meeting."

**Responsibilities:** District-level resource allocation and crime review. **Pain points:** Currently manages by lagging aggregate statistics, manually compiled (Phase 1, Section 3.1). **AI expectations:** Wants trend synthesis with the ability to drill into any specific case that looks anomalous. **Trust requirement:** Numbers must be more defensible than the manual process they replace, not merely faster to produce. **Success criteria:** Real-time visibility without losing the audit-grade defensibility of the current (slow) process.

### 7.5 The SCRB Analyst — "I need this to improve data quality, not just consume it."

**Responsibilities:** CCTNS data administration, MO/fingerprint bureau operation, statistical reporting to NCRB (Phase 1, Section 1.2). **Pain points:** Inherits whatever data quality stations produce, with limited systematic detection tooling. **AI expectations:** Wants the platform to surface likely data-quality issues (e.g., probable alias-matching errors) as a byproduct of normal use, not just consume records as given. **Trust requirement:** Must be able to audit and correct anything the platform asserts about a record's quality or linkage. **Success criteria:** A measurable, not just felt, improvement in the data quality SCRB is accountable for.

### 7.6 Senior Police Leadership — "I am accountable for what this platform does, even when I'm not the one using it."

**Responsibilities:** Policy, resourcing, public accountability. **Pain points:** Strategic decisions currently lag ground reality (Phase 1, Section 3.1). **AI expectations:** Wants strategic synthesis, but cares most about the platform never creating legal or reputational exposure — this persona is the ultimate owner of the risk register established in the prior phase. **Trust requirement:** Needs confidence that the hard exclusions (Section 5) are enforced structurally, not just documented. **Success criteria:** Demonstrable operational value with zero incidents of the platform crossing its defined boundaries.

### 7.7 The System Administrator — "I need to know exactly who can see what, and catch it immediately if that's wrong."

**Responsibilities:** RBAC configuration, user provisioning, platform health monitoring. **Objectives:** No role creep, no unauthorized access, no silent degradation in availability. **AI expectations:** Wants visibility into usage patterns and the ability to flag or restrict anomalous access (e.g., a user querying well outside their legitimate caseload). **Trust requirement:** Full administrative visibility into who has access to what, at all times. **Success criteria:** Zero unauthorized cross-role access incidents; fast, low-friction provisioning for legitimate role changes.

### 7.8 The Auditor — "I do not take the platform's word for its own compliance."

**Responsibilities:** Independent review of platform usage and outputs against the hard exclusions and governance principles established in this research program — specifically including verification that no demographic-correlated or person-level predictive output has been produced. **Objectives:** Catch boundary violations the platform's own self-reporting might miss. **AI expectations:** Wants complete, non-reconstructable-after-the-fact logs — not a summary the platform itself generated about its own behavior. **Trust requirement:** The strictest of any persona — the auditor's role is specifically to not extend the platform the benefit of the doubt. **Success criteria:** Ability to independently verify, not just be told, that the platform stayed within its designed boundaries.

---

## 8. Operational Journeys

For each journey: today's workflow and its bottleneck, the platform-assisted future workflow, and the decision point that remains, unambiguously, the investigator's alone.

### 8.1 Murder Investigation

| | Today | With the platform |
|---|---|---|
| Workflow | Scene visit, statements, FSL referral, manual case-diary notes | Same investigative steps, but the IO can ask "has this MO appeared in the district/state in the last 3 years" mid-investigation and get a sourced, confidence-scored candidate list |
| Bottleneck | FSL turnaround (unchanged by this platform — an upstream dependency, not a capability gap) and manual cross-referencing of MO patterns | Manual cross-referencing is addressed directly; FSL turnaround remains outside this product's scope |
| Cognitive burden | Holding possible MO matches in memory while waiting for forensic confirmation | Reduced — the candidate list exists outside the IO's memory, checkable on demand |
| **Decision point (always human):** | Whether a candidate match is operationally relevant, and what to do about it | Unchanged — the platform surfaces, the IO decides |

### 8.2 Financial Fraud

| | Today | With the platform |
|---|---|---|
| Workflow | Manual compilation of transaction trails and victim statements across institutions | Conversational assembly of the known evidence trail into a structured, exportable product for preservation requests |
| Bottleneck | Multi-institution coordination (banks, telecom) — a human/inter-institutional process | **Explicitly unchanged.** The platform cannot and will not contact external institutions autonomously — this is a hard product boundary (Section 12), not a current limitation awaiting a future version |
| Decision point | Which preservation requests to prioritize given time-criticality | Unchanged — the platform informs the prioritization, never acts on it |

### 8.3 Cybercrime

| | Today | With the platform |
|---|---|---|
| Workflow | Manual timeline assembly across complaint, platform/bank responses, I4C coordination | Faster timeline assembly and contradiction-surfacing across multiple reporting sources |
| Bottleneck | Time-critical fund-trail freezing depends on manual, cross-institution human coordination | **Explicitly unchanged**, same boundary as 8.2 |
| Decision point | Whether and how urgently to escalate | Unchanged |

### 8.4 Organized Crime

| | Today | With the platform |
|---|---|---|
| Workflow | Informal, Crime-Branch-maintained gang charts; tacit network knowledge | Network structure (centrality, brokers, who connects to whom) made visible and queryable below specialist-unit level for the first time |
| Bottleneck | Network reasoning has historically required specialist tools (i2/Gotham-class) that don't reach routine casework | Addressed directly — this is the platform's clearest differentiator (per the prior phase's strategic-differentiation finding) |
| Decision point | Whether/how to act on a structural finding (e.g., removing a "central" actor) | Unchanged, and deliberately so — the platform describes structure, it does not recommend disruption actions, given the documented risk that removing a central actor can fragment a network into more numerous, harder-to-track factions |

### 8.5 Missing Person

| | Today | With the platform |
|---|---|---|
| Workflow | Manual cross-record search for matches against existing databases | Faster cross-record search with explicit confidence on any candidate match |
| Bottleneck | Urgency vs. thoroughness trade-off under time pressure | The platform reduces search time without changing the urgency judgment itself |
| Decision point | When an ambiguous case escalates beyond routine handling | Unchanged — escalation judgment remains human, informed by faster information, not delegated to a threshold the platform sets unilaterally |

### 8.6 Repeat Offender Investigation

| | Today | With the platform |
|---|---|---|
| Workflow | Manual recall of "have I seen this before" by individual officers | Statistically-grounded MO-similarity surfacing (once validated and released per the capability roadmap) and place/time pattern context |
| Bottleneck | This pattern-recognition skill currently depends on years of personally-accumulated case memory (Phase 2's expertise findings) | Directly democratizes access to pattern recognition that previously required tenure, without claiming the resulting suggestion is itself a conclusion |
| Decision point | Whether a surfaced similarity is operationally meaningful | Unchanged |

### 8.7 Emerging Crime Pattern Investigation

| | Today | With the platform |
|---|---|---|
| Workflow | An analyst or supervisor notices a pattern only if they happen to see enough cases across stations to recognize it | Cross-station pattern/trend surfacing available proactively to analysts, not dependent on one person's incidental visibility across cases |
| Bottleneck | Patterns that span multiple stations are the least visible of all, since no individual officer sees the whole picture | Directly addressed — this is the clearest "Crime Pattern Discovery/Trend Detection" use case in the entire journey set |
| Decision point | Whether a surfaced pattern warrants a resourcing or strategic response | Unchanged — remains a District Supervisor/Senior Leadership judgment, informed but not made by the platform |

---

## 9. Human-AI Collaboration Philosophy

### 9.1 Division of responsibility

| Always the investigator | Best assisted by AI | Never the AI |
|---|---|---|
| Deciding what to investigate next | Retrieving and cross-referencing records | Generating a person-level risk score |
| Judging a witness's credibility in person | Surfacing cross-case patterns and similarity scores | Producing a narrative offender-characteristic profile |
| Forming and revising hypotheses | Reconciling conflicting timelines and flagging contradictions | Correlating any output with caste, religion, or community, directly or by proxy |
| Deciding when evidence is sufficient to act | Translating and structuring exportable products | Recommending an arrest, charge, or verdict |
| Signing the chargesheet | Maintaining conversational context across a session | Contacting external institutions (banks, telecoms) autonomously |
| Assessing diagnosticity of a specific fact in a specific case | Visualizing network structure, timelines, and hotspots | Modifying any official record |

### 9.2 How disagreement is handled

If the platform's retrieved evidence conflicts with an investigator's working theory, it presents the conflict neutrally — what was found, where it came from, why it's inconsistent with the stated theory — and stops there. **It does not insist, escalate its framing, or repeat the contradiction with growing emphasis if the investigator proceeds anyway.** The disagreement is logged (so a supervisor or auditor can see it occurred) precisely so the investigator's authority does not need to be enforced by the platform overriding them — accountability is preserved through visibility, not through the platform asserting its own conclusion was correct.

### 9.3 How trust is established — progressively, not asserted

Per the Human-AI Interaction guidelines this report draws on (Amershi et al., 2019, CHI), setting accurate expectations about system capability and reliability is foundational to all subsequent trust — and overclaiming early is harder to recover from than underclaiming. This product's trust-building sequence mirrors the capability rollout already established in the prior phase: an investigator should be able to rely on retrieval and cross-referencing (Capabilities A, B) long before being asked to weigh a statistically-validated MO-similarity score (Capability E) or a place-time forecast (Capability D) — trust is built bottom-up, on the platform's most-evidenced capabilities first, not asserted uniformly across a feature list on day one.

### 9.4 How explainability appears — by default, not on demand

Most reviewed platforms (per the prior phase's benchmark) treat explainability as a button to click, separate from the answer itself. This product's commitment is the opposite: **the source and confidence of an answer are part of the answer**, not a secondary disclosure. A deeper, full reasoning-trace view should also exist — for supervisor review, audit, or an investigator who genuinely wants to dig in — but its existence is additive, not a substitute for explainability being present by default in the first, fastest answer the investigator sees.

---

## 10. Conversational Experience Principles

The conversation is the product, so each of the brief's specific questions is answered directly, grounded in Phase 2/3's cognitive and tradecraft findings and in the Amershi et al. (2019) Human-AI Interaction guidelines (organized, in the original research, into behavior at first use, during interaction, when the system is wrong, and over time — the same four moments structure this section).

### 10.1 At first use and at the start of each conversation

**How investigations begin:** Anchored to a case where one exists — the platform should already know which case the investigator is working from context (Capability A's session state), not require them to re-establish it. A free-standing query mode exists separately for cross-case/analyst use (Persona 7.2) where no single case is the anchor.

**How investigators ask questions:** In ordinary spoken or typed language, in English or Kannada, with no special query syntax — this is the entire point of Conversational Intelligence as a mandatory requirement, and any departure from natural phrasing is a design failure, not a user-training gap to close later.

### 10.2 During interaction

**How AI understands intent:** By first classifying, internally, whether a question is a *retrieval* question ("what do we know") or a *reasoning* question ("what does this mean") — and being honest in the answer's framing about which one it actually answered, since these carry very different confidence profiles.

**How context is preserved:** Session-level memory tied to the active case, with a visible, checkable indicator of what the platform currently treats as context — directly operationalizing Guideline 12 ("remember recent interactions") while avoiding the opposite failure (silently carrying forward outdated context the investigator has since moved past).

**How follow-up conversations work:** An investigator should be able to return to a case days later and resume, including being shown a brief recap of where the conversation left off — extending session memory across, not just within, a single sitting.

**How evidence is referenced:** Every factual claim carries a specific, checkable source (case number, exhibit ID, record ID) inline with the claim, not bundled into a generic "sources" list at the end the investigator has to manually cross-reference back.

**How uncertainty is communicated:** Through structured, consistent confidence language — not vague hedging ("might be," "possibly") and not false precision (a specific percentage implying more rigor than the underlying evidence supports) — directly applying Phase 3's Words-of-Estimative-Probability finding (Section 3.2 there) at the interface level.

**How confidence is presented:** Visually and verbally distinct from the answer's content, so an investigator skimming under time pressure cannot mistake a low-confidence answer for a high-confidence one — operationalizing Guideline 2 ("make clear how well the system can do what it can do") as a per-answer property, not a one-time onboarding disclosure.

**How conflicting evidence is handled:** Surfaced explicitly as a finding in its own right ("Record A states X; Record B states Y; these conflict") rather than silently resolved by picking one source or averaging — directly extending Phase 2's source-reconciliation findings (Section 5.3 there) into interface behavior.

**When AI asks clarifying questions:** Only when the ambiguity would materially change the answer — not reflexively. Over-asking under caseload pressure is its own trust failure (Section 2.2), so the bar for interrupting the investigator with a question is deliberately higher than the bar for simply answering with appropriately scoped confidence and letting the investigator correct it if needed.

### 10.3 When the system is wrong, uncertain, or asked to overstep

**When AI refuses to answer:** When answering would require producing one of Section 5's excluded categories (a person-level risk inference, a demographic-correlated suspicion, a narrative offender characterization) — and the refusal states specifically why, naming the boundary, rather than a generic "I can't help with that." A generic refusal reads as the platform being unhelpful; a specific one reads as the platform being principled — these are different trust outcomes for what is structurally the same action.

**When AI recommends actions:** It doesn't recommend actions in the directive sense — but it can surface precedent ("in similar past cases, X was a commonly taken next step") framed explicitly as informational pattern, not instruction. The distinction is not cosmetic: a directive frame implies the platform has weighed the current case's specifics and reached a conclusion about what should happen; an informational frame makes clear it has only retrieved what happened elsewhere, leaving the weighing to the investigator.

**When AI remains silent:** When there is no grounded evidence for what's being asked. Silence, or an explicit "I don't have evidence for this," is the correct behavior here — not a fluent, plausible-sounding answer manufactured to avoid seeming unhelpful. This is the single most important behavioral commitment in this entire section, given Phase 3's finding (Section 10.2 there) that confident-seeming fabrication is mechanistically harder to detect than an obvious capability gap.

### 10.4 Over time

**How conversations transition into timelines, maps, network graphs, and reports:** As a natural extension of an existing answer — an investigator who asks "show me how these events relate over time" should get a timeline generated from the same underlying, already-cited facts, not be redirected to a separate tool and asked to re-specify the question. The visualization is a different *view* of an answer already given, never a separate analytical pass the investigator has to trigger and interpret independently.

**Sustained use:** As an investigator's trust in specific capabilities grows (Section 9.3), the platform should reflect that — surfacing more of its reasoning trace by default for a power user (Persona 7.2's Crime Analyst) than for a first-time user, without ever making the underlying source/confidence information harder to reach for either.

---

## 11. Product Scope

The platform will:

- Answer natural-language questions (English/Kannada, text/voice) grounded in the state's existing crime records, with visible source and confidence on every answer.
- Surface cross-case patterns, aliases, and similarities that a human would otherwise need years of accumulated case memory to recognize.
- Visualize relationships, timelines, and aggregate spatial/temporal patterns as natural extensions of a conversational answer.
- Generate statistically-validated MO/behavioral similarity scores (once released per the capability roadmap), with stated accuracy, never a narrative characterization.
- Forecast place-and-time crime patterns at the aggregate level (once released), never a person-level risk.
- Surface aggregate structural/environmental context (once released, with external legal/ethics review complete), never demographic-correlated suspicion.
- Produce exportable, source-carrying products (e.g., PDF summaries) for case-diary or chargesheet use.
- Log every query and output for audit, and enforce role-based access aligned to existing organizational hierarchy.

---

## 12. Out-of-Scope Items

The platform will never:

- Generate a person-level predictive risk score of any kind.
- Generate a narrative offender-characteristic profile presented as established fact.
- Correlate any output with caste, religion, or community identity — directly, or by proxy variable.
- Recommend an arrest, a charge, or assert a conclusion about guilt or innocence.
- Contact, query, or act on external institutions (banks, telecoms, other agencies) autonomously.
- Modify, delete, or directly edit any official record.
- Produce an answer without an accompanying source and confidence indicator — there is no "quick mode" that skips this.
- Operate as a sole decision-maker in any process where an investigator currently holds that authority.

These are not features deferred to a later version. With the partial exception of the capabilities still pending release (D, E, F per the prior phase's roadmap), these are permanent boundaries, not a current-limitation list.

---

## 13. Governance Principles

1. **Governance is structural, not optional.** Every capability's output passes through the same confidence/source/access layer before reaching a user — this was established as the single highest-leverage design decision in the prior phase's report and is restated here as a product commitment, not just a capability-architecture one.
2. **The riskiest capabilities carry the strictest release gates.** Place/time forecasting and structural context analysis do not ship until governance has been demonstrated in production on lower-risk capabilities first (Section 5, Principle 5).
3. **Audit logs are themselves access-controlled and reviewed by a party independent of the platform's own reporting.** An auditor's trust requirement (Persona 7.8) specifically excludes taking the platform's self-report at face value.
4. **Every boundary violation, however minor, is treated as a governance event, not a bug ticket.** Given the demonstrated pattern (Phase 3) that available safeguards are skipped under real institutional pressure, this product treats near-misses as signal, not noise.
5. **No capability is released on the strength of technical readiness alone.** Statistical validation (Capability E) and external legal/ethics review (Capability F) are release conditions, not best-practice suggestions.

---

## 14. Responsible AI Principles

1. **Human authority is preserved structurally, in what the product refuses to do, not only in what it states it values.** Section 12's exclusions are the operative expression of this principle; everything else is supporting detail.
2. **Confidence is communicated honestly, even when honesty means admitting the platform doesn't know.** This is treated as more important to the platform's long-term trust than appearing consistently capable (Section 10.3).
3. **Bias mitigation is a design input, not an audit output.** The Habitual-Offenders-Act-specific exclusion (Section 12) was identified and designed against *before* any version of the relevant capability was built — bias review precedes release, it does not follow a complaint.
4. **Explainability is a default behavior, not a feature flag.** Every output is explainable by construction (Section 9.4); nothing requires special configuration to become auditable.
5. **The platform's own limitations are disclosed as plainly as its capabilities.** This includes disclosing, to leadership and to investigators, the genuinely unresolved risks carried forward from the prior phase's risk register (e.g., that automation bias is not fully solved by confidence annotations alone) — overstating this platform's reliability would itself be a governance failure.

---

## 15. Success Metrics

| Dimension | Metric | Measurement caution |
|---|---|---|
| Operational | Median time from query to actionable answer, vs. current manual baseline | Should be measured per persona — an IO's "actionable" and an analyst's "actionable" are different thresholds |
| Investigator productivity | Reduction in time spent on manual cross-referencing and triple data entry | Risk of measuring time saved without checking whether evidentiary quality held constant or improved — both must be tracked together |
| Cognitive burden | Self-reported reduction in working-memory load for timeline/network tasks (qualitative) | Self-report is the only practical measure here, and should be treated as directional, not precise — consistent with this report's general caution about overstating measurement precision |
| Intelligence quality | Rate of validated cross-case links surfaced that an assigned IO had not already identified | The most operationally meaningful metric in this table, and also the hardest to measure reliably without a retrospective audit process |
| Adoption | Active use rate across rank/station, specifically checking whether adoption concentrates only among already tech-comfortable officers | A flat adoption number can mask exactly the inequity (junior/rural officers least served) this product exists to address |
| Conversation effectiveness | Rate of follow-up clarifications needed per resolved query | Should fall over time as the platform's intent-classification improves, but should not be optimized so aggressively that genuinely ambiguous queries stop being clarified (Section 10.2's stated trade-off) |
| Trust | Voluntary, repeated use by experienced investigators specifically (Persona 7.1) — the population most able to function without the platform | A more meaningful trust signal than overall usage, since experienced investigators have the least to gain from a tool that isn't genuinely good |
| Explainability | Percentage of outputs with complete, checkable source/confidence annotation | Should be 100% by design (Section 9.4) — any measured shortfall here is a defect, not a target to gradually improve |
| Operational accuracy | Precision/recall of cross-case and MO-linkage suggestions against retrospectively known ground truth | Per Phase 3's calibration findings, accuracy and stated confidence should be evaluated jointly — a system can be accurate on average while still being poorly calibrated case-by-case |
| Decision support quality | Supervisor/court-facing assessment of whether platform-assisted findings strengthened or weakened a chargesheet's defensibility | The most consequential metric in this table and the hardest to gather systematically — likely requires direct, periodic review rather than automated tracking |
| Challenge 01 compliance | Full mapping against the Challenge Traceability Matrix established in the prior phase | Binary per requirement — every mandatory item is either demonstrably met within its defined scope, or it is not |

---

## 16. Executive Recommendations

1. **Sequence trust-building deliberately.** Launch with the capabilities carrying the strongest evidence (retrieval/synthesis, cross-case resolution) and the structural governance layer beneath them; do not launch any version that includes the riskier capabilities (place/time forecasting, behavioral linkage, structural context) without their respective release gates demonstrably satisfied.
2. **Treat Kannada parity as a launch-blocking requirement, not a localization pass.** A platform that performs well in English and poorly in Kannada has not met Challenge 01's stated requirement, regardless of overall capability.
3. **Build the "show your work" behavior into the answer format itself, before any other UX polish.** Every other product principle in this report depends on this one being true from the first release, not added later.
4. **Instrument the success metrics in Section 15 from day one, especially adoption-by-persona and the supervisor/court-facing defensibility metric** — both are the metrics most likely to reveal a problem (e.g., a tool that only experienced, tech-comfortable officers use, or that creates more legal exposure than it resolves) that simpler usage statistics would miss.
5. **Revisit this product vision after the first release cycle**, specifically checking whether the "augmentation, not automation" commitment (Section 4) held under real deployment pressure — consistent with the prior phase's own finding that this is a prediction, not yet a measurement, for this specific platform.

---

## Closing Note

This document translates the capability strategy into a lived experience for eight distinct people who will actually touch this platform — and its central commitment is the same one that has run through every phase of this research program: **trust is built through demonstrated, checkable behavior, not through confident design language.** Every principle in this report can be falsified by observing the product directly — does every answer carry a source, does the platform ever generate an excluded output, does an auditor's review confirm what the logs claim — and that falsifiability is deliberate. A product vision that cannot be checked against the product's actual behavior is not a governing specification; it is a slogan.

*This report builds on the Strategic Capability Formulation Report and Phases 1–3's validated research, adding the Amershi et al. (2019, CHI) Guidelines for Human-AI Interaction as new supporting evidence for the conversational-design principles in Section 10. It proposes product vision and experience principles only — no architecture, AI model, or implementation technology — and, like every phase before it, has not been validated against KSP/SCRB's actual investigators, supervisors, or governance capacity.*
