---
title: "Interpretation Pipeline Run"
artifact: RUNBOOK-002
status: Active
mode: agentic
trigger: on-demand
author: cristos
created: 2026-03-13
last-updated: 2026-03-13
validates:
  - SPEC-019
  - SPEC-021
  - SPEC-022
parent-epic: EPIC-009
depends-on: []
---

# Interpretation Pipeline Run

## Purpose

End-to-end procedure for running the persona interpretation pipeline across meeting bundles. Covers four stages: bundle refresh, per-meeting interpretation, cumulative fold, and brief generation. Use for the initial backfill (all historical meetings) and for ongoing manual runs when new evidence lands.

## Prerequisites

- Python 3 with `anthropic`, `pyyaml` packages available (use `uv run` if not installed)
- `ANTHROPIC_API_KEY` set in the environment
- Meeting bundles exist in `data/interpretation/bundles/` (run `bundle_meetings.py` if not)
- Validated personas exist in `docs/persona/Validated/` (14 currently)

## Steps

### Stage 1: Refresh bundles

1. **Action:** Regenerate meeting bundles from current evidence pools. [bash]
   ```bash
   uv run python3 scripts/bundle_meetings.py
   ```
   **Expected:** Bundle manifests created/updated in `data/interpretation/bundles/`. Protected bundles (manually curated) are preserved unless `--force` is used. Console output lists each meeting and its affiliated sources.

2. **Action:** Verify bundle count matches expected meetings. [bash]
   ```bash
   ls data/interpretation/bundles/ | wc -l
   ```
   **Expected:** Count matches the number of discovered meetings (currently 20: 7 school board + 13 city council).

### Stage 2: Per-meeting interpretation

3. **Action:** Run interpretation across all bundles, all personas. Process chronologically so that any resume point is clear. [bash]
   ```bash
   for bundle in $(ls -d data/interpretation/bundles/*/ | sort); do
     meeting_id=$(basename "$bundle")
     echo "=== Interpreting: $meeting_id ==="
     uv run python3 scripts/interpret_meeting.py "$bundle"
   done
   ```
   **Expected:** Each meeting produces 14 persona interpretation files in `data/interpretation/meetings/<meeting-id>/`. Existing interpretations are skipped (resume-safe). Failed personas are logged but don't halt the loop.

   **Cost estimate:** ~280 LLM calls (20 meetings x 14 personas), each ~4K output tokens on claude-sonnet-4. Budget approximately $5-10 for the full backfill.

4. **Action:** Verify interpretation coverage. [bash]
   ```bash
   for dir in data/interpretation/meetings/*/; do
     count=$(ls "$dir"PERSONA-*.md 2>/dev/null | wc -l)
     echo "$(basename "$dir"): $count/14 personas"
   done
   ```
   **Expected:** All meetings show 14/14. Investigate any gaps — likely LLM failures that can be retried with `--force --persona PERSONA-NNN`.

### Stage 3: Cumulative fold

5. **Action:** Run the fold engine chronologically across all meetings. Order matters — each fold builds on prior cumulative state. [bash]
   ```bash
   for bundle in $(ls -d data/interpretation/bundles/*/ | sort); do
     meeting_id=$(basename "$bundle")
     echo "=== Folding: $meeting_id ==="
     uv run python3 scripts/fold_meeting.py "$meeting_id"
   done
   ```
   **Expected:** Cumulative records created in `data/interpretation/cumulative/<PERSONA-NNN>/<date>.md`. Summary views regenerated for each persona after each fold. Existing records are skipped (idempotent).

6. **Action:** Verify cumulative coverage. [bash]
   ```bash
   for dir in data/interpretation/cumulative/PERSONA-*/; do
     count=$(ls "$dir"2*.md 2>/dev/null | wc -l)
     echo "$(basename "$dir"): $count records"
   done
   ```
   **Expected:** Each persona directory has one record per meeting they interpreted. Summary.md exists and is current.

### Stage 4: Brief generation (optional)

7. **Action:** Generate briefs for the next upcoming meeting. Only meaningful if a future meeting date is known. [bash]
   ```bash
   uv run python3 scripts/generate_briefs.py <YYYY-MM-DD>
   ```
   Replace `<YYYY-MM-DD>` with the upcoming meeting date. Add `--agenda <path>` if an agenda file is available.
   **Expected:** Per-persona briefs in `data/interpretation/briefs/<date>/`. Each brief has four sections: Since Last Meeting, Open Questions, Agenda Implications, Watch For.

### Stage 5: Commit results

8. **Action:** Review and commit the generated data. [bash]
   ```bash
   git add data/interpretation/
   git status
   ```
   **Expected:** New files in `meetings/`, `cumulative/`, and optionally `briefs/`. Review a sample interpretation and fold for quality before committing.

## Alternative: Claude Code Agent Execution

The fold stage (Stage 3) can be executed via Claude Code agents instead of the Python scripts. This uses the Max subscription instead of API credits. Dispatch one agent per persona — each reads the persona definition, prior cumulative records, and per-meeting interpretations, then writes the fold output directly. All 14 agents run in parallel; within each agent, meetings are processed sequentially (chronological order matters).

The interpretation stage (Stage 2) requires the Python scripts since the prompts include the full meeting bundle context (~50K tokens). Fold and summary prompts are smaller and work well as agent tasks.

## Teardown

No teardown needed. All outputs are additive and idempotent. To regenerate specific outputs, use `--force` on the relevant script with `--persona` to target specific personas.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "No bundle manifest found" | Bundle directory missing or empty | Run `bundle_meetings.py` first (step 1) |
| Persona count < 14 for a meeting | LLM rate limit or transient failure | Retry with `--force --persona PERSONA-NNN` |
| Fold produces empty deltas | First meeting for persona — no prior state | Expected behavior for the earliest meeting |
| "ANTHROPIC_API_KEY not set" | Missing env var | Export the key or use a `.env` file |
| Interpretation validation warnings | Output slightly out of schema | Check warnings — soft validation. Re-run with `--force` if critical |

## Run Log

| Date | Executor | Result | Duration | Notes |
|------|----------|--------|----------|-------|
| 2026-03-13 | cristos | - | - | Template created |
| 2026-03-14 | claude-code | Pass | ~45 min | Backfill: 9 budget meetings x 14 personas. Interpretation via API scripts (batches 1-2 stopped, scoped to school board + joint budget meetings). Fold via Claude Code agents (14 parallel, one per persona). 126 interpretation docs, 126 cumulative records, 14 summaries. Briefs skipped (no upcoming date). Note: 2026-02-04 budget forum slides PDF not readable — transcript only. |

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-13 | — | Created directly in Active — steps derived from implemented specs |
