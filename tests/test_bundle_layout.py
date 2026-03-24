"""Tests for bundle directory layout and path helpers — SPEC-016, AC1 & AC3.

RED phase: tests for bundle_dir_name(), load_bundle(), resolve_source_paths(),
and discover_bundles() before implementation exists.

Derives from:
  AC1 — bundles stored at data/interpretation/bundles/<YYYY-MM-DD>-<body>/
  AC3 — all referenced source paths resolve to valid normalized markdown files
"""

import datetime
from pathlib import Path

import pytest
import yaml

from pipeline.bundle_layout import (
    bundle_dir_name,
    bundle_dir_path,
    load_bundle,
    discover_bundles,
    resolve_source_paths,
)


# ---------------------------------------------------------------------------
# bundle_dir_name
# ---------------------------------------------------------------------------

class TestBundleDirName:
    """AC1: naming convention is YYYY-MM-DD-body."""

    def test_school_board(self):
        assert bundle_dir_name(
            datetime.date(2026, 3, 2), "school-board"
        ) == "2026-03-02-school-board"

    def test_city_council(self):
        assert bundle_dir_name(
            datetime.date(2025, 12, 1), "city-council"
        ) == "2025-12-01-city-council"

    def test_from_meeting_bundle(self):
        """Should also accept a MeetingBundle object."""
        from pipeline.bundle_schema import MeetingBundle

        bundle = MeetingBundle.from_dict({
            "schema_version": "1.0",
            "meeting_date": "2026-03-02",
            "meeting_type": "regular",
            "body": "school-board",
            "sources": [{
                "source_id": "src-001",
                "source_type": "transcript",
                "title": "Transcript",
                "path": "data/raw/transcript.vtt",
            }],
        })
        assert bundle_dir_name(bundle.meeting_date, bundle.body) == "2026-03-02-school-board"


# ---------------------------------------------------------------------------
# bundle_dir_path
# ---------------------------------------------------------------------------

class TestBundleDirPath:
    """AC1: full path is <project_root>/data/interpretation/bundles/<dir_name>/."""

    def test_returns_path(self):
        root = Path("/project")
        result = bundle_dir_path(datetime.date(2026, 3, 2), "school-board", root)
        assert result == root / "data" / "interpretation" / "bundles" / "2026-03-02-school-board"

    def test_is_path_object(self):
        root = Path("/project")
        result = bundle_dir_path(datetime.date(2026, 3, 2), "school-board", root)
        assert isinstance(result, Path)


# ---------------------------------------------------------------------------
# load_bundle (from directory)
# ---------------------------------------------------------------------------

class TestLoadBundle:
    """Load a MeetingBundle from a bundle directory."""

    def test_load_from_directory(self, tmp_path):
        """Load a manifest.yaml from a bundle directory."""
        bundle_dir = tmp_path / "2026-03-02-school-board"
        bundle_dir.mkdir()
        manifest = {
            "schema_version": "1.0",
            "meeting_date": "2026-03-02",
            "meeting_type": "regular",
            "body": "school-board",
            "sources": [{
                "source_id": "src-001",
                "source_type": "transcript",
                "title": "Transcript",
                "path": "data/raw/transcript.vtt",
            }],
        }
        (bundle_dir / "manifest.yaml").write_text(
            yaml.dump(manifest, default_flow_style=False)
        )
        bundle = load_bundle(bundle_dir)
        assert bundle.meeting_type == "regular"
        assert bundle.body == "school-board"

    def test_missing_manifest_raises(self, tmp_path):
        """A directory without manifest.yaml should raise FileNotFoundError."""
        bundle_dir = tmp_path / "2026-03-02-school-board"
        bundle_dir.mkdir()
        with pytest.raises(FileNotFoundError):
            load_bundle(bundle_dir)


# ---------------------------------------------------------------------------
# discover_bundles
# ---------------------------------------------------------------------------

class TestDiscoverBundles:
    """Find all bundle directories under a bundles root."""

    def test_finds_bundles(self, tmp_path):
        """Should return paths to directories containing manifest.yaml."""
        bundles_root = tmp_path / "data" / "interpretation" / "bundles"
        bundles_root.mkdir(parents=True)

        for name in ["2026-03-02-school-board", "2026-03-05-city-council"]:
            d = bundles_root / name
            d.mkdir()
            (d / "manifest.yaml").write_text("schema_version: '1.0'\n")

        # Directory without manifest should be excluded
        (bundles_root / "incomplete").mkdir()

        result = discover_bundles(bundles_root)
        assert len(result) == 2
        names = [p.name for p in result]
        assert "2026-03-02-school-board" in names
        assert "2026-03-05-city-council" in names

    def test_empty_dir_returns_empty(self, tmp_path):
        bundles_root = tmp_path / "data" / "interpretation" / "bundles"
        bundles_root.mkdir(parents=True)
        assert discover_bundles(bundles_root) == []

    def test_nonexistent_dir_returns_empty(self, tmp_path):
        assert discover_bundles(tmp_path / "nonexistent") == []

    def test_sorted_by_name(self, tmp_path):
        """Results should be sorted by directory name (chronological)."""
        bundles_root = tmp_path / "bundles"
        bundles_root.mkdir()

        for name in ["2026-03-05-city-council", "2025-12-01-city-council",
                      "2026-01-12-school-board"]:
            d = bundles_root / name
            d.mkdir()
            (d / "manifest.yaml").write_text("schema_version: '1.0'\n")

        result = discover_bundles(bundles_root)
        names = [p.name for p in result]
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# AC3: resolve_source_paths
# ---------------------------------------------------------------------------

class TestResolveSourcePaths:
    """AC3: all referenced source paths resolve to valid files."""

    def test_all_paths_valid(self, tmp_path):
        """When all source paths exist, returns no errors."""
        # Create a fake source file
        src_file = tmp_path / "data" / "raw" / "transcript.vtt"
        src_file.parent.mkdir(parents=True)
        src_file.write_text("WEBVTT\n")

        from pipeline.bundle_schema import MeetingBundle
        bundle = MeetingBundle.from_dict({
            "schema_version": "1.0",
            "meeting_date": "2026-03-02",
            "meeting_type": "regular",
            "body": "school-board",
            "sources": [{
                "source_id": "src-001",
                "source_type": "transcript",
                "title": "Transcript",
                "path": "data/raw/transcript.vtt",
            }],
        })
        errors = resolve_source_paths(bundle, project_root=tmp_path)
        assert errors == []

    def test_missing_path_reported(self, tmp_path):
        """When a source path doesn't exist, it's reported as an error."""
        from pipeline.bundle_schema import MeetingBundle
        bundle = MeetingBundle.from_dict({
            "schema_version": "1.0",
            "meeting_date": "2026-03-02",
            "meeting_type": "regular",
            "body": "school-board",
            "sources": [{
                "source_id": "src-001",
                "source_type": "transcript",
                "title": "Transcript",
                "path": "data/raw/nonexistent.vtt",
            }],
        })
        errors = resolve_source_paths(bundle, project_root=tmp_path)
        assert len(errors) == 1
        assert "nonexistent.vtt" in errors[0]

    def test_normalized_path_checked(self, tmp_path):
        """When normalized_path is set but missing, it's reported."""
        # Create raw file but not normalized
        src_file = tmp_path / "data" / "raw" / "transcript.vtt"
        src_file.parent.mkdir(parents=True)
        src_file.write_text("WEBVTT\n")

        from pipeline.bundle_schema import MeetingBundle
        bundle = MeetingBundle.from_dict({
            "schema_version": "1.0",
            "meeting_date": "2026-03-02",
            "meeting_type": "regular",
            "body": "school-board",
            "sources": [{
                "source_id": "src-001",
                "source_type": "transcript",
                "title": "Transcript",
                "path": "data/raw/transcript.vtt",
                "normalized_path": "docs/troves/transcript.md",
            }],
        })
        errors = resolve_source_paths(bundle, project_root=tmp_path)
        assert len(errors) == 1
        assert "normalized_path" in errors[0]

    def test_agenda_ref_checked(self, tmp_path):
        """When agenda_ref is set but missing, it's reported."""
        src_file = tmp_path / "data" / "raw" / "transcript.vtt"
        src_file.parent.mkdir(parents=True)
        src_file.write_text("WEBVTT\n")

        from pipeline.bundle_schema import MeetingBundle
        bundle = MeetingBundle.from_dict({
            "schema_version": "1.0",
            "meeting_date": "2026-03-02",
            "meeting_type": "regular",
            "body": "school-board",
            "agenda_ref": "data/raw/agenda.pdf",
            "sources": [{
                "source_id": "src-001",
                "source_type": "transcript",
                "title": "Transcript",
                "path": "data/raw/transcript.vtt",
            }],
        })
        errors = resolve_source_paths(bundle, project_root=tmp_path)
        assert len(errors) == 1
        assert "agenda_ref" in errors[0]
