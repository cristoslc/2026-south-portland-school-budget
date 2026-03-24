---
id: SPEC-030
title: PERSONA-015 Journey Map Validation Failure
type: bug
parent-initiative: ""
parent-epic: ""
status: Active
priority-weight: low
created: 2026-03-24
last-updated: 2026-03-24
---

# SPEC-030: PERSONA-015 Journey Map Validation Failure

## Problem

`test_interpretation_examples.py::test_example_validates[PERSONA-015]` fails because the PERSONA-015 interpretation for `2026-03-02-school-board` uses a Mermaid `journey` block instead of the required markdown table with columns: `Position | Meeting Event | Persona Cognitive State | Persona Emotional State`.

This is likely a prompt regression — the interpretation was generated before the journey_map table format was standardized in SPEC-018.

## Fix

Re-run the interpretation for PERSONA-015 on `2026-03-02-school-board` to regenerate with the current prompt (which enforces the table format).

```bash
python3 scripts/interpret_meeting.py data/interpretation/bundles/2026-03-02-school-board --persona PERSONA-015 --force
```

## Acceptance Criteria

- [ ] `python3 -m pytest tests/test_interpretation_examples.py -k PERSONA-015` passes
- [ ] Journey map section uses the markdown table format per SPEC-018

## Lifecycle

| Phase | Date | Commit |
|-------|------|--------|
| Active | 2026-03-24 | |
