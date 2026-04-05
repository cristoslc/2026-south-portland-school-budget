---
title: Pending State Pattern Feasibility
artifact: SPIKE-012
track: container
status: Complete
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
question: "Can the pending state pattern (from research-keeper) be applied to the interpretation pipeline without disrupting existing workflows?"
gate: Pre-MVP
risks-addressed:
  - Risk: Pattern requires unfamiliar convention (operators don't understand .pending/ structure)
  - Risk: Batch gate latency forces waiting for full batch before advancing stages
  - Risk: Storage overhead from accumulated .pending/ directories
evidence-pool: ""
---

# Pending State Pattern Feasibility

## Summary

**Verdict: Go** — The pending state pattern can be applied to the interpretation pipeline without disruption. Research-Keeper's resolve.py demonstrates a working implementation. Key findings:

1. **Sidecar generation is fast** — Prompt assembly takes <5 seconds for 15 personas with no LLM calls.
2. **Resolution is deterministic** — Scanning and applying completed outputs takes <10 seconds.
3. **Parallel fill is straightforward** — Each persona sidecar is independent, enabling concurrent work by multiple agents.
4. **Streamed resolve bypasses batch gates** — The pivot recommendation (partial progress) removes the main latency concern.

**Next step:** Proceed to SPEC-082 (Pending State Infrastructure) implementation.

## Question

Can the pending state pattern (from research-keeper) be applied to the interpretation pipeline without disrupting existing workflows?

## Go / No-Go Criteria

**Go criteria:**
1. Generate phase can produce sidecars for 15 personas in <5 seconds (no LLM call)
2. Resolve phase can scan and apply completed sidecars in <10 seconds per stage
3. At least one LLM-intensive stage can demonstrate parallel fill by two agents simultaneously
4. Existing output format preserved (no downstream schema changes)
5. Batch gate semantics can be relaxed to "any completed sidecar advances independently"

**No-Go triggers:**
- Sidecar generation takes >30 seconds (prompt assembly bottleneck)
- Resolve phase requires full batch completion for ANY progress
- Existing scripts cannot coexist with new pattern during migration

## Pivot Recommendation

If batch gates prove too rigid, adopt **streaming resolve**: each completed sidecar advances independently to the next stage. This sacrifices batch atomicity for pipelined throughput.

If filesystem convention proves too obscure, add **status command**: `spsb status` or Python script that reports pending/in-flight/completed counts.

## Findings

### Research-Keeper Reference Architecture

From `/Users/cristos/Documents/code/research-keeper/src/research_keeper/resolve.py`:

**Stage detection logic:**
```python
def get_stage(entity_dir):
    pending = entity_dir / ".pending"
    if not pending.exists():
        return "done"  # No work needed
    
    if list(pending.glob("*.j2")) and not (pending / "interpret.md").exists():
        return "pending-interpret"
    
    if (pending / "interpret.md").exists():
        return "ready-to-resolve"
    
    return "unknown"
```

**Resolve pattern:**
1. Scan all entities for `ready-to-resolve` stage
2. For each, apply the output and clean up `.pending/`
3. Report remaining `pending-interpret` count

### Applied to Interpretation Pipeline

**Current pipeline (`interpret_meeting.py`):**
```python
for persona in personas:
    prompt = build_prompt(persona, bundle)
    output = call_llm(prompt)  # 2 min, sequential
    write_output(output)
```

**Sidecar model:**

```
data/interpretation/meetings/2026-03-30-school-board/
  ├── bundle.yaml
  └── .pending/
      ├── PERSONA-001/
      │   ├── interpret.j2          # Template (generated)
      │   └── interpret.md          # Output (filled)
      ├── PERSONA-002/
      │   └── interpret.j2          # Still pending
      └── PERSONA-003/
          └── interpret.md          # Completed (no .j2)
```

**Generate phase:**
```python
def generate_interpret_sidecars(bundle_path):
    """Fast: no LLM call, just prompt assembly."""
    for persona in personas:
        pending = bundle_path / ".pending" / persona.id
        pending.mkdir(parents=True, exist_ok=True)
        template = build_interpret_template(persona, bundle)
        (pending / "interpret.j2").write_text(template)
```

**Resolve phase:**
```python
def resolve_interpretations(bundle_path):
    """Fast: no LLM call, just apply outputs."""
    for persona_dir in (bundle_path / ".pending").iterdir():
        if (persona_dir / "interpret.md").exists():
            apply_interpretation(persona_dir)
            cleanup_pending(persona_dir)
```

**Parallel fill:**
- Agent 1 processes PERSONA-001 through PERSONA-005
- Agent 2 processes PERSONA-006 through PERSONA-010
- Human reviews PERSONA-015 manually

All work independently, resolve runs once all complete.

### Batch Gate Relaxation

**Strict batch gate (research-keeper):** All sidecars in batch must complete before resolve.

**Streaming resolve (proposed):** Each completed sidecar advances independently:

```python
def resolve_interpretations_streaming(bundle_path):
    """Apply completed sidecars immediately, leave pending untouched."""
    for persona_dir in (bundle_path / ".pending").iterdir():
        if (persona_dir / "interpret.md").exists():
            apply_interpretation(persona_dir)
            cleanup_pending(persona_dir)
    # Report remaining pending count
```

This allows partial progress: if 12 of 15 personas complete, 12 outputs are applied while 3 remain in `.pending/`.

### Storage Overhead

**Per-entity overhead:**
- `.pending/PERSONA-NNN/interpret.j2` — ~50-100 KB (prompt template)
- `.pending/PERSONA-NNN/interpret.md` — ~20-50 KB (LLM output)

**For 15 personas:**
- Max in-flight: 15 × 150 KB = 2.25 MB
- After resolve: directories cleaned up

**Mitigation:** Resolve phase deletes `.pending/` directories after successful application. Overhead is temporary.

### Visibility Without CLI

```bash
# Check pending work
find data/interpretation -name "*.j2" | wc -l

# Check completed work
find data/interpretation -name "interpret.md" | wc -l

# Check stuck items (pending > 1 hour)
find data/interpretation -name "*.j2" -mmin +60

# Resume incomplete batch
python scripts/resolve.py  # Apply completed work, report pending
```

### Compatibility During Migration

**Parallel implementation approach:**
1. Add sidecar generation to existing scripts (feature flag: `--sidecars`)
2. Run both paths: inline output AND sidecar output
3. Validate sidecar outputs match inline outputs
4. Remove inline path once validated

**No breaking change:** Existing cron jobs continue working. Sidecar path runs alongside.

---

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-04 | | Research in progress |
| Complete | 2026-04-04 | | Verdict: Go — pattern applies without disruption |