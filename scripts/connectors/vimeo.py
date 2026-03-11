#!/usr/bin/env python3
"""Vimeo VTT Connector — live discovery of SPC-TV channel videos.

Enumerates the SPC-TV Vimeo channel on every run, filters to FY27-relevant
meetings, and downloads VTTs for videos not already local. Uses
pipeline.discovery.DiscoveryHistory for attempt tracking and backoff.

No API token required — uses yt-dlp for both channel enumeration and download.

Usage:
    python3 scripts/connectors/vimeo.py              # download all missing VTTs
    python3 scripts/connectors/vimeo.py --check-only # list what would be downloaded
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

# Add project root to path so pipeline.discovery is importable
sys.path.insert(0, PROJECT_ROOT)
from pipeline.discovery import DiscoveryHistory  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("vimeo-connector")

# ---------------------------------------------------------------------------
# Filter criteria (top-level constants for easy FY adjustment)
# ---------------------------------------------------------------------------

CHANNEL_ID = "spctv"
CHANNEL_URL = f"https://vimeo.com/{CHANNEL_ID}/videos"

TITLE_PREFIXES = ["spboe_", "spcc_", "spccws_"]
DATE_CUTOFF = "2025-12-01"

# Title prefix → data directory subtree
PREFIX_TO_TYPE = {
    "spboe_": "school-board",
    "spcc_": "city-council",
    "spccws_": "city-council",
}

# History file per meeting type
HISTORY_PATHS = {
    "school-board": os.path.join(
        PROJECT_ROOT, "data", "school-board", "meetings", "discovery.jsonl"
    ),
    "city-council": os.path.join(
        PROJECT_ROOT, "data", "city-council", "meetings", "discovery.jsonl"
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def check_yt_dlp():
    """Verify yt-dlp is available."""
    if not shutil.which("yt-dlp"):
        log.error("yt-dlp not found on PATH. Install with: brew install yt-dlp")
        sys.exit(1)


def discover_channel(channel_id):
    """List all videos on a Vimeo channel using yt-dlp.

    Returns a list of dicts with keys: id, title, upload_date.
    """
    url = CHANNEL_URL.format(channel=channel_id)
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        "--no-warnings",
        url,
    ]

    log.info("Discovering videos on channel: %s", channel_id)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        log.error("Timeout listing channel %s", channel_id)
        return []

    if result.returncode != 0:
        log.error("yt-dlp channel listing failed: %s", result.stderr.strip()[:300])
        return []

    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            videos.append({
                "id": str(data.get("id", "")),
                "title": data.get("title", ""),
                "upload_date": data.get("upload_date", ""),  # YYYYMMDD
            })
        except json.JSONDecodeError:
            continue

    log.info("Found %d video(s) on channel", len(videos))
    return videos


def matches_filters(video, prefixes, after_date):
    """Check if a video matches the discovery filters.

    Args:
        video:      dict with 'title' and 'upload_date' keys
        prefixes:   list of title prefixes to match (e.g., ['spboe_', 'spcc_'])
        after_date: minimum date string (YYYY-MM-DD) or None
    """
    title = video.get("title", "").lower()

    if prefixes:
        if not any(title.startswith(p.lower()) for p in prefixes):
            return False

    if after_date:
        video_date = None
        upload = video.get("upload_date", "")
        if upload and len(upload) == 8:
            video_date = f"{upload[:4]}-{upload[4:6]}-{upload[6:8]}"
        else:
            m = re.search(r"(\d{8})", title)
            if m:
                d = m.group(1)
                video_date = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        if video_date and video_date < after_date:
            return False

    return True


def infer_meeting_type(title):
    """Return the meeting type ('school-board' or 'city-council') from title."""
    lower = title.lower()
    for prefix, mtype in PREFIX_TO_TYPE.items():
        if lower.startswith(prefix):
            return mtype
    return "school-board"  # default for SPC-TV


def infer_metadata(video):
    """Infer meeting type, subtype, date, and output path from video metadata.

    Returns a dict with keys: vimeo_id, type, subtype, date, output.
    """
    title = video.get("title", "").lower()
    vimeo_id = video["id"]

    meeting_type = infer_meeting_type(video.get("title", ""))

    if "budget forum" in title:
        subtype = "budget-forum"
    elif "budget workshop" in title:
        subtype = "budget-workshop"
    elif "workshop" in title:
        subtype = "workshop"
    else:
        subtype = "regular-meeting"

    upload_date = video.get("upload_date", "")
    if upload_date and len(upload_date) == 8:
        date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    else:
        m = re.search(r"(\d{8})", video.get("title", ""))
        if m:
            d = m.group(1)
            date = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        else:
            m = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", video.get("title", ""))
            if m:
                month, day, year = m.group(1), m.group(2), m.group(3)
                if len(year) == 2:
                    year = f"20{year}"
                date = f"{year}-{int(month):02d}-{int(day):02d}"
            else:
                date = "unknown"

    dir_name = date
    if subtype != "regular-meeting":
        dir_name = f"{date}-{subtype}"

    output = f"data/{meeting_type}/meetings/{dir_name}/transcript.en-x-autogen.vtt"

    return {
        "vimeo_id": vimeo_id,
        "type": meeting_type,
        "subtype": subtype,
        "date": date,
        "output": output,
    }


def download_vtt(vimeo_id, output_path):
    """Download VTT captions for a single Vimeo video.

    Returns (success: bool, error_msg: str).
    """
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--sub-lang", "en-x-autogen",
            "--sub-format", "vtt",
            "--skip-download",
            "--no-warnings",
            "-o", os.path.join(tmpdir, "video.%(ext)s"),
            f"https://vimeo.com/{vimeo_id}",
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60
            )
        except subprocess.TimeoutExpired:
            msg = f"Timeout downloading VTT for Vimeo ID {vimeo_id}"
            log.error(msg)
            return False, msg

        if result.returncode != 0:
            stderr = result.stderr.strip()
            if "no subtitles" in stderr.lower() or "no subtitle" in stderr.lower():
                msg = f"No auto-generated captions for Vimeo ID {vimeo_id}"
                log.warning(msg)
            else:
                msg = (
                    f"yt-dlp failed for Vimeo ID {vimeo_id} "
                    f"(exit {result.returncode}): {stderr[:200]}"
                )
                log.error(msg)
            return False, result.stderr.strip()[:200]

        vtt_files = [f for f in os.listdir(tmpdir) if f.endswith(".vtt")]
        if not vtt_files:
            msg = f"No VTT file produced for Vimeo ID {vimeo_id}"
            log.warning(msg)
            return False, msg

        shutil.move(os.path.join(tmpdir, vtt_files[0]), output_path)
        return True, ""


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def run(check_only=False):
    """Enumerate SPC-TV channel, filter, diff against disk, download missing."""
    check_yt_dlp()

    videos = discover_channel(CHANNEL_ID)
    if not videos:
        log.warning("No videos returned from channel — exiting")
        return 0

    relevant = [v for v in videos if matches_filters(v, TITLE_PREFIXES, DATE_CUTOFF)]
    log.info(
        "Filtered to %d relevant video(s) (from %d total, prefixes=%s, after=%s)",
        len(relevant), len(videos), TITLE_PREFIXES, DATE_CUTOFF,
    )

    if not relevant:
        log.info("No relevant videos found — nothing to do")
        return 0

    # Lazy-load history instances per meeting type
    histories = {}

    def get_history(meeting_type):
        if meeting_type not in histories:
            histories[meeting_type] = DiscoveryHistory(HISTORY_PATHS[meeting_type])
        return histories[meeting_type]

    stats = {"skipped": 0, "backoff": 0, "downloaded": 0, "failed": 0, "would_download": 0}

    for video in relevant:
        meta = infer_metadata(video)
        vimeo_id = meta["vimeo_id"]
        output_path = os.path.join(PROJECT_ROOT, meta["output"])
        vimeo_url = f"https://vimeo.com/{vimeo_id}"
        label = f"{meta['type']}/{meta['date']} (Vimeo {vimeo_id})"
        history = get_history(meta["type"])

        # Diff against disk — primary gate
        if os.path.exists(output_path):
            log.info("SKIP %s — already exists", label)
            stats["skipped"] += 1
            continue

        # Backoff check for previously failed URLs
        if not history.should_attempt(vimeo_url):
            log.debug("BACKOFF %s — within backoff window", label)
            stats["backoff"] += 1
            continue

        if check_only:
            log.info("WOULD DOWNLOAD %s → %s", label, meta["output"])
            stats["would_download"] += 1
            continue

        log.info("DOWNLOADING %s", label)
        success, error_msg = download_vtt(vimeo_id, output_path)
        if success:
            file_size = os.path.getsize(output_path)
            log.info("OK %s — %d bytes", label, file_size)
            history.record_attempt(vimeo_url, label, "ok")
            stats["downloaded"] += 1
        else:
            history.record_attempt(vimeo_url, label, "failed", error_msg)
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

    # Exit 0 on partial success — individual failures are non-fatal
    return 0


def main():
    parser = argparse.ArgumentParser(description="Vimeo VTT Connector")
    parser.add_argument(
        "--check-only", action="store_true",
        help="List what would be downloaded without downloading",
    )
    args = parser.parse_args()
    sys.exit(run(check_only=args.check_only))


if __name__ == "__main__":
    main()
