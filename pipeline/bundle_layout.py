"""Bundle directory layout and path helpers — SPEC-016, AC1 & AC3.

Provides utilities for naming bundle directories, loading bundles from
disk, discovering all bundles, and resolving source paths.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from pipeline.bundle_schema import MeetingBundle

BUNDLES_REL = Path("data") / "interpretation" / "bundles"


def bundle_dir_name(meeting_date: datetime.date, body: str) -> str:
    """Return the directory name for a bundle: YYYY-MM-DD-body."""
    return f"{meeting_date.isoformat()}-{body}"


def bundle_dir_path(
    meeting_date: datetime.date,
    body: str,
    project_root: Path,
) -> Path:
    """Return the full path to a bundle directory."""
    return project_root / BUNDLES_REL / bundle_dir_name(meeting_date, body)


def load_bundle(bundle_dir: Path) -> MeetingBundle:
    """Load a MeetingBundle from a bundle directory's manifest.yaml.

    Raises FileNotFoundError if manifest.yaml does not exist.
    """
    from pipeline.bundle_schema import MeetingBundle

    manifest_path = bundle_dir / "manifest.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"No manifest.yaml in {bundle_dir}"
        )
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return MeetingBundle.from_dict(data)


def discover_bundles(bundles_root: Path) -> list[Path]:
    """Find all bundle directories (containing manifest.yaml) under bundles_root.

    Returns sorted list of directory paths.
    """
    if not bundles_root.exists():
        return []
    dirs = [
        d for d in sorted(bundles_root.iterdir())
        if d.is_dir() and (d / "manifest.yaml").exists()
    ]
    return dirs


def resolve_source_paths(
    bundle: MeetingBundle,
    project_root: Path,
) -> list[str]:
    """Check that all source paths in a bundle resolve to existing files.

    Returns a list of error strings (empty if all paths are valid).
    AC3: all referenced source paths resolve to valid normalized markdown files.
    """
    errors = []

    for i, src in enumerate(bundle.sources):
        full_path = project_root / src.path
        if not full_path.exists():
            errors.append(
                f"sources[{i}].path: file not found — {src.path}"
            )
        if src.normalized_path:
            full_np = project_root / src.normalized_path
            if not full_np.exists():
                errors.append(
                    f"sources[{i}].normalized_path: file not found — {src.normalized_path}"
                )

    if bundle.agenda_ref:
        full_agenda = project_root / bundle.agenda_ref
        if not full_agenda.exists():
            errors.append(
                f"agenda_ref: file not found — {bundle.agenda_ref}"
            )

    return errors
