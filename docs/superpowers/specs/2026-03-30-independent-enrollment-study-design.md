# Independent Enrollment Study — Initiative Design

## Context

The South Portland School Board is voting on permanent closure of Kaler Elementary as part of an $8.4M structural budget gap. The administration cites declining enrollment (3,085 → 2,744 students, -11% since 2015-16; elementary specifically 1,401 → 1,080, -23% in 4 years) as the primary structural driver. However, no independent enrollment projections have been published. The board is making an irreversible infrastructure decision without answering whether the decline is structural or cyclical, without modeling the impact of LD 1829 housing density, CDS pre-K expansion (80-90 four-year-olds in FY27), or multilingual learner pipeline sensitivity to federal policy shifts (1% → 17% since 2015).

## Intent

This initiative produces an independent, evidence-based enrollment analysis with two phases:

**Phase 1 (immediate):** Expose the gaps in the district's published enrollment assumptions. Per-persona briefs with interventionist framing — not neutral gap identification, but "here's what you need to know before this decision gets made, and here's what nobody has shown you yet." Each persona receives the message in their own frame.

**Phase 2 (sustained):** Build a 5-year cohort survival projection model with scenario brackets that serves as a testable baseline. Not point estimates, but ranges under explicit assumptions — baseline trend continuation, housing density absorption, multilingual learner pipeline shifts, CDS pre-K ramp.

## Position in Architecture

This initiative is **upstream** of:
- INITIATIVE-001 (Budget Lever Analysis) — lever savings depend on enrollment assumptions
- INITIATIVE-003 (Interpretation Pipeline) — persona briefs consume enrollment findings
- INITIATIVE-004 (Public Budget Site) — enrollment projections published to site

## Scope

**In scope:**
- Audit of district-published enrollment claims mapped to source evidence
- Data acquisition via swain-search troves: Maine DOE grade-level enrollment, DHHS birth records, city housing permits, school choice transfer data
- Cohort survival model with grade-level resolution, 5-year horizon (FY27–FY31)
- Scenario brackets: baseline, LD 1829 housing absorption, multilingual learner pipeline shifts, CDS pre-K ramp
- Per-persona Phase 1 briefs (gap analysis, interventionist tone)
- Per-persona Phase 2 briefs (projection findings integrated)
- Structured enrollment data outputs for downstream consumption

**Stretch goals (data-gated):**
- Building-level capacity analysis (functional capacity vs. seat count given SPED/ELL/behavioral space needs)
- Building-level enrollment projections (census block overlay with catchment zone boundaries)

**Out of scope:**
- Route-level transportation modeling (separate initiative)
- Advocacy for or against closure

**Known limitations to disclose:**
- No access to Infinite Campus (district SIS) data
- School choice transfer records may not be publicly available at district level
- Building-level stretch goals gated on data acquisition feasibility

## Epic Decomposition

**EPIC A: Enrollment Data Acquisition** — Trove collection via swain-search. Maine DOE grade-level enrollment (10+ years), DHHS birth records by municipality, city housing permits, school choice transfer data. Also: extract and catalog every enrollment claim and assumption from existing evidence pools.

**EPIC B: Enrollment Gap Analysis & Phase 1 Briefs** — (Depends on A) Audit district's published enrollment basis against what a responsible closure decision requires. Document each gap: what question should have been answered, what evidence exists, what's missing, why it matters. Per-persona briefs through interpretation pipeline. Interventionist tone.

**EPIC C: Cohort Survival Model & 5-Year Projections** — (Depends on A) Build demographic projection model. Grade-level cohort survival with retention/attrition rates. Layer in birth rate pipeline, housing absorption, multilingual learner sensitivity, CDS ramp. Scenario brackets. Structured data output.

**EPIC D: Phase 2 Briefs & Baseline Publication** — (Depends on B, C) Integrate projection findings into per-persona briefs. Publish independent baseline to site. Frame with testable predictions.

**SPIKE (under EPIC A): Building-Level Data Feasibility** — Time-boxed investigation of building-level data availability. District presentation room counts, FOAA request viability, census block overlay approach. Gates stretch goals.

## Success Criteria

1. Every enrollment assumption in the district's closure recommendation identified, sourced, assessed as supported/unsupported/unpublished
2. Phase 1 persona briefs published before City Council budget adoption
3. Cohort survival model produces 5-year projections with at least 3 scenario brackets
4. Projection data structured and consumable by INITIATIVE-001
5. Phase 2 persona briefs published with explicit testable predictions
6. Known limitations disclosed transparently in every deliverable
