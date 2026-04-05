---
title: "Reconfiguration Context Analysis Track"
artifact: SPEC-088
track: implementable
status: Active
author: cristos
created: 2026-04-05
last-updated: 2026-04-05
type: feature
parent-epic: ""
parent-initiative: INITIATIVE-004
linked-artifacts:
  - SPEC-070
  - SPEC-081
  - INITIATIVE-006
depends-on-artifacts:
  - SPEC-070
  - SPEC-081
addresses: []
evidence-pool: "school-integration-policy"
source-issue: ""
swain-do: required
---

# Reconfiguration Context Analysis Track

## Problem Statement

The site presents the FY27 budget and transportation analysis as if reconfiguration started in 2025. It did not. South Portland ran a year-long Boundaries and Configurations process in 2023-2024 with a steering committee, community engagement forums, and board deliberations that produced specific May 2024 action items: investigate magnet programs, controlled choice, triennial attendance zone review, and resource equity for high-need schools. National research (TCF nine-districts report) validates several of these approaches as best practice for voluntary integration.

This history is missing from the site. The `school-integration-policy` trove captures the SPSD Boundaries page and the TCF report, but does not yet include the community engagement findings, steering committee reports, or board meeting minutes that tell the full story. Residents reading the site have no way to connect the current reconfiguration to the process that preceded it.

The "Transportation" nav entry also implies the site has only one analytical lens beyond budget briefings. A second analysis track — reconfiguration context — belongs alongside it.

## Desired Outcomes

1. The site has an "Analysis" section with two tracks: Transportation Analysis (existing) and Reconfiguration Context (new).
2. The Reconfiguration Context page tells the full 2024 process story — community engagement, steering committee, board deliberations, decisions — grounded in primary sources.
3. National research findings are bridged to South Portland's situation without editorializing.
4. An accountability checklist tracks the May 2024 action items with factual delivery status, accessible but not the primary framing.
5. The homepage presents both analysis tracks as peers alongside the general briefings.
6. The pipeline's keyword-triggered reference context (SPEC-081) surfaces 2024 findings in briefings where relevant topics arise.

## External Behavior

### Phase 1: Trove expansion

The `school-integration-policy` trove currently has 2 sources. Before building the site page, expand it with:

- Board meeting minutes from the 2024 Boundaries & Configurations process
- Community engagement session summaries or reports
- Steering committee findings or recommendations
- The consultant report on magnet programs and controlled choice (if publicly available; if not, document the gap)
- Annual attendance zone demographic report (if published; if not, document the gap)

Update the trove synthesis to reflect the expanded source base. Update keyword triggers in the manifest to cover new content.

### Phase 2: Site restructure

**Navigation change:**
- "Transportation" nav item becomes "Analysis"
- `/analysis/` landing page indexes two tracks as cards:
  - Transportation Analysis (links to existing `/transportation-analysis/`)
  - Reconfiguration Context (links to new `/analysis/reconfiguration-context/`)

**New page — `/analysis/reconfiguration-context/`:**

Content flows in three parts:

1. **The 2024 process** — What happened during the Boundaries & Configurations review. Who was involved (steering committee, community forums, Board). What the community said. What the steering committee recommended. How the Board deliberated. What they decided in May 2024. Sourced from trove materials, presented as factual narrative.

2. **Research bridge** — What the TCF nine-districts report finds about voluntary integration (system-wide goals, controlled choice with free transportation, detracking). Where South Portland's 2024 directives align with best practice. Where they do not yet reach (no system-wide targets, no detracking policy, intra-district only). Presented as context, not judgment.

3. **Accountability checklist (collapsible)** — The May 2024 Board action items listed with delivery status:
   - Delivered / Not yet delivered / Unknown
   - Factual status only, no commentary on what gaps mean
   - Rendered as a collapsible/expandable section so it is findable but not the lead

**Source attribution footer** consistent with site conventions.

**Homepage changes:**
- The "Budget Briefings" section becomes "Briefings & Analysis" with a 4-card grid:
  - General Budget Briefing
  - Upcoming Meeting Briefing
  - Transportation Analysis
  - Reconfiguration Context
- The standalone "Transportation Analysis" section lower on the page is removed (now represented in the top grid)
- Budget Community Lenses and Transportation Community Lenses sections remain below unchanged

### Phase 3: Briefing integration (two-pass)

**Pass 1:** Run after trove expansion is complete. The expanded trove synthesis and keyword triggers feed into SPEC-081's reference context injection system. No manual briefing edits needed — the pipeline handles injection when a briefing paragraph matches a trigger keyword (`boundaries`, `controlled choice`, `magnet`, `attendance zone`, `guiding principles`, `steering committee`, `integration`, `detracking`, etc.).

**Pass 2:** Regenerate briefings. The LLM draws on the injected 2024 context where relevant. Not every persona will trigger it — a student persona discussing band cuts will not get integration research. A community member discussing attendance boundaries will.

### Constraints

- No adversarial framing. The 2024 process narrative, the research bridge, and the accountability checklist present facts. They do not editorialize about what gaps mean or assign blame for undelivered items.
- The accountability checklist is collapsible — present but not the primary reading experience.
- Trove expansion must precede site page construction (Phase 1 before Phase 2).
- Briefing regeneration requires trove expansion to be complete (Phase 1 before Phase 3).
- Site restructure (Phase 2) and briefing regeneration (Phase 3) can proceed in parallel after Phase 1.

## Acceptance Criteria

- AC-1: The `school-integration-policy` trove contains at least 4 primary sources covering the 2024 process (board minutes, community engagement, steering committee, and/or consultant findings). Gaps are documented in the synthesis.
- AC-2: The site nav shows "Analysis" instead of "Transportation" and the landing page indexes both tracks.
- AC-3: `/analysis/reconfiguration-context/` renders the three-part page (process narrative, research bridge, collapsible accountability checklist) sourced from the expanded trove.
- AC-4: The homepage "Briefings & Analysis" section shows 4 peer cards (2 general briefings + 2 analysis tracks).
- AC-5: The standalone "Transportation Analysis" homepage section is removed.
- AC-6: After briefing regeneration, at least one persona briefing that discusses attendance boundaries or integration topics includes 2024 context drawn from the trove. Personas that do not trigger relevant keywords have no 2024 content injected.
- AC-7: The accountability checklist is rendered as a collapsible element, not a primary page section.
- AC-8: No adversarial or editorializing language appears in the reconfiguration context page or in briefings that received 2024 context injection.

## Scope & Constraints

**In scope:**
- Trove expansion with 2024 process sources
- Nav restructure (Transportation -> Analysis)
- New reconfiguration context page
- Homepage layout update
- Two-pass briefing regeneration via SPEC-081

**Out of scope:**
- New community-lens briefings for the reconfiguration track (future work)
- Inter-district analysis (Hartford/Louisville style)
- Consultant report content if not publicly available (document the gap)
- Changes to the transportation analysis pages or content

## Implementation Approach

Three phases with a dependency gate:

1. **Phase 1 — Trove expansion:** Collect additional 2024 sources via browser automation and web fetch. Normalize to markdown. Update manifest, synthesis, and keyword triggers. Commit to trunk.

2. **Phase 2 — Site restructure:** Rename nav, create Analysis landing page, build reconfiguration context page from trove content, update homepage layout. Depends on Phase 1 completion.

3. **Phase 3 — Briefing integration:** Run pipeline with expanded trove context. Two passes: first to verify trigger injection, second to regenerate briefings. Depends on Phase 1 completion. Can run in parallel with Phase 2.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Spec written | 2026-04-05 | — | — |
