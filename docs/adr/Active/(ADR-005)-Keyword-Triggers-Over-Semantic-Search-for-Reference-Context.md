---
title: "Keyword Triggers Over Semantic Search for Reference Context"
artifact: ADR-005
track: standing
status: Active
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
linked-artifacts:
  - INITIATIVE-003
  - INITIATIVE-006
  - DESIGN-002
  - SPEC-081
depends-on-artifacts: []
evidence-pool: "school-integration-policy"
---

# Keyword Triggers Over Semantic Search for Reference Context

## Context

The evidence pipeline interprets meeting content through persona lenses but has no mechanism for injecting historical or reference context from non-meeting troves. When a school board meeting discusses "controlled choice" or "attendance zones," the interpreter lacks the background that the district explored these concepts in a 2023-2024 steering committee process and that national research (TCF, 2016) documents outcomes from nine districts that tried these approaches.

The question is how to conditionally inject this reference material: always, by semantic similarity, or by keyword match.

## Decision

Use curated keyword trigger lists stored in trove manifests. At interpretation time, a lightweight string scan of the meeting content checks for trigger matches. When any trigger hits, the matched trove's synthesis is injected into the prompt as a `<reference_context>` block.

The prompt explicitly instructs the LLM to use reference context only where the meeting content engages with the topic, and not to flag absences. Absence tracking is handled by the fold layer's existing thread lifecycle mechanism.

## Alternatives Considered

**Semantic search (embedding-based retrieval).** Would catch conceptual matches when speakers use different phrasing. Rejected because: (1) municipal meeting speakers reuse the same domain terms consistently — the vocabulary is small and stable; (2) embedding infrastructure adds dependencies (vector store, embedding model, similarity threshold tuning) to a pipeline that currently runs on flat files and `claude -p`; (3) failure modes are harder to diagnose than a missing keyword. Revisit if the project expands to cover unstructured community input with unpredictable phrasing.

**Always-inject all reference context.** Simple to implement. Rejected because: (1) risks biasing the LLM to find connections that aren't there, violating the project's editorial guardrail against adversarial framing; (2) wastes prompt tokens on irrelevant context; (3) makes interpretation non-reproducible depending on which troves exist at any given time.

**Two-pass interpretation (blind first, then with context).** Most thorough but doubles LLM cost per meeting per persona. Rejected as disproportionate for the current project scale.

## Consequences

**Positive:**
- No new infrastructure dependencies. Trigger matching is string comparison in Python.
- Trigger lists are auditable — you can read the manifest and know exactly which terms activate which context.
- False negatives are visible and fixable: if a meeting uses an unanticipated term, it shows up when reviewing briefs, and the trigger list gets updated.
- Editorial discipline is preserved: interpretation stays grounded in what was said, fold tracks temporal patterns, briefs surface gaps.

**Accepted downsides:**
- Trigger lists require manual curation per trove source. This is low-effort for 15 troves but scales linearly.
- Conceptual matches without shared vocabulary will be missed. A speaker saying "bringing different neighborhoods together" won't trigger "integration" unless that synonym is added.
- Trigger specificity matters — overly broad triggers (e.g., "school") would inject context into every meeting. Lists need periodic review.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-04 | -- | Decision adopted after discussion of semantic search trade-offs |
