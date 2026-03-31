---
title: "Question Artifact Type"
artifact: SPEC-034
track: implementable
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-30
priority-weight: high
type: feature
parent-epic: EPIC-021
linked-artifacts:
  - ADR-004
  - SPIKE-008
depends-on-artifacts: []
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Question Artifact Type

## Problem Statement

The key questions tracking system needs a data model for canonical questions. ADR-004 decided that each question is a standalone artifact following swain conventions — not a monolithic YAML file. This spec defines the QUESTION-NNN artifact type: its template, definition, folder structure, frontmatter schema, and body sections.

## Desired Outcomes

Pipeline code and agents can create, read, update, and link QUESTION artifacts using the same patterns they use for every other swain artifact. Questions appear in the spec graph, can be referenced from `linked-artifacts` in other artifact types, and carry per-question supporting docs in their directories.

## External Behavior

**Inputs:**
- Canonical question phrasing, first-raised date and source, persona variant framings

**Outputs:**
- A `docs/question/<Phase>/(QUESTION-NNN)-<Slug>/(QUESTION-NNN)-<Slug>.md` file
- A `references/question-definition.md` in the swain-design skill references
- A `references/question-template.md.template` in the swain-design skill references

**Constraints:**
- Must follow ADR-004: individual files, swain frontmatter conventions, standing lifecycle track
- Lifecycle phases: Proposed, Active (open question), Resolved, Retired, Superseded
- Frontmatter must include question-specific fields alongside standard swain fields
- Body must include persona variants as a structured section (not embedded in frontmatter — frontmatter stays machine-scannable, body stays human-readable)

## Acceptance Criteria

1. **Given** a question-definition.md and question-template.md.template exist in the swain-design references directory, **when** an agent reads the template, **then** it can create a valid QUESTION artifact with all required frontmatter fields and body sections.

2. **Given** a QUESTION artifact exists at `docs/question/Active/(QUESTION-001)-Transportation-Logistics/`, **when** another artifact references it via `linked-artifacts: [QUESTION-001]`, **then** `resolve-artifact-link.sh QUESTION-001` returns the correct relative path.

3. **Given** the question definition specifies lifecycle phases, **when** a question is resolved, **then** it can be transitioned from Active to Resolved with a lifecycle table entry — following the same move-directory pattern as other artifacts.

4. **Given** the frontmatter schema includes `priority-score`, `scored-at`, `first-raised`, `resolution-status`, and `persona-count`, **when** the pipeline reads these fields, **then** it can compute rankings without parsing the body.

5. **Given** the body includes a `## Persona Variants` section with a table of persona ID, framing, first-seen date, and resolved status, **when** a human reads the artifact in Typora, **then** they can see at a glance who is asking this question and in what terms.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|

## Scope & Constraints

**In scope:** Template, definition, folder structure convention, frontmatter schema, body section design, initial seed of 5 QUESTION artifacts from SPIKE-008 prototype data.

**Out of scope:** Pipeline code that creates/updates these artifacts (SPEC-035, SPEC-036). Resolution stress-test logic (SPEC-037). Evergreen brief integration (SPEC-038).

**Frontmatter schema (proposed):**

```yaml
title: "Short human-readable question title"
artifact: QUESTION-NNN
track: standing
status: Active          # Proposed | Active | Resolved | Retired | Superseded
author: pipeline
created: YYYY-MM-DD
last-updated: YYYY-MM-DD
canonical: >-
  One-sentence canonical phrasing of the question.
first-raised: YYYY-MM-DD
first-raised-source: "Description of where/when the question was first raised"
resolution-status: open  # open | claimed | resolved
priority-score: 540      # age_days x persona_count, computed by pipeline
scored-at: YYYY-MM-DD    # date the score was last computed
persona-count: 10        # number of distinct personas with variants
linked-artifacts: []
depends-on-artifacts: []
```

**Body sections:**

```markdown
# {Title}

## Canonical Question

{Full canonical phrasing — may be longer than the frontmatter `canonical` field}

## Persona Variants

| Persona | Framing | First Seen | Resolved |
|---------|---------|-----------|----------|
| PERSONA-001 | {their specific version} | YYYY-MM-DD | No |
| ... | ... | ... | ... |

## Resolution Evidence

{Empty until claimed/resolved. When evidence appears, cite transcript
references and dates.}

## Stress Test Results

{Per-persona pass/fail when resolution is claimed. Empty until tested.}

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
```

## Implementation Approach

1. Create `references/question-definition.md` modeled on persona-definition.md (standing track, phase directories, conventions).
2. Create `references/question-template.md.template` with the frontmatter schema and body sections above.
3. Create `docs/question/Active/` directory structure.
4. Seed 5 QUESTION artifacts (QUESTION-001 through QUESTION-005) from the SPIKE-008 prototype data, migrating from the `questions.yaml` format to individual files.
5. Delete `data/interpretation/questions/questions.yaml` (superseded by individual artifacts).
6. Verify `resolve-artifact-link.sh` handles QUESTION-NNN references (may need a pattern addition).

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Operator-requested; implements ADR-004 |
