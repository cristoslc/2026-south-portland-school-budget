---
title: Pending State Pattern for LLM Pipeline Coordination
artifact: ADR-006
track: standing
status: Active
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
linked-artifacts:
  - EPIC-035
  - INITIATIVE-003
depends-on-artifacts: []
evidence-pool: ""
---

# Pending State Pattern for LLM Pipeline Coordination

## Context

The current LLM pipeline architecture (`interpret_meeting.py`, `generate_briefs.py`, etc.) couples LLM invocation directly into Python scripts:

```python
for persona in personas:
    prompt = build_prompt(persona, bundle)
    output = call_llm(prompt)  # Blocking call
    write_output(output)
```

This approach creates several problems:

1. **Sequential bottleneck** — 15 personas × ~2 minutes = 30+ minutes with no parallelization
2. **No visibility** — operators cannot see progress until scripts complete
3. **Vendor lock-in** — the pipeline is death-grip coupled to Claude via `call_llm()`; no other agentic runtime can participate
4. **No recovery** — failures require restarting from the beginning
5. **No human checkpoint** — LLM output flows directly to disk without review opportunity

The project needs an architecture that:
- Decouples LLM work from pipeline orchestration
- Enables parallel execution by multiple agents (human or machine)
- Provides visibility into in-flight work
- Supports runtime-agnostic operation (Claude, Codex, Crush, human operators)
- Allows resumption from failures without re-running completed stages

Research-Keeper (github.com/cristoslc/research-keeper) demonstrates a successful pattern: the **pending state pattern with sidecars**.

## Decision

Adopt the **pending state pattern** for LLM-intensive pipeline stages:

1. **Sidecar generation phase** — Generate `.j2` template files containing prompts and context
2. **Fill phase** — Agents/humans complete sidecars in parallel (runtime-agnostic)
3. **Resolve phase** — Scan for completed outputs, apply to final artifacts, advance pipeline state

State is derived **entirely from filesystem convention**:

```
entity/
├── content.md           # Source material
└── .pending/
    ├── task.j2         # Template (work queued)
    └── task.md         # Output (work completed)
```

**Stage detection:**
- `.pending` absent → no work needed
- `.pending/task.j2` without `task.md` → pending work
- `.pending/task.md` present → ready to resolve

Batch gates prevent partial work from cascading: a stage only advances when **all** items in the batch complete.

**Affected stages:**
- Interpret (persona interpretations per meeting)
- Brief (persona briefs per meeting)
- Question extraction (per bundle)
- Transport analysis (per configuration)
- Cumulative fold (per persona)

**Unaffected stages:**
- Discovery connectors (pure I/O)
- Normalization (deterministic transforms)
- Bundle creation (schema validation)
- Site build (static generation)

## Alternatives Considered

### Alternative 1: Inline Parallel Invocation

Run N scripts in parallel with `--persona` flag:

```bash
python scripts/interpret_meeting.py bundle --persona PERSONA-001 &
python scripts/interpret_meeting.py bundle --persona PERSONA-002 &
wait
```

**Why not chosen:** Parallelization requires operator orchestration outside the pipeline. No visibility into in-flight work. Still coupled to single runtime. No human checkpoint. Addresses only the sequential bottleneck, not the other four problems.

### Alternative 2: Task Queue (Celery/RQ)

Push LLM calls to a task queue, workers consume and process:

**Why not chosen:** Adds infrastructure dependency (Redis, worker processes). Requires persistent queue state. Complex failure handling. Overkill for a single-operator project. Visibility still requires separate dashboard.

### Alternative 3: Database-Backed State Machine

Track pipeline state in SQLite with stage transitions:

**Why not chosen:** Database state diverges from filesystem state (source of truth drift). Debugging requires querying DB. Less portable than files. The pending pattern achieves state derivation from filesystem without additional state store.

### Alternative 4: MCP Server for LLM Work

Expose pipeline stages as MCP tools, allow external agents to invoke:

**Why not chosen:** MCP is a transport protocol, not a coordination model. Requires running server. Doesn't solve parallelization or visibility without additional orchestration.

## Consequences

### Positive

- **Runtime agnostic** — any agent (Claude, Codex, Crush, human) can fill sidecars
- **Parallelizable by design** — multiple agents work simultaneously on different sidecars
- **Visible state** — `ls .pending/` shows instantaneous work queue
- **Resumable** — partial completion survives crashes; resume from .pending
- **Human checkpoint** — review/edit `.md` outputs before resolve
- **Error isolation** — failure in one sidecar doesn't block others
- **No new dependencies** — filesystem is the state store; works everywhere

### Negative

- **More moving parts** — generate/fill/resolve phases instead of one script
- **Filesystem convention** — operators must understand `.pending/` structure
- **Batch gate latency** — must wait for full batch before advancing stages
- **Storage overhead** — `.pending/` directories accumulate until resolution

### Neutral

- **Migration required** — existing scripts must be refactored; not backward compatible
- **New runbook needed** — operators need procedures for fill/resume/retry

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-04 | | Initial adoption |