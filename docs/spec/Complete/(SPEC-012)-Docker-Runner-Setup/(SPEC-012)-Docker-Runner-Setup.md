---
title: "Docker Runner Setup"
artifact: SPEC-012
status: Complete
author: cristos
created: 2026-03-11
last-updated: 2026-03-11
parent-epic: EPIC-005
linked-research: []
linked-adrs: []
depends-on: []
addresses: []
trove: ""
swain-do: required
---

# Docker Runner Setup

## Problem Statement

The evidence pipeline workflow runs on GitHub-hosted runners, consuming ~300 min/month of the 2,000 min free tier quota. With 4x/day scheduling this would consume ~1,200 min/month — 60% of the quota. A self-hosted Docker runner eliminates quota usage entirely, starts faster (deps pre-installed), and keeps all data processing local.

## External Behavior

**Inputs:**
- GitHub runner registration token (one-time, from repo Settings > Actions > Runners)
- Repository URL

**Outputs:**
- A running Docker container that polls GitHub for workflow jobs
- Pipeline jobs execute locally with pre-installed Python dependencies

**Preconditions:**
- Docker (Desktop or Engine) installed on the host
- Network access to github.com (outbound only — no inbound ports)

**Postconditions:**
- Runner appears in repo Settings > Actions > Runners as "Idle"
- Scheduled pipeline workflow dispatches to self-hosted runner
- If self-hosted runner is offline, workflow falls back to hosted runner

**Constraints:**
- Runner image must include: Python 3.12, pyyaml, pdfplumber, beautifulsoup4, markdownify, openpyxl, yt-dlp, git, git-lfs
- Container must auto-restart on failure (docker-compose restart policy)
- No secrets baked into the image — registration token passed via environment variable

## Acceptance Criteria

1. **Given** the Docker runner is started with a valid registration token, **when** it connects to GitHub, **then** it appears as an idle self-hosted runner in the repository settings.

2. **Given** the pipeline workflow is triggered (manually or on schedule), **when** the self-hosted runner is online, **then** the job runs on the self-hosted runner.

3. **Given** the self-hosted runner is offline, **when** the pipeline workflow is triggered, **then** the job falls back to the hosted ubuntu-latest runner.

4. **Given** the workflow schedule, **when** a full day passes, **then** the pipeline runs at approximately 8 AM and 8 PM ET.

5. **Given** the runner container crashes, **when** Docker detects the failure, **then** the container auto-restarts.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| 1. Runner registers with GitHub | `start.sh` runs `config.sh --url --token --unattended`; cleanup trap deregisters on stop | Pass |
| 2. Self-hosted runner executes jobs | `pipeline.yml` primary job uses `runs-on: self-hosted`; no setup-python or pip install needed (deps baked in) | Pass |
| 3. Hosted fallback when offline | `update-evidence-fallback` job triggers with `if: needs.update-evidence.result == 'failure'`; runs on `ubuntu-latest` with pip cache | Pass |
| 4. 2x/day at 8 AM and 8 PM ET | Cron `0 0,1,12,13 * * *` covers both EDT and EST offsets for 8 AM and 8 PM | Pass |
| 5. Auto-restart on crash | `docker-compose.yml` uses `restart: unless-stopped` | Pass |

## Scope & Constraints

- Single runner instance only (no autoscaling)
- Runner runs as root in the container (acceptable for this use case — no untrusted code)
- Registration token must be manually generated once; runner handles re-registration on restart
- macOS (Darwin) host assumed — Docker Desktop for Mac

## Implementation Approach

1. Create `infra/runner/Dockerfile` — base on `ubuntu:24.04`, install Python 3.12 + pip deps + git + git-lfs + GitHub Actions runner agent
2. Create `infra/runner/docker-compose.yml` — single service with restart policy, env vars for token and repo URL
3. Create `infra/runner/start.sh` — entrypoint script that registers the runner (or re-uses existing config) and starts the listener
4. Update `.github/workflows/pipeline.yml` — dual-job strategy: self-hosted primary, hosted fallback; 2x/day schedule
5. Add `infra/runner/.env.example` documenting required environment variables

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-11 | 0cfb861 | Initial creation |
| Implemented | 2026-03-11 | 0cfb861 | All infra files created, workflow updated |
