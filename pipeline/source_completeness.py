"""Source completeness checker — SPEC-016, AC2.

Verifies that every source in the evidence pool appears in exactly one
bundle or in the inter-meeting evidence set.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class CompletenessReport:
    """Result of the source completeness check."""

    total_pool_sources: int
    affiliated_sources: int
    missing_sources: list[str] = field(default_factory=list)
    duplicate_sources: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return len(self.missing_sources) == 0 and len(self.duplicate_sources) == 0


def _collect_pool_source_paths(project_root: Path) -> set[str]:
    """Collect all source paths from evidence pool manifests."""
    pools_dir = project_root / "docs" / "evidence-pools"
    if not pools_dir.exists():
        return set()

    paths = set()
    for pool_dir in sorted(pools_dir.iterdir()):
        manifest = pool_dir / "manifest.yaml"
        if not manifest.exists():
            continue
        with open(manifest, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data or "sources" not in data:
            continue
        for src in data["sources"]:
            if "path" in src:
                paths.add(src["path"])
    return paths


def _collect_bundle_source_paths(project_root: Path) -> list[str]:
    """Collect all source paths from bundle manifests (may contain duplicates)."""
    bundles_dir = project_root / "data" / "interpretation" / "bundles"
    if not bundles_dir.exists():
        return []

    paths = []
    for bundle_dir in sorted(bundles_dir.iterdir()):
        manifest = bundle_dir / "manifest.yaml"
        if not manifest.exists():
            continue
        with open(manifest, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data or "sources" not in data:
            continue
        for src in data["sources"]:
            if "path" in src:
                paths.append(src["path"])
    return paths


def _collect_inter_meeting_source_paths(project_root: Path) -> list[str]:
    """Collect all source paths from the inter-meeting manifest."""
    manifest = (
        project_root / "data" / "interpretation" / "inter-meeting" / "manifest.yaml"
    )
    if not manifest.exists():
        return []
    with open(manifest, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or "entries" not in data:
        return []
    return [
        entry["source_path"]
        for entry in data["entries"]
        if "source_path" in entry
    ]


def check_source_completeness(project_root: Path) -> CompletenessReport:
    """Check that every evidence pool source is in exactly one bundle
    or inter-meeting entry.
    """
    pool_paths = _collect_pool_source_paths(project_root)

    bundle_paths = _collect_bundle_source_paths(project_root)
    im_paths = _collect_inter_meeting_source_paths(project_root)

    all_affiliated = bundle_paths + im_paths
    affiliated_counts = Counter(all_affiliated)
    affiliated_set = set(all_affiliated)

    missing = sorted(pool_paths - affiliated_set)
    duplicates = sorted(p for p, c in affiliated_counts.items() if c > 1 and p in pool_paths)

    return CompletenessReport(
        total_pool_sources=len(pool_paths),
        affiliated_sources=len(affiliated_set & pool_paths),
        missing_sources=missing,
        duplicate_sources=duplicates,
    )
