#!/usr/bin/env python3
"""Validate cumulative interpretation records and summary views.

Checks for cumulative records:
  - YAML frontmatter has required fields (schema_version, persona_id,
    meeting_date, meeting_type, body, prior_meeting, interpretation_date)
  - All three body sections exist (Interpretation, Deltas, Emotional Register)
  - Delta category values are from the allowed enum
  - Interpretation section word count is within range (~200-400 words,
    with soft warning outside 150-500)
  - Prior_meeting is null for first record, valid date otherwise
  - Frontmatter date formats are ISO 8601

Checks for summary views:
  - YAML frontmatter has required fields (schema_version, persona_id,
    last_meeting_date, record_count, generated_date)
  - All five body sections exist (Current Understanding, Timeline,
    Active Supersessions, Open Threads, Resolved Threads)
  - Current Understanding word count is within range (~150-300 words)

Usage:
    python3 scripts/validate_cumulative.py <record.md>
    python3 scripts/validate_cumulative.py --summary <summary.md>
    python3 scripts/validate_cumulative.py --all
    python3 scripts/validate_cumulative.py --summary --all

Exit codes:
    0 -- valid
    1 -- validation errors found
    2 -- usage error (bad arguments, file not found)
"""

import argparse
import datetime
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("validate_cumulative")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# --- Schema constants ---

VALID_MEETING_TYPES = {
    "regular", "workshop", "special",
    "budget-forum", "budget-workshop", "joint",
}

VALID_BODIES = {"school-board", "city-council"}

VALID_DELTA_CATEGORIES = {
    "new_information", "position_shift", "supersession",
    "thread_opened", "thread_resolved",
}

PERSONA_ID_PATTERN = re.compile(r"^PERSONA-\d{3}$")

# Word count ranges (soft limits -- warnings, not errors)
INTERPRETATION_WORD_MIN = 150
INTERPRETATION_WORD_MAX = 500
INTERPRETATION_WORD_IDEAL_MIN = 200
INTERPRETATION_WORD_IDEAL_MAX = 400

SUMMARY_UNDERSTANDING_WORD_MIN = 100
SUMMARY_UNDERSTANDING_WORD_MAX = 400


def parse_date(value, field_name):
    """Parse and validate an ISO 8601 date string. Returns (date, errors)."""
    errors = []
    if not isinstance(value, str):
        if isinstance(value, datetime.date):
            return value, errors
        errors.append(f"{field_name}: expected string, got {type(value).__name__}")
        return None, errors

    try:
        return datetime.date.fromisoformat(value), errors
    except ValueError:
        errors.append(
            f"{field_name}: invalid date format '{value}' — expected YYYY-MM-DD"
        )
        return None, errors


def split_frontmatter_and_body(text):
    """Split a markdown document with YAML frontmatter into (frontmatter_str, body_str).

    Expects the document to start with '---' and have a closing '---'.
    Returns (frontmatter_str, body_str) or (None, None) on failure.
    """
    text = text.lstrip("\ufeff")  # strip BOM if present
    if not text.startswith("---"):
        return None, None

    end = text.find("\n---", 3)
    if end == -1:
        return None, None

    frontmatter_str = text[3:end].strip()
    body_str = text[end + 4:].strip()
    return frontmatter_str, body_str


def parse_frontmatter(frontmatter_str, yaml_mod):
    """Parse YAML frontmatter string. Returns (dict, errors)."""
    errors = []
    try:
        data = yaml_mod.safe_load(frontmatter_str)
    except Exception as e:
        errors.append(f"frontmatter: YAML parse error — {e}")
        return None, errors

    if data is None:
        errors.append("frontmatter: empty or null YAML")
        return None, errors

    if not isinstance(data, dict):
        errors.append("frontmatter: expected a YAML mapping")
        return None, errors

    return data, errors


def count_words(text):
    """Count words in a text string."""
    return len(text.split())


def get_section_content(body, section_name, next_section_pattern=r"^###?\s+"):
    """Extract content between a section header and the next section.

    Returns (content_str, found_bool).
    """
    pattern = rf"^###?\s+{re.escape(section_name)}\s*$"
    match = re.search(pattern, body, re.MULTILINE)
    if not match:
        return "", False

    start = match.end()
    next_match = re.search(next_section_pattern, body[start:], re.MULTILINE)
    if next_match:
        content = body[start:start + next_match.start()].strip()
    else:
        content = body[start:].strip()

    return content, True


# --- Record validation ---

def validate_record_frontmatter(data):
    """Validate cumulative record frontmatter fields. Returns list of errors."""
    errors = []

    # schema_version (required)
    sv = data.get("schema_version")
    if sv is None:
        errors.append("frontmatter: missing required field 'schema_version'")
    elif str(sv) != "1.0":
        errors.append(f"frontmatter: schema_version expected '1.0', got '{sv}'")

    # persona_id (required)
    pid = data.get("persona_id")
    if pid is None:
        errors.append("frontmatter: missing required field 'persona_id'")
    elif not isinstance(pid, str):
        errors.append(
            f"frontmatter: persona_id expected string, got {type(pid).__name__}"
        )
    elif not PERSONA_ID_PATTERN.match(pid):
        errors.append(
            f"frontmatter: persona_id '{pid}' does not match expected "
            f"pattern PERSONA-NNN"
        )

    # meeting_date (required)
    md = data.get("meeting_date")
    if md is None:
        errors.append("frontmatter: missing required field 'meeting_date'")
    else:
        _, date_errs = parse_date(md, "frontmatter.meeting_date")
        errors.extend(date_errs)

    # meeting_type (required)
    mt = data.get("meeting_type")
    if mt is None:
        errors.append("frontmatter: missing required field 'meeting_type'")
    elif mt not in VALID_MEETING_TYPES:
        errors.append(
            f"frontmatter: meeting_type '{mt}' — expected one of: "
            f"{', '.join(sorted(VALID_MEETING_TYPES))}"
        )

    # body (required)
    body = data.get("body")
    if body is None:
        errors.append("frontmatter: missing required field 'body'")
    elif body not in VALID_BODIES:
        errors.append(
            f"frontmatter: body '{body}' — expected one of: "
            f"{', '.join(sorted(VALID_BODIES))}"
        )

    # prior_meeting (required — null or date)
    if "prior_meeting" not in data:
        errors.append("frontmatter: missing required field 'prior_meeting'")
    else:
        pm = data["prior_meeting"]
        if pm is not None:
            _, date_errs = parse_date(pm, "frontmatter.prior_meeting")
            errors.extend(date_errs)

    # interpretation_date (required)
    idate = data.get("interpretation_date")
    if idate is None:
        errors.append("frontmatter: missing required field 'interpretation_date'")
    else:
        _, date_errs = parse_date(idate, "frontmatter.interpretation_date")
        errors.extend(date_errs)

    # Check for unexpected fields
    known_fields = {
        "schema_version", "persona_id", "persona_name",
        "meeting_date", "meeting_type", "body",
        "prior_meeting", "interpretation_date", "interpreter_model",
    }
    for key in data:
        if key not in known_fields:
            errors.append(f"frontmatter: unexpected field '{key}'")

    return errors


def validate_record_interpretation(body):
    """Validate the Interpretation section of a cumulative record. Returns errors."""
    errors = []

    content, found = get_section_content(body, "Interpretation")
    if not found:
        errors.append("body: missing '### Interpretation' section")
        return errors

    if not content:
        errors.append("interpretation: section is empty")
        return errors

    wc = count_words(content)
    if wc < INTERPRETATION_WORD_MIN:
        errors.append(
            f"interpretation: word count {wc} is below minimum "
            f"({INTERPRETATION_WORD_MIN})"
        )
    elif wc > INTERPRETATION_WORD_MAX:
        errors.append(
            f"interpretation: word count {wc} exceeds maximum "
            f"({INTERPRETATION_WORD_MAX})"
        )

    return errors


def validate_record_deltas(body):
    """Validate the Deltas section of a cumulative record. Returns errors."""
    errors = []

    content, found = get_section_content(body, "Deltas")
    if not found:
        errors.append("body: missing '### Deltas' section")
        return errors

    if not content:
        errors.append("deltas: section is empty")
        return errors

    # Find table rows — look for lines starting with |
    table_lines = []
    in_table = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("|"):
            in_table = True
            # Skip header and separator rows
            if re.match(r"^\|[\s\-|:]+\|$", stripped):
                continue
            # Skip header row (contains "Category")
            if "Category" in stripped and "Description" in stripped:
                continue
            table_lines.append(stripped)
        elif in_table and not stripped:
            break  # end of table

    if len(table_lines) == 0:
        errors.append("deltas: no data rows found in table")
        return errors

    # Validate each row
    for i, line in enumerate(table_lines):
        row_num = i + 1
        prefix = f"deltas[{row_num}]"

        # Split by | and clean up
        raw_cells = line.split("|")
        if raw_cells and raw_cells[0].strip() == "":
            raw_cells = raw_cells[1:]
        if raw_cells and raw_cells[-1].strip() == "":
            raw_cells = raw_cells[:-1]
        cells = [c.strip() for c in raw_cells]

        if len(cells) < 2:
            errors.append(
                f"{prefix}: expected at least 2 columns (Category, Description), "
                f"found {len(cells)}"
            )
            continue

        # Validate category
        category = cells[0]
        if category not in VALID_DELTA_CATEGORIES:
            errors.append(
                f"{prefix}: invalid category '{category}' — expected one of: "
                f"{', '.join(sorted(VALID_DELTA_CATEGORIES))}"
            )

        # Validate description is non-empty
        description = cells[1]
        if not description or description == "--" or description == "—":
            errors.append(f"{prefix}: description is empty")

    return errors


def validate_record_emotional_register(body):
    """Validate the Emotional Register section. Returns errors."""
    errors = []

    content, found = get_section_content(body, "Emotional Register")
    if not found:
        errors.append("body: missing '### Emotional Register' section")
        return errors

    if not content:
        errors.append("emotional_register: section is empty")
    elif len(content) < 10:
        errors.append(
            f"emotional_register: content too short ({len(content)} chars, "
            f"expected at least 10)"
        )

    return errors


def validate_record(text, yaml_mod):
    """Validate a full cumulative record document. Returns list of errors."""
    errors = []

    fm_str, body = split_frontmatter_and_body(text)
    if fm_str is None:
        errors.append(
            "document: missing or malformed YAML frontmatter (no --- delimiters)"
        )
        return errors

    data, parse_errors = parse_frontmatter(fm_str, yaml_mod)
    errors.extend(parse_errors)
    if data is not None:
        errors.extend(validate_record_frontmatter(data))

    if not body:
        errors.append("document: body is empty (no content after frontmatter)")
        return errors

    errors.extend(validate_record_interpretation(body))
    errors.extend(validate_record_deltas(body))
    errors.extend(validate_record_emotional_register(body))

    return errors


# --- Summary validation ---

def validate_summary_frontmatter(data):
    """Validate summary view frontmatter fields. Returns list of errors."""
    errors = []

    # schema_version (required)
    sv = data.get("schema_version")
    if sv is None:
        errors.append("frontmatter: missing required field 'schema_version'")
    elif str(sv) != "1.0":
        errors.append(f"frontmatter: schema_version expected '1.0', got '{sv}'")

    # persona_id (required)
    pid = data.get("persona_id")
    if pid is None:
        errors.append("frontmatter: missing required field 'persona_id'")
    elif not isinstance(pid, str):
        errors.append(
            f"frontmatter: persona_id expected string, got {type(pid).__name__}"
        )
    elif not PERSONA_ID_PATTERN.match(pid):
        errors.append(
            f"frontmatter: persona_id '{pid}' does not match expected "
            f"pattern PERSONA-NNN"
        )

    # last_meeting_date (required)
    lmd = data.get("last_meeting_date")
    if lmd is None:
        errors.append("frontmatter: missing required field 'last_meeting_date'")
    else:
        _, date_errs = parse_date(lmd, "frontmatter.last_meeting_date")
        errors.extend(date_errs)

    # record_count (required)
    rc = data.get("record_count")
    if rc is None:
        errors.append("frontmatter: missing required field 'record_count'")
    elif not isinstance(rc, int):
        errors.append(
            f"frontmatter: record_count expected integer, got {type(rc).__name__}"
        )
    elif rc < 1:
        errors.append(
            f"frontmatter: record_count must be at least 1, got {rc}"
        )

    # generated_date (required)
    gd = data.get("generated_date")
    if gd is None:
        errors.append("frontmatter: missing required field 'generated_date'")
    else:
        _, date_errs = parse_date(gd, "frontmatter.generated_date")
        errors.extend(date_errs)

    # Check for unexpected fields
    known_fields = {
        "schema_version", "persona_id", "persona_name",
        "last_meeting_date", "record_count", "generated_date",
    }
    for key in data:
        if key not in known_fields:
            errors.append(f"frontmatter: unexpected field '{key}'")

    return errors


def validate_summary_sections(body):
    """Validate the body sections of a summary view. Returns errors."""
    errors = []

    # Current Understanding
    cu_content, cu_found = get_section_content(body, "Current Understanding")
    if not cu_found:
        errors.append("body: missing '### Current Understanding' section")
    elif not cu_content:
        errors.append("current_understanding: section is empty")
    else:
        wc = count_words(cu_content)
        if wc < SUMMARY_UNDERSTANDING_WORD_MIN:
            errors.append(
                f"current_understanding: word count {wc} is below minimum "
                f"({SUMMARY_UNDERSTANDING_WORD_MIN})"
            )
        elif wc > SUMMARY_UNDERSTANDING_WORD_MAX:
            errors.append(
                f"current_understanding: word count {wc} exceeds maximum "
                f"({SUMMARY_UNDERSTANDING_WORD_MAX})"
            )

    # Timeline of Understanding Shifts
    tl_content, tl_found = get_section_content(
        body, "Timeline of Understanding Shifts"
    )
    if not tl_found:
        errors.append(
            "body: missing '### Timeline of Understanding Shifts' section"
        )
    elif not tl_content:
        errors.append("timeline: section is empty")

    # Active Supersessions
    _, as_found = get_section_content(body, "Active Supersessions")
    if not as_found:
        errors.append("body: missing '### Active Supersessions' section")
    # May be empty (no supersessions yet) -- that's valid

    # Open Threads
    _, ot_found = get_section_content(body, "Open Threads")
    if not ot_found:
        errors.append("body: missing '### Open Threads' section")
    # May be empty -- that's valid

    # Resolved Threads
    _, rt_found = get_section_content(body, "Resolved Threads")
    if not rt_found:
        errors.append("body: missing '### Resolved Threads' section")
    # May be empty -- that's valid

    return errors


def validate_summary(text, yaml_mod):
    """Validate a full summary view document. Returns list of errors."""
    errors = []

    fm_str, body = split_frontmatter_and_body(text)
    if fm_str is None:
        errors.append(
            "document: missing or malformed YAML frontmatter (no --- delimiters)"
        )
        return errors

    data, parse_errors = parse_frontmatter(fm_str, yaml_mod)
    errors.extend(parse_errors)
    if data is not None:
        errors.extend(validate_summary_frontmatter(data))

    if not body:
        errors.append("document: body is empty (no content after frontmatter)")
        return errors

    errors.extend(validate_summary_sections(body))

    return errors


# --- File discovery ---

def find_all_records():
    """Find all cumulative record files (not summary views)."""
    cumulative_dir = PROJECT_ROOT / "data" / "interpretation" / "cumulative"
    if not cumulative_dir.exists():
        return []
    records = []
    for persona_dir in sorted(cumulative_dir.iterdir()):
        if not persona_dir.is_dir():
            continue
        for md_file in sorted(persona_dir.glob("*.md")):
            if md_file.name != "summary.md":
                records.append(md_file)
    return records


def find_all_summaries():
    """Find all summary view files."""
    cumulative_dir = PROJECT_ROOT / "data" / "interpretation" / "cumulative"
    if not cumulative_dir.exists():
        return []
    summaries = []
    for persona_dir in sorted(cumulative_dir.iterdir()):
        if not persona_dir.is_dir():
            continue
        summary_file = persona_dir / "summary.md"
        if summary_file.exists():
            summaries.append(summary_file)
    return summaries


# --- Main ---

def _validate_file(doc_path, is_summary, yaml_mod):
    """Load and validate a single file. Returns error count."""
    rel = (
        doc_path.relative_to(PROJECT_ROOT)
        if doc_path.is_relative_to(PROJECT_ROOT)
        else doc_path
    )

    try:
        text = doc_path.read_text(encoding="utf-8")
    except Exception as e:
        log.error("%s — read error: %s", rel, e)
        return 1

    if not text.strip():
        log.error("%s — file is empty", rel)
        return 1

    if is_summary:
        errors = validate_summary(text, yaml_mod)
    else:
        errors = validate_record(text, yaml_mod)

    if errors:
        log.error("%s — %d validation error(s):", rel, len(errors))
        for err in errors:
            log.error("  %s", err)
    else:
        log.info("%s — valid", rel)

    return len(errors)


def main():
    parser = argparse.ArgumentParser(
        description="Validate cumulative interpretation records and summary views"
    )
    parser.add_argument(
        "document", nargs="?",
        help="Path to a cumulative record or summary .md file to validate",
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="Treat the document as a summary view (default: treat as record)",
    )
    parser.add_argument(
        "--all", action="store_true",
        help=(
            "Validate all cumulative records (and summaries if --summary). "
            "Without --summary, validates all records and all summaries."
        ),
    )
    args = parser.parse_args()

    if not args.document and not args.all:
        parser.error("either provide a document path or use --all")

    try:
        import yaml
    except ImportError:
        log.error("PyYAML is required: pip install pyyaml")
        sys.exit(2)

    total_errors = 0
    files_checked = 0

    if args.all:
        if args.summary:
            # Only validate summaries
            summaries = find_all_summaries()
            if not summaries:
                log.info(
                    "No summary views found in "
                    "data/interpretation/cumulative/"
                )
            for s in summaries:
                files_checked += 1
                total_errors += _validate_file(s, is_summary=True, yaml_mod=yaml)
        else:
            # Validate all records and all summaries
            records = find_all_records()
            if not records:
                log.info(
                    "No cumulative records found in "
                    "data/interpretation/cumulative/"
                )
            for r in records:
                files_checked += 1
                total_errors += _validate_file(r, is_summary=False, yaml_mod=yaml)

            summaries = find_all_summaries()
            if not summaries:
                log.info(
                    "No summary views found in "
                    "data/interpretation/cumulative/"
                )
            for s in summaries:
                files_checked += 1
                total_errors += _validate_file(s, is_summary=True, yaml_mod=yaml)

        log.info("")
        log.info(
            "Checked %d file(s), %d error(s) total",
            files_checked, total_errors,
        )

    else:
        doc_path = Path(args.document).resolve()
        if not doc_path.exists():
            log.error("File not found: %s", doc_path)
            sys.exit(2)

        total_errors = _validate_file(
            doc_path, is_summary=args.summary, yaml_mod=yaml
        )

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
