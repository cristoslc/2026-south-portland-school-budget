---
title: "Retro: INITIATIVE-005 Decomposition & Data Acquisition"
artifact: RETRO-2026-03-31-initiative-005-data-acquisition
track: standing
status: Active
created: 2026-03-31
last-updated: 2026-03-31
scope: "Session covering INITIATIVE-005 decomposition into EPICs/SPECs and EPIC-022 data acquisition"
period: "2026-03-30 — 2026-03-31"
linked-artifacts:
  - INITIATIVE-005
  - EPIC-022
  - EPIC-023
  - EPIC-024
  - EPIC-025
  - SPEC-039
  - SPEC-040
  - SPEC-041
  - SPIKE-009
---

# Retro: INITIATIVE-005 Decomposition & Data Acquisition

## Summary

Single session decomposed INITIATIVE-005 (Independent Enrollment Study) from a bare initiative into 4 EPICs, 9 SPECs, 1 SPIKE, and then executed the data acquisition track (EPIC-022) nearly to completion. Collected 12 years of grade-level NCES enrollment data, extracted 27 enrollment claims from 3 evidence pools, gathered supplementary demographic data (births, housing permits), and completed SPIKE-009 (building-level feasibility — Conditional Go). Session ended when the operator discovered a parallel worktree (citizen-studies) had created overlapping artifacts.

## Artifacts

| Artifact | Title | Outcome |
|----------|-------|---------|
| EPIC-022 | Enrollment Data Acquisition | Active — data acquisition substantially complete |
| EPIC-023 | Enrollment Gap Analysis & Phase 1 Briefs | Active — children created, blocked on EPIC-022 |
| EPIC-024 | Cohort Survival Model | Active — children created, blocked on EPIC-022 |
| EPIC-025 | Phase 2 Briefs & Baseline Publication | Proposed — downstream of 023+024 |
| SPEC-039 | Maine DOE Enrollment Data Collection | Data collected (NCES trove created) |
| SPEC-040 | District Enrollment Claims Catalog | Catalog created (27 claims, JSON) |
| SPEC-041 | Supplementary Demographic Data | Data collected (births + permits); school choice gap documented |
| SPIKE-009 | Building-Level Data Feasibility | Complete — Conditional Go |

## Reflection

### What went well

**Chrome browser automation for data collection was highly effective.** The NCES ELSI Table Generator is an interactive web tool with no API. Using Chrome automation (click-through + JavaScript injection for bulk checkbox selection) turned a tedious 30-minute manual task into a 5-minute automated one. The operator's nudge to "use Chrome and Puppeteer" was the key unlock — without it, the session would have stalled on trying to find non-existent APIs.

**Parallel research agents for source discovery.** Launching simultaneous agents to research Maine DOE data sources and explore trove infrastructure saved significant time. The trove infrastructure agent provided the exact directory structure and normalization format, eliminating guesswork.

**The sopo-data4good redistricting tool was an unexpected goldmine for SPIKE-009.** It was already in the troves and contained building capacity data, census block overlays, and working catchment zone algorithms — converting what could have been a weeks-long feasibility study into a quick evidence review.

**Autonomous mode worked well for artifact creation.** The operator's instruction to "approve all related specs and epics, continue writing/decomposing as needed" enabled a highly productive burst — 4 EPICs and 9 SPECs created, promoted, and indexed in one pass without stop-start confirmation overhead.

### What was surprising

**Parallel worktree collision.** A citizen-studies worktree was running concurrently and created overlapping enrollment claims artifacts (YAML format in `docs/troves/enrollment-claims/` vs our JSON in `data/enrollment-claims/`). The worktree also decomposed INITIATIVE-005 with different SPEC numbering (SPEC-051, SPEC-054). This wasn't detected until mid-session. The `next-artifact-id.sh` script is designed to prevent ID collisions across worktrees, but when two sessions independently decompose the same initiative, the structural overlap (not just ID collision) is the real problem.

**CDC WONDER only has county-level birth data, not municipal.** The initial research suggested municipal birth data would be available from "DHHS vital records," but in practice, CDC WONDER provides county-level only (Cumberland County). Municipal birth counts require parsing individual annual city reports (19MB PDFs) or filing a Maine CDC data request. The county-level proxy (8.25% population share) validated well against actual kindergarten enrollment, making it sufficient for modeling.

**The NCES ELSI tool has no API and no bulk download for place-level grade data.** Multiple attempts to find a programmatic data source (Education Data Portal API, CCD bulk files, direct URLs) failed. The ELSI web tool was the only path to grade-level district enrollment data, confirming that browser automation is a necessary capability for government data collection.

### What would change

**Check for parallel worktrees before decomposing an initiative.** The citizen-studies collision could have been caught with a `git worktree list` + branch content scan at session start. When an initiative already has commits on another branch, the session should surface that before creating artifacts.

**Collect school-level NCES data alongside district-level.** The ELSI tool was already open and configured; switching from "District" to "Public School" would have taken 2 minutes and provided the school-level enrollment history that SPIKE-009 identified as available. Missing this means a return trip to ELSI later.

**Start with the data gap report, not the data.** Writing SPEC-041's data gap report at the end surfaced the school choice gap and pre-2016 birth gap. If the gap analysis had been the first step, the session could have prioritized which data to collect and which gaps to document without collecting.

### Patterns observed

**Government data collection follows a predictable frustration curve:** documentation suggests data exists → the portal has no direct download → interactive tools require browser automation → the data format needs transformation. This pattern held for NCES (ELSI), CDC WONDER, Census BPS, and Maine DOE. Budget time for browser automation in all government data specs.

**Trove creation and claims extraction are naturally parallel.** SPEC-039 (data) and SPEC-040 (claims) had no dependency between them — they could have been dispatched to parallel agents. The serial execution worked but was suboptimal.

**The "approve all and continue" autonomous mode is the right default for artifact decomposition.** The operator's time is better spent on review after the fact than on approval gates during creation. The artifacts are Proposed until promoted — the safety net is the phase system, not the creation ceremony.

## Learnings captured

| Item | Type | Summary |
|------|------|---------|
| feedback_retro_browser_automation.md | memory | Chrome/Puppeteer is essential for government data portals — no APIs exist |
| feedback_retro_check_parallel_worktrees.md | memory (existing — reinforced) | Check parallel worktrees before decomposing initiatives to prevent structural overlap |
