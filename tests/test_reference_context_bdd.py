"""BDD integration tests for keyword-triggered reference context (SPEC-081).

These test the full integration path: bundle loading → trigger matching →
prompt construction, using realistic data structures.
"""

import importlib.util
import sys
from pathlib import Path

import yaml

# Import interpret_meeting.py as a module (same pattern as test_generate_briefs)
_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "interpret_meeting.py"
)
_spec = importlib.util.spec_from_file_location("interpret_meeting", _SCRIPT_PATH)
im = importlib.util.module_from_spec(_spec)
sys.modules["interpret_meeting"] = im
_spec.loader.exec_module(im)

from pipeline.reference_context import match_reference_triggers, build_reference_context_block


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_trove_with_triggers(tmp_path, trove_id, trigger_lists, synthesis):
    """Create a trove with triggers on its sources."""
    trove_dir = tmp_path / "docs" / "troves" / trove_id
    trove_dir.mkdir(parents=True, exist_ok=True)
    sources = []
    for i, triggers in enumerate(trigger_lists):
        sources.append({
            "source-id": f"src-{i}",
            "type": "web",
            "title": f"Source {i}",
            "triggers": triggers,
        })
    manifest = {
        "trove": trove_id,
        "created": "2026-04-04",
        "refreshed": "2026-04-04",
        "tags": ["test"],
        "sources": sources,
    }
    (trove_dir / "manifest.yaml").write_text(
        yaml.dump(manifest, default_flow_style=False)
    )
    (trove_dir / "synthesis.md").write_text(synthesis)


class _FakePersona:
    """Minimal persona object matching interpret_meeting.py's interface."""
    def __init__(self, pid="PERSONA-001", name="Test Parent"):
        self.id = pid
        self.name = name
        self.content = f"---\ntitle: {name}\n---\n\n# {name}\n\nA test persona."
        self.reaction_audience = "a friend, catching them up"


def _make_bundle_data(meeting_text, meeting_id="2026-04-04-test"):
    """Create a minimal bundle_data dict."""
    return {
        "manifest": {},
        "meeting_id": meeting_id,
        "meeting_context": meeting_text,
        "title": "Test Meeting",
        "date": "2026-04-04",
        "duration": "01:30:00",
    }


# ---------------------------------------------------------------------------
# Scenario: Meeting discusses boundaries — reference context appears in prompt
# ---------------------------------------------------------------------------

class TestScenarioMeetingDiscussesBoundaries:
    """
    Given a trove with triggers for boundary/configuration terms
    And a meeting where the board discusses attendance zones and Brickhill
    When the interpretation prompt is built
    Then the prompt contains a <reference_context> block
    And the block contains the trove's synthesis
    And the block appears between </instruction> and <meeting_context>
    And the editorial guardrail is present
    """

    def test_full_prompt_integration(self, tmp_path):
        _make_trove_with_triggers(
            tmp_path, "school-integration-policy",
            [
                ["boundaries", "Brickhill", "attendance zone"],
                ["magnet", "controlled choice"],
            ],
            "# Synthesis\n\nThe district explored controlled choice in 2024.",
        )

        meeting_text = (
            "The superintendent presented three reconfiguration options. "
            "Discussion focused on attendance zone changes affecting the "
            "Brickhill neighborhood. Several parents asked about controlled "
            "choice as an alternative."
        )

        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        ref_block = build_reference_context_block(matches)

        persona = _FakePersona()
        bundle = _make_bundle_data(meeting_text)
        prompt = im.build_prompt(persona, bundle, reference_context_block=ref_block)

        # Block is present
        assert "<reference_context>" in prompt
        assert "</reference_context>" in prompt

        # Synthesis content included
        assert "controlled choice in 2024" in prompt

        # Block is between </instruction> and <meeting_context>
        instr_end = prompt.index("</instruction>")
        ref_start = prompt.index("<reference_context>")
        meeting_start = prompt.index("<meeting_context>")
        assert instr_end < ref_start < meeting_start

        # Editorial guardrail
        ref_section = prompt[ref_start:prompt.index("</reference_context>")]
        assert "absence" in ref_section.lower() or "not raised" in ref_section.lower()


# ---------------------------------------------------------------------------
# Scenario: Meeting has no relevant topics — prompt is unchanged
# ---------------------------------------------------------------------------

class TestScenarioMeetingNoRelevantTopics:
    """
    Given a trove with triggers for boundary/configuration terms
    And a meeting that only discusses the transportation budget
    When the interpretation prompt is built
    Then the prompt does NOT contain a <reference_context> block
    And the prompt is otherwise identical to the pre-SPEC-081 format
    """

    def test_no_injection_when_no_triggers(self, tmp_path):
        _make_trove_with_triggers(
            tmp_path, "school-integration-policy",
            [["boundaries", "Brickhill", "attendance zone"]],
            "Synthesis content.",
        )

        meeting_text = (
            "The transportation budget was reviewed. Bus route changes "
            "will take effect in September."
        )

        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        ref_block = build_reference_context_block(matches)

        persona = _FakePersona()
        bundle = _make_bundle_data(meeting_text)

        prompt_with = im.build_prompt(persona, bundle, reference_context_block=ref_block)
        prompt_without = im.build_prompt(persona, bundle)

        assert "<reference_context>" not in prompt_with
        assert "<reference_context>" not in prompt_without
        # The only difference should be an empty string vs empty string
        assert prompt_with == prompt_without


# ---------------------------------------------------------------------------
# Scenario: Multiple troves compete — top 3 by hit count win
# ---------------------------------------------------------------------------

class TestScenarioMultipleTrovesCompete:
    """
    Given 4 troves with triggers
    And meeting text that matches all 4
    When reference context is built
    Then only the top 3 by hit count are injected
    And they appear in descending hit-count order
    """

    def test_top_three_injected(self, tmp_path):
        _make_trove_with_triggers(
            tmp_path, "trove-high",
            [["budget", "cost", "funding", "tax", "revenue"]],
            "High hit trove.",
        )
        _make_trove_with_triggers(
            tmp_path, "trove-medium",
            [["budget", "cost", "funding"]],
            "Medium hit trove.",
        )
        _make_trove_with_triggers(
            tmp_path, "trove-low-a",
            [["budget"]],
            "Low-A trove.",
        )
        _make_trove_with_triggers(
            tmp_path, "trove-low-b",
            [["budget"]],
            "Low-B trove.",
        )

        meeting_text = (
            "The budget includes cost estimates for funding. Revenue "
            "projections show a tax increase is needed."
        )

        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        ref_block = build_reference_context_block(matches)

        assert len(matches) == 3
        assert "High hit trove." in ref_block
        assert "Medium hit trove." in ref_block
        # One of the low troves is included, the other is not
        low_count = sum(1 for t in ["Low-A trove.", "Low-B trove."] if t in ref_block)
        assert low_count == 1


# ---------------------------------------------------------------------------
# Scenario: Trove without triggers is invisible to matching
# ---------------------------------------------------------------------------

class TestScenarioTroveWithoutTriggers:
    """
    Given a trove with no triggers fields on any source
    And a meeting that contains words from the trove's tags
    When trigger matching runs
    Then the trove is NOT matched (tags are not triggers)
    """

    def test_tags_are_not_triggers(self, tmp_path):
        trove_dir = tmp_path / "docs" / "troves" / "budget-docs"
        trove_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "trove": "budget-docs",
            "created": "2026-04-04",
            "tags": ["budget", "fiscal", "revenue"],
            "sources": [
                {"source-id": "s1", "type": "document", "title": "Budget Book"},
            ],
        }
        (trove_dir / "manifest.yaml").write_text(
            yaml.dump(manifest, default_flow_style=False)
        )
        (trove_dir / "synthesis.md").write_text("Budget synthesis.")

        meeting_text = "The budget and revenue projections were discussed."
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert len(matches) == 0
