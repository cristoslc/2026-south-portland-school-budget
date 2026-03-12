"""Tests for source completeness invariant — SPEC-016, AC2.

RED phase: tests for check_source_completeness() which verifies that
every source in the evidence pool appears in exactly one bundle or
in the inter-meeting evidence set.

Derives from:
  AC2 — given the full set of meeting bundles, when all manifests are
        collected, then every source in the evidence pool appears in
        exactly one bundle or in the inter-meeting evidence set
"""

from pathlib import Path

import pytest
import yaml

from pipeline.source_completeness import (
    check_source_completeness,
    CompletenessReport,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, default_flow_style=False))


def _setup_pool(tmp_path, sources):
    """Create an evidence pool manifest with given sources."""
    pool_dir = tmp_path / "docs" / "evidence-pools" / "test-pool"
    pool_dir.mkdir(parents=True)
    _write_yaml(pool_dir / "manifest.yaml", {
        "pool": "test-pool",
        "sources": sources,
    })
    return pool_dir


def _setup_bundle(tmp_path, name, sources):
    """Create a bundle with given sources."""
    bundle_dir = tmp_path / "data" / "interpretation" / "bundles" / name
    _write_yaml(bundle_dir / "manifest.yaml", {
        "schema_version": "1.0",
        "meeting_date": name[:10],
        "meeting_type": "regular",
        "body": name[11:],
        "sources": sources,
    })
    return bundle_dir


def _setup_inter_meeting(tmp_path, entries):
    """Create an inter-meeting manifest."""
    im_dir = tmp_path / "data" / "interpretation" / "inter-meeting"
    _write_yaml(im_dir / "manifest.yaml", {
        "schema_version": "1.0",
        "entries": entries,
    })


# ---------------------------------------------------------------------------
# CompletenessReport
# ---------------------------------------------------------------------------

class TestCompletenessReport:

    def test_complete_report(self):
        r = CompletenessReport(
            total_pool_sources=5,
            affiliated_sources=5,
            missing_sources=[],
            duplicate_sources=[],
        )
        assert r.is_complete
        assert r.missing_sources == []
        assert r.duplicate_sources == []

    def test_missing_sources(self):
        r = CompletenessReport(
            total_pool_sources=5,
            affiliated_sources=4,
            missing_sources=["data/raw/missing.vtt"],
            duplicate_sources=[],
        )
        assert not r.is_complete

    def test_duplicate_sources(self):
        r = CompletenessReport(
            total_pool_sources=5,
            affiliated_sources=6,
            missing_sources=[],
            duplicate_sources=["data/raw/dup.vtt"],
        )
        assert not r.is_complete


# ---------------------------------------------------------------------------
# check_source_completeness
# ---------------------------------------------------------------------------

class TestCheckSourceCompleteness:
    """AC2: every pool source is in exactly one bundle or inter-meeting."""

    def test_all_sources_affiliated(self, tmp_path):
        """When every pool source is in exactly one bundle, report is complete."""
        pool_sources = [
            {"id": "001", "path": "data/raw/a.vtt"},
            {"id": "002", "path": "data/raw/b.pdf"},
        ]
        _setup_pool(tmp_path, pool_sources)

        _setup_bundle(tmp_path, "2026-03-02-school-board", [
            {"source_id": "001", "source_type": "transcript",
             "title": "A", "path": "data/raw/a.vtt"},
            {"source_id": "002", "source_type": "document",
             "title": "B", "path": "data/raw/b.pdf"},
        ])

        report = check_source_completeness(tmp_path)
        assert report.is_complete
        assert report.total_pool_sources == 2
        assert report.affiliated_sources == 2

    def test_missing_source_detected(self, tmp_path):
        """A pool source not in any bundle or inter-meeting is reported missing."""
        pool_sources = [
            {"id": "001", "path": "data/raw/a.vtt"},
            {"id": "002", "path": "data/raw/b.pdf"},
        ]
        _setup_pool(tmp_path, pool_sources)

        _setup_bundle(tmp_path, "2026-03-02-school-board", [
            {"source_id": "001", "source_type": "transcript",
             "title": "A", "path": "data/raw/a.vtt"},
        ])

        report = check_source_completeness(tmp_path)
        assert not report.is_complete
        assert "data/raw/b.pdf" in report.missing_sources

    def test_inter_meeting_sources_count(self, tmp_path):
        """Sources in inter-meeting manifest satisfy the completeness check."""
        pool_sources = [
            {"id": "001", "path": "data/raw/a.vtt"},
            {"id": "002", "path": "data/news/article.md"},
        ]
        _setup_pool(tmp_path, pool_sources)

        _setup_bundle(tmp_path, "2026-03-02-school-board", [
            {"source_id": "001", "source_type": "transcript",
             "title": "A", "path": "data/raw/a.vtt"},
        ])

        _setup_inter_meeting(tmp_path, [{
            "entry_id": "im-001",
            "date_posted": "2026-03-04",
            "source_type": "news-article",
            "source_path": "data/news/article.md",
            "description": "Article",
            "date_range": {
                "posted_after": "2026-03-02",
                "posted_before": "2026-03-05",
            },
        }])

        report = check_source_completeness(tmp_path)
        assert report.is_complete

    def test_duplicate_source_detected(self, tmp_path):
        """A pool source in multiple bundles is reported as duplicate."""
        pool_sources = [
            {"id": "001", "path": "data/raw/a.vtt"},
        ]
        _setup_pool(tmp_path, pool_sources)

        _setup_bundle(tmp_path, "2026-03-02-school-board", [
            {"source_id": "001", "source_type": "transcript",
             "title": "A", "path": "data/raw/a.vtt"},
        ])
        _setup_bundle(tmp_path, "2026-03-05-city-council", [
            {"source_id": "001", "source_type": "transcript",
             "title": "A copy", "path": "data/raw/a.vtt"},
        ])

        report = check_source_completeness(tmp_path)
        assert not report.is_complete
        assert "data/raw/a.vtt" in report.duplicate_sources

    def test_multiple_pools(self, tmp_path):
        """Sources from multiple evidence pools are all checked."""
        # Pool 1
        pool1 = tmp_path / "docs" / "evidence-pools" / "pool-1"
        pool1.mkdir(parents=True)
        _write_yaml(pool1 / "manifest.yaml", {
            "pool": "pool-1",
            "sources": [{"id": "001", "path": "data/raw/a.vtt"}],
        })

        # Pool 2
        pool2 = tmp_path / "docs" / "evidence-pools" / "pool-2"
        pool2.mkdir(parents=True)
        _write_yaml(pool2 / "manifest.yaml", {
            "pool": "pool-2",
            "sources": [{"id": "002", "path": "data/raw/b.pdf"}],
        })

        _setup_bundle(tmp_path, "2026-03-02-school-board", [
            {"source_id": "001", "source_type": "transcript",
             "title": "A", "path": "data/raw/a.vtt"},
            {"source_id": "002", "source_type": "document",
             "title": "B", "path": "data/raw/b.pdf"},
        ])

        report = check_source_completeness(tmp_path)
        assert report.is_complete
        assert report.total_pool_sources == 2

    def test_no_pools_empty_report(self, tmp_path):
        """With no evidence pools, the report has 0 sources and is trivially complete."""
        report = check_source_completeness(tmp_path)
        assert report.is_complete
        assert report.total_pool_sources == 0
