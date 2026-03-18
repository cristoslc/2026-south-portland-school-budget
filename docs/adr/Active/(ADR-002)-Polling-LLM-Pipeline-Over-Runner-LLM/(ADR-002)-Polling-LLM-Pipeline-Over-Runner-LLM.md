---
title: "Polling LLM Pipeline Over Runner-Based LLM"
artifact: ADR-002
track: standing
status: Active
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
linked-artifacts:
  - EPIC-012
  - EPIC-013
  - SPIKE-007
  - VISION-003
  - INITIATIVE-003
depends-on-artifacts: []
trove: ""
---

# Polling LLM Pipeline Over Runner-Based LLM

## Context

The interpretation pipeline has two fundamentally different kinds of work:

1. **Deterministic scraping** — connectors download from Vimeo, Diligent, and budget pages; normalizers transform VTT/PDF/HTML to markdown; bundlers group evidence by meeting date. These are stateless, fast, and need no secrets beyond API keys already on the runner.

2. **LLM inference** — per-meeting interpretation, cumulative fold, and brief generation all call `claude -p` (Claude CLI). These require an authenticated Claude session, consume Max subscription capacity, and produce large structured outputs.

EPIC-012 and SPIKE-007 were framed around installing and authenticating the Claude CLI on the self-hosted GitHub Actions runner. This approach has several problems:

- **Authentication complexity.** `claude login` requires an interactive browser flow. Persisting credentials on an ephemeral Docker runner means either baking secrets into the image or re-authenticating per run — neither is clean.
- **Coupling.** Tying LLM calls to the runner means a runner outage or Docker rebuild blocks the entire interpretation chain, not just evidence collection.
- **Rate/cost opacity.** LLM calls running unattended on a cron schedule with no human in the loop risk hitting rate limits or producing garbage without anyone noticing.
- **Wrong execution model.** The runner is designed for polling external sources and committing results. LLM inference is a different class of work — longer-running, higher-value, and benefits from human review before results are committed.

## Decision

Split the pipeline into two independent tracks:

- **Track 1 — Deterministic (runner).** The self-hosted runner continues to run evidence collection on a cron schedule, exactly as it does today via `pipeline.yml`. It also runs meeting bundling as a new post-evidence step, since bundling is deterministic. When new or changed bundles are detected, it signals readiness (e.g., by committing a manifest or pushing a tag).

- **Track 2 — LLM inference (local polling).** A local machine (or any machine with an authenticated Claude session) polls for new evidence/bundles — either by watching git for upstream changes or by checking a signal file. When it detects work, it runs the interpretation → fold → brief chain. Results are committed and pushed after optional human review.

The two tracks are decoupled: Track 1 produces inputs that Track 2 consumes. Track 2 can run on any schedule — manual, cron, or triggered by a git hook. The runner never needs Claude CLI access.

## Alternatives Considered

### A. Runner-based LLM (EPIC-012 / SPIKE-007 approach)

Install and authenticate `claude` CLI on the self-hosted Docker runner. Run the full pipeline (evidence + interpretation) in a single GitHub Actions workflow.

**Rejected because:** Authentication is fragile on ephemeral containers, couples two different workload types, and removes human oversight from LLM outputs. SPIKE-007's investigation questions (auth persistence, session isolation, rate limits) are symptoms of a fundamentally wrong architecture, not solvable problems.

### B. API-key based LLM calls on runner

Replace `claude -p` with direct Anthropic API calls using `ANTHROPIC_API_KEY` stored as a GitHub secret. Avoids the CLI auth problem entirely.

**Rejected because:** Moves from Max subscription (flat rate) to per-token API billing, which is expensive for ~280+ calls per backfill. Also doesn't address the coupling and oversight concerns.

### C. Hybrid — runner triggers, local executes

Runner detects new evidence and sends a webhook/notification to trigger LLM work on a local machine.

**Deferred.** This is a refinement of the chosen approach — the polling model can evolve toward push-based triggering later. Starting with polling is simpler and requires no webhook infrastructure.

## Consequences

**Positive:**
- Runner stays simple — no Claude CLI, no LLM secrets, no session management
- LLM work runs where authentication already exists (local dev machine with `claude login`)
- Human can review interpretation outputs before they're committed
- Each track can fail independently without blocking the other
- Bundling moves into Track 1, reducing manual steps

**Negative:**
- Requires a local machine to be available for LLM polling (not fully autonomous)
- Two-track model needs a coordination mechanism (signal file, git-based detection, or manual trigger)
- Brief generation timing depends on when the local poller runs, not a fixed schedule

**Accepted trade-offs:**
- Less automation than the runner-based approach, but more reliable and auditable
- The "local machine" constraint is acceptable for a single-maintainer project — if the project scales, the polling model can evolve toward a dedicated inference service

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-16 | — | Initial creation; supersedes SPIKE-007 framing |
| Adopted | 2026-03-16 | — | Decision adopted; gates EPIC-013 activation |
