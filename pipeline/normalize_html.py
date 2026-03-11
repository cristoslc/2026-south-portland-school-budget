#!/usr/bin/env python3
"""Convert HTML content (e.g., Diligent Community agenda) to evidence pool source markdown.

Uses BeautifulSoup for parsing and markdownify for HTML-to-markdown conversion.
Strips Diligent UI chrome and extracts the agenda body.

Usage:
    python3 -m pipeline.normalize_html <html_file> <pool_dir> \
        --title "Agenda Title" [--date 2026-01-06] [--source-url "https://..."]
"""

import argparse
import os
import sys

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from pipeline.pool_utils import (
    add_source_to_manifest,
    fetched_now,
    find_duplicate,
    next_source_id,
    read_manifest,
    sha256_bytes,
    write_manifest,
    write_source_markdown,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Common Diligent UI chrome selectors to strip
CHROME_SELECTORS = [
    "nav", "header", "footer",
    ".navbar", ".sidebar", ".breadcrumb",
    "#header", "#footer", "#navigation",
    "[role='navigation']", "[role='banner']", "[role='contentinfo']",
]


def normalize_html(html_path, pool_dir, title, date=None, source_url=None):
    """Convert an HTML file to evidence pool source markdown.

    Args:
        html_path: Path to the HTML file.
        pool_dir: Path to the target evidence pool directory.
        title: Source title for frontmatter.
        date: Optional date string for the filename slug.
        source_url: Optional source URL for frontmatter.

    Returns:
        Path to the created markdown file, or None if duplicate.
    """
    html_path = os.path.abspath(html_path)
    pool_dir = os.path.abspath(pool_dir)

    with open(html_path, "rb") as f:
        raw_bytes = f.read()

    file_hash = sha256_bytes(raw_bytes)
    html_content = raw_bytes.decode("utf-8", errors="replace")

    manifest = read_manifest(pool_dir)

    dup = find_duplicate(manifest, file_hash)
    if dup:
        sid = dup.get("source-id") or dup.get("id")
        print(f"Skipping: duplicate of source {sid} (hash match)", file=sys.stderr)
        return None

    # Extract and convert
    markdown_body = _html_to_markdown(html_content)

    source_id = next_source_id(manifest)
    rel_path = os.path.relpath(html_path, PROJECT_ROOT)

    if date:
        slug = f"{source_id}-{_slugify(title)}-{date}"
    else:
        slug = f"{source_id}-{_slugify(title)}"
    filename = f"{slug}.md"

    frontmatter = {
        "source-id": source_id,
        "title": title,
        "type": "local",
        "path": rel_path,
        "fetched": fetched_now(),
        "hash": file_hash,
    }
    if source_url:
        frontmatter["source-url"] = source_url

    out_path = write_source_markdown(pool_dir, filename, frontmatter, markdown_body)

    manifest_entry = {
        "source-id": source_id,
        "title": title,
        "type": "local",
        "path": rel_path,
        "hash": file_hash,
        "file": f"sources/{filename}",
    }
    add_source_to_manifest(manifest, manifest_entry)
    write_manifest(pool_dir, manifest)

    line_count = len(markdown_body.splitlines())
    print(f"Created {filename} (source-id: {source_id}, {line_count} lines)")
    return out_path


def _html_to_markdown(html_content):
    """Parse HTML, strip chrome, convert to markdown."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Strip UI chrome elements
    for selector in CHROME_SELECTORS:
        for el in soup.select(selector):
            el.decompose()

    # Strip script and style tags
    for tag in soup.find_all(["script", "style", "link", "meta"]):
        tag.decompose()

    # Try to find the main content area
    main = (
        soup.find("main")
        or soup.find(id="content")
        or soup.find(class_="content")
        or soup.find("article")
        or soup.find("body")
        or soup
    )

    # Convert to markdown
    markdown = md(str(main), heading_style="ATX", bullets="-", strip=["img"])

    # Clean up excessive whitespace
    lines = markdown.splitlines()
    cleaned = []
    blank_count = 0
    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(stripped)

    return "\n".join(cleaned).strip()


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
        description="Convert an HTML file to evidence pool source markdown."
    )
    parser.add_argument("html_file", help="Path to the HTML file")
    parser.add_argument("pool_dir", help="Path to the target evidence pool directory")
    parser.add_argument("--title", required=True, help="Source title")
    parser.add_argument("--date", help="Date string for filename (e.g., 2026-01-06)")
    parser.add_argument("--source-url", help="Source URL for frontmatter")
    args = parser.parse_args()

    result = normalize_html(args.html_file, args.pool_dir, args.title,
                            date=args.date, source_url=args.source_url)
    if result is None:
        sys.exit(0)


if __name__ == "__main__":
    main()
