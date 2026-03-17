"""Tests for poll_interpret.py gap detection logic."""

import datetime
import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# scripts/ is not a Python package — load the module from its file path.
_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "poll_interpret.py"
_spec = importlib.util.spec_from_file_location("poll_interpret", _SCRIPT_PATH)
pi = importlib.util.module_from_spec(_spec)
sys.modules["poll_interpret"] = pi
_spec.loader.exec_module(pi)


# ---------------------------------------------------------------------------
# Helpers: build mock directory trees inside tmp_path
# ---------------------------------------------------------------------------

def _make_personas(tmp_path, names):
    """Create persona dirs like (PERSONA-001)-Foo under tmp_path."""
    d = tmp_path / "docs" / "persona" / "Validated"
    d.mkdir(parents=True, exist_ok=True)
    for name in names:
        (d / name).mkdir()
    return d


def _make_bundles(tmp_path, meeting_ids, *, with_manifest=True):
    """Create bundle dirs with optional manifest.yaml."""
    d = tmp_path / "data" / "interpretation" / "bundles"
    d.mkdir(parents=True, exist_ok=True)
    for mid in meeting_ids:
        md = d / mid
        md.mkdir()
        if with_manifest:
            (md / "manifest.yaml").touch()
    return d


def _make_interpretations(tmp_path, meeting_id, persona_nums):
    """Create PERSONA-NNN.md files in the meetings dir."""
    d = tmp_path / "data" / "interpretation" / "meetings" / meeting_id
    d.mkdir(parents=True, exist_ok=True)
    for n in persona_nums:
        (d / f"PERSONA-{n:03d}.md").touch()
    return d


def _make_cumulative(tmp_path, persona_id, dates):
    """Create cumulative fold records for a persona."""
    d = tmp_path / "data" / "interpretation" / "cumulative" / persona_id
    d.mkdir(parents=True, exist_ok=True)
    for date_str in dates:
        (d / f"{date_str}.md").touch()
    return d


# ---------------------------------------------------------------------------
# Fixtures: patch module-level directory constants
# ---------------------------------------------------------------------------

@pytest.fixture()
def dirs(tmp_path):
    """Patch all module-level directory constants to point at tmp_path."""
    patches = {
        "PERSONA_DIR": tmp_path / "docs" / "persona" / "Validated",
        "BUNDLES_DIR": tmp_path / "data" / "interpretation" / "bundles",
        "MEETINGS_DIR": tmp_path / "data" / "interpretation" / "meetings",
        "CUMULATIVE_DIR": tmp_path / "data" / "interpretation" / "cumulative",
    }
    with (
        patch.object(pi, "PERSONA_DIR", patches["PERSONA_DIR"]),
        patch.object(pi, "BUNDLES_DIR", patches["BUNDLES_DIR"]),
        patch.object(pi, "MEETINGS_DIR", patches["MEETINGS_DIR"]),
        patch.object(pi, "CUMULATIVE_DIR", patches["CUMULATIVE_DIR"]),
    ):
        yield tmp_path


# ---------------------------------------------------------------------------
# 1. count_personas
# ---------------------------------------------------------------------------

class TestCountPersonas:
    def test_no_dir(self, dirs):
        assert pi.count_personas() == 0

    def test_empty_dir(self, dirs):
        _make_personas(dirs, [])
        assert pi.count_personas() == 0

    def test_counts_valid_personas(self, dirs):
        _make_personas(dirs, [
            "(PERSONA-001)-Budget-Hawk",
            "(PERSONA-002)-Parent-Advocate",
            "(PERSONA-003)-Teacher-Rep",
        ])
        assert pi.count_personas() == 3

    def test_ignores_non_persona_dirs(self, dirs):
        persona_dir = _make_personas(dirs, [
            "(PERSONA-001)-Budget-Hawk",
        ])
        # Add a non-matching dir
        (persona_dir / "random-folder").mkdir()
        # Add a file (not a dir)
        (persona_dir / "notes.txt").touch()
        assert pi.count_personas() == 1


# ---------------------------------------------------------------------------
# 2. list_bundles
# ---------------------------------------------------------------------------

class TestListBundles:
    def test_no_dir(self, dirs):
        assert pi.list_bundles() == []

    def test_returns_sorted_meeting_ids(self, dirs):
        _make_bundles(dirs, [
            "2026-03-15-school-board",
            "2026-03-02-school-board",
            "2026-03-10-city-council",
        ])
        result = pi.list_bundles()
        assert result == [
            "2026-03-02-school-board",
            "2026-03-10-city-council",
            "2026-03-15-school-board",
        ]

    def test_requires_manifest(self, dirs):
        bundles_dir = _make_bundles(dirs, ["2026-03-02-school-board"])
        # Add a bundle WITHOUT manifest
        no_manifest = bundles_dir / "2026-03-10-city-council"
        no_manifest.mkdir()
        result = pi.list_bundles()
        assert result == ["2026-03-02-school-board"]

    def test_ignores_non_meeting_dirs(self, dirs):
        bundles_dir = _make_bundles(dirs, ["2026-03-02-school-board"])
        bad = bundles_dir / "not-a-meeting"
        bad.mkdir()
        (bad / "manifest.yaml").touch()
        assert pi.list_bundles() == ["2026-03-02-school-board"]


# ---------------------------------------------------------------------------
# 3. count_interpretations
# ---------------------------------------------------------------------------

class TestCountInterpretations:
    def test_no_dir(self, dirs):
        assert pi.count_interpretations("2026-03-02-school-board") == 0

    def test_counts_persona_files(self, dirs):
        _make_interpretations(dirs, "2026-03-02-school-board", [1, 2, 3])
        assert pi.count_interpretations("2026-03-02-school-board") == 3

    def test_ignores_non_persona_files(self, dirs):
        d = _make_interpretations(dirs, "2026-03-02-school-board", [1])
        (d / "summary.md").touch()
        (d / "PERSONA-bad.md").touch()
        (d / "notes.txt").touch()
        assert pi.count_interpretations("2026-03-02-school-board") == 1


# ---------------------------------------------------------------------------
# 4. list_folded_meetings
# ---------------------------------------------------------------------------

class TestListFoldedMeetings:
    def test_no_dir(self, dirs):
        assert pi.list_folded_meetings("PERSONA-001") == set()

    def test_returns_date_stems(self, dirs):
        _make_cumulative(dirs, "PERSONA-001", ["2026-03-02", "2026-03-10"])
        result = pi.list_folded_meetings("PERSONA-001")
        assert result == {"2026-03-02", "2026-03-10"}

    def test_excludes_summary(self, dirs):
        d = _make_cumulative(dirs, "PERSONA-001", ["2026-03-02"])
        (d / "summary.md").touch()
        result = pi.list_folded_meetings("PERSONA-001")
        assert result == {"2026-03-02"}


# ---------------------------------------------------------------------------
# 5. extract_meeting_date
# ---------------------------------------------------------------------------

class TestExtractMeetingDate:
    def test_school_board(self):
        assert pi.extract_meeting_date("2026-03-02-school-board") == "2026-03-02"

    def test_city_council(self):
        assert pi.extract_meeting_date("2026-03-10-city-council") == "2026-03-10"

    def test_short_id(self):
        assert pi.extract_meeting_date("2026-03") == "2026-03"

    def test_bare_date(self):
        assert pi.extract_meeting_date("2026-03-02") == "2026-03-02"


# ---------------------------------------------------------------------------
# 6. detect_gaps
# ---------------------------------------------------------------------------

class TestDetectGaps:
    """Tests for the main gap detection logic."""

    @pytest.fixture(autouse=True)
    def _freeze_date(self):
        """Pin 'today' to 2026-03-16 for deterministic tests."""
        fake_today = datetime.date(2026, 3, 16)
        with patch("scripts.poll_interpret.datetime") as mock_dt:
            mock_dt.date.today.return_value = fake_today
            mock_dt.date.side_effect = lambda *a, **kw: datetime.date(*a, **kw)
            yield

    def test_no_bundles(self, dirs):
        gaps = pi.detect_gaps(3)
        assert gaps["needs_interpretation"] == []
        assert gaps["needs_fold"] == []
        assert gaps["interpretation_complete"] == []

    def test_uninterpreted_meeting(self, dirs):
        """A bundled meeting with zero interpretations needs interpretation."""
        _make_bundles(dirs, ["2026-03-02-school-board"])
        gaps = pi.detect_gaps(3)
        assert gaps["needs_interpretation"] == [("2026-03-02-school-board", 0)]
        assert gaps["interpretation_complete"] == []

    def test_partial_interpretation(self, dirs):
        """A meeting with fewer than num_personas interpretations still needs work."""
        _make_bundles(dirs, ["2026-03-02-school-board"])
        _make_interpretations(dirs, "2026-03-02-school-board", [1])
        gaps = pi.detect_gaps(14)
        assert gaps["needs_interpretation"] == [("2026-03-02-school-board", 1)]

    def test_fully_interpreted_no_fold(self, dirs):
        """Fully interpreted meeting without fold record needs folding."""
        _make_personas(dirs, [
            "(PERSONA-001)-A", "(PERSONA-002)-B", "(PERSONA-003)-C",
        ])
        _make_bundles(dirs, ["2026-03-02-school-board"])
        _make_interpretations(dirs, "2026-03-02-school-board", [1, 2, 3])
        gaps = pi.detect_gaps(3)
        assert gaps["needs_interpretation"] == []
        assert gaps["interpretation_complete"] == ["2026-03-02-school-board"]
        assert "2026-03-02-school-board" in gaps["needs_fold"]

    def test_fully_interpreted_and_folded(self, dirs):
        """Fully interpreted + folded meeting needs nothing."""
        _make_personas(dirs, [
            "(PERSONA-001)-A", "(PERSONA-002)-B",
        ])
        _make_bundles(dirs, ["2026-03-02-school-board"])
        _make_interpretations(dirs, "2026-03-02-school-board", [1, 2])
        _make_cumulative(dirs, "PERSONA-001", ["2026-03-02"])
        _make_cumulative(dirs, "PERSONA-002", ["2026-03-02"])
        gaps = pi.detect_gaps(2)
        assert gaps["needs_interpretation"] == []
        assert gaps["needs_fold"] == []

    def test_future_meeting_excluded(self, dirs):
        """Meetings after today should not appear in needs_interpretation."""
        _make_bundles(dirs, [
            "2026-03-02-school-board",   # past
            "2026-03-20-school-board",   # future
        ])
        _make_interpretations(dirs, "2026-03-02-school-board", [1, 2, 3])
        gaps = pi.detect_gaps(3)
        # Future meeting should not appear anywhere
        future_ids = [mid for mid, _ in gaps["needs_interpretation"]]
        assert "2026-03-20-school-board" not in future_ids
        assert "2026-03-20-school-board" not in gaps["interpretation_complete"]

    def test_today_meeting_included(self, dirs):
        """A meeting on today's date IS eligible for interpretation."""
        _make_bundles(dirs, ["2026-03-16-school-board"])
        gaps = pi.detect_gaps(3)
        assert gaps["needs_interpretation"] == [("2026-03-16-school-board", 0)]

    def test_partial_fold_across_personas(self, dirs):
        """If one persona is missing a fold, the meeting needs fold."""
        _make_personas(dirs, [
            "(PERSONA-001)-A", "(PERSONA-002)-B",
        ])
        _make_bundles(dirs, ["2026-03-02-school-board"])
        _make_interpretations(dirs, "2026-03-02-school-board", [1, 2])
        # Only persona-001 has the fold
        _make_cumulative(dirs, "PERSONA-001", ["2026-03-02"])
        gaps = pi.detect_gaps(2)
        assert "2026-03-02-school-board" in gaps["needs_fold"]

    def test_chronological_fold_order(self, dirs):
        """needs_fold should be in chronological order."""
        _make_personas(dirs, [
            "(PERSONA-001)-A", "(PERSONA-002)-B",
        ])
        _make_bundles(dirs, [
            "2026-03-10-city-council",
            "2026-03-02-school-board",
        ])
        _make_interpretations(dirs, "2026-03-02-school-board", [1, 2])
        _make_interpretations(dirs, "2026-03-10-city-council", [1, 2])
        gaps = pi.detect_gaps(2)
        assert gaps["needs_fold"] == [
            "2026-03-02-school-board",
            "2026-03-10-city-council",
        ]
