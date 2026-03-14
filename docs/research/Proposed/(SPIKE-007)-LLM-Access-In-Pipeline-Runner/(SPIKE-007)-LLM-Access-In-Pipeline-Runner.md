---
title: "LLM Access in Pipeline Runner"
artifact: SPIKE-007
status: Proposed
author: cristos
created: 2026-03-13
last-updated: 2026-03-13
parent-epic: EPIC-012
linked-adrs: []
depends-on: []
time-box: "2 hours"
evidence-pool: ""
---

# LLM Access in Pipeline Runner

## Question

Can the self-hosted GitHub Actions runner (Docker-based, per SPEC-012) make Anthropic API calls to run the interpretation pipeline automatically? What are the constraints, and what's the simplest path to enabling it?

## Context

The interpretation pipeline scripts (`interpret_meeting.py`, `fold_meeting.py`, `generate_briefs.py`) call the Anthropic API directly using `claude-sonnet-4`. The existing evidence pipeline runs on a self-hosted Docker runner with no LLM dependencies. Adding interpretation to the automated pipeline requires:

1. API key access (GitHub secret → runner environment)
2. Outbound HTTPS to `api.anthropic.com` (network egress from Docker container)
3. Python `anthropic` SDK available in the runner image
4. Understanding of cost implications for automated runs

A secondary question: is there value in having Claude Code itself available on the runner (for agentic execution of the runbook), or is direct script invocation sufficient?

## Investigation Plan

1. **API key delivery** — verify `ANTHROPIC_API_KEY` can be passed as a GitHub Actions secret and is available inside the self-hosted Docker runner. Check if the existing runner Dockerfile/compose setup passes secrets through.

2. **Network egress** — confirm the Docker runner can reach `api.anthropic.com:443`. The existing pipeline already reaches `vimeo.com`, `diligentcommunity.com`, and `github.com`, so this is likely fine.

3. **SDK availability** — check if `anthropic` is in the runner's Python environment, or if it needs to be added to the Dockerfile/requirements. The fallback job (ubuntu-latest) installs packages via `uv` — same approach could work.

4. **Cost modeling** — estimate per-run costs for incremental interpretation (1-2 new meetings x 14 personas per pipeline run) vs. the cron frequency (2x daily). Calculate monthly API spend.

5. **Claude Code on runner** — assess whether installing Claude Code on the runner adds value beyond direct script calls. Likely conclusion: not worth the complexity for a scheduled pipeline.

## Go/No-Go Criteria

| Criterion | Threshold | Pivot if fails |
|-----------|-----------|----------------|
| API key reachable in runner | Secret is available as env var in Docker container | Use GitHub-hosted runner for interpretation step only (separate job) |
| Network egress works | Can reach api.anthropic.com from runner | Add proxy config or use hosted runner |
| Cost per incremental run | < $1 per pipeline invocation | Reduce persona count for automated runs or run less frequently |
| End-to-end test | One meeting interpreted + folded in CI | Fall back to manual runs with RUNBOOK-002 |

## Findings

_(To be filled during investigation)_

## Recommendation

_(To be filled after investigation)_

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-13 | — | Initial creation |
