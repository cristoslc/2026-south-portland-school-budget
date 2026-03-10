---
title: "Normalization Script Reuse Assessment"
artifact: SPIKE-003
status: Complete
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
question: "Can the existing parse_vtt.py, build_evidence_pool.py, and add_key_points.py scripts be used as-is in an automated pipeline, or do they need refactoring?"
gate: Pre-MVP
risks-addressed:
  - Existing scripts may require interactive input or manual path configuration that blocks automation
  - Output format may not match current evidence pool source structure without manual post-processing
depends-on: []
evidence-pool: ""
---

# Normalization Script Reuse Assessment

## Question

Can the existing Python scripts in `scripts/` be invoked non-interactively to convert raw source files into evidence pool markdown? Specifically:

1. Does `parse_vtt.py` accept input/output paths as arguments, or does it require interactive prompts?
2. Does `build_evidence_pool.py` produce output matching the current evidence pool source format (YAML frontmatter + structured body)?
3. What manual steps currently happen between running these scripts and committing a finished evidence pool source?
4. For PDF conversion, is there an existing path or do we need a new converter?

## Go / No-Go Criteria

- **Go:** At least `parse_vtt.py` can be called non-interactively with minor modifications (adding CLI args). The output is close enough to the evidence pool format that a thin wrapper can bridge the gap.
- **No-Go:** Scripts are fundamentally interactive (e.g., require human judgment at multiple decision points mid-execution) and would need a full rewrite to automate.

## Pivot Recommendation

If existing scripts can't be adapted: write new, purpose-built conversion functions as a Python module (`pipeline/normalize.py`) that imports only the useful parsing logic from the existing scripts. Don't try to make the old scripts do something they weren't designed for.

## Findings

### parse_vtt.py: Go -- fully non-interactive

Takes a VTT file path as a CLI argument, outputs to stdout. No prompts, no interactivity. Returns duration on line 1, then merged transcript with `**[MM:SS]**` timestamps. Can be called via `subprocess.run()` exactly as `build_evidence_pool.py` already does.

**Reuse verdict:** Use as-is. Import `parse_vtt()` and `merge_segments()` directly for tighter integration, or keep calling as a subprocess.

### build_evidence_pool.py: Partial reuse -- hardcoded but well-structured

The script is fully non-interactive (no prompts, no user input). However, it has significant hardcoding:

- **Hardcoded absolute paths** (`BASE_DIR = "/Users/cristos/..."`) -- needs parameterization
- **Hardcoded source lists** (`VTT_SOURCES`, `TXT_SOURCES`) -- every meeting is manually enumerated with source ID, filename, date directory, and title
- **Hardcoded to one pool** (city-council-meetings-2026) -- can't process other pools without modification
- **Hardcoded dates** (`fetched: 2026-03-09T00:00:00Z`) in frontmatter

The processing functions (`process_vtt()`, `process_txt()`, `build_manifest()`) are well-structured and produce correctly formatted output (YAML frontmatter + markdown body). The manifest builder generates valid `manifest.yaml`.

**Reuse verdict:** Extract `process_vtt()` and `process_txt()` as library functions with parameterized paths. The logic is sound; the hardcoding is the only problem. Don't rewrite -- refactor into a module that accepts arguments.

### add_key_points.py: No reuse for pipeline

This script contains manually-written key point summaries hardcoded as a Python dictionary. It's a one-time data entry script, not a transformation pipeline. Key points require human judgment (or LLM analysis) and can't be automated mechanically.

**Reuse verdict:** Not applicable to the pipeline. Key point extraction stays in the human/agent workflow (swain-search synthesis).

### PDF conversion: New capability needed

No existing script handles PDF-to-markdown conversion. The existing evidence pool for budget documents (`fy27-budget-documents`) has markdown source files, but these were likely created via the Claude Code MCP tools (`pdf-to-markdown`, `pptx-to-markdown`). For the pipeline, options include:

1. **MCP tools** (`pdf-to-markdown`) -- available but tied to the Claude Code runtime, not standalone
2. **Python libraries** -- `pdfplumber`, `pymupdf`, or `marker` for text extraction; quality varies by PDF structure
3. **Pandoc** -- can convert some formats but poor with slide-heavy PDFs

**Recommendation:** Use a Python PDF library (`pdfplumber` or `pymupdf`) for standalone operation. Accept lower quality than MCP tools for automated runs; flag complex PDFs for manual review.

### Summary

| Script | Non-interactive? | Reusable? | Action needed |
|--------|-----------------|-----------|---------------|
| `parse_vtt.py` | Yes | Yes, as-is | None |
| `build_evidence_pool.py` | Yes | Core functions yes | Parameterize paths and source lists |
| `add_key_points.py` | Yes (but hardcoded data) | No | Stays manual/agent |
| PDF converter | N/A | Doesn't exist | Build new with pdfplumber/pymupdf |

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Planned | 2026-03-10 | _pending_ | Initial creation |
| Active | 2026-03-10 | _pending_ | Code review of all three scripts |
| Complete | 2026-03-10 | _pending_ | Go -- parse_vtt reusable as-is, build_evidence_pool needs path refactoring, PDF is new work |
