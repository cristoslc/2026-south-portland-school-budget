"""Keyword-triggered reference context injection for interpretation prompts.

Scans trove manifests for source-level ``triggers`` arrays. When meeting
content contains any trigger term (case-insensitive literal match), the
trove's synthesis is collected for prompt injection.

See ADR-005 and SPEC-081 for design rationale.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import yaml


MAX_REFERENCE_TROVES = 3

REFERENCE_PREAMBLE = """\
The following reference material provides historical context relevant to \
topics raised in this meeting. Use it to ground your interpretation where \
the meeting content directly engages with these topics.

Do not flag the absence of discussion on these topics. Do not speculate \
about why referenced topics were or were not raised. Only use this context \
when the meeting content directly engages with it."""


def match_reference_triggers(
    meeting_text: str,
    troves_dir: Path,
) -> List[Dict]:
    """Scan trove manifests for trigger matches against meeting text.

    Args:
        meeting_text: Concatenated meeting content (all sources).
        troves_dir: Path to ``docs/troves/`` directory.

    Returns:
        List of match dicts sorted by hit_count descending, capped at
        MAX_REFERENCE_TROVES.  Each dict has keys: trove_id, hit_count,
        synthesis.
    """
    if not troves_dir.is_dir():
        return []

    text_lower = meeting_text.lower()
    results = []

    for manifest_path in sorted(troves_dir.glob("*/manifest.yaml")):
        trove_dir = manifest_path.parent
        try:
            manifest = yaml.safe_load(manifest_path.read_text())
        except Exception:
            continue

        if not manifest or "sources" not in manifest:
            continue

        hit_count = 0
        for source in manifest["sources"]:
            triggers = source.get("triggers")
            if not triggers:
                continue
            for trigger in triggers:
                if trigger.lower() in text_lower:
                    hit_count += 1

        if hit_count == 0:
            continue

        synthesis_path = trove_dir / "synthesis.md"
        synthesis = ""
        if synthesis_path.is_file():
            synthesis = synthesis_path.read_text()

        results.append({
            "trove_id": manifest.get("trove", trove_dir.name),
            "hit_count": hit_count,
            "synthesis": synthesis,
        })

    results.sort(key=lambda r: r["hit_count"], reverse=True)
    return results[:MAX_REFERENCE_TROVES]


def build_reference_context_block(matches: List[Dict]) -> str:
    """Build the ``<reference_context>`` prompt block from matched troves.

    Returns empty string when there are no matches (AC-4).
    """
    if not matches:
        return ""

    sections = []
    for m in matches:
        sections.append(f"#### Trove: {m['trove_id']}\n\n{m['synthesis']}")

    body = "\n\n".join(sections)
    return f"""\
<reference_context>
{REFERENCE_PREAMBLE}

{body}
</reference_context>"""
