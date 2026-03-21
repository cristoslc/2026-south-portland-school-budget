#!/usr/bin/env python3
"""Budget Page Live Discovery Connector — download documents from spsdme.org/budget27.

Fetches the budget page on every run, extracts document links, and downloads
any that are not already present locally. Uses DiscoveryHistory for history
tracking and backoff.

Supported document types: PDF (Google Drive), XLSX (Google Sheets export),
PDF (Google Docs export). Google Slides pubembed URLs are logged as unsupported
and skipped.

Usage:
    python3 scripts/connectors/budget_page.py              # download missing docs
    python3 scripts/connectors/budget_page.py --check-only # list what would be downloaded
"""

import argparse
import html as _html
import logging
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import unquote as _url_unquote
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pipeline.discovery import DiscoveryHistory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("budget-page-connector")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

BUDGET_PAGE_URL = "https://www.spsdme.org/budget27"
DOCUMENTS_DIR = os.path.join(PROJECT_ROOT, "data", "school-board", "budget-fy27", "documents")
HISTORY_PATH = os.path.join(PROJECT_ROOT, "data", "school-board", "budget-fy27", "discovery.jsonl")
SNAPSHOTS_DIR = os.path.join(PROJECT_ROOT, "data", "school-board", "budget-fy27", "page-snapshots")

# Google URL patterns
DRIVE_FILE_RE = re.compile(r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)")
DOCS_RE = re.compile(r"docs\.google\.com/document/d/([a-zA-Z0-9_-]+)")
SHEETS_RE = re.compile(r"docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)")
SLIDES_RE = re.compile(r"docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)")
SLIDES_PUBEMBED_RE = re.compile(
    r"docs\.google\.com/presentation/d/e/([a-zA-Z0-9_-]+)/(?:pubembed|embed)"
)

# Extract all Google Drive/Docs/Sheets/Slides links from the page
PAGE_LINK_RE = re.compile(
    r'(https://(?:drive\.google\.com/file/d/|docs\.google\.com/'
    r'(?:document|spreadsheets|presentation)/d/)[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_.?=&%-]*)*)'
)

# Capture surrounding anchor text near a link
LINK_CONTEXT_RE = re.compile(
    r'(?:>([^<]{1,100})<[^>]*(?:href|src)=["\']?'
    r'(https://(?:drive\.google\.com|docs\.google\.com)[^"\'>\s]+)'
    r'|'
    r'(?:href|src)=["\']?'
    r'(https://(?:drive\.google\.com|docs\.google\.com)[^"\'>\s]+)'
    r'["\']?[^>]*>([^<]{1,100})<)',
    re.IGNORECASE,
)


def _extract_doc_id(url):
    """Extract the Google document/file ID from a Google URL.

    Returns the alphanumeric ID string (globally unique), or None if unrecognised.
    Checked in priority order: pubembed (captures pubid before SLIDES_RE grabs 'e'),
    then Drive, Docs, Sheets, Slides edit.
    """
    m = SLIDES_PUBEMBED_RE.search(url)
    if m:
        return m.group(1)
    for pattern in (DRIVE_FILE_RE, DOCS_RE, SHEETS_RE, SLIDES_RE):
        m = pattern.search(url)
        if m:
            return m.group(1)
    return None


_CD_RFC5987_RE = re.compile(r"filename\*\s*=\s*UTF-8''([^;\s]+)", re.IGNORECASE)
_CD_PLAIN_RE = re.compile(r'filename\s*=\s*["\']?([^"\';\r\n]+)', re.IGNORECASE)


def _parse_content_disposition(header, extension):
    """Extract and sanitize a filename from a Content-Disposition header value.

    Prefers RFC 5987 ``filename*=UTF-8''...`` over plain ``filename=...``.
    URL-decodes the value, replaces whitespace and unsafe chars with hyphens,
    and ensures the result ends with *extension*.  Returns None if no filename
    is found or the header is empty.
    """
    if not header:
        return None
    m = _CD_RFC5987_RE.search(header)
    raw = _url_unquote(m.group(1)) if m else None
    if raw is None:
        m = _CD_PLAIN_RE.search(header)
        raw = m.group(1).strip().strip('"\'') if m else None
    if not raw:
        return None
    # Sanitize: keep alphanumerics, dots, hyphens; collapse everything else to '-'
    stem, sep, _ = raw.rpartition(".")
    stem = stem if sep else raw  # no extension in CD name — use full string
    sanitized = re.sub(r"[^a-zA-Z0-9.\-]+", "-", stem).strip("-")
    if not sanitized:
        return None
    return sanitized[:80] + extension


def classify_url(url):
    """Classify a Google URL and return (url_type, export_url, extension).

    url_type is one of: "drive_pdf", "docs_pdf", "sheets_xlsx", "slides_unsupported".
    Returns (None, None, None) for unrecognised URLs.
    """
    m = SLIDES_PUBEMBED_RE.search(url)
    if m:
        pub_id = m.group(1)
        export_url = f"https://docs.google.com/presentation/d/e/{pub_id}/export?format=pdf"
        return "slides_pdf", export_url, ".pdf"

    m = SLIDES_RE.search(url)
    if m:
        pres_id = m.group(1)
        export_url = f"https://docs.google.com/presentation/d/{pres_id}/export?format=pdf"
        return "slides_pdf", export_url, ".pdf"

    m = DRIVE_FILE_RE.search(url)
    if m:
        file_id = m.group(1)
        export_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return "drive_pdf", export_url, ".pdf"

    m = DOCS_RE.search(url)
    if m:
        doc_id = m.group(1)
        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"
        return "docs_pdf", export_url, ".pdf"

    m = SHEETS_RE.search(url)
    if m:
        doc_id = m.group(1)
        export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=xlsx"
        return "sheets_xlsx", export_url, ".xlsx"

    return None, None, None


def _fetch_html(page_url):
    """Fetch the raw HTML of page_url. Returns HTML string or None on error."""
    req = Request(page_url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; budget-connector/1.0)",
        "Accept": "text/html",
    })
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except (URLError, HTTPError) as e:
        log.error("Failed to fetch budget page %s: %s", page_url, e)
        return None


def _extract_links_from_html(raw_html, page_url):
    """Extract Google document links from already-fetched HTML.

    Returns a list of dicts: [{url, label}, ...].
    """
    # Build URL -> label map from anchor context
    url_labels = {}
    for m in LINK_CONTEXT_RE.finditer(raw_html):
        pre_text, pre_url, post_url, post_text = m.groups()
        url = pre_url or post_url
        label = (pre_text or post_text or "").strip()
        if url and label:
            base = url.split("?")[0]
            url_labels[base] = label

    # Extract unique links
    seen = set()
    unique = []
    for link in PAGE_LINK_RE.findall(raw_html):
        base = link.split("?")[0]
        if base not in seen:
            seen.add(base)
            unique.append({"url": link, "label": url_labels.get(base, "")})

    if not unique:
        log.warning(
            "Zero document links found on %s — page structure may have changed",
            page_url,
        )
    else:
        log.info("Found %d document link(s) on %s", len(unique), page_url)

    return unique


def fetch_page_links(page_url):
    """Fetch the budget page and extract all Google document links.

    Returns a list of dicts: [{url, label}, ...].
    On network error, returns an empty list (logged as error).
    """
    raw_html = _fetch_html(page_url)
    if raw_html is None:
        return []
    return _extract_links_from_html(raw_html, page_url)


def _fragment_to_text(decoded_html):
    """Convert a single decoded HTML fragment to plain text with structure."""
    text = decoded_html

    # Headings → markdown-style markers
    for level in range(1, 7):
        text = re.sub(
            rf"<h{level}[^>]*>(.*?)</h{level}>",
            lambda m, l=level: f"\n{'#' * l} {re.sub(r'<[^>]+>', '', m.group(1)).strip()}\n",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

    # List items → bullet points
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "", text, flags=re.IGNORECASE)

    # Block elements → newlines
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(?:p|div|tr|td|th)>", "\n", text, flags=re.IGNORECASE)

    # Strip remaining tags
    text = re.sub(r"<[^>]+>", "", text)

    # Decode HTML entities
    text = _html.unescape(text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def page_html_to_text(raw_html):
    """Extract and convert budget page content from embedded CMS JSON.

    The Apptegy CMS embeds page content as JSON-encoded HTML fragments
    in a script blob. This function extracts all such \"html\":\"...\"
    fields, decodes their triple-escaped HTML, and converts to plain text.
    """
    # Matches \"html\":\"<content>\" patterns in the triple-escaped CMS JSON blob
    # Each field delimiter is one backslash + double-quote in the raw HTML.
    pattern = re.compile('\\\\"html\\\\":\\\\"(.*?)(?<!\\\\)\\\\"[,}]', re.DOTALL)

    text_parts = []
    for m in pattern.finditer(raw_html):
        val = m.group(1)
        # Decode triple-escaped HTML attribute quotes (3 backslashes + quote → quote)
        _triple_escaped_quote = chr(92) * 3 + chr(34)
        decoded = val.replace(_triple_escaped_quote, chr(34))
        fragment_text = _fragment_to_text(decoded)
        if len(fragment_text) > 10:
            text_parts.append(fragment_text)
    return "\n\n".join(text_parts)


def save_page_snapshot(raw_html):
    """Save a date-stamped plain-text snapshot of the budget page.

    One snapshot per UTC date. Skips if today's snapshot already exists.
    """
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshot_path = os.path.join(SNAPSHOTS_DIR, f"{date_str}.txt")
    if os.path.exists(snapshot_path):
        log.info("SKIP page snapshot — already exists for %s", date_str)
        return
    text = page_html_to_text(raw_html)
    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
    with open(snapshot_path, "w", encoding="utf-8") as f:
        f.write(f"Source: {BUDGET_PAGE_URL}\nSnapshot date: {date_str}\n\n{text}")
    log.info("OK page snapshot saved — %s (%d chars)", date_str, len(text))


def local_filename(url, label, extension):
    """Derive a local filename from URL and label.

    Uses the anchor-text label when available.  Falls back to the Google
    document ID (globally unique) rather than the URL path endpoint verb
    (edit/view/pubembed), which would produce collisions.
    """
    slug = re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')[:60] if label else ""
    if not slug:
        doc_id = _extract_doc_id(url)
        slug = doc_id if doc_id else url.split("?")[0].rstrip("/").split("/")[-1][:40]
    return slug + extension


def download_file(export_url, output_path, extension=".pdf"):
    """Download a file from export_url to output_path.

    Returns (success, cd_filename) where cd_filename is the sanitized filename
    derived from the Content-Disposition response header (or None if absent).
    The file is always written to output_path regardless of cd_filename.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    req = Request(export_url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; budget-connector/1.0)",
    })
    try:
        with urlopen(req, timeout=60) as resp:
            cd_header = resp.headers.get("Content-Disposition", "")
            content = resp.read()
            if len(content) < 100:
                log.error(
                    "Suspiciously small file (%d bytes) from %s", len(content), export_url
                )
                return False, None
            with open(output_path, "wb") as f:
                f.write(content)
        cd_filename = _parse_content_disposition(cd_header, extension)
        return True, cd_filename
    except (URLError, HTTPError) as e:
        log.error("Download failed for %s: %s", export_url, e)
        return False, None


def run(check_only=False):
    """Main connector logic — live discovery and download."""
    history = DiscoveryHistory(HISTORY_PATH)

    # Fetch the budget page once; save a daily snapshot, then extract document links
    raw_html = _fetch_html(BUDGET_PAGE_URL)
    if raw_html is None:
        log.warning("Failed to fetch budget page — exiting without downloading")
        return 0
    save_page_snapshot(raw_html)
    links = _extract_links_from_html(raw_html, BUDGET_PAGE_URL)
    if not links:
        log.warning("No links retrieved — page structure may have changed")
        return 0

    stats = {"skipped_existing": 0, "skipped_backoff": 0,
             "downloaded": 0, "failed": 0, "would_download": 0}

    for link_info in links:
        url = link_info["url"]
        label = link_info.get("label", "")

        url_type, export_url, extension = classify_url(url)

        # Unrecognised URL pattern
        if url_type is None:
            log.debug("Unrecognised URL pattern — skipping: %s", url)
            continue

        # Derive local path
        filename = local_filename(url, label, extension)
        output_path = os.path.join(DOCUMENTS_DIR, filename)

        # Skip if already on disk — check both the candidate path and any
        # previously-recorded local_path (for files renamed to their CD name)
        record = history.get_record(url)
        saved_local = record.get("local_path") if record else None
        saved_path = os.path.join(DOCUMENTS_DIR, saved_local) if saved_local else None
        if (saved_path and os.path.exists(saved_path)) or os.path.exists(output_path):
            display = saved_local if saved_path and os.path.exists(saved_path) else filename
            log.info("SKIP (exists) %s", display)
            stats["skipped_existing"] += 1
            continue

        # Check backoff
        if not history.should_attempt(url):
            stats["skipped_backoff"] += 1
            continue

        if check_only:
            log.info("WOULD DOWNLOAD %s → %s", label or url[:60], filename)
            stats["would_download"] += 1
            continue

        log.info("DOWNLOADING %s → %s", label or url[:60], filename)
        file_ext = extension if extension is not None else ".pdf"
        success, cd_filename = download_file(export_url, output_path, file_ext)
        if success:
            # Rename to Content-Disposition filename if Google provided one
            final_filename = filename
            if cd_filename and cd_filename != filename:
                cd_path = os.path.join(DOCUMENTS_DIR, cd_filename)
                if not os.path.exists(cd_path):
                    os.rename(output_path, cd_path)
                    final_filename = cd_filename
                    log.info("OK %s (%d bytes)", final_filename, os.path.getsize(cd_path))
                else:
                    os.remove(output_path)
                    final_filename = cd_filename
                    log.info("OK %s (merged with existing)", final_filename)
            else:
                log.info("OK %s — %d bytes", final_filename, os.path.getsize(output_path))
            history.record_attempt(url, label, "ok", local_path=final_filename)
            stats["downloaded"] += 1
        else:
            history.record_attempt(url, label, "failed",
                                   error="download error (see logs)")
            stats["failed"] += 1

    log.info("---")
    if check_only:
        log.info(
            "Check complete: %d would download, %d already exist, %d in backoff",
            stats["would_download"], stats["skipped_existing"],
            stats["skipped_backoff"],
        )
    else:
        log.info(
            "Done: %d downloaded, %d skipped (exist), %d failed, %d in backoff",
            stats["downloaded"], stats["skipped_existing"], stats["failed"],
            stats["skipped_backoff"],
        )

    # Exit 0 on partial success (individual failures are non-fatal)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Budget Page Live Discovery Connector")
    parser.add_argument(
        "--check-only", action="store_true",
        help="List what would be downloaded without downloading",
    )
    args = parser.parse_args()
    sys.exit(run(check_only=args.check_only))


if __name__ == "__main__":
    main()
