"""Tests for generate_briefs.py general briefing support."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "generate_briefs.py"
)
_spec = importlib.util.spec_from_file_location("generate_briefs", _SCRIPT_PATH)
gb = importlib.util.module_from_spec(_spec)
sys.modules["generate_briefs"] = gb
_spec.loader.exec_module(gb)


def _make_persona(tmp_path, persona_num, slug, title):
    persona_dir = tmp_path / "docs" / "persona" / "Active" / f"(PERSONA-{persona_num:03d})-{slug}"
    persona_dir.mkdir(parents=True, exist_ok=True)
    content = f"""\
# {title}

## Archetype Label
Test Audience

## Core Orientation
Needs clear, practical information about the budget.

## Lifecycle
Active
"""
    (persona_dir / "persona.md").write_text(content, encoding="utf-8")
    return persona_dir


def test_run_briefs_dry_run_includes_general_outputs(tmp_path):
    _make_persona(tmp_path, 1, "Concerned-Parent", "Maria")

    with (
        patch.object(gb, "PERSONA_DIR", tmp_path / "docs" / "persona" / "Active"),
        patch.object(gb, "BRIEFS_DIR", tmp_path / "data" / "interpretation" / "briefs"),
        patch.object(
            gb,
            "INTER_MEETING_MANIFEST",
            tmp_path / "data" / "interpretation" / "inter-meeting" / "manifest.yaml",
        ),
        patch.object(gb, "CUMULATIVE_DIR", tmp_path / "data" / "interpretation" / "cumulative"),
    ):
        personas = gb.load_personas()
        stats = gb.run_briefs("2026-03-23", personas, dry_run=True)

    assert stats["processed"] == 3
