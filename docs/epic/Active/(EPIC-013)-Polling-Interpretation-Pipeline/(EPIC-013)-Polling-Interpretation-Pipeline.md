---
title: "Polling Interpretation Pipeline"
artifact: EPIC-013
track: container
status: Active
author: cristos
created: 2026-03-16
last-updated: 2026-03-16
parent-vision: VISION-003
parent-initiative: INITIATIVE-003
linked-adrs:
  - ADR-002
linked-research: []
depends-on-artifacts:
  - EPIC-008
  - EPIC-009
  - EPIC-010
  - EPIC-011
supersedes: EPIC-012
success-criteria:
  - Local poller detects new evidence/bundles pushed by the runner and triggers the interpretation chain without manual intervention
  - Bundling runs as part of the deterministic pipeline (Track 1) after evidence collection
  - Interpretation, fold, and brief generation run locally via polling (Track 2) where Claude CLI is already authenticated
  - The two tracks are fully decoupled — runner failures don't block LLM work and vice versa
  - Brief generation produces updated briefs after each new meeting is interpreted and folded
addresses: []
trove: ""
---

# Polling Interpretation Pipeline

## Goal / Objective

Automate the interpretation chain (bundling → interpretation → fold → briefs) using a two-track architecture: the runner handles deterministic work and the local machine polls for new inputs and runs LLM inference. This replaces the EPIC-012 approach of putting Claude CLI on the runner.

## Scope Boundaries

**In scope:**
- Add bundling step to `pipeline.yml` (deterministic, runs on runner after evidence collection)
- Change-detection mechanism: how the local poller knows new work is available (git diff, signal file, manifest comparison)
- Local polling orchestrator: a script or daemon that watches for new bundles and runs interpret → fold → brief
- Incremental processing: only interpret meetings with new/changed bundles, only fold meetings with new interpretations
- Brief regeneration trigger: after fold completes, regenerate briefs for the next upcoming meeting

**Out of scope:**
- Evidence collection (already working in `pipeline.yml`)
- The interpretation/fold/brief scripts themselves (EPIC-008 through EPIC-011, all Complete)
- Push-based triggering (webhooks, notifications) — future refinement if polling proves insufficient
- Multi-user or multi-machine coordination

## Proposed Decomposition

| Artifact | Title | Status | Track |
|----------|-------|--------|-------|
| ADR-002 | Polling LLM Pipeline Over Runner-Based LLM | Proposed | — |
| _TBD_ | Add bundling step to pipeline.yml | — | Track 1 (runner) |
| _TBD_ | Change-detection mechanism (new bundle signal) | — | Bridge |
| _TBD_ | Local polling orchestrator | — | Track 2 (local) |
| _TBD_ | Incremental interpretation trigger | — | Track 2 (local) |
| _TBD_ | Post-fold brief regeneration | — | Track 2 (local) |

Child specs will be created when this epic moves to Active.

## Key Dependencies

- EPIC-008 (Meeting Bundler) — Complete. Bundling script exists; needs wiring into pipeline.yml.
- EPIC-009, EPIC-010, EPIC-011 — Complete. Interpretation, fold, and brief scripts exist and work manually.
- ADR-002 — Must be Adopted before this epic goes Active.

## Architecture

### Two-Track Model

```
Track 1 (Runner — deterministic, cron)          Track 2 (Local — LLM, polling)
┌──────────────────────────────────┐             ┌──────────────────────────────┐
│  Connectors (Vimeo, Diligent,   │             │  Poll for new bundles        │
│    budget pages)                 │             │    (git pull + diff check)   │
│         ↓                        │             │         ↓                    │
│  Normalizers (VTT, PDF, HTML)   │   git push  │  interpret_meeting.py        │
│         ↓                        │ ──────────→ │    (new/changed meetings)    │
│  bundle_meetings.py             │             │         ↓                    │
│         ↓                        │             │  fold_meeting.py             │
│  Commit + push                  │             │    (chronological order)     │
└──────────────────────────────────┘             │         ↓                    │
                                                 │  generate_briefs.py          │
                                                 │    (next upcoming meeting)   │
                                                 │         ↓                    │
                                                 │  Commit + push               │
                                                 └──────────────────────────────┘
```

### Change Detection

Track 2 needs to know what's new. Options to investigate in child specs:

1. **Git diff on bundles directory** — after `git pull`, compare `data/interpretation/bundles/` against the last-processed state
2. **Manifest hash** — Track 1 writes a `bundles-manifest.json` with hashes; Track 2 compares against its last-seen version
3. **Git tags** — Track 1 tags evidence commits; Track 2 processes unprocessed tags

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Proposed | 2026-03-16 | — | Initial creation; supersedes EPIC-012 |
| Active | 2026-03-16 | — | ADR-002 adopted; ready for spec decomposition |
