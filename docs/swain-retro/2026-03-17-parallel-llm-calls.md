# Retro: Serial LLM orchestration in Track 2 pipeline

**Date:** 2026-03-17
**Scope:** ADR-002 Track 2 pipeline — interpretation/fold/brief catch-up run
**Period:** 2026-03-17

## Summary

Implemented ADR-002 two-track architecture and ran the first full Track 2 catch-up: 21 interpretation calls, 11 meetings x 14 personas fold, and brief generation. The pipeline worked correctly but took ~10 hours due to purely serial execution of independent LLM calls.

## Reflection

### What went well
- Per-persona chunking (refactored from monolithic per-meeting calls) gave resilience — individual timeouts no longer crash the whole pipeline
- Gap detection correctly identifies what needs processing and skips completed work
- The `claude -p` subscription auth path works reliably once ANTHROPIC_API_KEY is stripped

### What was surprising
- The serial execution was never questioned across multiple iterations of the orchestrator. Each refactor (monolithic → per-meeting → per-persona) preserved the serial pattern without considering parallelism.

### What would change
- Start with parallelism as the default for independent subprocess dispatch
- Ask "what depends on what?" before writing any orchestration loop

### Patterns observed
- **Incremental refactoring preserves anti-patterns.** Moving from "one big call" to "many small calls" improved resilience but didn't improve throughput because the serial loop was carried forward each time.
- **Subprocess-per-call is fine for parallelism.** Each `claude -p` call is a separate process anyway — `ThreadPoolExecutor` with `subprocess.run` is the natural fit.

## Learnings captured

| Memory file | Type | Summary |
|------------|------|---------|
| feedback_retro_parallel_llm.md | feedback | Per-persona LLM calls are embarrassingly parallel; default to concurrent dispatch |
