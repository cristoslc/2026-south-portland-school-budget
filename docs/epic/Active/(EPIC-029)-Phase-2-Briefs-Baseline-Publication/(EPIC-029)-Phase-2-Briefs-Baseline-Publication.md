---
title: "Phase 2 Briefs & Baseline Publication"
artifact: EPIC-029
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
parent-vision: VISION-001
parent-initiative: INITIATIVE-005
priority-weight: medium
success-criteria:
  - Per-persona Phase 2 briefs generated integrating independent projection findings
  - Briefs include explicit testable predictions (e.g., "if enrollment is above X by FY29, the closure savings assumption was wrong")
  - Independent enrollment baseline published to the site
  - Methodology and assumptions page published for transparency
depends-on-artifacts:
  - EPIC-027
  - EPIC-028
addresses: []
evidence-pool: ""
---

# Phase 2 Briefs & Baseline Publication

## Goal / Objective

Integrate the independent enrollment projection findings (EPIC-028) back into per-persona briefs and publish the enrollment baseline to the site. Phase 2 briefs go beyond gap identification (Phase 1) to provide the independent analysis that fills those gaps. The baseline publication frames projections with testable predictions so the community can evaluate in future years whether the closure was justified by demographic trends.

## Desired Outcomes

Each persona receives an updated brief that says not just "this data was missing" but "here's what the data shows." The published baseline becomes a standing public resource: transparent assumptions, reproducible methodology, and explicit predictions that create accountability over time. If enrollment recovers to X by FY29, the community has a documented basis for revisiting the closure decision.

## Scope Boundaries

**In scope:**
- Per-persona Phase 2 brief generation through interpretation pipeline
- Enrollment baseline summary page for the site
- Methodology and assumptions page (how the model works, what inputs it uses, how to update it)
- Testable prediction formulation for each scenario bracket
- Publication via [INITIATIVE-004](../../../initiative/Active/(INITIATIVE-004)-Public-Budget-Site/(INITIATIVE-004)-Public-Budget-Site.md)

**Out of scope:**
- Model construction (EPIC-028)
- Data acquisition (EPIC-026)
- Transportation analysis (INITIATIVE-006)

## Child Specs

| Artifact | Title | Status |
|----------|-------|--------|
| SPEC-067 | Enrollment Phase 2 Persona Briefs | Active |
| SPEC-068 | Enrollment Baseline Site Page | Active |

## Key Dependencies

- EPIC-027 (Phase 1 briefs — establishes the gap framing that Phase 2 fills)
- EPIC-028 (projection model — produces the data Phase 2 briefs present)
- Interpretation pipeline ([INITIATIVE-003](../../../initiative/Active/(INITIATIVE-003)-Interpretation-Pipeline/(INITIATIVE-003)-Interpretation-Pipeline.md))
- Site infrastructure ([INITIATIVE-004](../../../initiative/Active/(INITIATIVE-004)-Public-Budget-Site/(INITIATIVE-004)-Public-Budget-Site.md))

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of INITIATIVE-005; user-approved |
