---
title: "Independent Enrollment Study"
artifact: INITIATIVE-005
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision:
  - VISION-001
priority-weight: high
success-criteria:
  - Every enrollment assumption in the district's closure recommendation identified, sourced, and assessed as supported/unsupported/unpublished
  - Phase 1 persona briefs published before City Council budget adoption
  - Cohort survival model produces 5-year projections with at least 3 scenario brackets (baseline, housing growth, migration shift)
  - Projection data structured and consumable by INITIATIVE-001 lever analysis
  - Phase 2 persona briefs published with explicit testable predictions
  - Known limitations disclosed transparently in every deliverable
depends-on-artifacts: []
addresses:
  - JOURNEY-002.PP-03
  - JOURNEY-001.PP-03
evidence-pool: ""
linked-artifacts:
  - INITIATIVE-001
  - INITIATIVE-003
  - INITIATIVE-004
---

# Independent Enrollment Study

## Strategic Focus

Produce an independent, evidence-based enrollment analysis that exposes the gaps in the district's published enrollment assumptions and builds a 5-year projection model with scenario brackets serving as a testable baseline for all downstream budget analysis.

The district is proposing permanent closure of Kaler Elementary based on declining enrollment (3,085 → 2,744 students, -11% since 2015-16; elementary 1,401 → 1,080, -23% in 4 years). But no independent enrollment projections have been published. The board is making an irreversible infrastructure decision without answering whether the decline is structural or cyclical, without modeling LD 1829 housing density impact, CDS pre-K expansion (80-90 four-year-olds in FY27), or multilingual learner pipeline sensitivity to federal policy (1% → 17% since 2015).

This initiative is **upstream** of [INITIATIVE-001](../(INITIATIVE-001)-Budget-Lever-Analysis/(INITIATIVE-001)-Budget-Lever-Analysis.md) (lever savings depend on enrollment assumptions), [INITIATIVE-003](../(INITIATIVE-003)-Interpretation-Pipeline/(INITIATIVE-003)-Interpretation-Pipeline.md) (persona briefs consume enrollment findings), and [INITIATIVE-004](../(INITIATIVE-004)-Public-Budget-Site/(INITIATIVE-004)-Public-Budget-Site.md) (enrollment projections published to site).

## Desired Outcomes

Residents understand what enrollment assumptions underlie the closure decision and can evaluate whether those assumptions are supported by evidence. The district faces public pressure to either release its internal projections or justify the decision without them. Within 6 months, an independent 5-year enrollment projection with scenario brackets exists as a public resource, enabling anyone to test the district's assumptions as new enrollment data arrives each fall.

For each persona: Maria knows whether her kids' school is at risk based on demographic trends, not just this year's budget math. Tom can evaluate whether closure savings hold up under different enrollment futures. Linda has the governance ammunition to demand projections before voting. Priya can see whether enrollment shifts are concentrating impact on the district's most vulnerable populations.

## Scope Boundaries

**In scope:**
- Audit of district-published enrollment claims and assumptions, mapped to source evidence
- Data acquisition via swain-search troves: Maine DOE grade-level enrollment history (10+ years), DHHS municipal birth records, city housing permit data, school choice transfer flows
- Cohort survival model with grade-level resolution for South Portland K-12
- 5-year projection (FY27-FY31) with scenario brackets: baseline trend continuation, LD 1829 housing density absorption, multilingual learner pipeline shifts (federal policy sensitivity), CDS pre-K mandate ramp
- Per-persona Phase 1 briefs highlighting gaps in the decision basis (interventionist tone — "here's what you need to know before this decision gets made, and here's what nobody has shown you yet")
- Per-persona Phase 2 briefs integrating independent projection findings
- Structured enrollment data outputs consumable by [INITIATIVE-001](../(INITIATIVE-001)-Budget-Lever-Analysis/(INITIATIVE-001)-Budget-Lever-Analysis.md) and the site

**Stretch goals (data-gated):**
- Building-level capacity analysis (functional capacity vs. seat count given growing SPED/ELL/behavioral space needs)
- Building-level enrollment projections (census block demographic overlay with catchment zone boundaries)

**Out of scope:**
- Route-level transportation modeling (separate initiative)
- Advocacy for or against closure — the deliverable is the missing analysis, not a recommendation

**Known limitations to disclose in deliverables:**
- No access to Infinite Campus (district SIS) data
- School choice transfer records may not be publicly available at district level
- Building-level stretch goals gated on data acquisition feasibility

## Tracks

**Track 1 — Gap Exposure (Phase 1):** Data acquisition + gap analysis + Phase 1 persona briefs. Time-sensitive — must land before City Council budget adoption.

**Track 2 — Independent Baseline (Phase 2):** Cohort survival model + 5-year projections + Phase 2 persona briefs + site publication. Sustained work with longitudinal value.

## Child Epics

| Artifact | Title | Status | Track |
|----------|-------|--------|-------|
| EPIC-022 | Enrollment Data Acquisition | Active | Both |
| EPIC-023 | Enrollment Gap Analysis & Phase 1 Briefs | Active | Track 1 |
| EPIC-024 | Cohort Survival Model & 5-Year Projections | Active | Track 2 |
| EPIC-025 | Phase 2 Briefs & Baseline Publication | Proposed | Track 2 |

## Small Work (Epic-less Specs)

_None currently._

## Key Dependencies

- **Evidence pools (existing):** fy27-budget-documents, school-board-budget-meetings, city-council-meetings-2026
- **Data acquisition (needed):** Maine DOE grade-level enrollment, DHHS vital records, city housing permits
- **Infrastructure:** Interpretation pipeline ([INITIATIVE-003](../(INITIATIVE-003)-Interpretation-Pipeline/(INITIATIVE-003)-Interpretation-Pipeline.md)) for persona briefs; site ([INITIATIVE-004](../(INITIATIVE-004)-Public-Budget-Site/(INITIATIVE-004)-Public-Budget-Site.md)) for publication
- **Downstream consumers:** [INITIATIVE-001](../(INITIATIVE-001)-Budget-Lever-Analysis/(INITIATIVE-001)-Budget-Lever-Analysis.md) (lever analysis depends on enrollment projections)

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created from brainstorming session; user-requested |
