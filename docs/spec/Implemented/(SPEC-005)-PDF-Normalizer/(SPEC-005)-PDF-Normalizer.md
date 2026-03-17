---
title: "PDF-to-Markdown Normalizer"
artifact: SPEC-005
status: Implemented
author: cristos
created: 2026-03-10
last-updated: 2026-03-10
parent-epic: EPIC-002
linked-research:
  - SPIKE-003
linked-adrs: []
depends-on: []
addresses: []
trove: ""
swain-do: required
linked-epics:
  - EPIC-001
linked-specs:
  - SPEC-003
  - SPEC-004
---

# PDF-to-Markdown Normalizer

## Problem Statement

Budget documents and presentation slides are distributed as PDFs. No existing script handles PDF-to-markdown conversion. Per SPIKE-003, this is new work. The converter must produce evidence pool source markdown from both text-heavy documents (agenda packets, budget reports) and slide-heavy presentations, using a Python PDF library for standalone operation without MCP runtime dependencies.

## External Behavior

**Input:**
- Path to a PDF file (e.g., `data/school-board/budget-fy27/meetings/2025-12-17-workshop/packet.pdf`)
- Metadata: title, date, document type (packet/slides/report)

**Output:**
- A markdown file matching the evidence pool source format:
  - YAML frontmatter with `source-id`, `title`, `type: document`, `path`, `fetched`, `hash`
  - Extracted text content preserving document structure (headings, lists, tables where feasible)
- Updated `manifest.yaml` entry for the target evidence pool

**Preconditions:**
- Python PDF library installed (`pdfplumber` or `pymupdf`)
- Target evidence pool directory exists

**Constraints:**
- Must produce output structurally consistent with existing PDF-sourced evidence pool files (e.g., `fy27-budget-documents/sources/001-workshop-packet-2025-12-17.md`)
- SHA-256 hash of the source PDF must be stored in frontmatter
- Slide-heavy PDFs may produce lower-fidelity output — flag these for manual review via a `notes` frontmatter field

## Acceptance Criteria

1. **Given** a text-heavy PDF (agenda packet), **when** the normalizer runs, **then** it produces markdown with extracted text preserving paragraph breaks and basic structure.
2. **Given** a slide-heavy PDF (presentation), **when** the normalizer runs, **then** it extracts slide text with slide-number markers (e.g., `## Slide 1`) and flags the output for manual review in the `notes` field.
3. **Given** a PDF file and metadata, **when** the normalizer runs, **then** the output has valid YAML frontmatter with all required fields (`source-id`, `title`, `type: document`, `path`, `fetched`, `hash`).
4. **Given** an existing evidence pool, **when** a new PDF is normalized into it, **then** `source-id` is auto-assigned as the next sequential ID.
5. **Given** a successful normalization, **when** the output is written, **then** `manifest.yaml` is updated with the new source entry.
6. **Given** the same PDF run twice, **when** the hash matches an existing source, **then** the normalizer skips or warns.

## Verification

| Criterion | Evidence | Result |
|-----------|----------|--------|
| AC1: Text-heavy PDF extracts with structure | Test on `packet.pdf` (2025-12-17) produces markdown with paragraph breaks, agenda structure preserved | Pass |
| AC2: Slide-heavy PDF with slide markers and notes flag | Slide detection uses page density heuristic (SPARSE_PAGE_THRESHOLD=200, SLIDE_HEAVY_RATIO=0.5); sparse pages get `## Slide N` markers and `notes` field set | Pass |
| AC3: Valid frontmatter with all required fields | Test output contains source-id, title, type: document, path, fetched, hash | Pass |
| AC4: Sequential source-id | Second PDF in same pool gets source-id 002 | Pass |
| AC5: manifest.yaml updated | test-results/normalize-pdf/manifest.yaml contains both source entries | Pass |
| AC6: Duplicate detection | Re-running same PDF skips with hash match warning | Pass |

## Scope & Constraints

**In scope:**
- PDF text extraction via `pdfplumber` or `pymupdf`
- Handling both text-heavy and slide-heavy PDFs
- CLI entry point accepting PDF path + metadata arguments
- Manifest update and duplicate detection

**Out of scope:**
- OCR for scanned/image PDFs (accept text-layer-only extraction)
- Table extraction with full fidelity (best-effort)
- PDF discovery or download (EPIC-001 / SPEC-003)

## Implementation Approach

1. Create `pipeline/normalize_pdf.py` with a `convert_pdf()` function
2. Use `pdfplumber` for text extraction (better table handling than pymupdf)
3. Detect slide-heavy vs text-heavy PDFs by page text density heuristic
4. Add CLI wrapper (argparse) for standalone use
5. Share manifest update and hash/duplicate logic with SPEC-004 (extract to `pipeline/pool_utils.py`)
6. Test against existing budget PDFs, compare output quality to MCP-generated sources

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Draft | 2026-03-10 | f1208a3 | Initial creation |
| Testing | 2026-03-10 | 63397e4 | Implementation complete, all bd tasks closed |
| Implemented | 2026-03-10 | 63397e4 | All acceptance criteria verified |
