---
title: "Claude CLI Access in Pipeline Runner"
artifact: SPIKE-007
status: Proposed
author: cristos
created: 2026-03-13
last-updated: 2026-03-16
parent-epic: EPIC-012
linked-adrs: []
depends-on: []
time-box: "2 hours"
evidence-pool: ""
---

# Claude CLI Access in Pipeline Runner

## Question

Can the self-hosted GitHub Actions runner authenticate and use the `claude` CLI (`claude -p`) for interpretation pipeline calls?

## Context

The interpretation pipeline scripts call `claude -p` as a subprocess to perform LLM interpretation and folding. The existing evidence pipeline runs on a self-hosted Docker runner with no LLM dependencies. Adding interpretation to the automated pipeline requires the Claude CLI to be installed, authenticated, and safe for concurrent use on the runner.

## Investigation Plan

1. **CLI installation** — can `claude` be installed on the Docker-based runner? Check binary availability for the runner's architecture, PATH setup, and whether it can be baked into the runner image or must be installed at job time.

2. **Authentication persistence** — `claude login` creates a session. Does it persist across workflow runs on the self-hosted runner? Where are credentials stored (`~/.claude/`, XDG config, etc.)? If the runner container is ephemeral, authentication may need to be re-established each run.

3. **Session management** — multiple concurrent pipeline runs could collide on a single CLI session. Is `--no-session-persistence` sufficient isolation? Test whether two simultaneous `claude -p` calls interfere with each other.

4. **Network egress** — does `claude -p` require different endpoints than the direct API (`api.anthropic.com`)? Check whether additional domains need firewall/proxy allowlisting for CLI auth handshake, telemetry, or session management.

5. **Cost modeling** — all calls use the Max subscription (no per-token API billing). Is there a rate limit or usage cap on `claude -p` that would throttle a full pipeline run (~280 calls)? Measure throughput for sequential and parallel invocations.

## Go/No-Go Criteria

| Criterion | Go | No-Go / Pivot |
|-----------|-----|----------------|
| CLI installs on runner | Binary available and functional in Docker image | Investigate alternative invocation (API fallback) |
| Auth persists across runs | Credentials survive between workflow invocations | Would need re-login per run — assess feasibility |
| Concurrent run isolation | Simultaneous `claude -p` calls don't collide | Serialize pipeline steps or use per-run config dirs |
| Rate limits | Full pipeline (~280 calls) completes without throttling | Rate limits make full pipeline infeasible — batch or reduce calls |

## Findings

_(To be filled during investigation)_

## Recommendation

_(To be filled after investigation)_

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-13 | — | Initial creation |
