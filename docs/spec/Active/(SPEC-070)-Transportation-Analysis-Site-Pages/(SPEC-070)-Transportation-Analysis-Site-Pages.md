---
title: "Transportation Analysis Site Pages"
artifact: SPEC-070
track: implementable
status: Active
author: cristos
created: 2026-03-31
last-updated: 2026-03-31
type: feature
parent-epic: EPIC-019
linked-artifacts:
  - INITIATIVE-004
  - INITIATIVE-006
depends-on-artifacts:
  - EPIC-014
  - SPEC-065
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Transportation Analysis Site Pages

## Problem Statement

The transportation analysis ([INITIATIVE-006](../../initiative/Active/(INITIATIVE-006)-Independent-Transportation-Analysis/(INITIATIVE-006)-Independent-Transportation-Analysis.md)) produced six analysis documents, a structured comparison JSON, and 16 persona briefs — all in `dist/transportation-analysis/`. The site has no pages for this content. The configuration comparison table, the fiscal exposure findings, and the per-persona transport briefs need to be accessible as a coherent section on the site.

## Desired Outcomes

The site has a `/transportation-analysis` section that presents the independent transportation analysis as a self-contained body of work. The capstone comparison table is the centerpiece, with drill-down into individual metrics and persona-specific briefs.

## External Behavior

**Content collection changes:**
- Add a `transportBriefings` collection in `site/src/content.config.ts` loading from `../dist/transportation-analysis/briefings/`
- Add a `transportAnalysis` collection loading from `../dist/transportation-analysis/*.md` (the 6 analysis docs + README)
- Add schema fields: `topic`, `source_specs` array (from transport brief frontmatter)
- Load `transport-comparison.json` as structured data for the comparison table component

**New pages:**
- `/transportation-analysis` — Landing page rendering `dist/transportation-analysis/README.md`. Features the configuration comparison table prominently (rendered from `transport-comparison.json`), links to individual analyses and methodology.
- `/transportation-analysis/methodology` — Renders `dist/transportation-analysis/METHODOLOGY.md`. The assumption tables are the key content — every estimate with its source and what would replace it.
- `/transportation-analysis/[slug]` — Individual analysis pages (split-family model, McKinney-Vento, etc.)
- `/transportation-analysis/briefings` — Index of transport persona briefs
- `/transportation-analysis/briefings/[slug]` — Individual transport persona brief pages

**Configuration comparison component:**
- Render the comparison table from `transport-comparison.json` as an interactive or well-formatted HTML table
- Highlight Option A vs. Option B contrast (the core finding)
- Show fiscal exposure as percentage of claimed savings
- Link each metric row to its source analysis page

**Navigation:**
- Add "Transportation Analysis" to the site's main navigation
- Cross-link from persona pages to their transport briefing
- Cross-link from the enrollment study section (the initiatives are related)

## Acceptance Criteria

- Given the transport content collections, when the site builds, then all 6 analysis docs and 16 briefs load without errors
- Given the `/transportation-analysis` landing page, when a visitor arrives, then the comparison table is visible and each configuration's fiscal exposure is clear
- Given `transport-comparison.json`, when rendered as a table, then all metrics show ranges (not point estimates) and link to source analyses
- Given the methodology page, when a visitor reads it, then every assumption is documented with what district data would replace it
- Given the briefing index, when a visitor browses, then each persona's transport brief is listed and linked
- Given a non-expert reader, when they land on the comparison page, then the key finding (Option A's exposure vs. claimed savings) is understandable within 10 seconds

## Scope & Constraints

**In scope:** Content collections, pages, comparison table rendering, navigation.
**Out of scope:** New analysis (INITIATIVE-006 handles that). Interactive route maps. V2 optimization results (EPIC-033). Custom chart/visualization components beyond the comparison table.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-31 | — | User-requested; site integration for INITIATIVE-006 deliverables |
