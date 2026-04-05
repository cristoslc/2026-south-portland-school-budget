---
title: "Retro: Keyword-Triggered Reference Context"
artifact: RETRO-2026-04-04-keyword-triggered-reference-context
track: standing
status: Active
created: 2026-04-04
last-updated: 2026-04-04
scope: "SPEC-081 implementation — from trove collection through pipeline integration"
period: "2026-04-04"
linked-artifacts:
  - ADR-005
  - SPEC-081
  - DESIGN-002
  - INITIATIVE-003
  - INITIATIVE-006
---

# Retro: Keyword-Triggered Reference Context

## Summary

Single-session arc from research collection through implemented pipeline feature. Collected two web sources into a new `school-integration-policy` trove, discussed integration strategy, decided on keyword triggers over semantic search, wrote ADR-005 and SPEC-081, then implemented with TDD + BDD + smoke tests. 5 files changed, 585 insertions, fully tested.

## Artifacts

| Artifact | Title | Outcome |
|----------|-------|---------|
| ADR-005 | Keyword Triggers Over Semantic Search for Reference Context | Active |
| SPEC-081 | Keyword-Triggered Reference Context Injection | Implemented (pending merge) |
| Trove: school-integration-policy | B&C page + TCF integration report | Created with 2 sources + 12 triggers |

## Reflection

### What went well

- **Design discussion produced a clean, minimal implementation.** The conversation moved from "how should this be integrated?" through semantic search evaluation to a concrete mechanism in a natural flow. The implementation landed at 106 lines — no over-engineering.
- **TDD cycles were tight and productive.** Red-green-refactor worked cleanly: 12 unit tests written first, all failed on import, implementation landed, all green. Then integration changes, full suite still green (261 existing + 12 new).
- **Smoke test against real bundles validated the design.** Running against actual meeting transcripts confirmed that municipal speakers use domain terms verbatim. The Dec 2025 meeting explicitly said "boundaries and configurations, AKA redistricting" — the exact trigger terms.
- **Trove → pipeline integration path is now established.** Adding `triggers` to manifest sources is a lightweight, auditable way to wire reference troves into interpretation. No schema migration, no new infrastructure.

### What was surprising

- **The SPSD B&C page required Chrome automation.** The `webpage-to-markdown` MCP tool returned only nav boilerplate — the page content is JS-rendered. Chrome browser automation was the reliable fallback. This is consistent with the prior learning about gov data portals.
- **The two user-provided URLs were thematically linked in a non-obvious way.** The B&C page mentions "magnet programs" and "controlled choice" — the exact strategies the TCF report documents outcomes for across 9 districts. The trove synthesis surfaced this connection.
- **Dec 2025 school board meeting triggered correctly.** Initially looked like a false positive but turned out the meeting explicitly discussed B&C. The trigger mechanism is more precise than expected — 2 occurrences of "boundaries" and 2 of "configurations" in a 156K-char transcript.

### What would change

- **BDD tests should be part of the initial test plan, not a reminder.** The user specified "TDD, BDD, smoke test" upfront. Unit tests were written first (good), but BDD integration tests required a prompt. The full test chain should be planned as distinct deliverables from the start.
- **The prompt f-string injection point could be cleaner.** Inserting `{reference_context_block}` into a 100-line f-string between `</instruction>` and `<meeting_context>` works but is fragile — any future prompt restructuring needs to account for the injection point. A builder pattern or template system would be more maintainable at scale.

### Patterns observed

- **Discussion → ADR → SPEC → implement in one session works** when the design space is small and the operator has clear opinions. The conversation itself served as the brainstorming phase.
- **Keyword triggers are the right abstraction for curated, domain-specific corpora.** Municipal meetings have stable vocabulary. The trigger list for `school-integration-policy` has 12 terms across 2 sources — manageable and auditable. Revisit if trove count exceeds ~30 or community input sources are added.

## Learnings captured

| Item | Type | Summary |
|------|------|---------|
| feedback_retro_bdd_in_test_plan.md | memory | BDD tests are a distinct deliverable — plan them alongside unit tests, not as an afterthought |
| feedback_retro_js_page_fallback.md | memory | Extend prior Chrome automation learning: webpage-to-markdown silently degrades on JS-rendered pages |
