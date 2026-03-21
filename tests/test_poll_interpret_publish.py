"""Tests for poll_interpret.py brief publishing behavior."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "poll_interpret.py"
_spec = importlib.util.spec_from_file_location("poll_interpret_publish", _SCRIPT_PATH)
pi = importlib.util.module_from_spec(_spec)
sys.modules["poll_interpret_publish"] = pi
_spec.loader.exec_module(pi)


def test_publish_briefs_includes_general_outputs(tmp_path):
    source_dir = tmp_path / "data" / "interpretation" / "briefs" / "2026-03-23"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "PERSONA-001.md").write_text("persona", encoding="utf-8")
    (source_dir / "PERSONA-000-upcoming.md").write_text("upcoming", encoding="utf-8")
    (source_dir / "PERSONA-000-evergreen.md").write_text("evergreen", encoding="utf-8")

    persona_dir = (
        tmp_path / "docs" / "persona" / "Active" / "(PERSONA-001)-Concerned-Parent"
    )
    persona_dir.mkdir(parents=True, exist_ok=True)

    with (
        patch.object(pi, "BRIEFS_DIR", tmp_path / "data" / "interpretation" / "briefs"),
        patch.object(pi, "DIST_BRIEFS_DIR", tmp_path / "dist" / "briefings"),
        patch.object(pi, "PERSONA_DIR", tmp_path / "docs" / "persona" / "Active"),
    ):
        assert pi.publish_briefs("2026-03-23") is True

    dist_dir = tmp_path / "dist" / "briefings"
    assert (dist_dir / "persona-001-concerned-parent.md").read_text(encoding="utf-8") == "persona"
    assert (dist_dir / "general-upcoming-briefing.md").read_text(encoding="utf-8") == "upcoming"
    assert (dist_dir / "general-budget-briefing.md").read_text(encoding="utf-8") == "evergreen"
