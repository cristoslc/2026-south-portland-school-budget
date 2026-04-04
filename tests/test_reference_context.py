"""Tests for keyword-triggered reference context injection (SPEC-081)."""

import textwrap
from pathlib import Path

import yaml

from pipeline.reference_context import match_reference_triggers, build_reference_context_block


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_trove(tmp_path, trove_id, sources_with_triggers, synthesis_text="Synthesis."):
    """Create a minimal trove directory with manifest and synthesis."""
    trove_dir = tmp_path / "docs" / "troves" / trove_id
    trove_dir.mkdir(parents=True, exist_ok=True)

    sources = []
    for src in sources_with_triggers:
        entry = {
            "source-id": src["id"],
            "type": "web",
            "title": src.get("title", src["id"]),
        }
        if "triggers" in src:
            entry["triggers"] = src["triggers"]
        sources.append(entry)

    manifest = {
        "trove": trove_id,
        "created": "2026-04-04",
        "refreshed": "2026-04-04",
        "tags": ["test"],
        "sources": sources,
    }
    (trove_dir / "manifest.yaml").write_text(yaml.dump(manifest, default_flow_style=False))
    (trove_dir / "synthesis.md").write_text(synthesis_text)
    return trove_dir


# ---------------------------------------------------------------------------
# TDD Cycle 1: Trigger matching
# ---------------------------------------------------------------------------

class TestMatchReferenceTriggers:
    """AC-1, AC-2, AC-5, AC-6."""

    def test_basic_trigger_match(self, tmp_path):
        """AC-1: triggers in meeting text produce a match."""
        _make_trove(tmp_path, "integration-policy", [
            {"id": "src-1", "triggers": ["controlled choice", "magnet"]},
        ])
        meeting_text = "the Board discussed controlled choice options for next year"
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert len(matches) == 1
        assert matches[0]["trove_id"] == "integration-policy"

    def test_case_insensitive(self, tmp_path):
        """AC-2: matching is case-insensitive."""
        _make_trove(tmp_path, "boundaries", [
            {"id": "src-1", "triggers": ["Brickhill", "attendance zone"]},
        ])
        meeting_text = "brickhill families expressed concern about ATTENDANCE ZONE review"
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert len(matches) == 1
        assert matches[0]["hit_count"] == 2

    def test_no_triggers_field_skipped(self, tmp_path):
        """AC-6: troves without triggers are skipped gracefully."""
        _make_trove(tmp_path, "budget-docs", [
            {"id": "src-1"},  # no triggers
        ])
        meeting_text = "budget documents were distributed"
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert len(matches) == 0

    def test_no_match_returns_empty(self, tmp_path):
        """Triggers that don't appear in text produce no match."""
        _make_trove(tmp_path, "integration", [
            {"id": "src-1", "triggers": ["controlled choice", "magnet"]},
        ])
        meeting_text = "the superintendent presented the transportation budget"
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert len(matches) == 0

    def test_multiple_troves_ranked_by_hit_count(self, tmp_path):
        """AC-5: when >3 troves match, top 3 by hit count are returned."""
        _make_trove(tmp_path, "trove-a", [
            {"id": "s1", "triggers": ["budget", "cost", "funding", "revenue", "tax"]},
        ], synthesis_text="A")
        _make_trove(tmp_path, "trove-b", [
            {"id": "s1", "triggers": ["budget", "cost", "funding"]},
        ], synthesis_text="B")
        _make_trove(tmp_path, "trove-c", [
            {"id": "s1", "triggers": ["budget"]},
        ], synthesis_text="C")
        _make_trove(tmp_path, "trove-d", [
            {"id": "s1", "triggers": ["budget"]},
        ], synthesis_text="D")

        meeting_text = "the budget includes cost estimates for funding, revenue projections, and tax impact"
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert len(matches) == 3
        assert matches[0]["trove_id"] == "trove-a"
        assert matches[1]["trove_id"] == "trove-b"

    def test_triggers_aggregated_across_sources(self, tmp_path):
        """Hit count sums across all sources in a trove."""
        _make_trove(tmp_path, "multi-source", [
            {"id": "s1", "triggers": ["magnet"]},
            {"id": "s2", "triggers": ["controlled choice"]},
        ])
        meeting_text = "the magnet program and controlled choice were discussed"
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert len(matches) == 1
        assert matches[0]["hit_count"] == 2

    def test_empty_troves_dir(self, tmp_path):
        """No troves directory is handled gracefully."""
        troves_dir = tmp_path / "docs" / "troves"
        # don't create it
        matches = match_reference_triggers("some text", troves_dir)
        assert matches == []

    def test_synthesis_content_returned(self, tmp_path):
        """Match result includes the trove's synthesis text."""
        _make_trove(tmp_path, "policy", [
            {"id": "s1", "triggers": ["equity"]},
        ], synthesis_text="# Synthesis\n\nKey findings about equity.")
        meeting_text = "equity in resource distribution was the main topic"
        matches = match_reference_triggers(meeting_text, tmp_path / "docs" / "troves")
        assert "Key findings about equity" in matches[0]["synthesis"]


# ---------------------------------------------------------------------------
# TDD Cycle 2: Prompt block construction
# ---------------------------------------------------------------------------

class TestBuildReferenceContextBlock:
    """AC-3, AC-4, AC-7."""

    def test_block_with_matches(self, tmp_path):
        """AC-3: matched troves produce a <reference_context> block."""
        _make_trove(tmp_path, "policy", [
            {"id": "s1", "triggers": ["equity"]},
        ], synthesis_text="# Synthesis\n\nEquity findings.")
        matches = match_reference_triggers(
            "equity was discussed", tmp_path / "docs" / "troves"
        )
        block = build_reference_context_block(matches)
        assert "<reference_context>" in block
        assert "</reference_context>" in block
        assert "Equity findings." in block

    def test_no_matches_returns_empty(self, tmp_path):
        """AC-4: no matches produce no block."""
        block = build_reference_context_block([])
        assert block == ""

    def test_editorial_guardrail_present(self, tmp_path):
        """AC-7: the preamble contains the no-absence-editorializing guardrail."""
        _make_trove(tmp_path, "policy", [
            {"id": "s1", "triggers": ["equity"]},
        ], synthesis_text="Findings.")
        matches = match_reference_triggers(
            "equity was discussed", tmp_path / "docs" / "troves"
        )
        block = build_reference_context_block(matches)
        # Must instruct LLM not to flag absence
        assert "absence" in block.lower() or "not raised" in block.lower() or "not mentioned" in block.lower()
        # Must instruct LLM to use context only when meeting engages
        assert "directly engages" in block.lower() or "directly engage" in block.lower()

    def test_multiple_troves_in_block(self, tmp_path):
        """Multiple matched troves each appear as labeled sections."""
        _make_trove(tmp_path, "trove-a", [
            {"id": "s1", "triggers": ["budget"]},
        ], synthesis_text="Trove A content.")
        _make_trove(tmp_path, "trove-b", [
            {"id": "s1", "triggers": ["budget"]},
        ], synthesis_text="Trove B content.")
        matches = match_reference_triggers(
            "budget discussion", tmp_path / "docs" / "troves"
        )
        block = build_reference_context_block(matches)
        assert "Trove A content." in block
        assert "Trove B content." in block
