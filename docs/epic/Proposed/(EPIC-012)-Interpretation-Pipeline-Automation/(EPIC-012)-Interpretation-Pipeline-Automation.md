---
title: "Interpretation Pipeline Automation"
artifact: EPIC-012
status: Proposed
author: cristos
created: 2026-03-13
last-updated: 2026-03-13
parent-vision: VISION-003
linked-adrs: []
linked-research:
  - SPIKE-007
addresses: []
success-criteria:
  - After evidence pool updates land (via pipeline.yml), new/changed meeting bundles are detected and interpretation is triggered automatically
  - Per-meeting interpretation, cumulative fold, and summary regeneration run without manual intervention
  - Pipeline runner has access to LLM API for interpretation calls
  - Failed interpretations are retried or flagged without blocking the pipeline
  - Brief generation is triggered on a schedule tied to upcoming meeting dates (or remains manual with a clear handoff)
---

# Interpretation Pipeline Automation

## Problem Statement

The evidence pipeline (connectors + normalizers) runs automatically on a cron schedule via GitHub Actions, but everything downstream — bundling, interpretation, fold, and briefs — requires manual execution. With 20+ meetings and 14 personas, manual runs are tedious and easy to forget. The pipeline should detect when new evidence lands and automatically run the interpretation chain.

## Key Questions (gated by SPIKE-007)

1. **Can the self-hosted runner access the Anthropic API?** The interpretation scripts call claude-sonnet-4 directly. The runner needs `ANTHROPIC_API_KEY` as a secret, and outbound HTTPS to `api.anthropic.com`.

2. **Is Claude Code available on the runner?** If we want agentic execution (e.g., Claude Code running the runbook), the runner needs Claude Code installed. This may be impractical — direct Python script invocation is more likely.

3. **Cost and rate limits.** A full backfill is ~280 LLM calls. Incremental runs after each evidence pull would be 1-2 meetings x 14 personas = 14-28 calls. Is this within budget for automated runs?

## Proposed Decomposition

Pending SPIKE-007 findings, likely specs:

- **Bundle refresh step** — add `bundle_meetings.py` to pipeline.yml after evidence pool commit
- **Interpretation trigger** — detect new/changed bundles and run `interpret_meeting.py` for affected meetings only (incremental, not full backfill)
- **Fold chain** — run `fold_meeting.py` for meetings that have new interpretations, in chronological order
- **Summary regeneration** — already handled by fold_meeting.py, but verify it works in CI context
- **Brief scheduling** — may remain manual or trigger on a schedule before known meeting dates

## Scope & Constraints

- Must not break existing evidence pipeline (pipeline.yml job 1/2)
- LLM costs should be bounded — incremental runs only, not full re-interpretation
- Must degrade gracefully if LLM API is unavailable (evidence pipeline still runs)
- Self-hosted runner is Docker-based — any new dependencies must be containerized

## Child Artifacts

| Artifact | Title | Status |
|----------|-------|--------|
| SPIKE-007 | LLM Access in Pipeline Runner | Proposed |

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-13 | — | Initial creation; gated on SPIKE-007 |
