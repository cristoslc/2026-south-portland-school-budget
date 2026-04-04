---
title: "Keyword-Triggered Reference Context Injection"
artifact: SPEC-081
track: implementable
status: Active
author: cristos
created: 2026-04-04
last-updated: 2026-04-04
priority-weight: high
type: enhancement
parent-epic: ""
parent-initiative: INITIATIVE-003
linked-artifacts:
  - ADR-005
  - DESIGN-002
depends-on-artifacts: []
addresses: []
evidence-pool: "school-integration-policy"
source-issue: ""
swain-do: required
---

# Keyword-Triggered Reference Context Injection

## Problem Statement

`interpret_meeting.py` builds prompts from persona definitions, fiscal context, and meeting bundle content. There is no mechanism to inject historical or reference context from non-meeting troves. When meetings discuss topics that have prior-year evidence (e.g., the 2023-2024 boundaries and configurations process, national integration research), the interpreter has no access to that background. This leads to shallower interpretations that miss connections a well-informed analyst would catch.

## Desired Outcomes

Persona interpretations become richer when meetings touch topics covered by reference troves. A persona brief about a meeting discussing "controlled choice" now reflects that the district explored this in 2024 and that national research documents outcomes. The mechanism is transparent — operators can see which triggers fired and which context was injected. Editorial discipline is preserved: the LLM grounds interpretation in what was said, not what wasn't.

## External Behavior

**Inputs:**
- Trove `manifest.yaml` gains an optional `triggers` array per source entry — a list of literal strings (case-insensitive)
- A new top-level manifest field `reference-synthesis` points to the file used as injection content (defaults to `synthesis.md`)

**Processing:**
- Before prompt construction, `build_prompt()` concatenates all meeting bundle source text
- A new function `match_reference_triggers(meeting_text, trove_manifests)` scans configured trove manifests for trigger matches
- For each trove with at least one trigger match, the trove's synthesis content is collected
- Matched context is injected as a `<reference_context>` block in the prompt, between `<instruction>` and `<meeting_context>`

**Outputs:**
- Interpretation prompts include a `<reference_context>` section when triggers match
- The section includes a preamble instructing the LLM to use context only where meeting content engages with the topic
- When no triggers match, the prompt is unchanged (no empty block)

**Constraints:**
- Trigger matching is literal string, case-insensitive — no regex, no stemming
- Maximum 3 reference troves injected per interpretation (to bound prompt size)
- If more than 3 match, select the 3 with the most trigger hits
- The `<reference_context>` preamble must include the no-absence-editorializing guardrail

## Acceptance Criteria

**AC-1: Trigger matching**
Given a trove manifest with `triggers: ["controlled choice", "magnet"]` on a source entry
When meeting content contains "the Board discussed controlled choice options"
Then `match_reference_triggers` returns that trove as a match

**AC-2: Case insensitivity**
Given triggers `["Brickhill", "attendance zone"]`
When meeting content contains "brickhill families" or "ATTENDANCE ZONE review"
Then the trove matches

**AC-3: Prompt injection**
Given one matching reference trove
When `build_prompt()` constructs the interpretation prompt
Then the prompt contains a `<reference_context>` block between `<instruction>` and `<meeting_context>`
And the block contains the trove's synthesis content
And the block contains the no-absence-editorializing preamble

**AC-4: No match, no change**
Given troves with triggers that don't appear in meeting content
When `build_prompt()` runs
Then the prompt has no `<reference_context>` block
And the prompt is identical to current behavior

**AC-5: Multiple trove ranking**
Given 4 troves with matching triggers (hit counts: 5, 3, 1, 1)
When `match_reference_triggers` runs
Then only the top 3 by hit count are returned

**AC-6: Manifest schema**
Given an existing trove manifest without `triggers` fields
When `match_reference_triggers` reads it
Then the trove is skipped (no error, no match)

**AC-7: Editorial guardrail**
The `<reference_context>` preamble must contain language directing the LLM to:
- Use reference context only when meeting content directly engages with the topic
- Not flag absence of discussion on reference topics
- Not speculate about why referenced topics were or were not raised

## Scope & Constraints

**In scope:**
- `triggers` field addition to trove manifest schema
- `match_reference_triggers()` function in a new module `pipeline/reference_context.py`
- Modification to `build_prompt()` in `scripts/interpret_meeting.py`
- Trigger configuration for the `school-integration-policy` trove as the first consumer
- Unit tests for trigger matching and prompt construction

**Out of scope:**
- Semantic search or embedding-based matching (see ADR-005)
- Modifications to fold or brief generation (fold already tracks thread lifecycles)
- Trigger auto-generation from trove content
- UI or reporting for which triggers fired (logging only for now)

## Implementation Approach

**TDD cycle 1 — Trigger matching:**
- Test: `match_reference_triggers` returns matching troves given meeting text with trigger terms
- Test: Case-insensitive matching works
- Test: Troves without triggers are skipped gracefully
- Test: Hit-count ranking with >3 matches
- Implement: `pipeline/reference_context.py` with `match_reference_triggers(meeting_text, trove_dir)`

**TDD cycle 2 — Prompt construction:**
- Test: `build_prompt` includes `<reference_context>` when triggers match
- Test: `build_prompt` omits block when no triggers match
- Test: Preamble contains editorial guardrail language
- Implement: Modify `build_prompt()` in `interpret_meeting.py` to call `match_reference_triggers` and inject context

**TDD cycle 3 — Integration:**
- Add triggers to `school-integration-policy` manifest
- Smoke test: run interpretation on a meeting known to discuss boundaries/reconfiguration
- Verify the reference context appears in the prompt and the interpretation references it

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-04-04 | -- | User-requested; implementing with TDD |
