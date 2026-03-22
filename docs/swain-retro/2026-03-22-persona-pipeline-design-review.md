---
title: "Retro: Persona Pipeline and Design Review"
artifact: RETRO-2026-03-22-persona-pipeline-design-review
track: standing
status: Active
created: 2026-03-22
last-updated: 2026-03-22
scope: "PERSONA-015 creation, pipeline catch-up, persona-lens design review"
period: "2026-03-22"
linked-artifacts:
  - PERSONA-015
  - INITIATIVE-004
  - EPIC-017
  - DESIGN-001
  - ADR-003
  - SPEC-028
  - SPEC-029
  - SPEC-030
  - SPEC-031
  - SPEC-032
  - SPEC-033
---

# Retro: Persona Pipeline and Design Review

## Summary

Third session pass on the static site, focused on three threads: (1) creating PERSONA-015 (Cross-Building Staff Advocate) from a community member's letter, (2) running the full interpretation pipeline to catch up the new persona across 21 meetings, and (3) conducting a persona-lens design review that produced 4 code fixes and 5 new specs. Also decomposed INITIATIVE-004 into 6 concrete epics, activated EPIC-017 (Question Hub), and created SPEC-028 (privacy-respecting analytics).

## What was accomplished

- **PERSONA-015 created** — Cross-Building Staff Advocate, generalized from a specific community letter to avoid doxxing
- **Full pipeline catch-up** — 21 interpretations + 21 cumulative folds + 1 briefing for the new persona (~2 hours wall time)
- **INITIATIVE-004 decomposed** — 6 epics (2 Complete, 1 Active, 3 Proposed), fixed stale linked-epic IDs
- **EPIC-017 (Question Hub) activated** — operator chose approach C (auto-extract + curate)
- **Design review** — 4 code fixes shipped, 5 specs created for future work
- **ADR-003 + DESIGN-001** created as standing docs for Astro and accessibility decisions

## Reflection

### What went well

- **Persona generalization was the right call.** The original letter was from a named district employee in a specific role. Generalizing to "cross-building staff advocate" protects privacy while preserving the archetype's distinctive insight: someone who sees operational inequities across all schools that single-building personas can't see.
- **The pipeline catch-up worked end-to-end.** New persona definition -> interpret 21 meetings -> fold 21 cumulative records -> generate briefing. The `--persona` flag on each script kept it scoped. The poll_interpret orchestrator detected the gaps automatically.
- **Persona-lens design review surfaced real issues.** Looking at the site as Maria, Tom, Jaylen, Linda, and Meg exposed problems that pure accessibility/visual review missed: the duplicate h1, missing persona routing, no TL;DR for sharing, student-hostile tone.
- **Batching decisions was efficient.** Three operator decisions (question sourcing, feedback mechanism, activation priority) answered in one message, unblocking three workstreams simultaneously.

### What was surprising

- **The pipeline crashed twice during fold step.** The poll_interpret process died silently at fold #18 and again at fold #18 on the second run. The later folds have larger cumulative context and the `claude -p` subprocess may be timing out or hitting memory limits. Had to finish the last 3 folds manually with individual `fold_meeting.py` calls.
- **The category map is duplicated across 5 files.** Adding PERSONA-015 required editing the same map in index.astro, briefings/index.astro, briefings/[...slug].astro, personas/index.astro, and personas/[id].astro. This is a maintenance smell — should be a shared component or data file.

### What would change

- **Extract the category map to a shared data file.** A single `src/data/personas.ts` that exports the map, used by all pages. Adding a persona shouldn't require editing 5 files.
- **Add pipeline resilience for late-stage folds.** The crash at fold #18 suggests the cumulative context is getting too large for a single subprocess call. Options: checkpoint and resume, or split the fold into summary + delta instead of full resynth.
- **Run the design review earlier.** The persona-lens review found issues that should have been caught before the first deploy. A review checklist ("walk through as each persona type") would prevent this.

### Patterns observed

- **Privacy in civic tech is a real constraint.** In a small district, role titles are personally identifying. "Multilingual Coordinator" = one specific person. The generalization approach (archetype over individual) should be the default for all personas.
- **Pipeline catch-up is the bottleneck for new personas.** Adding a persona takes 5 minutes to define but 2 hours to process through the interpretation pipeline. This is a strong argument for the question-first approach (EPIC-017) — questions can be seeded from existing briefings without per-persona pipeline runs.
- **Design reviews should be persona-driven from the start.** The WCAG/contrast/font-size review caught technical issues. The persona-lens review caught user experience issues. Both are necessary, in that order.

## Learnings captured

| Memory file | Type | Summary |
|------------|------|---------|
| feedback_retro_category_map.md | feedback | Category map duplicated across 5 files — extract to shared data |
