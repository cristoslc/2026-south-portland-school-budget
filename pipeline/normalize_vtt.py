#!/usr/bin/env python3
"""Convert a VTT transcript file into evidence pool source markdown.

Uses parse_vtt.py for VTT parsing, then wraps the output in evidence pool
source format (YAML frontmatter + structured body).

Usage:
    python3 -m pipeline.normalize_vtt <vtt_file> <pool_dir> \
        --title "Meeting Title" [--date 2026-01-12] [--notes "..."]
"""

import argparse
import os
import subprocess
import sys

from pipeline.pool_utils import (
    add_source_to_manifest,
    fetched_now,
    find_duplicate,
    next_source_id,
    read_manifest,
    sha256_file,
    write_manifest,
    write_source_markdown,
)

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
PARSER_SCRIPT = os.path.join(SCRIPTS_DIR, "parse_vtt.py")
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


def normalize_vtt(vtt_path, pool_dir, title, date=None, notes=None):
    """Convert a VTT file to evidence pool source markdown.

    Args:
        vtt_path: Path to the VTT file.
        pool_dir: Path to the target evidence pool directory.
        title: Source title for frontmatter.
        date: Optional date string for the filename slug.
        notes: Optional notes for frontmatter.

    Returns:
        Path to the created markdown file, or None if duplicate.
    """
    vtt_path = os.path.abspath(vtt_path)
    pool_dir = os.path.abspath(pool_dir)
    file_hash = sha256_file(vtt_path)

    manifest = read_manifest(pool_dir)

    dup = find_duplicate(manifest, file_hash)
    if dup:
        sid = dup.get("source-id") or dup.get("id")
        print(f"Skipping: duplicate of source {sid} (hash match)", file=sys.stderr)
        return None

    # Parse VTT using parse_vtt.py
    result = subprocess.run(
        [sys.executable, PARSER_SCRIPT, vtt_path],
        capture_output=True, text=True, check=True,
    )
    lines = result.stdout.strip().split("\n")
    duration = lines[0]
    transcript_text = "\n".join(lines[1:]).strip()

    source_id = next_source_id(manifest)
    rel_path = os.path.relpath(vtt_path, PROJECT_ROOT)

    # Build filename slug
    if date:
        slug = f"{source_id}-{_slugify(title)}-{date}"
    else:
        slug = f"{source_id}-{_slugify(title)}"
    filename = f"{slug}.md"

    frontmatter = {
        "source-id": source_id,
        "title": title,
        "type": "media",
        "path": rel_path,
        "fetched": fetched_now(),
        "hash": file_hash,
        "duration": duration,
        "speakers": [],
        "notes": notes or "Auto-generated Vimeo captions. May contain transcription errors.",
    }

    body = f"# {title}\n\n**Duration:** {duration}\n**Source:** Auto-generated Vimeo captions (VTT)\n\n## Transcript\n\n{transcript_text}"

    out_path = write_source_markdown(pool_dir, filename, frontmatter, body)

    # Update manifest
    manifest_entry = {
        "source-id": source_id,
        "title": title,
        "type": "media",
        "path": rel_path,
        "hash": file_hash,
        "file": f"sources/{filename}",
        "duration": duration,
    }
    add_source_to_manifest(manifest, manifest_entry)
    write_manifest(pool_dir, manifest)

    print(f"Created {filename} (source-id: {source_id}, duration: {duration})")
    return out_path


def _slugify(text):
    """Convert title to a filename-safe slug."""
    import re
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    # Truncate to keep filenames reasonable
    if len(slug) > 60:
        slug = slug[:60].rstrip("-")
    return slug


def main():
    parser = argparse.ArgumentParser(
        description="Convert a VTT file to evidence pool source markdown."
    )
    parser.add_argument("vtt_file", help="Path to the VTT file")
    parser.add_argument("pool_dir", help="Path to the target evidence pool directory")
    parser.add_argument("--title", required=True, help="Source title")
    parser.add_argument("--date", help="Date string for filename (e.g., 2026-01-12)")
    parser.add_argument("--notes", help="Notes for frontmatter")
    args = parser.parse_args()

    result = normalize_vtt(args.vtt_file, args.pool_dir, args.title,
                           date=args.date, notes=args.notes)
    if result is None:
        sys.exit(0)


if __name__ == "__main__":
    main()
