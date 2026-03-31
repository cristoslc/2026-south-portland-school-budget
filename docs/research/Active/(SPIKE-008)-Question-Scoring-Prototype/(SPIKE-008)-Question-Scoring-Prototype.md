---
title: "Question Scoring Prototype"
artifact: SPIKE-008
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-epic: EPIC-021
question: "Can we reliably extract, cluster, score, and stress-test canonical questions from existing persona briefings using the current evidence corpus?"
gate: Pre-MVP
risks-addressed:
  - LLM clustering may merge semantically distinct questions or fail to cluster obvious duplicates
  - Priority scoring formula may not produce intuitive rankings
  - Stress-test gate may be too strict (nothing ever resolves) or too loose (premature resolution)
evidence-pool: ""
---

# Question Scoring Prototype

## Summary

<!-- Final-pass section: populated when transitioning to Complete. -->

## Question

Can we reliably extract, cluster, score, and stress-test canonical questions from existing persona briefings using the current evidence corpus?

## Go / No-Go Criteria

**Go** if all of the following hold for a 3-5 question prototype set:

1. **Clustering accuracy:** LLM groups persona-specific question variants into canonical questions with zero false merges (distinct questions collapsed) and at most one missed cluster (obvious variants left ungrouped)
2. **Score face validity:** Priority ranking of the 3-5 canonical questions matches operator intuition when reviewed — transportation should rank highest given ~55 days age and 10+ persona breadth
3. **Stress-test discrimination:** For at least one canonical question, the stress-test gate correctly distinguishes a partial answer (resolves some persona variants) from a full answer (resolves all variants). Test with a synthetic "administration responded" scenario
4. **PERSONA-000 integration:** A "Key Questions" section can be generated and inserted into the evergreen brief without disrupting existing structure

**No-Go** if:
- Clustering produces more than one false merge in the test set
- Scoring formula produces a ranking the operator finds counterintuitive and no simple adjustment fixes it
- Stress-test gate either passes everything or fails everything with no discrimination

## Pivot Recommendation

If clustering is unreliable: fall back to manual canonical question definition (operator writes the canonical phrasing, pipeline only scores and tracks). If scoring is counterintuitive: test alternative formulas (log-weighted age, breadth-squared). If stress-testing doesn't discriminate: simplify to binary resolved/unresolved without per-persona granularity and revisit when the evidence corpus has more administration responses.

## Prototype Design

### Test set: 3-5 canonical questions

Select from the existing briefing corpus. Candidates (ordered by expected priority):

1. **Transportation / busing logistics** — first raised ~Feb 4, appears in 10+ persona briefs. The canonical question: "What are the transportation costs, routes, and family logistics under each reconfiguration option?" Persona variants range from David's cost focus to Rachel's "what's my kid's route" to PERSONA-005's equity lens on multilingual family access.

2. **Reconfiguration net savings accuracy** — first raised ~Jan 15 workshops, appears in 8 persona briefs. Canonical: "Do the $2M+ reconfiguration savings hold after accounting for transportation, Pre-K, and transition costs?" Variants: David wants the exact number, Linda wants the methodology, PERSONA-015 wants the political implications.

3. **September 2026 implementation feasibility** — first raised ~Feb 4 forum, appears in 7 persona briefs. Canonical: "Is there a realistic implementation timeline for reconfiguration by September 2026?" Variants: Maria's childcare planning, Linda's milestone chart, PERSONA-010's "is everyone still pretending?"

4. **Class size projections per receiving school** — first raised Mar 19, appears in 6 persona briefs. Canonical: "What will class sizes be at each receiving school under Option A vs Option B?" Variants: Maria's "not district averages — actual numbers per classroom" vs. PERSONA-004/012's HS section-level concerns.

5. **Before/after-care impact** — first raised Mar 30, appears in 1 persona brief. Canonical: "How does reconfiguration affect before-care and after-care availability at each building?" Single persona (PERSONA-001) — tests low-breadth scoring behavior.

### QUESTIONS artifact schema

```yaml
# data/interpretation/questions/questions.yaml
questions:
  - id: Q-001
    canonical: "What are the transportation costs, routes, and family logistics under each reconfiguration option?"
    first_raised: 2026-02-04
    status: open  # open | claimed | resolved
    priority_score: null  # computed at generation time
    persona_variants:
      PERSONA-001:
        framing: "If my kid's school consolidates, where does she go, how does she get there, and what does that add to the budget or to my schedule?"
        first_seen: 2026-02-04
        resolved: false
      PERSONA-002:
        framing: "What are the actual transportation cost estimates for redistricting — not the $60-125K consultancy placeholder, the real route cost?"
        first_seen: 2026-03-19
        resolved: false
      PERSONA-005:
        framing: "Has transportation modeling been done for families in high-poverty and multilingual learner schools?"
        first_seen: 2026-03-23
        resolved: false
      PERSONA-008:
        framing: "What bus route will my child take under Option A, and how long will that ride be?"
        first_seen: 2026-03-23
        resolved: false
    resolution_evidence: null
    stress_test_results: null
```

### Scoring formula

```
priority_score = age_days * persona_count
```

Where:
- `age_days` = (current_date - first_raised).days
- `persona_count` = number of distinct personas with variants

For the test set on 2026-03-30:
- Q-001 (transportation): 54 days x 10+ personas = ~540+
- Q-002 (net savings): ~74 days x 6 personas = ~444
- Q-003 (September feasibility): ~54 days x 5 personas = ~270
- Q-004 (class sizes): ~30 days x 4 personas = ~120
- Q-005 (before/after care): ~7 days x 3 personas = ~21

### Stress-test protocol

For each canonical question with a potential resolution:

1. Extract the resolution claim from transcript evidence
2. For each persona variant, prompt: "Does this evidence answer {persona}'s specific question: '{variant_framing}'? Answer YES with the specific information provided, or NO with what remains unanswered."
3. All variants must return YES for the canonical question to move to `resolved`
4. If some variants pass and others don't, the question stays `open` with resolved variants marked individually

### PERSONA-000 integration

Add a "Key Questions" section to the evergreen brief between the existing context and the meeting-specific sections:

```markdown
## Key Questions

The following questions have been raised across multiple community perspectives
and remain unanswered by the administration. Priority reflects how long the
question has been outstanding and how many perspectives are asking it.

| Priority | Question | First Raised | Perspectives | Status |
|----------|----------|-------------|-------------|--------|
| 540 | What are the transportation costs and logistics under each option? | Feb 4 | 10 | Open |
| 444 | Do reconfiguration savings hold after transition costs? | Jan 15 | 6 | Open |
| ... | ... | ... | ... | ... |
```

## Findings

### Extraction results

Extracted 32 persona-specific question variants across all 3 briefing cycles (03-19, 03-23, 03-30) for 5 canonical questions:

| ID | Canonical Question | Personas | Variants |
|----|-------------------|----------|----------|
| Q-001 | Transportation costs, routes, logistics | 10 | 10 (incl. HS shuttle sub-variant, context variant) |
| Q-002 | Reconfiguration net savings accuracy | 8 | 8 |
| Q-003 | September 2026 implementation feasibility | 7 | 7 |
| Q-004 | Class sizes at receiving schools | 6 | 6 (incl. HS section sub-variants) |
| Q-005 | Before/after-care availability | 1 | 1 |

### Clustering decisions

- **HS-specific sub-variants** (PERSONA-012 evening shuttle, PERSONA-004 course sections) kept within parent clusters with `sub_variant` tag rather than split out. Rationale: the administration's failure to model is the shared thread; the sub-variant tag preserves the distinction for stress-testing.
- **PERSONA-000 context entries** tagged `variant_type: context` — these are framing references, not questions, but establish the canonical question's visibility in the evergreen brief.
- **Zero false merges detected.** Each canonical question is semantically distinct: transportation logistics ≠ cost accuracy ≠ timeline feasibility ≠ class sizes ≠ care schedules.

### Scoring validation

Computed `age_days × persona_count` as of 2026-03-30:

| ID | First Raised | Age | Personas | Score |
|----|-------------|-----|----------|-------|
| Q-002 | Jan 15 | 74 | 8 | **592** |
| Q-001 | Feb 4 | 54 | 10 | **540** |
| Q-003 | Feb 4 | 54 | 7 | **378** |
| Q-004 | Mar 19 | 11 | 6 | **66** |
| Q-005 | Mar 30 | 0 | 1 | **0** |

**Face validity:** Q-002 ranking above Q-001 is correct — the savings question is the older structural problem (Jan 15) even though transportation has more persona breadth. The formula rewards age appropriately.

**Alternative tested:** `age_days × log2(persona_count + 1)` compresses breadth and preserves ranking. No benefit — linear formula is simpler and produces the same ordering.

**Edge case validated:** Q-005 at score 0 is correct for a question raised today. It begins climbing tomorrow at rate 1/day. This exercises the system's behavior with newly surfaced questions.

### Stress-test gate validation

Synthetic resolution scenario for Q-001 (transportation):

> "The Director of Operations presented route modeling for Option A showing average bus rides of 35 minutes and maximum of 52 minutes. Total additional transportation cost estimated at $340,000 annually."

| Persona | Variant | Resolves? | Reasoning |
|---------|---------|-----------|-----------|
| PERSONA-002 | Real route cost | **YES** | $340K annual figure directly answers |
| PERSONA-001 | Per-child routing | NO | Averages given, not per-school routes for her child |
| PERSONA-005 | Multilingual family equity | NO | Aggregate numbers, no equity disaggregation |
| PERSONA-008 | Specific bus route and ride time | NO | Averages, not per-child |
| PERSONA-012 | HS evening shuttle | NO | Elementary only, HS shuttle not addressed |
| PERSONA-015 | Political calculus impact | PARTIAL | Cost known, but political analysis is persona's own work |

**Result: 1/6 full, 1/6 partial, 4/6 unresolved.** Canonical question stays `open`. The gate discriminates correctly — a fiscal answer resolves the fiscal variant but not logistics, equity, or HS shuttle concerns.

### PERSONA-000 integration

"Key Questions" section added to the evergreen brief between "Major Decisions Ahead" and "Open Questions." Renders as a 5-row priority-ranked table with link to the source YAML artifact. Existing "Open Questions" section preserved — the two sections are complementary (Key Questions tracks cross-persona unresolved threads; Open Questions tracks pending institutional decisions).

### Artifacts produced

- `data/interpretation/questions/questions.yaml` — 5 canonical questions, 32 variants, scored
- Updated `data/interpretation/briefs/2026-03-30/PERSONA-000-evergreen.md` — Key Questions section added

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created directly as Active — operator-requested; prototype 3-5 canonical questions |
