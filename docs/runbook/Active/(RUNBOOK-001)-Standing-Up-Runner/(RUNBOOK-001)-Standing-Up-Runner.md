---
title: "Standing Up the Self-Hosted Runner"
artifact: RUNBOOK-001
status: Active
mode: manual
trigger: on-demand
author: cristos
created: 2026-03-11
last-updated: 2026-03-11
validates:
  - SPEC-012
  - EPIC-005
parent-epic: EPIC-005
depends-on:
  - SPEC-012
---

# Standing Up the Self-Hosted Runner

## Purpose

Step-by-step procedure for setting up the Docker-based self-hosted GitHub Actions runner. Run once for initial setup, or again after a machine migration or Docker reset.

## Prerequisites

- Docker Desktop (or Docker Engine + Compose) installed and running
- GitHub account with admin access to the repository
- Terminal access on the host machine
- Internet connectivity (outbound to github.com)

## Steps

1. **Action:** Generate a runner registration token.
   Navigate to the repository on GitHub → Settings → Actions → Runners → New self-hosted runner. Copy the token from the configuration command (the `--token` value). Tokens expire after 1 hour — complete setup promptly.
   **Expected:** A token string like `AABCDE...`.

2. **Action:** Create the environment file.
   ```bash
   cd infra/runner
   cp .env.example .env
   ```
   Edit `.env` and set:
   - `GITHUB_REPOSITORY=<owner>/<repo>` (e.g., `cristoslc/2026-south-portland-school-budget`)
   - `RUNNER_TOKEN=<token from step 1>`
   - `RUNNER_NAME=<optional, defaults to hostname>`
   **Expected:** `.env` file exists with valid values.

3. **Action:** Build and start the runner.
   ```bash
   docker compose up -d --build
   ```
   **Expected:** Container builds successfully and starts. Logs show "Listening for Jobs".

4. **Action:** Verify runner registration.
   Check GitHub → Settings → Actions → Runners.
   **Expected:** Runner appears with a green "Idle" status.

5. **Action:** Trigger a test run.
   ```bash
   gh workflow run pipeline.yml
   ```
   **Expected:** The workflow dispatches to the self-hosted runner. Check the run log — it should show `runs-on: self-hosted` in the job details.

6. **Action:** Verify auto-restart.
   ```bash
   docker compose restart runner
   ```
   **Expected:** Container restarts and reconnects. Runner returns to "Idle" in GitHub within ~30 seconds.

## Teardown

To decommission the runner:
```bash
cd infra/runner
docker compose down
```
Then remove the runner from GitHub → Settings → Actions → Runners → (select runner) → Remove.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Token expired" on startup | Registration token is >1 hour old | Generate a new token (step 1) and update `.env` |
| Runner stays "Offline" | Container not running or network issue | Check `docker compose logs runner` and verify outbound HTTPS |
| Workflow runs on hosted instead of self-hosted | Runner labels don't match | Verify runner has `self-hosted` label in GitHub settings |
| "Must not run with sudo" error | Runner agent doesn't like root | The Dockerfile sets `RUNNER_ALLOW_RUNASROOT=1`; verify env var is set |

## Run Log

| Date | Executor | Result | Duration | Notes |
|------|----------|--------|----------|-------|
| 2026-03-11 | cristos | - | - | Template created |

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-11 | 0cfb861 | Initial creation |
| Active | 2026-03-11 | 0cfb861 | Steps validated against implementation |
