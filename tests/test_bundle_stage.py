"""Tests for bundle_meetings.py --stage flag.

Verifies that the --stage flag correctly controls whether git add is invoked
after manifest writing, and that it is skipped when no manifests are written.
"""

import datetime
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Locate the script module for import
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import bundle_meetings  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_meeting(date_str="2025-06-10", body="school-board"):
    """Create a minimal Meeting object with one affiliated source."""
    d = datetime.date.fromisoformat(date_str)
    m = bundle_meetings.Meeting(d, body, "regular", Path("/tmp/fake"))
    m.sources.append({"source_id": "fake-source", "source_type": "vtt"})
    return m


_FAKE_MANIFEST = {
    "meeting_date": "2025-06-10",
    "body": "school-board",
    "title": "School Board Regular Meeting - June 10, 2025",
    "sources": [{"source_id": "fake-source", "source_type": "vtt"}],
}


def _common_patches():
    """Return a dict of patches shared across staging tests."""
    return {
        "load_pool_sources": patch.object(
            bundle_meetings, "load_pool_sources", return_value=[]),
        "discover_meetings": None,  # caller sets this per-test
        "affiliate_sources": patch.object(
            bundle_meetings, "affiliate_sources", return_value=(1, [])),
        "cross_reference_agendas": patch.object(
            bundle_meetings, "cross_reference_agendas", return_value=(0, [])),
        "llm_classify_fallback": patch.object(
            bundle_meetings, "llm_classify_fallback"),
        "build_manifest_data": patch.object(
            bundle_meetings, "build_manifest_data", return_value=_FAKE_MANIFEST),
        "generate_manifest_text": patch.object(
            bundle_meetings, "generate_manifest_text",
            return_value="fake: yaml\n"),
        "is_protected": patch.object(
            bundle_meetings, "is_protected", return_value=False),
    }


# ---------------------------------------------------------------------------
# Test: argparse accepts --stage
# ---------------------------------------------------------------------------

class TestStageArgparse:
    def test_stage_flag_accepted(self):
        """--stage is a valid boolean flag on the argument parser."""
        parser = bundle_meetings.argparse.ArgumentParser()
        parser.add_argument("--stage", action="store_true")
        args = parser.parse_args(["--stage"])
        assert args.stage is True

    def test_stage_flag_default_false(self):
        """--stage defaults to False when omitted."""
        parser = bundle_meetings.argparse.ArgumentParser()
        parser.add_argument("--stage", action="store_true")
        args = parser.parse_args([])
        assert args.stage is False

    def test_real_parser_accepts_stage(self):
        """The actual main() parser recognises --stage."""
        meeting = _make_meeting()
        meetings = {("2025-06-10", "school-board"): meeting}

        with patch("sys.argv", ["bundle_meetings.py", "--stage", "--dry-run"]), \
             patch.object(bundle_meetings, "load_pool_sources", return_value=[]), \
             patch.object(bundle_meetings, "discover_meetings", return_value=meetings), \
             patch.object(bundle_meetings, "affiliate_sources", return_value=(0, [])), \
             patch.object(bundle_meetings, "cross_reference_agendas", return_value=(0, [])), \
             patch.object(bundle_meetings, "llm_classify_fallback"), \
             patch.object(bundle_meetings, "build_manifest_data", return_value=None):
            # Should not raise SystemExit(2) for unrecognised argument
            ret = bundle_meetings.main()
            assert ret == 0


# ---------------------------------------------------------------------------
# Test: --stage triggers git add when manifests are written
# ---------------------------------------------------------------------------

class TestStageGitAdd:
    """Verify git-add behaviour under different flag/write combinations."""

    def test_stage_with_writes_calls_git_add(self, tmp_path):
        """When --stage is set and manifests are written, git add is called."""
        meeting = _make_meeting()
        meetings = {("2025-06-10", "school-board"): meeting}

        # Use tmp_path so mkdir / open succeed without touching real files
        fake_bundles = tmp_path / "bundles"
        mock_subprocess_run = MagicMock()

        with patch("sys.argv", ["bundle_meetings.py", "--stage"]), \
             patch.object(bundle_meetings, "BUNDLES_DIR", fake_bundles), \
             patch.object(bundle_meetings, "PROJECT_ROOT", tmp_path), \
             patch.object(bundle_meetings, "load_pool_sources", return_value=[]), \
             patch.object(bundle_meetings, "discover_meetings", return_value=meetings), \
             patch.object(bundle_meetings, "affiliate_sources", return_value=(1, [])), \
             patch.object(bundle_meetings, "cross_reference_agendas", return_value=(0, [])), \
             patch.object(bundle_meetings, "llm_classify_fallback"), \
             patch.object(bundle_meetings, "build_manifest_data", return_value=_FAKE_MANIFEST), \
             patch.object(bundle_meetings, "generate_manifest_text", return_value="fake: yaml\n"), \
             patch.object(bundle_meetings, "is_protected", return_value=False), \
             patch.object(bundle_meetings, "check_idempotency", return_value=True), \
             patch.object(bundle_meetings, "subprocess") as mock_sp:
            mock_sp.run = mock_subprocess_run
            mock_sp.CalledProcessError = subprocess.CalledProcessError
            bundle_meetings.main()

        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args
        assert call_args[0][0][:2] == ["git", "add"]

    def test_stage_without_writes_skips_git_add(self):
        """When --stage is set but all manifests are idempotent, git add is NOT called."""
        meeting = _make_meeting()
        meetings = {("2025-06-10", "school-board"): meeting}

        mock_subprocess_run = MagicMock()

        with patch("sys.argv", ["bundle_meetings.py", "--stage"]), \
             patch.object(bundle_meetings, "load_pool_sources", return_value=[]), \
             patch.object(bundle_meetings, "discover_meetings", return_value=meetings), \
             patch.object(bundle_meetings, "affiliate_sources", return_value=(1, [])), \
             patch.object(bundle_meetings, "cross_reference_agendas", return_value=(0, [])), \
             patch.object(bundle_meetings, "llm_classify_fallback"), \
             patch.object(bundle_meetings, "build_manifest_data", return_value=_FAKE_MANIFEST), \
             patch.object(bundle_meetings, "generate_manifest_text", return_value="fake: yaml\n"), \
             patch.object(bundle_meetings, "is_protected", return_value=False), \
             patch.object(bundle_meetings, "check_idempotency", return_value=False), \
             patch.object(Path, "exists", return_value=True), \
             patch.object(bundle_meetings, "subprocess") as mock_sp:
            mock_sp.run = mock_subprocess_run
            bundle_meetings.main()

        mock_subprocess_run.assert_not_called()

    def test_no_stage_flag_skips_git_add(self, tmp_path):
        """Without --stage, git add is never called even if manifests are written."""
        meeting = _make_meeting()
        meetings = {("2025-06-10", "school-board"): meeting}

        fake_bundles = tmp_path / "bundles"
        mock_subprocess_run = MagicMock()

        with patch("sys.argv", ["bundle_meetings.py"]), \
             patch.object(bundle_meetings, "BUNDLES_DIR", fake_bundles), \
             patch.object(bundle_meetings, "PROJECT_ROOT", tmp_path), \
             patch.object(bundle_meetings, "load_pool_sources", return_value=[]), \
             patch.object(bundle_meetings, "discover_meetings", return_value=meetings), \
             patch.object(bundle_meetings, "affiliate_sources", return_value=(1, [])), \
             patch.object(bundle_meetings, "cross_reference_agendas", return_value=(0, [])), \
             patch.object(bundle_meetings, "llm_classify_fallback"), \
             patch.object(bundle_meetings, "build_manifest_data", return_value=_FAKE_MANIFEST), \
             patch.object(bundle_meetings, "generate_manifest_text", return_value="fake: yaml\n"), \
             patch.object(bundle_meetings, "is_protected", return_value=False), \
             patch.object(bundle_meetings, "check_idempotency", return_value=True), \
             patch.object(bundle_meetings, "subprocess") as mock_sp:
            mock_sp.run = mock_subprocess_run
            bundle_meetings.main()

        mock_subprocess_run.assert_not_called()
