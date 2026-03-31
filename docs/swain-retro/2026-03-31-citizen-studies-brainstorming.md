---
title: "Retro: Citizen Studies Brainstorming & Decomposition"
artifact: RETRO-2026-03-31-citizen-studies
track: standing
status: Active
created: 2026-03-31
last-updated: 2026-03-31
scope: "INITIATIVE-005 and INITIATIVE-006 — brainstorming, artifact creation, decomposition to specs, initial data acquisition"
period: "2026-03-30 — 2026-03-31"
linked-artifacts:
  - INITIATIVE-005
  - INITIATIVE-006
  - EPIC-026
  - EPIC-027
  - EPIC-028
  - EPIC-029
  - EPIC-030
  - EPIC-031
  - EPIC-032
  - EPIC-033
  - SPIKE-009
  - SPIKE-010
---

# Retro: Citizen Studies Brainstorming & Decomposition

## Summary

In a single extended session, two new initiatives were brainstormed, designed, created, decomposed into 8 epics + 2 spikes + 21 specs, and partially executed through initial data acquisition across 6 troves. An early course correction — grounding analysis in the project's existing evidence pools rather than producing generic textbook responses — led to sharper, evidence-specific framing. The session also produced the project's first original analytical finding: South Portland is likely a net student importer, meaning the enrollment decline is demographic rather than behavioral.

## Artifacts

| Artifact | Title | Outcome |
|----------|-------|---------|
| INITIATIVE-005 | Independent Enrollment Study | Active — fully decomposed, data acquisition partially complete |
| INITIATIVE-006 | Independent Transportation Analysis | Active — fully decomposed, data acquisition partially complete |
| EPIC-026..029 | Enrollment epics (data, gap analysis, model, publication) | Active — SPEC-048/051/052 executed |
| EPIC-030..032 | Transport epics (data, modeling, briefs) | Active — SPEC-053/054/055 executed |
| EPIC-033 | Configuration Space Optimization (V2) | Proposed — stretch goal |
| SPIKE-009 | Building-Level Data Feasibility | Active — not yet investigated |
| SPIKE-010 | Walk Zone & Pedestrian Infrastructure Audit | Active — not yet investigated |

## Reflection

### What went well

1. **Brainstorming grounded in evidence produced sharp framing.** An early course correction forced the analysis to draw directly from the project's existing evidence pools — meeting transcripts, budget documents, persona briefs — rather than producing generic research summaries. This produced genuinely useful strategic insights, like the distinction between "the district hasn't analyzed this" vs. "the district explicitly confirmed no analysis exists and none will be done before the vote." The latter is much more powerful and came from reading the actual transcripts.

2. **Persona-informed metric design.** When asked which transport metrics to prioritize, the agent consulted the existing persona briefs rather than guessing. This surfaced the three-tier priority structure (fiscal exposure leads, family logistics grounds, governance accountability frames) directly from what the personas were already telling us.

3. **Getting the tone right required iteration.** The first draft of INITIATIVE-006's strategic focus was adversarial — implying the administration refused to do its job. The revised framing is factual and inviting: "the district has not published estimates... these estimates would benefit from district data... contributions are welcome." This is stronger in a public context because it's unimpeachable — it states what's missing without assigning blame.

4. **Autonomous decomposition works when the scope is pre-validated.** After thorough brainstorming alignment on both initiatives, the full decomposition (21 specs, 6 troves) proceeded without needing to stop for additional decisions. The brainstorming phase front-loaded the hard choices; execution was mechanical.

5. **Data quality questioning caught a significant error.** The initial school choice analysis estimated 730-930 students not enrolled in South Portland public schools — a 20-25% gap. Sensitivity analysis on the census age brackets revealed this was wrong: once pre-school-age children are subtracted from the under-18 count, public enrollment likely *exceeds* the resident school-age population. The corrected finding — that South Portland is a net student importer — is more interesting and more useful than the incorrect estimate it replaced.

### What was surprising

1. **The other worktree.** A parallel session had already created its own decomposition of INITIATIVE-005 with different artifact numbering (EPIC-022..025, SPEC-039..047) and had collected the NCES enrollment data. This created a numbering collision that needs reconciliation — a known hazard of concurrent worktree-based development.

2. **Maine DOE data is harder to access than expected.** The enrollment data is behind a SharePoint link requiring authentication, and the ELSI tool requires JavaScript interaction. The NCES CCD data (from the other worktree) was the viable alternative. The transport expenditure data was more accessible — a direct PDF download from Maine DOE.

3. **South Portland as net student importer.** This was the session's most significant analytical finding and it was discovered by accident — the school choice transfer analysis (SPEC-052) was supposed to estimate outflow, but the sensitivity analysis revealed the enrollment *exceeds* the estimated school-age population. This reframes the entire enrollment narrative: the decline isn't families leaving, it's fewer children being born/living in South Portland.

### What would change

1. **Check for parallel worktrees before starting decomposition.** The artifact numbering collision was avoidable. Before creating new epics and specs, check `git worktree list` and scan for active work on the same initiative. This is a process gap.

2. **Start with data acquisition feasibility, not spec writing.** The session wrote 21 specs before discovering that some data sources (Maine DOE enrollment) were harder to access than assumed. A quick spike on data availability before full decomposition would have produced a more realistic spec set.

3. **The initial generic response wasted time.** The first response was a textbook "here's what an enrollment study covers" summary that didn't draw on any of the project's existing evidence. With 12 evidence pool sources, 15 persona briefs, and detailed synthesis documents already in the repo, the analysis should have been grounded in project-specific data from the start. The lesson: always read the existing evidence before framing new work.

4. **Transport expenditure data should include multiple years.** Only FY25 was collected. The synthesis notes this gap, but the spec should have been scoped for 3-year trend data from the beginning.

### Patterns observed

1. **Brainstorming through execution in a single session works when autonomy is pre-authorized.** The key enabler was a clear delegation: make reasonable choices, produce a first pass, flag decisions for review. Without this, the session would have stalled at spec decomposition waiting for approval on each of 21 specs.

2. **Domain expertise surfaces through targeted skepticism.** The most valuable human contributions weren't writing specs or designing artifacts — they were sharp questions that steered the work away from errors: questioning the scope of a full enrollment study, asking whether the administration had legitimate reasons for not producing transport estimates, and flagging suspicious data quality in the census analysis.

3. **Worktree isolation creates merge debt.** This session and the parallel session both created valid work that now needs reconciliation. The worktree model is good for isolation during active work but creates a coordination cost for convergent initiatives.

4. **Claims catalogs as first-class deliverables.** The enrollment and transportation claims catalogs (SPEC-051, SPEC-054) turned out to be more than intermediate data — the chronological record of questions asked and not answered is itself a powerful document. The transport claims synthesis ("The Chronological Pattern") tells a governance accountability story that the persona briefs can use directly.

## Learnings captured

| Item | Type | Summary |
|------|------|---------|
| feedback_first_pass_preferred.md | memory (already written) | Prefer rough first pass over blocking on decisions |
| feedback_retro_check_parallel_worktrees.md | memory (new) | Check for parallel worktrees before creating new artifacts on the same initiative |
| feedback_retro_ground_in_evidence.md | memory (new) | Never give generic responses when rich project evidence exists — read the repo first |
| project_retro_net_importer.md | memory (new) | South Portland is likely a net student importer — enrollment decline is demographic not behavioral |
