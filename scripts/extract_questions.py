#!/usr/bin/env python3
"""Extract, deduplicate, and evidence-link budget questions from persona briefs.

Parses Open Questions sections from all briefing files, uses LLM to
deduplicate semantically similar questions and assign topic categories,
links questions to trove evidence sources, and filters to only include
questions with at least one sourced answer.

Usage:
    python3 scripts/extract_questions.py
    python3 scripts/extract_questions.py --dry-run
    python3 scripts/extract_questions.py --briefs-date 2026-03-30

Exit codes:
    0 — success
    1 — extraction or LLM call failed
    2 — usage error
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.llm_client import call_llm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("extract_questions")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BRIEFS_DIR = PROJECT_ROOT / "data" / "interpretation" / "briefs"
TROVES_DIR = PROJECT_ROOT / "docs" / "troves"
DIST_DIR = PROJECT_ROOT / "dist"


def parse_open_questions(content: str) -> list[dict]:
    """Extract individual questions from an Open Questions markdown section."""
    # Find the Open Questions section
    pattern = r"^##\s+Open Questions\s*$"
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return []

    # Get content until next section or end
    rest = content[match.end():]
    next_section = re.search(r"^##\s+", rest, re.MULTILINE)
    section_text = rest[:next_section.start()] if next_section else rest

    questions = []
    lines = section_text.strip().split("\n")

    # Detect format: look for bold category headers on non-bullet lines
    # Format C: "**Category Header:**\n- plain question\n- plain question"
    current_category = None

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("---"):
            continue

        # Bold category header (standalone, not a bullet)
        cat_match = re.match(r"^\*\*(.+?)\*\*:?\s*$", stripped)
        if cat_match and not stripped.startswith("-"):
            current_category = cat_match.group(1).strip().rstrip(":")
            continue

        # Skip non-bullet preamble lines (e.g., "Carrying into March 30...")
        if not stripped.startswith("- "):
            # Could be continuation text; skip
            continue

        # It's a bullet point
        bullet_text = stripped[2:].strip()
        if not bullet_text:
            continue

        # Format A: "**Bold question?** context..."
        bold_match = re.match(r"\*\*(.+?\??)\*\*\s*(.*)", bullet_text, re.DOTALL)
        if bold_match:
            q_text = bold_match.group(1).strip()
            ctx = bold_match.group(2).strip()
            questions.append({"question": q_text, "context": ctx})
            continue

        # Format B/C: Plain-text question (with or without category header)
        # Must contain a question mark to be treated as a question
        if "?" in bullet_text:
            # Extract up to the first question mark + sentence as the question
            # Some bullets have multiple sentences; take the whole thing
            ctx = f"(Category: {current_category})" if current_category else ""
            questions.append({"question": bullet_text, "context": ctx})

    return questions


def load_all_questions(briefs_date=None) -> list[dict]:
    """Load raw questions from all briefing files."""
    all_questions = []

    if briefs_date:
        date_dirs = [BRIEFS_DIR / briefs_date]
    else:
        date_dirs = sorted(BRIEFS_DIR.iterdir())

    for date_dir in date_dirs:
        if not date_dir.is_dir():
            continue
        for brief_path in sorted(date_dir.glob("PERSONA-*.md")):
            # Extract persona ID from filename
            fname = brief_path.stem
            persona_match = re.match(r"(PERSONA-\d+)", fname)
            if not persona_match:
                continue
            persona_id = persona_match.group(1)

            content = brief_path.read_text(encoding="utf-8")
            questions = parse_open_questions(content)
            for q in questions:
                q["persona_id"] = persona_id
                q["source_file"] = str(brief_path.relative_to(PROJECT_ROOT))
                q["brief_date"] = date_dir.name
            all_questions.extend(questions)
            log.info(
                "Parsed %d questions from %s (%s)",
                len(questions), persona_id, date_dir.name
            )

    return all_questions


def load_trove_sources() -> list[dict]:
    """Load all trove manifest sources for evidence linking."""
    sources = []
    for manifest_path in TROVES_DIR.glob("*/manifest.yaml"):
        import yaml
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        trove_id = manifest.get("trove", manifest_path.parent.name)
        for src in manifest.get("sources", []):
            sources.append({
                "trove": trove_id,
                "source_id": src.get("source-id", ""),
                "title": src.get("title", ""),
                "type": src.get("type", ""),
                "path": src.get("path", ""),
                "file": src.get("file", ""),
            })
    return sources


def make_slug(question: str) -> str:
    """Generate a URL-safe slug from question text."""
    # Remove punctuation, lowercase, replace spaces with hyphens
    text = question.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    # Truncate to reasonable length
    if len(text) > 60:
        text = text[:60].rsplit("-", 1)[0]
    return text


def deduplicate_and_categorize(raw_questions: list[dict], trove_sources: list[dict]) -> list[dict]:
    """Use LLM to deduplicate, categorize, and evidence-link questions."""
    # Build source catalog for the LLM
    source_catalog = []
    for src in trove_sources:
        source_catalog.append({
            "trove": src["trove"],
            "title": src["title"],
            "type": src["type"],
        })

    prompt = f"""You are rewriting budget questions for a public website about the South Portland FY27 school budget. The audience is ordinary residents — parents, taxpayers, students, neighbors. They are not policy analysts.

## Writing rules (CRITICAL)

- Target Flesch-Kincaid grade level 8.5. Use short sentences. Use common words.
- Questions should sound like what a neighbor would ask at a kitchen table, not what a policy wonk would write in a memo.
- No jargon. Translate terms: "RIF" → "layoff notices", "reconfiguration" → "school reorganization", "material weakness" → "serious financial audit problem", "semesterization" → "switching to semester-long classes", "impact bargaining" → "union negotiations over layoff effects".
- Answers ("context") should be 2-3 plain sentences. State what we know, then what we don't. Don't hedge with bureaucratic language — just say "we don't know yet" or "this hasn't been made public."
- Evidence detail should be one plain sentence explaining what that source says.

## Bad example (too complex)
"What accountability structure is being put in place to prevent continued mismanagement of Title I, IDEA, and ELL-designated federal funds?"

## Good example (grade 8.5)
"How is the district making sure federal education money is spent correctly?"

## Raw Questions

Here are all the raw questions extracted from persona briefings. Many are semantically similar — asked by different personas about the same underlying topic.

{json.dumps(raw_questions, indent=2)}

## Available Evidence Sources

{json.dumps(source_catalog, indent=2)}

## Task

1. **Deduplicate**: Group semantically similar questions. For each group, write ONE clear, simple question a resident would actually ask. List all persona IDs that asked a variant.

2. **Categorize**: Assign each question to exactly one category:
   - School Closures
   - Staffing Cuts
   - Tax Impact
   - Programs & Classes
   - How Decisions Get Made
   - Equity & Fairness
   - What Happens Next

3. **Evidence Link**: For each question, identify which evidence sources contain relevant information. Only link sources that genuinely help answer the question.

4. **Answer**: Write a 2-3 sentence plain-language answer. State facts first, then what's still unknown. Write like you're explaining to a smart neighbor, not a school board member.

5. **Filter**: ONLY include questions that have at least one evidence source. Drop questions with no traceable answer.

## Output Format

Return a JSON array (no markdown fencing, just raw JSON):

[
  {{
    "question": "Simple, clear question a resident would ask?",
    "category": "One of the categories above",
    "personas": ["PERSONA-001", "PERSONA-003"],
    "evidence": [
      {{
        "trove": "trove-id",
        "title": "Source title from the catalog",
        "detail": "One plain sentence about what this source says."
      }}
    ],
    "context": "2-3 plain sentences answering the question. What we know. What we don't."
  }}
]

Return ONLY the JSON array. No other text."""

    system_prompt = (
        "You are a plain-language writer producing structured data for a public website. "
        "Write at a Flesch-Kincaid grade level of 8.5. Use short sentences and common words. "
        "Return only valid JSON with no markdown code fences. "
        "Be factual — do not invent evidence links."
    )

    log.info("Calling LLM for deduplication, categorization, and evidence linking...")
    result = call_llm(prompt, system_prompt=system_prompt)

    # Parse JSON from response — handle potential markdown fencing
    text = result.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        questions = json.loads(text)
    except json.JSONDecodeError as exc:
        log.error("Failed to parse LLM response as JSON: %s", exc)
        log.error("Response was: %s", text[:500])
        raise

    return questions


def add_slugs(questions: list[dict]) -> list[dict]:
    """Add unique slugs to each question."""
    seen_slugs = set()
    for q in questions:
        slug = make_slug(q["question"])
        # Ensure uniqueness
        base_slug = slug
        counter = 2
        while slug in seen_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        seen_slugs.add(slug)
        q["slug"] = slug
    return questions


def main():
    parser = argparse.ArgumentParser(
        description="Extract and deduplicate budget questions from persona briefs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--briefs-date",
        help="Process only briefs from this date (YYYY-MM-DD). Default: latest date.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and count questions without calling LLM",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DIST_DIR / "questions.json",
        help="Output path (default: dist/questions.json)",
    )

    args = parser.parse_args()

    # Default to latest briefs date
    if not args.briefs_date:
        date_dirs = sorted(
            [d for d in BRIEFS_DIR.iterdir() if d.is_dir()],
            key=lambda d: d.name,
        )
        if not date_dirs:
            log.error("No briefing date directories found in %s", BRIEFS_DIR)
            sys.exit(2)
        args.briefs_date = date_dirs[-1].name
        log.info("Using latest briefs date: %s", args.briefs_date)

    # Step 1: Parse raw questions
    raw_questions = load_all_questions(args.briefs_date)
    log.info("Extracted %d raw questions from briefs", len(raw_questions))

    if args.dry_run:
        # Show summary and exit
        personas = set(q["persona_id"] for q in raw_questions)
        log.info("Dry run — %d questions from %d personas", len(raw_questions), len(personas))
        for q in raw_questions[:5]:
            log.info("  [%s] %s", q["persona_id"], q["question"][:80])
        if len(raw_questions) > 5:
            log.info("  ... and %d more", len(raw_questions) - 5)
        return

    # Step 2: Load trove sources for evidence linking
    trove_sources = load_trove_sources()
    log.info("Loaded %d trove sources for evidence linking", len(trove_sources))

    # Step 3: Deduplicate, categorize, evidence-link via LLM
    questions = deduplicate_and_categorize(raw_questions, trove_sources)
    log.info("LLM produced %d deduplicated questions", len(questions))

    # Step 4: Add slugs
    questions = add_slugs(questions)

    # Step 5: Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    log.info("Wrote %d questions to %s", len(questions), args.output)

    # Summary by category
    categories = {}
    for q in questions:
        cat = q.get("category", "Uncategorized")
        categories[cat] = categories.get(cat, 0) + 1
    log.info("Categories:")
    for cat, count in sorted(categories.items()):
        log.info("  %s: %d", cat, count)


if __name__ == "__main__":
    main()
