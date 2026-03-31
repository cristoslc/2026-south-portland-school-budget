#!/usr/bin/env python3
"""SPC-TV TelVue Connector — discovery and VTT extraction from TelVue VOD.

Enumerates the SPC-TV TelVue VOD player on every run, filters to relevant
South Portland meetings (Board of Education, City Council), and downloads
VTTs for videos not already local. Uses pipeline.discovery.DiscoveryHistory
for attempt tracking and backoff.

Usage:
    python3 scripts/connectors/telvue.py              # download all missing VTTs
    python3 scripts/connectors/telvue.py --check-only  # list what would be downloaded
"""

import argparse
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

sys.path.insert(0, PROJECT_ROOT)
from pipeline.discovery import DiscoveryHistory  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("telvue-connector")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TELVUE_PLAYER_ID = "NzN-Z2CpIDNbXMWB16nIzGKjRlHJozGq"
TELVUE_VOD_URL = (
    f"https://videoplayer.telvue.com/player/{TELVUE_PLAYER_ID}/videos"
    "?autostart=false&showtabssearch=true&fullscreen=false"
)
TELVUE_MEDIA_BASE = f"https://videoplayer.telvue.com/player/{TELVUE_PLAYER_ID}/media"

DATE_CUTOFF = "2025-12-01"

# Title patterns → meeting type
TITLE_PATTERNS = [
    (re.compile(r"board of education", re.IGNORECASE), "school-board"),
    (re.compile(r"city council", re.IGNORECASE), "city-council"),
    (re.compile(r"budget workshop", re.IGNORECASE), "school-board"),
]

# Month name → number
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

HISTORY_PATHS = {
    "school-board": os.path.join(
        PROJECT_ROOT, "data", "school-board", "meetings", "discovery.jsonl"
    ),
    "city-council": os.path.join(
        PROJECT_ROOT, "data", "city-council", "meetings", "discovery.jsonl"
    ),
}


# ---------------------------------------------------------------------------
# Page parsing
# ---------------------------------------------------------------------------


def parse_telvue_page(html):
    """Parse TelVue VOD listing HTML and extract video entries.

    Returns a list of dicts with keys: media_id, title, duration.
    """
    videos = []
    media_url_pattern = re.compile(
        rf"/player/{re.escape(TELVUE_PLAYER_ID)}/media/(\d+)"
    )
    duration_pattern = re.compile(r"\b(\d{2}:\d{2}:\d{2})\b")

    # Split HTML into segments between media links to isolate each video's context
    media_matches = list(media_url_pattern.finditer(html))
    if not media_matches:
        return videos

    seen_ids = set()
    for i, match in enumerate(media_matches):
        media_id = match.group(1)
        if media_id in seen_ids:
            continue
        seen_ids.add(media_id)

        # Context: from this match to the next media link (or end of segment)
        start = match.start()
        # Find next different media_id
        end = len(html)
        for j in range(i + 1, len(media_matches)):
            if media_matches[j].group(1) != media_id:
                end = media_matches[j].start()
                break
        context = html[start:end]

        # Extract title: text inside tags following the media link
        title = ""
        # Look for span/generic content with meeting-like text
        title_matches = re.findall(r">([^<]{10,})<", context)
        for candidate in title_matches:
            candidate = candidate.strip()
            if any(kw in candidate.lower() for kw in [
                "south portland", "budget workshop", "city council",
                "board of education", "planning board",
            ]):
                title = candidate
                break

        # Extract duration
        duration = ""
        dur_match = duration_pattern.search(context)
        if dur_match:
            duration = dur_match.group(1)

        if title:
            videos.append({
                "media_id": media_id,
                "title": title,
                "duration": duration,
            })

    return videos


# ---------------------------------------------------------------------------
# Metadata inference
# ---------------------------------------------------------------------------


def infer_date_from_title(title):
    """Extract date from TelVue title format.

    Handles: "South Portland Board of Education - March 30 2026"
             "Budget Workshop I - March 2 2026"
    """
    # Pattern: Month Day Year at end of title (optional comma after day)
    m = re.search(
        r"(\w+)\s+(\d{1,2}),?\s+(\d{4})\s*$",
        title.strip(),
    )
    if m:
        month_name = m.group(1).lower()
        day = int(m.group(2))
        year = int(m.group(3))
        month_num = MONTHS.get(month_name)
        if month_num:
            return f"{year}-{month_num:02d}-{day:02d}"

    return "unknown"


def infer_meeting_type(title):
    """Return meeting type from title, or None if not a tracked type."""
    for pattern, meeting_type in TITLE_PATTERNS:
        if pattern.search(title):
            return meeting_type
    return None


def infer_subtype(title):
    """Return meeting subtype from title."""
    lower = title.lower()
    if "budget workshop" in lower or "budget forum" in lower:
        return "budget-workshop"
    if "workshop" in lower:
        return "workshop"
    return "regular-meeting"


def matches_filters(video):
    """Check if a video matches discovery filters.

    Must be a tracked meeting type and after DATE_CUTOFF.
    """
    meeting_type = infer_meeting_type(video["title"])
    if meeting_type is None:
        return False

    date = infer_date_from_title(video["title"])
    if date != "unknown" and date < DATE_CUTOFF:
        return False

    return True


def infer_metadata(video):
    """Infer full metadata from a video entry.

    Returns dict with: media_id, type, subtype, date, output, telvue_url.
    """
    media_id = video["media_id"]
    meeting_type = infer_meeting_type(video["title"])
    subtype = infer_subtype(video["title"])
    date = infer_date_from_title(video["title"])

    dir_name = date
    if subtype != "regular-meeting":
        dir_name = f"{date}-{subtype}"

    output = f"data/{meeting_type}/meetings/{dir_name}/transcript.en-x-autogen.vtt"
    telvue_url = f"{TELVUE_MEDIA_BASE}/{media_id}"

    return {
        "media_id": media_id,
        "type": meeting_type,
        "subtype": subtype,
        "date": date,
        "output": output,
        "telvue_url": telvue_url,
    }


def should_skip_existing(output_path):
    """Return True if the transcript file already exists on disk."""
    return os.path.exists(output_path)


# ---------------------------------------------------------------------------
# Fetching and downloading
# ---------------------------------------------------------------------------


def fetch_telvue_page():
    """Fetch the TelVue VOD listing page.

    Uses yt-dlp --flat-playlist first; falls back to curl for HTML scraping.
    """
    # Try curl for HTML content (TelVue pages are mostly server-rendered)
    cmd = [
        "curl", "-sL", "--max-time", "30",
        TELVUE_VOD_URL,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except subprocess.TimeoutExpired:
        log.error("Timeout fetching TelVue page")

    log.error("Failed to fetch TelVue VOD page")
    return ""


def download_vtt(media_id, output_path):
    """Download VTT captions for a TelVue video.

    Uses yt-dlp to extract captions from the TelVue stream.
    Returns (success: bool, error_msg: str).
    """
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    telvue_url = f"{TELVUE_MEDIA_BASE}/{media_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--skip-download",
            "--no-warnings",
            "-o", os.path.join(tmpdir, "video.%(ext)s"),
            telvue_url,
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )
        except subprocess.TimeoutExpired:
            msg = f"Timeout downloading VTT for TelVue media {media_id}"
            log.error(msg)
            return False, msg

        if result.returncode != 0:
            stderr = result.stderr.strip()
            msg = (
                f"yt-dlp failed for TelVue media {media_id} "
                f"(exit {result.returncode}): {stderr[:200]}"
            )
            log.error(msg)
            return False, msg

        vtt_files = [f for f in os.listdir(tmpdir) if f.endswith(".vtt")]
        if not vtt_files:
            msg = f"No VTT file produced for TelVue media {media_id}"
            log.warning(msg)
            return False, msg

        shutil.move(os.path.join(tmpdir, vtt_files[0]), output_path)
        return True, ""


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def run(check_only=False, project_root=None):
    """Enumerate SPC-TV, filter, diff against disk, download missing."""
    if project_root is None:
        project_root = PROJECT_ROOT

    if not check_only:
        if not shutil.which("yt-dlp"):
            log.error("yt-dlp not found on PATH. Install with: brew install yt-dlp")
            return 1

    html = fetch_telvue_page()
    if not html:
        log.warning("Empty page returned — exiting")
        return 0

    videos = parse_telvue_page(html)
    if not videos:
        log.warning("No videos found on page — exiting")
        return 0

    relevant = [v for v in videos if matches_filters(v)]
    log.info(
        "Filtered to %d relevant video(s) (from %d total)",
        len(relevant), len(videos),
    )

    if not relevant:
        log.info("No relevant videos found — nothing to do")
        return 0

    histories = {}

    def get_history(meeting_type):
        if meeting_type not in histories:
            history_path = os.path.join(
                project_root, "data", meeting_type, "meetings", "discovery.jsonl"
            )
            histories[meeting_type] = DiscoveryHistory(history_path)
        return histories[meeting_type]

    stats = {"skipped": 0, "backoff": 0, "downloaded": 0, "failed": 0, "would_download": 0}

    for video in relevant:
        meta = infer_metadata(video)
        media_id = meta["media_id"]
        output_path = os.path.join(project_root, meta["output"])
        telvue_url = meta["telvue_url"]
        label = f"{meta['type']}/{meta['date']} (TelVue {media_id})"
        history = get_history(meta["type"])

        if should_skip_existing(output_path):
            log.info("SKIP %s — already exists", label)
            stats["skipped"] += 1
            continue

        if not history.should_attempt(telvue_url):
            log.debug("BACKOFF %s — within backoff window", label)
            stats["backoff"] += 1
            continue

        if check_only:
            log.info("WOULD DOWNLOAD %s → %s", label, meta["output"])
            stats["would_download"] += 1
            continue

        log.info("DOWNLOADING %s", label)
        success, error_msg = download_vtt(media_id, output_path)
        if success:
            file_size = os.path.getsize(output_path)
            log.info("OK %s — %d bytes", label, file_size)
            history.record_attempt(telvue_url, label, "ok")
            stats["downloaded"] += 1
        else:
            history.record_attempt(telvue_url, label, "failed", error_msg)
            stats["failed"] += 1

    log.info("---")
    if check_only:
        log.info(
            "Check complete: %d would download, %d already exist, %d in backoff",
            stats["would_download"], stats["skipped"], stats["backoff"],
        )
    else:
        log.info(
            "Done: %d downloaded, %d skipped, %d failed, %d in backoff",
            stats["downloaded"], stats["skipped"], stats["failed"], stats["backoff"],
        )

    return 0


def main():
    parser = argparse.ArgumentParser(description="SPC-TV TelVue Connector")
    parser.add_argument(
        "--check-only", action="store_true",
        help="List what would be downloaded without downloading",
    )
    args = parser.parse_args()
    sys.exit(run(check_only=args.check_only))


if __name__ == "__main__":
    main()
