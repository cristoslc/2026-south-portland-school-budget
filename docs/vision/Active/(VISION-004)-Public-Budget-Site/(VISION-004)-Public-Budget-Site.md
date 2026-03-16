---
title: "Public Budget Site"
artifact: VISION-004
track: standing
status: Active
product-type: personal
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
depends-on-artifacts:
  - VISION-001
  - VISION-002
  - VISION-003
evidence-pool: ""
---

# Public Budget Site

## Target Audience

South Portland residents — parents, teachers, taxpayers, students, school board members, journalists, and community advocates who want to understand the FY27 school budget and its implications. The initial audience is the South Portland community; the vision accommodates future sites for other civic analysis projects.

## Value Proposition

Give residents a place to find answers to the budget questions they're actually asking — not a document dump, not a meeting archive, but a question-first interface that draws on AI-analyzed meeting records and budget documents to provide sourced, persona-aware answers with full transparency about methodology and limitations.

## Problem Statement

The analysis outputs from VISION-001/002/003 (evidence pools, persona interpretations, cumulative narratives, briefings) exist as structured markdown in a git repository. They are comprehensive and well-organized for a technical audience but completely inaccessible to the South Portland residents they're meant to serve. There is no public-facing surface for this work.

## Existing Landscape

- **District website** — publishes agendas and meeting videos but no analysis or synthesis
- **Local news** (Sentry, Forecaster) — covers headlines but not the sustained, multi-meeting narrative arcs that the interpretation pipeline captures
- **No independent budget analysis site** exists for South Portland
- **General civic tech** (BallotReady, OpenSecrets) — covers elections and campaign finance, not municipal budgets

## Build vs. Buy

Tier 3 — build from scratch. No existing platform provides question-first navigation over AI-generated civic analysis with inline source citations and community feedback. The closest analogs (static documentation sites, civic dashboards) don't support the persona-routing and temporal narrative model that makes this analysis distinctive. Astro as a static site generator provides the right balance of content-collection tooling and component flexibility without a heavy runtime.

## Maintenance Budget

Low-moderate during budget season (Mar-Jun 2026). The site rebuilds automatically from pipeline outputs — ongoing effort is limited to triaging community feedback (flags, question suggestions) and occasional question curation. After the budget vote, maintenance drops to archival — the site becomes a record of the budget season.

## Success Metrics

- Residents can find answers to their primary budget questions within two clicks from the landing page
- At least one question answer or briefing is shared in a public forum (school board meeting, community group, local news)
- Community members submit question suggestions or flag inaccuracies (evidence the feedback loop works)
- Site rebuilds automatically after pipeline runs without manual intervention

## Non-Goals

- Advocating for specific budget outcomes — the site is descriptive, not prescriptive
- Replacing official district communications
- Building a general-purpose civic analysis platform (though the architecture should be reusable)
- Real-time data — the site reflects the state of the analysis as of the last pipeline run
- Native mobile app — responsive web is sufficient

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-16 | — | Created directly in Active; design validated through brainstorming session |
