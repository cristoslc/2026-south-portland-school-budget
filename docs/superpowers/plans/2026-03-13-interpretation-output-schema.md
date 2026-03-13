# Interpretation Output Schema Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the per-meeting interpretation contract with SPEC-018 so the schema, validator, sample documents, and generator prompt all use the same three-layer format and downstream specs can rely on it.

**Architecture:** Keep `data/interpretation/meetings/<meeting-id>/<persona-id>.md` as the physical storage format, with YAML frontmatter plus three markdown sections. Treat `data/interpretation/schema/interpretation-output-schema.yaml` and `scripts/validate_interpretation.py` as the canonical contract pair: the schema defines the logical shape and the validator enforces the markdown representation used by the repo's exemplars and future generators.

**Tech Stack:** Python 3.11, PyYAML, pytest, markdown documents with YAML frontmatter

---

## Chunk 1: Contract Realignment

### Task 1: Lock the approved markdown contract in tests

**Files:**
- Create: `tests/test_validate_interpretation.py`
- Modify: `scripts/validate_interpretation.py`
- Test: `tests/test_validate_interpretation.py`

- [ ] **Step 1: Write the failing validator tests**

```python
def test_accepts_boolean_open_question_and_numeric_threat_levels(tmp_path):
    doc = _valid_interpretation_doc(
        open_question=True,
        threat_level=5,
        emotional_valence="negative",
    )
    errors = validate_interpretation(doc, yaml)
    assert errors == []


def test_rejects_legacy_string_open_question_and_named_threat_levels(tmp_path):
    doc = _valid_interpretation_doc(
        open_question="What happens next?",
        threat_level="high",
        emotional_valence="alarmed",
    )
    errors = validate_interpretation(doc, yaml)
    assert any("open_question" in err for err in errors)
    assert any("threat_level" in err for err in errors)


def test_requires_spec_018_journey_columns():
    doc = _valid_interpretation_doc(
        journey_header="| Position | Meeting Event | Persona Cognitive State | Persona Emotional State |"
    )
    errors = validate_interpretation(doc, yaml)
    assert errors == []
```

- [ ] **Step 2: Run the focused test file and confirm it fails for the expected reasons**

Run: `uv run pytest tests/test_validate_interpretation.py -q`
Expected: FAIL because the current validator still accepts legacy values (`alarmed`, `high`, question text strings) and still expects the older six-column journey map table.

- [ ] **Step 3: Update the validator to match SPEC-018 exactly**

Implementation notes:
- Replace the legacy emotional valence enum with `positive`, `negative`, `neutral`.
- Require `threat_level` to parse as an integer in the range `1..5`.
- Require `open_question` to parse as a boolean literal (`true` / `false`).
- Change journey map validation to the four required columns: `Position`, `Meeting Event`, `Persona Cognitive State`, `Persona Emotional State`.
- Keep the section-count checks and the reactions free-form length check.
- Continue to validate frontmatter dates and required IDs.

- [ ] **Step 4: Re-run the validator tests**

Run: `uv run pytest tests/test_validate_interpretation.py -q`
Expected: PASS

- [ ] **Step 5: Commit the validator contract work**

```bash
git add tests/test_validate_interpretation.py scripts/validate_interpretation.py
git commit -m "test: lock SPEC-018 interpretation validator contract"
```

### Task 2: Realign the canonical schema artifacts with the approved contract

**Files:**
- Create: `tests/test_interpretation_schema_contract.py`
- Modify: `data/interpretation/schema/interpretation-output-schema.yaml`
- Modify: `data/interpretation/schema/README.md`
- Test: `tests/test_interpretation_schema_contract.py`

- [ ] **Step 1: Write the failing schema-artifact tests**

```python
def test_schema_requires_spec_018_fields():
    schema = yaml.safe_load(
        Path("data/interpretation/schema/interpretation-output-schema.yaml").read_text()
    )
    point = schema["$defs"]["structured_point"]
    beat = schema["$defs"]["journey_beat"]

    assert point["properties"]["emotional_valence"]["enum"] == [
        "positive",
        "negative",
        "neutral",
    ]
    assert point["properties"]["threat_level"]["minimum"] == 1
    assert point["properties"]["threat_level"]["maximum"] == 5
    assert point["properties"]["open_question"]["type"] == "boolean"
    assert beat["required"] == [
        "position",
        "meeting_event",
        "persona_cognitive_state",
        "persona_emotional_state",
    ]
```

- [ ] **Step 2: Run the schema tests and confirm they fail**

Run: `uv run pytest tests/test_interpretation_schema_contract.py -q`
Expected: FAIL because the checked-in schema still defines the older eight-value emotion enum, `1..4` threat levels, string `open_question`, and the old journey beat field names.

- [ ] **Step 3: Update the YAML schema and schema README**

Implementation notes:
- Make the YAML schema and README describe the same contract the validator enforces.
- Update the example document in the README so its structured points and journey map illustrate the approved field names and value ranges.
- Add a short compatibility note explaining that obsolete fields from the SPIKE-005 draft (`timestamp_range`, `beat_label`, `internal_monologue`, named threat levels, question-text open questions) are no longer part of the normative SPEC-018 contract.

- [ ] **Step 4: Re-run the schema contract tests**

Run: `uv run pytest tests/test_interpretation_schema_contract.py -q`
Expected: PASS

- [ ] **Step 5: Commit the schema artifact realignment**

```bash
git add tests/test_interpretation_schema_contract.py \
  data/interpretation/schema/interpretation-output-schema.yaml \
  data/interpretation/schema/README.md
git commit -m "docs: align interpretation schema artifacts with SPEC-018"
```

## Chunk 2: Exemplars And Generator Alignment

### Task 3: Migrate the exemplar interpretation documents and prove persona differentiation

**Files:**
- Create: `tests/test_interpretation_examples.py`
- Modify: `data/interpretation/meetings/2026-03-02-school-board/PERSONA-001.md`
- Modify: `data/interpretation/meetings/2026-03-02-school-board/PERSONA-006.md`
- Modify: `data/interpretation/meetings/2026-03-02-school-board/PERSONA-012.md`
- Test: `tests/test_interpretation_examples.py`

- [ ] **Step 1: Write the failing exemplar tests**

```python
def test_example_documents_validate_against_spec_018_contract():
    for path in EXAMPLE_DOCS:
        text = path.read_text(encoding="utf-8")
        assert validate_interpretation(text, yaml) == []


def test_examples_show_cross_persona_difference():
    docs = [parse_example(path) for path in EXAMPLE_DOCS]
    first_facts = {doc["persona_id"]: {point["fact"] for point in doc["structured_points"]} for doc in docs}
    first_valences = {
        doc["persona_id"]: {point["fact"]: point["emotional_valence"] for point in doc["structured_points"]}
        for doc in docs
    }

    assert len(set(map(frozenset, first_facts.values()))) > 1 or has_shared_fact_valence_delta(first_valences)
```

- [ ] **Step 2: Run the exemplar tests and confirm they fail**

Run: `uv run pytest tests/test_interpretation_examples.py -q`
Expected: FAIL because the current example documents still use named threat levels, question text strings, and the superseded journey-map table.

- [ ] **Step 3: Rewrite the three sample interpretation documents**

Implementation notes:
- Keep the same meeting (`2026-03-02-school-board`) and personas (`PERSONA-001`, `PERSONA-006`, `PERSONA-012`) so downstream work still has stable sample inputs.
- Convert structured points to the approved values: `positive|negative|neutral`, integer threat levels `1..5`, boolean `open_question`.
- Replace the journey map with the four-column representation required by SPEC-018.
- Preserve the free-form first-person reaction voice so the examples remain useful as human review fixtures.
- Ensure the three personas remain meaningfully different, not just reworded copies.

- [ ] **Step 4: Re-run the exemplar tests**

Run: `uv run pytest tests/test_interpretation_examples.py -q`
Expected: PASS

- [ ] **Step 5: Commit the exemplar migration**

```bash
git add tests/test_interpretation_examples.py \
  data/interpretation/meetings/2026-03-02-school-board/PERSONA-001.md \
  data/interpretation/meetings/2026-03-02-school-board/PERSONA-006.md \
  data/interpretation/meetings/2026-03-02-school-board/PERSONA-012.md
git commit -m "test: add SPEC-018 exemplar coverage"
```

### Task 4: Bring the interpretation generator onto the same contract and verify the end-to-end surface

**Files:**
- Modify: `scripts/interpret_meeting.py`
- Modify: `scripts/validate_interpretation.py`
- Test: `tests/test_validate_interpretation.py`
- Test: `tests/test_interpretation_examples.py`

- [ ] **Step 1: Add a failing regression around generator prompt drift**

```python
def test_generator_prompt_uses_spec_018_field_names():
    prompt = build_output_contract_snippet(...)
    assert "positive / negative / neutral" in prompt
    assert "Threat level: [1-5]" in prompt
    assert "Position | Meeting Event | Persona Cognitive State | Persona Emotional State" in prompt
```

- [ ] **Step 2: Run the focused regression and confirm it fails**

Run: `uv run pytest tests/test_validate_interpretation.py tests/test_interpretation_examples.py -k "generator or contract" -q`
Expected: FAIL because `scripts/interpret_meeting.py` still instructs the model to emit the deprecated values and section structure.

- [ ] **Step 3: Update the runner prompt and quick validation hook**

Implementation notes:
- Change the output contract snippet in `scripts/interpret_meeting.py` so the model is asked for the SPEC-018 field names and value ranges.
- Make `_quick_validate()` check the same section names and journey map header the full validator now expects.
- Avoid introducing a second independent rule set; if a small shared helper extracted from `scripts/validate_interpretation.py` reduces drift, do that as part of this task.

- [ ] **Step 4: Run the full verification set**

Run: `uv run pytest tests/test_validate_interpretation.py tests/test_interpretation_schema_contract.py tests/test_interpretation_examples.py -q`
Expected: PASS

Run: `python3 scripts/validate_interpretation.py --all`
Expected: exit code `0` and all checked interpretation documents reported as valid.

- [ ] **Step 5: Commit the generator-alignment pass**

```bash
git add scripts/interpret_meeting.py scripts/validate_interpretation.py \
  tests/test_validate_interpretation.py \
  tests/test_interpretation_schema_contract.py \
  tests/test_interpretation_examples.py
git commit -m "feat: align interpretation generator with SPEC-018"
```

Plan complete and saved to `docs/superpowers/plans/2026-03-13-interpretation-output-schema.md`. Ready to execute?
