---
title: "Retro: Question Scoring Spike"
artifact: RETRO-2026-03-30-question-scoring-spike
track: standing
status: Active
created: 2026-03-30
last-updated: 2026-03-30
scope: "SPIKE-008 execution — question extraction, clustering, scoring, stress-testing prototype"
period: "2026-03-30"
linked-artifacts:
  - EPIC-021
  - SPIKE-008
  - EPIC-017
  - INITIATIVE-003
---

# Retro: Question Scoring Spike

## Summary

We went from idea to GO verdict in one session. We started by talking through how to surface unanswered questions across persona briefings. After sketching the design in conversation, we created [EPIC-021](../epic/Active/(EPIC-021)-Key-Questions-Tracking/(EPIC-021)-Key-Questions-Tracking.md) and [SPIKE-008](../research/Active/(SPIKE-008)-Question-Scoring-Prototype/(SPIKE-008)-Question-Scoring-Prototype.md), then ran the spike in a worktree. The result: a QUESTIONS file with 5 key questions and 32 persona-specific versions, a scoring formula that works, a stress-test gate that catches partial answers, and a new section in the evergreen brief.

## Artifacts

| Artifact | Title | Outcome |
|----------|-------|---------|
| [EPIC-021](../epic/Active/(EPIC-021)-Key-Questions-Tracking/(EPIC-021)-Key-Questions-Tracking.md) | Key Questions Tracking | Created — Active, awaiting spec decomposition post-spike |
| [SPIKE-008](../research/Active/(SPIKE-008)-Question-Scoring-Prototype/(SPIKE-008)-Question-Scoring-Prototype.md) | Question Scoring Prototype | Complete — GO on all 4 criteria |

## Reflection

### What went well

**Talking it through first made a better design.** The CHATONLY phase let us shape the approach before writing anything formal. The stress-test gate — where every persona's version of the question must be answered before it counts as resolved — came out of that conversation. The operator guided the design step by step ("make it pipeline-level," "stress-test against every persona," "maybe a new QUESTIONS artifact") instead of reacting to a finished proposal.

**Parallel agents cut research time in half.** We split the extraction across two agents: one searched for transportation questions, the other covered the remaining four topics. Both returned structured results with citations that went straight into the YAML file with no rework.

**The simple scoring formula just works.** `age_days x persona_count` is about as basic as it gets. It ranks questions the way you'd expect, and a fancier version (log-weighted breadth) produced the same ordering. No reason to add complexity when the raw signal is already clear.

**The stress-test passed on the first try.** We fed in a fake transportation answer ("average 35-minute rides, $340K annual cost") and checked it against all six persona versions of the question. It resolved David's cost question but failed Rachel's "what's my kid's route," the equity lens on multilingual families, and the high school shuttle concern. That's exactly right — a general answer doesn't close a question that people are asking in different ways for different reasons.

### What was surprising

**Savings outranked transportation.** We expected transportation to score highest because 10 personas ask about it. But the savings question was raised three weeks earlier (Jan 15 vs. Feb 4), and that extra age pushed it ahead. On reflection, that's right — the savings gap is the older, more structural problem.

**Before/after-care is a one-persona question.** Only Maria (PERSONA-001) raises extended care concerns. That's useful for testing — a brand-new, narrow question starts at score zero and climbs by one point per day. But it also means the pipeline should flag questions that only one person asks but that affect many families.

**The worktree didn't have our new files.** We created the EPIC and SPIKE on main's working directory but didn't commit them before branching into the worktree. The worktree copies from the last commit, not from uncommitted files. We had to copy the files over by hand. Small friction, easy to avoid next time.

### What would change

**Commit artifacts before entering the worktree.** We should have committed the EPIC and SPIKE files before branching. The right sequence is: create artifacts, commit, then enter the worktree. That way the worktree has everything it needs from the start.

**Consider splitting the YAML into one file per question.** A single `questions.yaml` works fine for 5 questions, but it might not hold up at 20 or more. When we write specs for [EPIC-021](../epic/Active/(EPIC-021)-Key-Questions-Tracking/(EPIC-021)-Key-Questions-Tracking.md), we should decide whether each question gets its own file (like persona briefs do) or stays in one index.

### Patterns observed

**The pipeline is becoming the product.** This is the fourth pipeline feature under [INITIATIVE-003](../initiative/Active/(INITIATIVE-003)-Interpretation-Pipeline/(INITIATIVE-003)-Interpretation-Pipeline.md) (after interpretation, cumulative fold, and upcoming-event briefs). The pipeline no longer just transforms data — it tracks what the administration has not answered and scores those gaps by age and breadth. The QUESTIONS artifact makes this shift concrete: it doesn't summarize what was said, it tracks what was *not* said.

**Persona variants are powerful beyond briefings.** Per-persona framing has been useful since [SPIKE-005](../research/Complete/(SPIKE-005)-Interpretation-Prompt-Design/(SPIKE-005)-Interpretation-Prompt-Design.md) (interpretation prompt design). This spike found a new use: treating variant diversity as a resolution gate. The same idea could apply to other cross-cutting checks — for example, testing whether the administration addressed an equity concern by checking it against every persona's specific version of that concern.

## Learnings captured

| Memory file | Type | Summary |
|------------|------|---------|
| feedback_retro_artifact_before_worktree.md | feedback | Commit artifacts to trunk before entering a worktree |
| project_retro_pipeline_as_product.md | project | Pipeline evolved from ETL to analytical accountability engine |
