---
title: "Question Artifacts Over YAML Index"
artifact: ADR-004
track: standing
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
linked-artifacts:
  - EPIC-021
  - SPIKE-008
depends-on-artifacts: []
evidence-pool: ""
---

# Question Artifacts Over YAML Index

## Context

SPIKE-008 prototyped a key questions tracking system using a single `data/interpretation/questions/questions.yaml` file containing all canonical questions, their persona variants, scores, and resolution state. The prototype validated the scoring formula, stress-test gate, and PERSONA-000 integration — but it used the wrong data model.

Every other entity in this project — personas, specs, epics, spikes, ADRs — is an individual artifact file with YAML frontmatter, a markdown body, and a lifecycle table. The YAML index approach breaks this pattern. It makes questions second-class citizens: they can't be linked from other artifacts using standard `linked-artifacts` references, they don't appear in the spec graph, they don't have lifecycle phases, and they can't carry supporting docs alongside them.

## Decision

Each canonical question is a standalone artifact following swain conventions:

- **Prefix:** `QUESTION-NNN`
- **Lifecycle track:** Standing (like Personas and ADRs — they persist and evolve, they aren't "shipped")
- **Folder structure:** `docs/question/<Phase>/(QUESTION-NNN)-<Slug>/`
- **Frontmatter:** Standard swain fields (`artifact`, `status`, `created`, `last-updated`, `linked-artifacts`) plus question-specific fields (`canonical`, `first-raised`, `first-raised-source`, `priority-score`, `scored-at`, `resolution-status`)
- **Body:** Canonical phrasing, persona variants table, resolution evidence, stress-test results
- **Template:** A question-specific template in `references/question-template.md.template`
- **Definition:** A question-specific definition in `references/question-definition.md`

The pipeline writes and updates individual QUESTION files the same way it writes persona briefs — one file per entity, machine-readable frontmatter, human-readable body.

## Alternatives Considered

**Single YAML index (rejected — SPIKE-008 prototype approach).** Simpler to write and parse, but breaks every convention in the project. Questions can't participate in the artifact graph, can't be linked from specs or epics, can't carry supporting docs, and can't have independent lifecycle states. A monolithic file also creates merge conflicts when multiple pipeline runs update different questions concurrently.

**JSON files per question (rejected).** Machine-readable but not human-readable. Operators review questions in Typora and the terminal — markdown with frontmatter is the established format.

## Consequences

**Positive:**
- Questions are first-class artifacts: linkable, graphable, lifecycle-tracked
- Per-question files enable independent lifecycle transitions (one question can be resolved while others stay open)
- Supporting docs (resolution evidence, stress-test logs) can live alongside each question in its folder
- The spec graph and chart tools can include questions without modification (they already parse frontmatter)
- Pipeline writes are atomic per-question — no monolithic file contention

**Accepted downsides:**
- More files on disk (one directory per question vs. one YAML file)
- Pipeline must iterate over question directories rather than parsing a single file
- The question template and definition files need to be created as project-local additions to swain-design's reference set

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Adopted — operator corrected SPIKE-008 prototype approach |
