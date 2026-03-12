"""Schema validation module — SPEC-016, AC5.

Validates bundle and inter-meeting manifests using the dataclass layer.
Provides both programmatic API and CLI entry point.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from pipeline.bundle_layout import discover_bundles
from pipeline.bundle_schema import MeetingBundle
from pipeline.inter_meeting_schema import InterMeetingManifest


@dataclass
class ValidationResult:
    """Result of validating a single manifest file."""

    path: Path
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_manifest(
    manifest_path: Path,
    inter_meeting: bool = False,
) -> ValidationResult:
    """Validate a single manifest file.

    Raises FileNotFoundError if the file does not exist.
    """
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        raise FileNotFoundError(f"File not found: {manifest_path}")

    errors = []

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return ValidationResult(path=manifest_path, errors=[f"YAML parse error: {e}"])

    if data is None:
        return ValidationResult(
            path=manifest_path,
            errors=["empty or null YAML document"],
        )

    if not isinstance(data, dict):
        return ValidationResult(
            path=manifest_path,
            errors=["expected a YAML mapping at top level"],
        )

    try:
        if inter_meeting:
            InterMeetingManifest.from_dict(data)
        else:
            MeetingBundle.from_dict(data)
    except ValueError as e:
        errors = str(e).split("; ")

    return ValidationResult(path=manifest_path, errors=errors)


def validate_all_bundles(bundles_root: Path) -> list[ValidationResult]:
    """Validate all bundle manifests under a bundles root directory."""
    bundle_dirs = discover_bundles(bundles_root)
    results = []
    for bundle_dir in bundle_dirs:
        manifest = bundle_dir / "manifest.yaml"
        results.append(validate_manifest(manifest))
    return results
