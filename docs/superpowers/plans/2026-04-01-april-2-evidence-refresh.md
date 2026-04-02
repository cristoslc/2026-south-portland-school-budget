# April 2 Evidence Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ingest the April 1 district evidence for the April 2, 2026 special budget meeting and regenerate the upcoming public brief outputs with the new agenda and inter-meeting evidence.

**Architecture:** Add the two new April 1 sources as normalized markdown artifacts, register them in the FY27 budget trove and inter-meeting manifest, then rerun the existing brief generator with the April 2 agenda file so the published outputs refresh through the normal pipeline.

**Tech Stack:** Markdown source artifacts, YAML manifests, Python brief generator, local publish script

---

### Task 1: Add normalized evidence sources

**Files:**
- Create: `docs/troves/fy27-budget-documents/sources/048-special-budget-meeting-agenda-2026-04-02/048-special-budget-meeting-agenda-2026-04-02.md`
- Create: `docs/troves/fy27-budget-documents/sources/049-elementary-reconfiguration-road-map-2026-04-01/049-elementary-reconfiguration-road-map-2026-04-01.md`
- Create: `data/interpretation/inter-meeting/sources/2026-04-01-special-budget-agenda.md`
- Create: `data/interpretation/inter-meeting/sources/2026-04-01-elementary-reconfiguration-road-map.md`

- [ ] Capture the raw source content locally for the agenda PDF and the rendered `es2627` page.
- [ ] Write normalized markdown versions that preserve the factual structure, dates, links, and implementation details.

### Task 2: Register the new evidence

**Files:**
- Modify: `docs/troves/fy27-budget-documents/manifest.yaml`
- Modify: `docs/troves/fy27-budget-documents/synthesis.md`
- Modify: `data/interpretation/inter-meeting/manifest.yaml`

- [ ] Add both April 1 sources to the FY27 budget trove manifest with hashes and source metadata.
- [ ] Update the trove synthesis so the new agenda and implementation page affect the documented timeline and open questions.
- [ ] Add both sources to the inter-meeting manifest with the correct `posted_after` / `posted_before` window for the April 2 brief.

### Task 3: Regenerate and publish the April 2 briefs

**Files:**
- Create: `data/interpretation/briefs/2026-04-02/*`
- Modify: `dist/enrollment-study/briefings/*`

- [ ] Run the brief generator for `2026-04-02` with the revised agenda file.
- [ ] Publish the refreshed brief outputs into `dist/enrollment-study/briefings/`.
- [ ] Inspect the general upcoming brief to confirm the April 2 frontmatter and narrative changed as expected.

### Task 4: Verify the refresh

**Files:**
- Verify only

- [ ] Run the relevant verification commands for source registration, brief generation, and publish.
- [ ] Check git diff to confirm the update is limited to the new evidence and regenerated brief outputs.
