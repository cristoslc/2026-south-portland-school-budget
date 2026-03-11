#!/usr/bin/env python3
"""Convert a PDF file into evidence pool source markdown.

Uses pdfplumber for text extraction. Detects slide-heavy vs text-heavy PDFs
by page text density and adjusts output format accordingly.

Usage:
    python3 -m pipeline.normalize_pdf <pdf_file> <pool_dir> \
        --title "Document Title" [--date 2026-01-12]
"""

import argparse
import os
import sys

import pdfplumber

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

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Pages with fewer than this many characters are considered "sparse" (slide-like)
SPARSE_PAGE_THRESHOLD = 200
# If more than this fraction of pages are sparse, treat as slide-heavy
SLIDE_HEAVY_RATIO = 0.5


def normalize_pdf(pdf_path, pool_dir, title, date=None):
    """Convert a PDF file to evidence pool source markdown.

    Args:
        pdf_path: Path to the PDF file.
        pool_dir: Path to the target evidence pool directory.
        title: Source title for frontmatter.
        date: Optional date string for the filename slug.

    Returns:
        Path to the created markdown file, or None if duplicate.
    """
    pdf_path = os.path.abspath(pdf_path)
    pool_dir = os.path.abspath(pool_dir)
    file_hash = sha256_file(pdf_path)

    manifest = read_manifest(pool_dir)

    dup = find_duplicate(manifest, file_hash)
    if dup:
        sid = dup.get("source-id") or dup.get("id")
        print(f"Skipping: duplicate of source {sid} (hash match)", file=sys.stderr)
        return None

    # Extract text from PDF
    pages_text, is_slide_heavy = _extract_pdf(pdf_path)

    source_id = next_source_id(manifest)
    rel_path = os.path.relpath(pdf_path, PROJECT_ROOT)

    if date:
        slug = f"{source_id}-{_slugify(title)}-{date}"
    else:
        slug = f"{source_id}-{_slugify(title)}"
    filename = f"{slug}.md"

    notes = None
    if is_slide_heavy:
        notes = "Slide-heavy PDF — extracted text may lack context. Manual review recommended."

    frontmatter = {
        "source-id": source_id,
        "title": title,
        "type": "document",
        "path": rel_path,
        "fetched": fetched_now(),
        "hash": file_hash,
    }
    if notes:
        frontmatter["notes"] = notes

    body = _format_body(title, pages_text, is_slide_heavy)

    out_path = write_source_markdown(pool_dir, filename, frontmatter, body)

    manifest_entry = {
        "source-id": source_id,
        "title": title,
        "type": "document",
        "path": rel_path,
        "hash": file_hash,
        "file": f"sources/{filename}",
    }
    add_source_to_manifest(manifest, manifest_entry)
    write_manifest(pool_dir, manifest)

    page_count = len(pages_text)
    label = "slide-heavy" if is_slide_heavy else "text-heavy"
    print(f"Created {filename} (source-id: {source_id}, {page_count} pages, {label})")
    return out_path


def _extract_pdf(pdf_path):
    """Extract text from each page and determine if slide-heavy.

    Returns:
        Tuple of (list of page texts, is_slide_heavy bool).
    """
    pages = []
    sparse_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text.strip())
            if len(text.strip()) < SPARSE_PAGE_THRESHOLD:
                sparse_count += 1

    total = len(pages) if pages else 1
    is_slide_heavy = (sparse_count / total) >= SLIDE_HEAVY_RATIO
    return pages, is_slide_heavy


def _format_body(title, pages_text, is_slide_heavy):
    """Format extracted pages as markdown body."""
    if is_slide_heavy:
        sections = []
        for i, text in enumerate(pages_text, 1):
            if text:
                sections.append(f"## Slide {i}\n\n{text}")
        return f"# {title}\n\n" + "\n\n".join(sections)
    else:
        # Text-heavy: join pages with double newlines, no slide markers
        non_empty = [t for t in pages_text if t]
        return "\n\n".join(non_empty)


def _slugify(text):
    """Convert title to a filename-safe slug."""
    import re
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    if len(slug) > 60:
        slug = slug[:60].rstrip("-")
    return slug


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to evidence pool source markdown."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("pool_dir", help="Path to the target evidence pool directory")
    parser.add_argument("--title", required=True, help="Source title")
    parser.add_argument("--date", help="Date string for filename (e.g., 2026-01-12)")
    args = parser.parse_args()

    result = normalize_pdf(args.pdf_file, args.pool_dir, args.title, date=args.date)
    if result is None:
        sys.exit(0)


if __name__ == "__main__":
    main()
