"""Tests for schema validation script — SPEC-016, AC5.

RED phase: tests for validate_manifest() which uses the dataclass layer
to validate bundle and inter-meeting manifests programmatically.

Derives from:
  AC5 — schema validated by Python script; enforces required fields and
        rejects malformed manifests
"""

from pathlib import Path

import pytest
import yaml

from pipeline.validate_schema import (
    validate_manifest,
    validate_all_bundles,
    ValidationResult,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_manifest(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, default_flow_style=False))


def _valid_bundle():
    return {
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


def _valid_inter_meeting():
    return {
        "schema_version": "1.0",
        "entries": [{
            "entry_id": "im-001",
            "date_posted": "2026-03-04",
            "source_type": "news-article",
            "source_path": "data/news/article.md",
            "description": "News article",
            "date_range": {
                "posted_after": "2026-03-02",
                "posted_before": "2026-03-05",
            },
        }],
    }


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------

class TestValidationResult:
    """ValidationResult holds path, validity, and error list."""

    def test_valid_result(self):
        r = ValidationResult(path=Path("manifest.yaml"), errors=[])
        assert r.is_valid
        assert r.errors == []

    def test_invalid_result(self):
        r = ValidationResult(
            path=Path("manifest.yaml"),
            errors=["missing field: body"],
        )
        assert not r.is_valid
        assert len(r.errors) == 1


# ---------------------------------------------------------------------------
# validate_manifest — bundle
# ---------------------------------------------------------------------------

class TestValidateBundle:
    """AC5: validates bundle manifests."""

    def test_valid_bundle(self, tmp_path):
        manifest = tmp_path / "manifest.yaml"
        _write_manifest(manifest, _valid_bundle())
        result = validate_manifest(manifest)
        assert result.is_valid

    def test_missing_required_field(self, tmp_path):
        data = _valid_bundle()
        del data["body"]
        manifest = tmp_path / "manifest.yaml"
        _write_manifest(manifest, data)
        result = validate_manifest(manifest)
        assert not result.is_valid
        assert any("body" in e for e in result.errors)

    def test_invalid_enum(self, tmp_path):
        data = _valid_bundle()
        data["meeting_type"] = "informal"
        manifest = tmp_path / "manifest.yaml"
        _write_manifest(manifest, data)
        result = validate_manifest(manifest)
        assert not result.is_valid
        assert any("meeting_type" in e for e in result.errors)

    def test_invalid_yaml(self, tmp_path):
        manifest = tmp_path / "manifest.yaml"
        manifest.write_text(": invalid: yaml: [")
        result = validate_manifest(manifest)
        assert not result.is_valid

    def test_empty_file(self, tmp_path):
        manifest = tmp_path / "manifest.yaml"
        manifest.write_text("")
        result = validate_manifest(manifest)
        assert not result.is_valid

    def test_nonexistent_file(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            validate_manifest(tmp_path / "nonexistent.yaml")


# ---------------------------------------------------------------------------
# validate_manifest — inter-meeting
# ---------------------------------------------------------------------------

class TestValidateInterMeeting:
    """AC5: validates inter-meeting manifests."""

    def test_valid_inter_meeting(self, tmp_path):
        manifest = tmp_path / "manifest.yaml"
        _write_manifest(manifest, _valid_inter_meeting())
        result = validate_manifest(manifest, inter_meeting=True)
        assert result.is_valid

    def test_invalid_date_range(self, tmp_path):
        data = _valid_inter_meeting()
        data["entries"][0]["date_range"]["posted_after"] = "2026-03-10"
        manifest = tmp_path / "manifest.yaml"
        _write_manifest(manifest, data)
        result = validate_manifest(manifest, inter_meeting=True)
        assert not result.is_valid
        assert any("posted_after" in e for e in result.errors)


# ---------------------------------------------------------------------------
# validate_all_bundles
# ---------------------------------------------------------------------------

class TestValidateAllBundles:
    """AC5: validates full bundle set."""

    def test_all_valid(self, tmp_path):
        bundles_root = tmp_path / "data" / "interpretation" / "bundles"
        for name in ["2026-03-02-school-board", "2026-03-05-city-council"]:
            d = bundles_root / name
            d.mkdir(parents=True)
            data = _valid_bundle()
            data["body"] = name.split("-", 3)[3]
            _write_manifest(d / "manifest.yaml", data)

        results = validate_all_bundles(bundles_root)
        assert all(r.is_valid for r in results)
        assert len(results) == 2

    def test_mixed_validity(self, tmp_path):
        bundles_root = tmp_path / "data" / "interpretation" / "bundles"

        # Valid bundle
        d1 = bundles_root / "2026-03-02-school-board"
        d1.mkdir(parents=True)
        _write_manifest(d1 / "manifest.yaml", _valid_bundle())

        # Invalid bundle (missing body)
        d2 = bundles_root / "2026-03-05-city-council"
        d2.mkdir(parents=True)
        bad = _valid_bundle()
        del bad["body"]
        _write_manifest(d2 / "manifest.yaml", bad)

        results = validate_all_bundles(bundles_root)
        valid_count = sum(1 for r in results if r.is_valid)
        invalid_count = sum(1 for r in results if not r.is_valid)
        assert valid_count == 1
        assert invalid_count == 1

    def test_empty_bundles_dir(self, tmp_path):
        bundles_root = tmp_path / "bundles"
        bundles_root.mkdir()
        results = validate_all_bundles(bundles_root)
        assert results == []
