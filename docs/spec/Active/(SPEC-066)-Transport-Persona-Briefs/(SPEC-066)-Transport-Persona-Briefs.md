---
title: "Transport Persona Briefs"
artifact: SPEC-066
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
type: feature
parent-epic: EPIC-032
linked-artifacts:
  - INITIATIVE-006
  - SPEC-065
depends-on-artifacts:
  - SPEC-065
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Transport Persona Briefs

## Problem Statement

The transport configuration comparison (SPEC-065) produces the analytical foundation. Each persona needs to receive these findings in their own frame — Maria needs to know about split-building mornings, David needs the dollar figure, Linda needs the governance record, Dana needs the contradictions.

## Desired Outcomes

15 persona-specific transportation briefs plus 1 general brief, published to the site. Each brief leads with fiscal exposure, grounds in family logistics, frames with governance context (the chronological record of transport questions asked and not answered).

## External Behavior

**Inputs:**
- Transport configuration comparison (SPEC-065 output)
- Transportation claims catalog (SPEC-054 output) — the governance timeline
- Existing persona definitions (PERSONA-001 through PERSONA-015)
- Interpretation pipeline (INITIATIVE-003)

**Outputs:**
- 15 persona-specific transport briefs in `dist/briefings/transportation/`
- 1 general transport brief for non-persona audiences
- Published to site via INITIATIVE-004

**Persona-specific framing (key examples):**
- **Maria (001):** Split-family count, before/after care gap, "how many mornings will I spend doing split-building drop-offs?"
- **David (002):** Fiscal exposure total, comparison to claimed savings, "this is the bill nobody's talking about"
- **Rachel (008):** Configuration comparison focused on her family's specific situation, ride time implications
- **Tom (006):** Unfunded mandate total, per-household cost implications
- **Linda (007):** Governance timeline — questions asked, not answered, vote taken without this analysis
- **Dana (009):** The contradiction: voted on reconfiguration without transport modeling, administration said cost "not significant" without having modeled it
- **Priya (005):** Equity dimension — who rides longest, McKinney-Vento impact on vulnerable families

**Constraints:**
- Must use existing interpretation pipeline
- Tone: rigorous and factual, interventionist framing, open invitation to district
- Each brief must disclose known limitations and data gaps

## Acceptance Criteria

- Given the comparison data and 15 personas, when briefs are generated, then each persona receives a brief in their specific frame
- Given the general brief, when read by a non-expert, then the configuration comparison and fiscal exposure are accessible
- Given the governance timeline from SPEC-054, when included in briefs, then the chronological pattern of deferral is visible
- Given publication, when deployed, then briefs are accessible alongside existing persona briefings on the site

## Scope & Constraints

**In scope:** Brief generation, publication.
**Out of scope:** New analysis. V2 optimization findings.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-032 |
