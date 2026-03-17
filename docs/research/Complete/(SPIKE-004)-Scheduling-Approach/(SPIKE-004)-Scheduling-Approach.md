---
title: "Pipeline Scheduling Approach"
artifact: SPIKE-004
status: Complete
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
question: "What is the simplest reliable way to run the evidence pipeline on a schedule from a personal Mac?"
gate: Pre-MVP
risks-addressed:
  - macOS cron/launchd jobs may not run reliably on a laptop that sleeps
  - Cloud-based scheduling (GitHub Actions) may not have access to local git repo or credentials
depends-on: []
trove: ""
linked-research:
  - SPIKE-001
  - SPIKE-002
---

# Pipeline Scheduling Approach

## Question

What is the simplest reliable way to run the evidence pipeline on a daily or on-demand schedule? Options to evaluate:

1. **launchd (macOS)** -- native, runs on wake from sleep, but plist configuration is verbose and debugging is painful.
2. **cron** -- simpler config, but doesn't handle sleep/wake well on macOS.
3. **GitHub Actions** -- runs in the cloud, can push results back. Requires secrets for Vimeo API token and git push credentials. Decoupled from laptop availability.
4. **Manual with a reminder** -- just run `./scripts/pipeline.py run` when reminded. Simplest but defeats the "automated" goal.

Key constraints: runs on the author's MacBook, budget season is ~4 months, pipeline needs git access to commit staged changes.

## Go / No-Go Criteria

- **Go:** One of the options can reliably execute the pipeline at least once per day during budget season with less than 30 minutes of setup.
- **No-Go:** All options require significant infrastructure investment (server, Docker, CI pipeline configuration) disproportionate to a 4-month personal project.

## Pivot Recommendation

If fully automated scheduling proves too heavy: use a hybrid approach -- manual trigger (`./scripts/pipeline.py run`) wrapped in a shell alias, with a daily calendar reminder. Accept "semi-automated" over "fully automated" to preserve the maintenance budget.

## Findings

### Context from other spikes

SPIKE-001 and SPIKE-002 significantly simplified the pipeline's dependency profile:

- **Vimeo VTT download** uses `yt-dlp` -- a standalone CLI tool with no API keys or authentication
- **Diligent Community agendas** use a public REST API -- plain HTTP GET, no auth, no browser needed
- **spsdme.org budget page** is static HTML with PDF links -- `curl` is sufficient

No component requires browser automation, API tokens, or authentication. This means the pipeline can run in any environment with Python, `yt-dlp`, and internet access -- including GitHub Actions.

### Option evaluation

| Option | Setup | Reliability | Runs when laptop sleeps? | Git integration |
|--------|-------|-------------|--------------------------|-----------------|
| **GitHub Actions** (cron) | ~15 min | High | Yes | Native (push from workflow) |
| **launchd** (macOS) | ~20 min | Medium (wake handling) | Only on wake | Local git |
| **cron** (macOS) | ~5 min | Low (skips during sleep) | No | Local git |
| **Manual + alias** | ~2 min | Depends on human | N/A | Local git |

### Recommendation: GitHub Actions

**GitHub Actions is the best fit.** The repo is already on GitHub (`cristoslc/2026-south-portland-school-budget`), auth is configured, and no secrets are needed (yt-dlp and the Diligent API are both unauthenticated).

A workflow would:
1. Run on a cron schedule (e.g., daily at 8 AM ET)
2. Check out the repo
3. Install `yt-dlp` and Python dependencies
4. Run the pipeline script
5. If changes exist, commit and push

**Advantages over local scheduling:**
- Runs regardless of laptop state (sleep, off, traveling)
- No macOS plist/cron debugging
- Workflow file is version-controlled and portable
- Free tier is sufficient (pipeline runs are short -- a few minutes max)

**Risks:**
- yt-dlp on GitHub Actions needs installing per run (but it's a pip install, ~5 seconds)
- GitHub Actions runners are Ubuntu, not macOS -- but none of the pipeline tools are platform-specific
- If the pipeline breaks, failure notifications come via GitHub (email or Slack integration)

### Fallback: manual + alias

If GitHub Actions setup is deferred or proves annoying, a shell alias provides 90% of the value:

```bash
alias budget-update='cd ~/Documents/projects/2026-south-portland-school-budget && python3 scripts/pipeline.py run'
```

Combined with a daily calendar reminder. This is the pivot recommendation's "semi-automated" approach and remains viable as a starting point while the Actions workflow is built.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Planned | 2026-03-10 | _pending_ | Initial creation |
| Active | 2026-03-10 | _pending_ | Evaluating options against spike findings |
| Complete | 2026-03-10 | _pending_ | GitHub Actions recommended; manual alias as fallback |
