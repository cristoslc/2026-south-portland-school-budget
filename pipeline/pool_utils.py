"""Shared utilities for evidence pool normalizers.

Provides manifest read/write, SHA-256 hashing, source-id assignment,
and duplicate detection used by all three normalizers (VTT, PDF, HTML).
"""

import hashlib
import os
from datetime import datetime, timezone

import yaml


def sha256_file(filepath):
    """Compute SHA-256 hash of a file, returned as 'sha256:<hex>'."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def sha256_bytes(data):
    """Compute SHA-256 hash of bytes, returned as 'sha256:<hex>'."""
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def read_manifest(pool_dir):
    """Read and return the manifest dict from a pool directory.

    Returns empty dict with 'sources: []' if manifest doesn't exist.
    """
    manifest_path = os.path.join(pool_dir, "manifest.yaml")
    if not os.path.exists(manifest_path):
        return {"sources": []}
    with open(manifest_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"sources": []}


def write_manifest(pool_dir, manifest):
    """Write manifest dict back to manifest.yaml.

    Updates the 'refreshed' field to today's date.
    """
    manifest["refreshed"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    manifest_path = os.path.join(pool_dir, "manifest.yaml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False,
                  allow_unicode=True)


def next_source_id(manifest):
    """Return the next sequential source-id as a zero-padded 3-digit string.

    Handles both 'source-id' and 'id' key conventions found in existing manifests.
    """
    sources = manifest.get("sources", [])
    if not sources:
        return "001"
    max_id = 0
    for s in sources:
        sid = s.get("source-id") or s.get("id") or "0"
        try:
            max_id = max(max_id, int(sid))
        except ValueError:
            continue
    return f"{max_id + 1:03d}"


def find_duplicate(manifest, file_hash):
    """Check if a source with this hash already exists in the manifest.

    Returns the source dict if found, None otherwise.
    """
    for s in manifest.get("sources", []):
        if s.get("hash") == file_hash:
            return s
    return None


def add_source_to_manifest(manifest, source_entry):
    """Append a source entry to the manifest's sources list."""
    if "sources" not in manifest:
        manifest["sources"] = []
    manifest["sources"].append(source_entry)


def write_source_markdown(pool_dir, filename, frontmatter_dict, body):
    """Write an evidence pool source markdown file.

    Args:
        pool_dir: Path to the evidence pool directory.
        filename: Output filename (e.g., '005-meeting-2026-01-12.md').
        frontmatter_dict: Dict of YAML frontmatter fields.
        body: Markdown body content (without leading newline).
    """
    sources_dir = os.path.join(pool_dir, "sources")
    os.makedirs(sources_dir, exist_ok=True)
    out_path = os.path.join(sources_dir, filename)

    lines = ["---"]
    for key, value in frontmatter_dict.items():
        if isinstance(value, list):
            if value:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: []")
        elif value is None:
            continue
        else:
            lines.append(f'{key}: "{value}"')
    lines.append("---")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write("\n\n")
        f.write(body)
        if not body.endswith("\n"):
            f.write("\n")

    return out_path


def fetched_now():
    """Return an ISO 8601 timestamp for the current time."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
