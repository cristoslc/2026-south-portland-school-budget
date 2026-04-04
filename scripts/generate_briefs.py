#!/usr/bin/env python3
"""Public Brief Generator.

Generates all public-facing briefings for an upcoming meeting date:
- per-persona upcoming briefs
- a general upcoming brief
- a general evergreen budget briefing

Usage:
    python3 scripts/generate_briefs.py <upcoming-meeting-date>
    python3 scripts/generate_briefs.py <upcoming-meeting-date> --dry-run
    python3 scripts/generate_briefs.py <upcoming-meeting-date> --agenda <path>
    python3 scripts/generate_briefs.py <upcoming-meeting-date> --persona PERSONA-001
    python3 scripts/generate_briefs.py <upcoming-meeting-date> --force

Exit codes:
    0 — all briefs succeeded (or dry-run completed)
    1 — one or more briefs failed
    2 — usage error (bad arguments, missing files, missing dependencies)
"""

import argparse
import concurrent.futures
import datetime
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.llm_client import call_llm, DEFAULT_MODEL as _DEFAULT_MODEL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("generate_briefs")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PERSONA_DIR = PROJECT_ROOT / "docs" / "persona" / "Active"
CUMULATIVE_DIR = PROJECT_ROOT / "data" / "interpretation" / "cumulative"
BUNDLES_DIR = PROJECT_ROOT / "data" / "interpretation" / "bundles"
INTER_MEETING_MANIFEST = (
    PROJECT_ROOT / "data" / "interpretation" / "inter-meeting" / "manifest.yaml"
)
BRIEFS_DIR = PROJECT_ROOT / "data" / "interpretation" / "briefs"

MODEL_ID = _DEFAULT_MODEL
GENERAL_PERSONA_ID = "PERSONA-000"
GENERAL_PERSONA_NAME = "General Community Member"
GENERAL_UPCOMING_FILE = "PERSONA-000-upcoming.md"
GENERAL_EVERGREEN_FILE = "PERSONA-000-evergreen.md"
GENERAL_SOURCE_BUNDLE_LIMIT = 3
PARALLEL_BATCH_SIZE = 3

# Per-source-type character limits for _truncate_text.
# Transcripts are much larger than other source types and need a higher ceiling
# to avoid silently clipping content (which causes the LLM to hallucinate that
# the source was incomplete).  Other types keep the conservative default.
SOURCE_CHAR_LIMITS = {
    "transcript": 500_000,   # ~125K tokens — full VTT with timestamps for a 5-hour meeting
}
DEFAULT_SOURCE_CHAR_LIMIT = 5_000

# Persona ID pattern
PERSONA_ID_RE = re.compile(r"^PERSONA-\d{3}$")
PERSONA_DIR_RE = re.compile(r"^\(PERSONA-(\d{3})\)-(.+)$")
MEETING_BUNDLE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-(school-board|city-council)$")


# ============================================================================
# Persona Loader (reused pattern from interpret_meeting.py)
# ============================================================================

class Persona:
    """A validated persona definition loaded from docs/persona/Validated/."""

    def __init__(self, persona_id, name, content, archetype=None):
        self.id = persona_id
        self.name = name
        self.content = content
        self.archetype = archetype

    def __repr__(self):
        return f"Persona({self.id}, {self.name})"


def build_general_audience_persona():
    """Return the synthetic broad-audience persona used for general briefs."""
    content = f"""\
# {GENERAL_PERSONA_NAME}

## Archetype Label
Broad Public Audience

## Core Orientation
This person wants a clear, accurate, plain-language understanding of the
school budget. They are not deeply embedded in district process and are not
approaching the issue from a specialized role. They want to know what is
changing, why it matters, what decisions are still open, and what the
practical impact could be for students, families, taxpayers, and the city.

## What They Care About
- What the total budget is and how it compares with prior proposals
- What major reductions, restorations, or tradeoffs are under discussion
- What decisions the board still needs to make
- What the likely impact is on schools, staffing, programs, and taxes
- What is confirmed versus still uncertain

## Information Needs
- Plain-language summary of the current budget picture
- Clear explanation of recent changes
- Upcoming decisions and timelines
- Major unresolved questions
- Specific items to watch in the next meeting

## Questions They Bring
- What changed since the last update?
- What are the biggest live decisions right now?
- What does this mean for the average resident or family?
- What should the public pay attention to next?
- Where can I verify the details myself?

## Tone And Framing
Use straightforward public-facing language. Avoid insider jargon. Prefer
synthesis over roleplay. Do not assume strong prior knowledge. Emphasize
confirmed facts, active decisions, and practical consequences.

## Reaction Audience
A neighbor, friend, or resident looking for a reliable summary
"""
    return Persona(
        persona_id=GENERAL_PERSONA_ID,
        name=GENERAL_PERSONA_NAME,
        content=content,
        archetype="Broad Public Audience",
    )


def load_personas(persona_dir=None):
    """Load all Validated persona definitions.

    Returns a list of Persona objects sorted by ID.
    """
    if persona_dir is None:
        persona_dir = PERSONA_DIR

    personas = []

    if not persona_dir.exists():
        log.error("Persona directory not found: %s", persona_dir)
        return personas

    for subdir in sorted(persona_dir.iterdir()):
        if not subdir.is_dir():
            continue

        dir_match = PERSONA_DIR_RE.match(subdir.name)
        if not dir_match:
            continue

        persona_num = dir_match.group(1)
        persona_id = f"PERSONA-{persona_num}"

        md_files = list(subdir.glob("*.md"))
        if not md_files:
            log.warning("No markdown file found in %s", subdir.name)
            continue

        md_path = md_files[0]
        content = md_path.read_text(encoding="utf-8")

        name = _extract_persona_name(content, persona_id)
        archetype = _extract_section(content, "Archetype Label")

        personas.append(Persona(
            persona_id=persona_id,
            name=name,
            content=content,
            archetype=archetype,
        ))

    log.info("Loaded %d persona(s) from %s", len(personas), persona_dir)
    return personas


def _extract_persona_name(content, persona_id):
    """Extract the first name from the H1 heading of a persona document."""
    h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if not h1_match:
        return persona_id
    heading = h1_match.group(1).strip()
    paren = heading.find("(")
    if paren > 0:
        return heading[:paren].strip()
    return heading


def _extract_section(content, section_title):
    """Extract the body text of a ## section from markdown content."""
    pattern = rf"^##\s+{re.escape(section_title)}\s*$"
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return None
    start = match.end()
    next_heading = re.search(r"^##\s+", content[start:], re.MULTILINE)
    if next_heading:
        section_text = content[start:start + next_heading.start()]
    else:
        section_text = content[start:]
    return section_text.strip()


def _extract_persona_body(content):
    """Extract persona content body (everything after frontmatter, before
    Lifecycle section)."""
    body = content.lstrip("\ufeff")
    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            body = body[end + 4:].strip()
    lifecycle_match = re.search(r"^##\s+Lifecycle\s*$", body, re.MULTILINE)
    if lifecycle_match:
        body = body[:lifecycle_match.start()].strip()
    return body


# ============================================================================
# Task 2: Agenda Loader with Fallback
# ============================================================================

def load_agenda(agenda_path=None, upcoming_date=None):
    """Load an agenda from a file path or try to find one in a bundle.

    Args:
        agenda_path: explicit path to an agenda file (from --agenda flag)
        upcoming_date: upcoming meeting date string for bundle lookup

    Returns:
        list of agenda item strings, or None if no agenda available
    """
    # Try explicit path first
    if agenda_path:
        path = Path(agenda_path)
        if not path.exists():
            log.warning("Agenda file not found: %s", path)
            return None
        return _parse_agenda_file(path)

    # Try to find agenda in a bundle manifest for the upcoming date
    if upcoming_date:
        bundles_dir = PROJECT_ROOT / "data" / "interpretation" / "bundles"
        if bundles_dir.exists():
            for bundle_dir in sorted(bundles_dir.iterdir()):
                if not bundle_dir.is_dir():
                    continue
                if bundle_dir.name.startswith(upcoming_date):
                    manifest_path = bundle_dir / "manifest.yaml"
                    if manifest_path.exists():
                        return _extract_agenda_from_bundle(manifest_path)

    log.info("No agenda available for %s", upcoming_date or "upcoming meeting")
    return None


def _parse_agenda_file(path):
    """Parse an agenda file into a list of agenda item strings.

    Handles numbered items (1. / 1) / I.) and bullet points (- / *).
    """
    text = Path(path).read_text(encoding="utf-8")
    return _parse_agenda_text(text)


def _parse_agenda_text(text):
    """Parse agenda text into a list of item strings.

    Recognizes:
    - Numbered items: "1. Item", "1) Item", "I. Item"
    - Bullet points: "- Item", "* Item"
    - Lines that look like agenda headers (all caps, short)
    """
    items = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        # Numbered items: 1. / 1) / I. / II.
        numbered = re.match(
            r"^(?:\d+[.)]\s+|[IVXLC]+[.)]\s+|[a-z][.)]\s+)(.+)$",
            line,
            re.IGNORECASE,
        )
        if numbered:
            items.append(numbered.group(1).strip())
            continue

        # Bullet points
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        if bullet:
            items.append(bullet.group(1).strip())
            continue

        # Lines that look like section headers (short, possibly capitalized)
        if len(line) < 100 and not line.startswith("#"):
            # Include non-empty lines as potential agenda items
            items.append(line)

    if items:
        log.info("Parsed %d agenda item(s)", len(items))
    return items if items else None


def _extract_agenda_from_bundle(manifest_path):
    """Try to extract agenda items from a bundle manifest.

    Looks for an agenda source file referenced in the bundle.
    """
    try:
        import yaml
    except ImportError:
        log.warning("PyYAML not available; cannot read bundle manifest")
        return None

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    if not manifest or not isinstance(manifest, dict):
        return None

    sources = manifest.get("sources", [])
    for src in sources:
        source_type = src.get("source_type", "")
        if source_type in ("agenda", "packet"):
            # Try normalized path first, then raw path
            for path_key in ("normalized_path", "path"):
                rel_path = src.get(path_key, "")
                if rel_path:
                    full_path = PROJECT_ROOT / rel_path
                    if full_path.exists() and full_path.suffix in (".md", ".txt"):
                        log.info("Found agenda in bundle: %s", full_path.name)
                        return _parse_agenda_file(full_path)

    return None


# ============================================================================
# Task 3: Inter-Meeting Evidence Loader
# ============================================================================

def load_inter_meeting_evidence(last_meeting_date, upcoming_date):
    """Load inter-meeting evidence events from the manifest.

    Filters entries by date range: after last_meeting_date, before
    upcoming_date.

    Args:
        last_meeting_date: ISO date string of the last folded meeting
                           (e.g., "2026-03-02"), or None
        upcoming_date: ISO date string of the upcoming meeting
                       (e.g., "2026-03-16")

    Returns:
        list of dicts with keys: entry_id, date_posted, source_type,
        title, description. Empty list if no entries match.
    """
    if not INTER_MEETING_MANIFEST.exists():
        log.info("Inter-meeting manifest not found: %s", INTER_MEETING_MANIFEST)
        return []

    try:
        import yaml
    except ImportError:
        log.warning("PyYAML not available; cannot read inter-meeting manifest")
        return []

    with open(INTER_MEETING_MANIFEST, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    if not manifest or not isinstance(manifest, dict):
        log.info("Inter-meeting manifest is empty or invalid")
        return []

    entries = manifest.get("entries", [])
    if not entries:
        log.info("No inter-meeting evidence entries in manifest")
        return []

    # Parse date boundaries
    try:
        upcoming_dt = datetime.date.fromisoformat(upcoming_date)
    except ValueError:
        log.error("Invalid upcoming date: %s", upcoming_date)
        return []

    if last_meeting_date:
        try:
            last_dt = datetime.date.fromisoformat(last_meeting_date)
        except ValueError:
            log.warning("Invalid last meeting date: %s — using all entries",
                        last_meeting_date)
            last_dt = None
    else:
        last_dt = None

    matching = []
    for entry in entries:
        date_posted = entry.get("date_posted", "")
        if not date_posted:
            continue

        try:
            posted_dt = datetime.date.fromisoformat(str(date_posted))
        except ValueError:
            continue

        # Filter: after last meeting, before upcoming meeting
        if last_dt and posted_dt <= last_dt:
            continue
        if posted_dt >= upcoming_dt:
            continue

        matching.append({
            "entry_id": entry.get("entry_id", "unknown"),
            "date_posted": str(date_posted),
            "source_type": entry.get("source_type", "unknown"),
            "title": entry.get("title", ""),
            "description": entry.get("description", "").strip(),
            "source_path": entry.get("source_path", ""),
            "normalized_path": entry.get("normalized_path", ""),
        })

    log.info("Found %d inter-meeting evidence event(s) in date range", len(matching))
    return matching


def _load_yaml(path):
    try:
        import yaml
    except ImportError:
        log.warning("PyYAML not available; cannot read %s", path)
        return None

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _truncate_text(text, max_chars=None, source_type=None):
    if max_chars is None:
        max_chars = SOURCE_CHAR_LIMITS.get(source_type, DEFAULT_SOURCE_CHAR_LIMIT)
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n\n[truncated]"


def _read_markdownish_source(rel_path):
    if not rel_path:
        return None

    full_path = PROJECT_ROOT / rel_path
    if not full_path.exists() or full_path.suffix not in (".md", ".txt", ".vtt"):
        return None

    return full_path.read_text(encoding="utf-8")


def _load_bundle_source_context(upcoming_date, limit=GENERAL_SOURCE_BUNDLE_LIMIT):
    """Load recent readable bundle sources for direct-evidence general briefs."""
    manifests = []
    if not BUNDLES_DIR.exists():
        return "No recent meeting bundle sources available."

    for bundle_dir in sorted(BUNDLES_DIR.iterdir(), reverse=True):
        if not bundle_dir.is_dir() or not MEETING_BUNDLE_RE.match(bundle_dir.name):
            continue

        meeting_date = bundle_dir.name[:10]
        if meeting_date >= upcoming_date:
            continue

        manifest_path = bundle_dir / "manifest.yaml"
        if manifest_path.exists():
            manifests.append(manifest_path)
        if len(manifests) >= limit:
            break

    blocks = []
    for manifest_path in manifests:
        manifest = _load_yaml(manifest_path)
        if not isinstance(manifest, dict):
            continue

        meeting_title = manifest.get("title", manifest_path.parent.name)
        meeting_date = manifest.get("meeting_date", manifest_path.parent.name[:10])

        for source in manifest.get("sources", []):
            content = None
            for key in ("normalized_path", "path"):
                content = _read_markdownish_source(source.get(key, ""))
                if content:
                    break

            if not content:
                continue

            source_title = source.get("title", "Untitled source")
            source_type = source.get("source_type", "unknown")
            blocks.append(
                f"--- Meeting: {meeting_title} ({meeting_date}) / "
                f"Source: {source_title} [{source_type}] ---\n\n"
                f"{_truncate_text(_strip_frontmatter(content), source_type=source_type)}"
            )

    if not blocks:
        return "No readable recent meeting bundle sources available."
    return "\n\n".join(blocks)


def _load_inter_meeting_source_context(inter_meeting_events):
    """Load readable inter-meeting source text for direct-evidence prompts."""
    blocks = []
    for event in inter_meeting_events:
        content = None
        for key in ("normalized_path", "source_path"):
            content = _read_markdownish_source(event.get(key, ""))
            if content:
                break

        if not content:
            continue

        title = event.get("title") or event.get("entry_id", "Untitled source")
        source_type = event.get("source_type", "unknown")
        blocks.append(
            f"--- Inter-meeting source: {title} "
            f"({event.get('date_posted', 'unknown date')}, {source_type}) ---\n\n"
            f"{_truncate_text(_strip_frontmatter(content), source_type=source_type)}"
        )

    if not blocks:
        return "No readable inter-meeting source text available."
    return "\n\n".join(blocks)


# ============================================================================
# Cumulative State Loader
# ============================================================================

def load_cumulative_state(persona_id):
    """Load cumulative interpretation state for a persona.

    Prefers summary.md if it exists; falls back to the latest
    individual record(s).

    Returns:
        dict with keys:
            has_cumulative: bool
            summary_text: str or None (full summary.md content)
            latest_records: list of str (record contents, newest first)
            last_meeting_date: str or None (most recent meeting date)
            open_threads: list of str (extracted from summary)
            active_supersessions: str or None (supersession table text)
    """
    persona_dir = CUMULATIVE_DIR / persona_id

    result = {
        "has_cumulative": False,
        "summary_text": None,
        "latest_records": [],
        "last_meeting_date": None,
        "open_threads": [],
        "active_supersessions": None,
    }

    if not persona_dir.exists():
        return result

    # Check for summary
    summary_path = persona_dir / "summary.md"
    if summary_path.exists():
        summary_text = summary_path.read_text(encoding="utf-8")
        result["has_cumulative"] = True
        result["summary_text"] = summary_text

        # Extract last_meeting_date from frontmatter
        fm_match = re.search(
            r"last_meeting_date:\s*\"?(\d{4}-\d{2}-\d{2})\"?",
            summary_text,
        )
        if fm_match:
            result["last_meeting_date"] = fm_match.group(1)

        # Extract open threads
        threads_section = _extract_section(summary_text, "Open Threads")
        if threads_section:
            result["open_threads"] = [
                line.lstrip("- ").strip()
                for line in threads_section.splitlines()
                if line.strip().startswith("-")
            ]

        # Extract active supersessions
        supersessions = _extract_section(summary_text, "Active Supersessions")
        if supersessions:
            result["active_supersessions"] = supersessions

        return result

    # No summary — fall back to individual records (newest first)
    record_files = sorted(
        [f for f in persona_dir.glob("*.md") if f.name != "summary.md"],
        reverse=True,
    )

    if record_files:
        result["has_cumulative"] = True
        result["last_meeting_date"] = record_files[0].stem  # e.g., "2026-03-02"

        # Load up to 3 most recent records
        for record_file in record_files[:3]:
            result["latest_records"].append(
                record_file.read_text(encoding="utf-8")
            )

    return result


# ============================================================================
# Task 1: Brief Prompt Template
# ============================================================================

BRIEF_SYSTEM_PROMPT = """\
You are a forward-looking brief generator for a municipal school budget \
analysis project. Your job is to prepare a specific community persona for \
an upcoming meeting by synthesizing their cumulative understanding, any \
new inter-meeting evidence, and the meeting agenda (if available) into \
an actionable brief.

Your output must be grounded in the cumulative state and evidence provided. \
Do not invent facts, quotes, or events. Your value-add is FORWARD-LOOKING: \
what should this persona pay attention to, ask about, or watch for at the \
upcoming meeting.

Editorial guidelines:
- Your tone should be that of a careful, fair-minded researcher — not an \
adversary or advocate. Document what is known and not known with precision.
- Distinguish clearly between "not yet provided" and "withheld." A gap \
between meetings is a gap, not evidence of intent. Administrative processes \
take time; do not frame normal timelines as suspicious or sinister.
- Do not editorialize about the significance of silence, absence, or delay \
unless the evidence specifically supports a pattern of non-response to a \
direct question asked on the record. Even then, state the factual pattern \
and let the reader draw conclusions.
- The project's credibility depends on restraint. Every claim of \
concealment, evasion, or bad faith that cannot be directly sourced to \
evidence undermines the entire analysis.

Critical instruction: Your brief must be DISTINCT to this persona. Different \
personas should focus on different agenda items, carry different concerns, \
and prepare different questions. If your brief could belong to any persona, \
you have failed."""

GENERAL_UPCOMING_SYSTEM_PROMPT = """\
You are a public briefing generator for a municipal school budget analysis
project. Your job is to prepare a broad, plain-language briefing for the next
upcoming meeting using direct evidence only: recent source documents,
inter-meeting evidence, and the agenda if available.

Write for an interested resident who wants clarity, not insider jargon.
Ground every substantive claim in the evidence provided. Do not invent facts,
quotes, or certainty where the sources are unresolved.

Maintain a fair, researcher tone. Distinguish "not yet provided" from
"withheld." Do not editorialize about gaps between meetings or frame normal
administrative timelines as suspicious."""

GENERAL_EVERGREEN_SYSTEM_PROMPT = """\
You are a public budget explainer for a municipal school budget analysis
project. Your job is to summarize the current state of the budget for a broad
audience using direct evidence only: recent meeting source documents and
inter-meeting evidence.

Write in plain language. Distinguish confirmed facts from unresolved issues.
Do not frame the output as a persona reaction or roleplay. Do not invent
facts, quotes, or certainty beyond the provided evidence.

Maintain a fair, researcher tone. Note what is known, what is pending, and
what has been asked but not answered — without editorializing about motives
or framing normal administrative processes as evasion."""


def build_brief_prompt(persona, cumulative_state, inter_meeting_events,
                       agenda_items, upcoming_date):
    """Construct the prompt for generating a single persona's brief.

    Args:
        persona: Persona object
        cumulative_state: dict from load_cumulative_state()
        inter_meeting_events: list from load_inter_meeting_evidence()
        agenda_items: list of agenda item strings, or None
        upcoming_date: ISO date string for the upcoming meeting

    Returns:
        str: The assembled user prompt.
    """
    persona_body = _extract_persona_body(persona.content)

    # Build cumulative context block
    if cumulative_state["summary_text"]:
        cumulative_block = _strip_frontmatter(cumulative_state["summary_text"])
    elif cumulative_state["latest_records"]:
        cumulative_block = "\n\n---\n\n".join(
            _strip_frontmatter(r) for r in cumulative_state["latest_records"]
        )
    else:
        cumulative_block = (
            "No cumulative interpretation records exist for this persona yet. "
            "This is a baseline brief generated from the persona definition "
            "alone. The persona has not yet processed any meetings."
        )

    # Build inter-meeting evidence block
    if inter_meeting_events:
        evidence_lines = []
        for evt in inter_meeting_events:
            title = evt.get("title") or evt.get("entry_id", "")
            evidence_lines.append(
                f"- **{title}** ({evt['date_posted']}, {evt['source_type']}): "
                f"{evt['description']}"
            )
        evidence_block = "\n".join(evidence_lines)
    else:
        evidence_block = "No inter-meeting evidence events in this period."

    # Build agenda block
    if agenda_items:
        agenda_block = "\n".join(f"- {item}" for item in agenda_items)
        agenda_instruction = (
            "An agenda is available for this meeting. For each agenda item, "
            "explain what it means to this persona and what they should pay "
            "attention to."
        )
    else:
        agenda_block = "Agenda not yet available."
        agenda_instruction = (
            "No agenda is available for this meeting. In the agenda_implications "
            "section, note that the agenda is not yet available and provide "
            "general guidance based on the persona's cumulative state and "
            "open questions — what topics are likely to come up, and what "
            "this persona should be prepared for."
        )

    # Build supersession watch block
    supersession_instruction = ""
    if cumulative_state["active_supersessions"]:
        supersession_instruction = (
            "\n\nIMPORTANT: This persona has positions that have been "
            "superseded during the budget season (see active supersessions "
            "in the cumulative state below). In the watch_for section, "
            "include specific items about what to watch for regarding "
            "these shifts — are the new positions being confirmed, "
            "further revised, or challenged?"
        )

    prompt = f"""\
<persona>
{persona_body}
</persona>

<cumulative_state>
{cumulative_block}
</cumulative_state>

<inter_meeting_evidence>
{evidence_block}
</inter_meeting_evidence>

<upcoming_agenda>
{agenda_block}
</upcoming_agenda>

<instruction>
Prepare a forward-looking brief for {persona.name} ({persona.id}) ahead \
of the upcoming meeting on {upcoming_date}.

{agenda_instruction}{supersession_instruction}

Produce a brief with EXACTLY these four sections, using the markdown headers \
shown. Write in a clear, direct style appropriate for someone preparing for \
a meeting — not academic, not casual.

## Since Last Meeting

Summarize new developments since the last meeting this persona processed. \
Include any inter-meeting evidence events and explain their significance \
through this persona's lens. If no new evidence exists, state that briefly \
and move on — do not speculate about the meaning of a gap between meetings.

## Open Questions

List the open questions and unresolved threads this persona is carrying into \
the upcoming meeting. Draw from the cumulative state's open threads and add \
any new questions raised by inter-meeting evidence. Write these as a bulleted \
list in the persona's voice — the way they would actually phrase these \
concerns, not in analyst language.

## Agenda Implications

{agenda_instruction}

For each item (or for the general meeting outlook if no agenda), explain:
- What this means for this persona specifically
- What they should listen for
- What questions they should prepare

## Watch For

List specific, actionable things this persona should watch for, listen for, \
or be prepared to ask about at the upcoming meeting. Include:
- Signs that open questions may be addressed
- Any superseded positions that could be revisited or further revised
- Body language, tone, or procedural signals that matter to this persona
- Specific people or roles whose statements this persona should track

Write these as a bulleted list of concrete, specific items — not vague \
generalities like "pay attention to the budget." Each item should be \
something this persona could actually act on during the meeting.
</instruction>"""

    return prompt


def build_general_upcoming_prompt(general_persona, source_context,
                                  inter_meeting_events, inter_meeting_context,
                                  agenda_items, upcoming_date):
    """Construct the general upcoming-meeting prompt."""
    persona_body = _extract_persona_body(general_persona.content)

    if inter_meeting_events:
        event_lines = [
            f"- **{evt.get('title') or evt.get('entry_id', '')}** "
            f"({evt['date_posted']}, {evt['source_type']}): "
            f"{evt['description']}"
            for evt in inter_meeting_events
        ]
        inter_meeting_block = "\n".join(event_lines)
    else:
        inter_meeting_block = "No inter-meeting evidence events in this period."

    if agenda_items:
        agenda_block = "\n".join(f"- {item}" for item in agenda_items)
        agenda_instruction = (
            "Use the agenda to explain what this meeting appears designed to "
            "do and which decisions are most likely to be advanced tonight."
        )
    else:
        agenda_block = "Agenda not yet available."
        agenda_instruction = (
            "No agenda is available. Explain what the public should watch for "
            "based on the latest direct evidence and note where uncertainty "
            "remains because the agenda has not yet been posted."
        )

    return f"""\
<audience_card>
{persona_body}
</audience_card>

<recent_bundle_sources>
{source_context}
</recent_bundle_sources>

<inter_meeting_evidence_summary>
{inter_meeting_block}
</inter_meeting_evidence_summary>

<inter_meeting_source_text>
{inter_meeting_context}
</inter_meeting_source_text>

<upcoming_agenda>
{agenda_block}
</upcoming_agenda>

<instruction>
Prepare a broad public briefing for the upcoming meeting on {upcoming_date}.
{agenda_instruction}

Produce a brief with EXACTLY these five sections, using the markdown headers
shown.

## Since Last Meeting

Summarize what changed since the latest meeting sources included here.
Highlight concrete updates from inter-meeting evidence and direct documents.

## What This Meeting Is For

Explain, in plain language, what this meeting appears intended to do.

## Decisions Likely Tonight

List the major decisions, votes, or directional calls that seem most likely
to be advanced, refined, or clarified at this meeting.

## Key Public Questions

Write a bulleted list of the biggest questions an informed resident would
still have walking into the meeting.

## What To Watch For

Write a bulleted list of concrete things the public should listen for,
including decision points, clarifications, conflicts, caveats, or signs that
the proposal is shifting.
</instruction>"""


def build_general_evergreen_prompt(general_persona, source_context,
                                   inter_meeting_events, inter_meeting_context,
                                   upcoming_date):
    """Construct the evergreen general public explainer prompt."""
    persona_body = _extract_persona_body(general_persona.content)

    if inter_meeting_events:
        event_lines = [
            f"- **{evt.get('title') or evt.get('entry_id', '')}** "
            f"({evt['date_posted']}, {evt['source_type']}): "
            f"{evt['description']}"
            for evt in inter_meeting_events
        ]
        inter_meeting_block = "\n".join(event_lines)
    else:
        inter_meeting_block = "No inter-meeting evidence events in this period."

    return f"""\
<audience_card>
{persona_body}
</audience_card>

<recent_bundle_sources>
{source_context}
</recent_bundle_sources>

<inter_meeting_evidence_summary>
{inter_meeting_block}
</inter_meeting_evidence_summary>

<inter_meeting_source_text>
{inter_meeting_context}
</inter_meeting_source_text>

<instruction>
Prepare an evergreen public explainer of the current budget picture as of
{upcoming_date}. This is not a meeting-prep brief; it is a current-state
summary for a broad audience.

Produce a brief with EXACTLY these five sections, using the markdown headers
shown.

## Budget Snapshot

Summarize the current proposal in plain language: what stage the budget is
in, the biggest live components, and the clearest headline facts supported by
the sources.

## What Changed

Explain the most important recent changes or clarifications reflected in the
evidence.

## Major Decisions Ahead

Identify the biggest unresolved decisions still in front of the board or city.

## Open Questions

Write a bulleted list of the main questions that remain unresolved based on
the evidence provided.

## Where To Verify

Write a bulleted list of the most useful source materials or source types a
reader should consult to verify details.
</instruction>"""


def _strip_frontmatter(text):
    """Strip YAML frontmatter from a markdown document."""
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return text.strip()
    end = text.find("\n---", 3)
    if end == -1:
        return text.strip()
    return text[end + 4:].strip()


# ============================================================================
# Task 4: Generator Script
# ============================================================================

def format_brief_output(persona, upcoming_date, has_agenda, response_text,
                        cumulative_state, inter_meeting_count):
    """Wrap LLM response in schema-conformant frontmatter + body."""
    today = datetime.date.today().isoformat()
    last_meeting = cumulative_state.get("last_meeting_date") or "null"
    if last_meeting != "null":
        last_meeting = f'"{last_meeting}"'

    frontmatter = f"""\
---
schema_version: "1.0"
persona_id: "{persona.id}"
persona_name: "{persona.name}"
upcoming_meeting_date: "{upcoming_date}"
generated_date: "{today}"
has_agenda: {"true" if has_agenda else "false"}
last_cumulative_meeting: {last_meeting}
inter_meeting_evidence_count: {inter_meeting_count}
---"""

    # Clean up the response — ensure it starts with the first section header
    body = response_text.strip()

    return f"{frontmatter}\n\n# Brief: {persona.name} ({persona.id})\n## Upcoming Meeting: {upcoming_date}\n\n{body}\n"


def format_general_brief_output(mode, response_text, *, has_agenda,
                                upcoming_date=None,
                                inter_meeting_count=0):
    """Wrap a general brief in non-persona frontmatter."""
    today = datetime.date.today().isoformat()
    frontmatter_lines = [
        "---",
        'schema_version: "1.0"',
        'brief_type: "general"',
        f'brief_mode: "{mode}"',
        f'generated_date: "{today}"',
        f'has_agenda: {"true" if has_agenda else "false"}',
        f"inter_meeting_evidence_count: {inter_meeting_count}",
    ]
    if upcoming_date:
        frontmatter_lines.append(f'upcoming_meeting_date: "{upcoming_date}"')
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)

    title = (
        "General Upcoming Briefing"
        if mode == "upcoming"
        else "General Budget Briefing"
    )
    subtitle = (
        f"## Upcoming Meeting: {upcoming_date}"
        if upcoming_date and mode == "upcoming"
        else "## Current Budget Picture"
    )
    body = response_text.strip()
    return f"{frontmatter}\n\n# {title}\n{subtitle}\n\n{body}\n"


def run_briefs(upcoming_date, personas, *, agenda_items=None, force=False,
               single_persona=None, dry_run=False):
    """Generate persona and general public briefs for an upcoming meeting.

    Args:
        upcoming_date: ISO date string for the upcoming meeting
        personas: list of Persona objects
        agenda_items: list of agenda item strings, or None
        force: if True, overwrite existing briefs
        single_persona: if set, only process this PERSONA-NNN
        dry_run: if True, do everything except the LLM call

    Returns:
        dict with counts: processed, skipped, failed,
                          with_cumulative, without_cumulative, general_processed
    """
    output_dir = BRIEFS_DIR / upcoming_date
    output_dir.mkdir(parents=True, exist_ok=True)

    include_general = single_persona is None or single_persona == GENERAL_PERSONA_ID
    if single_persona:
        if single_persona != GENERAL_PERSONA_ID:
            personas = [p for p in personas if p.id == single_persona]
        else:
            personas = []

        if not personas and not include_general:
            log.error("Persona %s not found in loaded personas", single_persona)
            return {"processed": 0, "skipped": 0, "failed": 1,
                    "with_cumulative": 0, "without_cumulative": 0,
                    "general_processed": 0}

    stats = {
        "processed": 0,
        "skipped": 0,
        "failed": 0,
        "with_cumulative": 0,
        "without_cumulative": 0,
        "general_processed": 0,
    }

    # Load inter-meeting evidence once (shared across all personas)
    # We need the last meeting date to filter — use the most recent cumulative
    # record across all personas as the baseline
    all_last_dates = []
    cumulative_states = {}

    for persona in personas:
        cs = load_cumulative_state(persona.id)
        cumulative_states[persona.id] = cs
        if cs["last_meeting_date"]:
            all_last_dates.append(cs["last_meeting_date"])

    # Use the most recent last_meeting_date across all personas
    global_last_date = max(all_last_dates) if all_last_dates else None
    inter_meeting_events = load_inter_meeting_evidence(
        global_last_date, upcoming_date
    )
    general_persona = build_general_audience_persona()
    general_source_context = _load_bundle_source_context(upcoming_date)
    inter_meeting_source_context = _load_inter_meeting_source_context(
        inter_meeting_events
    )

    def _generate_persona_brief(persona):
        """Generate a single persona brief. Returns (status, persona.id)."""
        output_path = output_dir / f"{persona.id}.md"
        cumulative_state = cumulative_states[persona.id]

        has_cum = cumulative_state["has_cumulative"]

        if output_path.exists() and not force:
            log.info("  [skip] %s — brief already exists: %s",
                     persona.id, output_path.name)
            return ("skipped", persona.id, has_cum)

        if output_path.exists() and force:
            log.info("  [force] %s — regenerating (existing brief will be "
                     "overwritten)", persona.id)

        prompt = build_brief_prompt(
            persona,
            cumulative_state,
            inter_meeting_events,
            agenda_items,
            upcoming_date,
        )
        prompt_tokens = estimate_tokens(BRIEF_SYSTEM_PROMPT + prompt)

        cumulative_label = (
            f"cumulative through {cumulative_state['last_meeting_date']}"
            if has_cum else "no cumulative (baseline)"
        )
        log.info("  [prompt] %s (%s) — ~%d tokens, %s",
                 persona.id, persona.name, prompt_tokens, cumulative_label)

        if dry_run:
            log.info("  [dry-run] %s — would call LLM (%s), write to %s",
                     persona.id, MODEL_ID, output_path.name)
            return ("processed", persona.id, has_cum)

        try:
            log.info("  [call] %s — calling %s ...", persona.id, MODEL_ID)
            output_text = call_llm(
                prompt, system_prompt=BRIEF_SYSTEM_PROMPT, model=MODEL_ID
            )

            if not output_text.strip():
                log.error("  [fail] %s — empty response from LLM", persona.id)
                return ("failed", persona.id, has_cum)

            validation_errors = _validate_brief(output_text)
            if validation_errors:
                log.warning("  [warn] %s — %d validation issue(s):",
                            persona.id, len(validation_errors))
                for err in validation_errors:
                    log.warning("    %s", err)

            has_agenda = agenda_items is not None
            formatted = format_brief_output(
                persona, upcoming_date, has_agenda, output_text,
                cumulative_state, len(inter_meeting_events),
            )

            output_path.write_text(formatted, encoding="utf-8")
            log.info("  [done] %s — wrote %s (%d chars)",
                     persona.id, output_path.name, len(formatted))
            return ("processed", persona.id, has_cum)

        except Exception as e:
            log.error("  [fail] %s — LLM call failed: %s", persona.id, e)
            return ("failed", persona.id, has_cum)

    # Run persona briefs in parallel batches
    total_persona = len(personas)
    completed_persona = 0
    if total_persona:
        log.info("  [batch] starting %d persona briefs (%d parallel)",
                 total_persona, PARALLEL_BATCH_SIZE)
    with concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_BATCH_SIZE) as pool:
        futures = {pool.submit(_generate_persona_brief, p): p for p in personas}
        for future in concurrent.futures.as_completed(futures):
            status, pid, has_cum = future.result()
            if has_cum:
                stats["with_cumulative"] += 1
            else:
                stats["without_cumulative"] += 1
            stats[status] += 1
            completed_persona += 1
            log.info("  [progress] persona %d/%d complete (%s — %s)",
                     completed_persona, total_persona, pid, status)

    if include_general:
        general_specs = [
            {
                "mode": "upcoming",
                "filename": GENERAL_UPCOMING_FILE,
                "system_prompt": GENERAL_UPCOMING_SYSTEM_PROMPT,
                "prompt": build_general_upcoming_prompt(
                    general_persona,
                    general_source_context,
                    inter_meeting_events,
                    inter_meeting_source_context,
                    agenda_items,
                    upcoming_date,
                ),
                "validator": _validate_general_upcoming_brief,
                "has_agenda": agenda_items is not None,
                "title": "general upcoming",
            },
            {
                "mode": "evergreen",
                "filename": GENERAL_EVERGREEN_FILE,
                "system_prompt": GENERAL_EVERGREEN_SYSTEM_PROMPT,
                "prompt": build_general_evergreen_prompt(
                    general_persona,
                    general_source_context,
                    inter_meeting_events,
                    inter_meeting_source_context,
                    upcoming_date,
                ),
                "validator": _validate_general_evergreen_brief,
                "has_agenda": False,
                "title": "general evergreen",
            },
        ]

        def _generate_general_brief(spec):
            """Generate a single general brief. Returns status string."""
            output_path = output_dir / spec["filename"]
            prompt_tokens = estimate_tokens(spec["system_prompt"] + spec["prompt"])

            if output_path.exists() and not force:
                log.info("  [skip] %s — brief already exists: %s",
                         spec["title"], output_path.name)
                return "skipped"

            if output_path.exists() and force:
                log.info("  [force] %s — regenerating (existing brief will be "
                         "overwritten)", spec["title"])

            log.info("  [prompt] %s — ~%d tokens", spec["title"], prompt_tokens)

            if dry_run:
                log.info("  [dry-run] %s — would call LLM (%s), write to %s",
                         spec["title"], MODEL_ID, output_path.name)
                return "processed"

            try:
                log.info("  [call] %s — calling %s ...", spec["title"], MODEL_ID)
                output_text = call_llm(
                    spec["prompt"],
                    system_prompt=spec["system_prompt"],
                    model=MODEL_ID,
                )

                if not output_text.strip():
                    log.error("  [fail] %s — empty response from LLM", spec["title"])
                    return "failed"

                validation_errors = spec["validator"](output_text)
                if validation_errors:
                    log.warning("  [warn] %s — %d validation issue(s):",
                                spec["title"], len(validation_errors))
                    for err in validation_errors:
                        log.warning("    %s", err)

                formatted = format_general_brief_output(
                    spec["mode"],
                    output_text,
                    has_agenda=spec["has_agenda"],
                    upcoming_date=upcoming_date if spec["mode"] == "upcoming" else None,
                    inter_meeting_count=len(inter_meeting_events),
                )

                output_path.write_text(formatted, encoding="utf-8")
                log.info("  [done] %s — wrote %s (%d chars)",
                         spec["title"], output_path.name, len(formatted))
                return "processed"

            except Exception as e:
                log.error("  [fail] %s — LLM call failed: %s", spec["title"], e)
                return "failed"

        # General briefs run in parallel too (only 2, but uses same pool pattern)
        total_general = len(general_specs)
        completed_general = 0
        log.info("  [batch] starting %d general briefs (%d parallel)",
                 total_general, PARALLEL_BATCH_SIZE)
        with concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_BATCH_SIZE) as pool:
            futures = {pool.submit(_generate_general_brief, s): s for s in general_specs}
            for future in concurrent.futures.as_completed(futures):
                status = future.result()
                stats[status] += 1
                if status == "processed":
                    stats["general_processed"] += 1
                completed_general += 1
                spec = futures[future]
                log.info("  [progress] general %d/%d complete (%s — %s)",
                         completed_general, total_general, spec["title"], status)

    return stats


def _validate_brief(text):
    """Quick structural validation of brief LLM output.

    Checks for the four required sections.
    Returns list of error strings (empty = looks good).
    """
    errors = []

    if "## Since Last Meeting" not in text:
        errors.append("missing '## Since Last Meeting' section")
    if "## Open Questions" not in text:
        errors.append("missing '## Open Questions' section")
    if "## Agenda Implications" not in text:
        errors.append("missing '## Agenda Implications' section")
    if "## Watch For" not in text:
        errors.append("missing '## Watch For' section")

    return errors


def _validate_general_upcoming_brief(text):
    errors = []
    required_sections = (
        "## Since Last Meeting",
        "## What This Meeting Is For",
        "## Decisions Likely Tonight",
        "## Key Public Questions",
        "## What To Watch For",
    )
    for section in required_sections:
        if section not in text:
            errors.append(f"missing '{section}' section")
    return errors


def _validate_general_evergreen_brief(text):
    errors = []
    required_sections = (
        "## Budget Snapshot",
        "## What Changed",
        "## Major Decisions Ahead",
        "## Open Questions",
        "## Where To Verify",
    )
    for section in required_sections:
        if section not in text:
            errors.append(f"missing '{section}' section")
    return errors


def estimate_tokens(text):
    """Rough token estimate: ~4 chars per token for English text."""
    return len(text) // 4


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Public Brief Generator"
    )
    parser.add_argument(
        "upcoming_meeting_date",
        help="Date of the upcoming meeting in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--agenda",
        help="Path to an agenda file (numbered list or bullet points)",
    )
    parser.add_argument(
        "--persona",
        help="Generate brief for only this persona (e.g., PERSONA-001)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help=(
            "Do everything except the LLM call: load data, build prompts, "
            "report what would happen"
        ),
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing briefs",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate date format
    try:
        datetime.date.fromisoformat(args.upcoming_meeting_date)
    except ValueError:
        log.error(
            "Invalid date format: '%s' — expected YYYY-MM-DD",
            args.upcoming_meeting_date,
        )
        sys.exit(2)

    # Validate --persona format
    if args.persona and not PERSONA_ID_RE.match(args.persona):
        log.error(
            "Invalid persona ID: '%s' — expected format PERSONA-NNN "
            "(e.g., PERSONA-001)",
            args.persona,
        )
        sys.exit(2)

    log.info("=== Public Brief Generator ===")
    log.info("Upcoming meeting: %s", args.upcoming_meeting_date)
    if args.dry_run:
        log.info("Mode: DRY RUN (no LLM calls will be made)")

    # Step 1: Load personas
    log.info("--- Loading personas ---")
    personas = load_personas()
    if not personas and args.persona != GENERAL_PERSONA_ID:
        log.error("No personas found. Check %s", PERSONA_DIR)
        sys.exit(2)

    # Step 2: Load agenda
    log.info("--- Loading agenda ---")
    agenda_items = load_agenda(
        agenda_path=args.agenda,
        upcoming_date=args.upcoming_meeting_date,
    )
    has_agenda = agenda_items is not None
    if has_agenda:
        log.info("Agenda: %d item(s) loaded", len(agenda_items))
    else:
        log.info("Agenda: not available (briefs will note this)")

    # Step 3: Generate briefs
    log.info("--- Generating briefs ---")
    log.info("Personas: %d", len(personas))
    if args.persona:
        log.info("Filter: %s only", args.persona)
    if args.force:
        log.info("Force: overwriting existing briefs")

    stats = run_briefs(
        args.upcoming_meeting_date,
        personas,
        agenda_items=agenda_items,
        force=args.force,
        single_persona=args.persona,
        dry_run=args.dry_run,
    )

    # Summary
    log.info("")
    log.info("=== Summary ===")
    log.info("Processed:         %d", stats["processed"])
    log.info("Skipped:           %d", stats["skipped"])
    log.info("Failed:            %d", stats["failed"])
    log.info("With cumulative:   %d", stats["with_cumulative"])
    log.info("Without cumulative:%d (baseline briefs)",
             stats["without_cumulative"])
    log.info("General briefs:    %d", stats["general_processed"])

    total = stats["processed"] + stats["skipped"] + stats["failed"]
    log.info("Total:             %d brief artifact(s)", total)

    log.info("")
    log.info("Agenda available:  %s", "yes" if has_agenda else "no")

    if args.dry_run:
        # In dry-run, show what inter-meeting evidence was found
        # (already logged during run_briefs, but summarize here)
        log.info("")
        log.info("--- Dry-run details ---")
        log.info("Personas with cumulative data: %d", stats["with_cumulative"])
        log.info("Personas without cumulative data: %d (would get baseline briefs)",
                 stats["without_cumulative"])

        # Estimate total token usage (load evidence once to avoid log noise)
        total_prompt_tokens = 0
        target_personas = personas
        if args.persona and args.persona != GENERAL_PERSONA_ID:
            target_personas = [p for p in personas if p.id == args.persona]

        all_last = [load_cumulative_state(p.id)["last_meeting_date"]
                    for p in personas]
        all_last = [d for d in all_last if d]
        global_last = max(all_last) if all_last else None
        evidence = load_inter_meeting_evidence(
            global_last, args.upcoming_meeting_date
        )
        log.info("Inter-meeting evidence events: %d", len(evidence))

        for persona in target_personas:
            cs = load_cumulative_state(persona.id)
            prompt = build_brief_prompt(
                persona, cs, evidence, agenda_items,
                args.upcoming_meeting_date,
            )
            total_prompt_tokens += estimate_tokens(BRIEF_SYSTEM_PROMPT + prompt)
        if not args.persona or args.persona == GENERAL_PERSONA_ID:
            general_persona = build_general_audience_persona()
            general_source_context = _load_bundle_source_context(
                args.upcoming_meeting_date
            )
            inter_meeting_source_context = _load_inter_meeting_source_context(
                evidence
            )
            total_prompt_tokens += estimate_tokens(
                GENERAL_UPCOMING_SYSTEM_PROMPT
                + build_general_upcoming_prompt(
                    general_persona,
                    general_source_context,
                    evidence,
                    inter_meeting_source_context,
                    agenda_items,
                    args.upcoming_meeting_date,
                )
            )
            total_prompt_tokens += estimate_tokens(
                GENERAL_EVERGREEN_SYSTEM_PROMPT
                + build_general_evergreen_prompt(
                    general_persona,
                    general_source_context,
                    evidence,
                    inter_meeting_source_context,
                    args.upcoming_meeting_date,
                )
            )
        log.info("Estimated total input tokens: ~%d", total_prompt_tokens)
        log.info("Estimated cost at $3/MTok input: ~$%.2f",
                 total_prompt_tokens * 3.0 / 1_000_000)

    output_dir = BRIEFS_DIR / args.upcoming_meeting_date
    log.info("")
    log.info("Output directory: %s", output_dir)

    if stats["failed"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
