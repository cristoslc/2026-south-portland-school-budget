# SPEC-070 Transportation Analysis Site Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete `/transportation-analysis` section to the Astro site for the INITIATIVE-006 deliverables, including landing, methodology, metric pages, briefing index, briefing detail pages, and comparison-table rendering.

**Architecture:** Extend the Astro content layer with transport-specific collections and a small custom loader that normalizes the transport markdown files before Astro parses them. Build the new transport routes by reusing the site's existing briefing and detail-page patterns, then add targeted navigation and cross-links so transport content is reachable from the rest of the site.

**Tech Stack:** Astro 6, astro:content collections, TypeScript, Markdown, JSON data, npm build verification

---

### Task 1: Add Transport Content Loaders

**Files:**
- Create: `site/src/lib/transport-content.ts`
- Modify: `site/src/content.config.ts`
- Test: `site` build via `npm run build`

- [ ] **Step 1: Write the failing test**

Define the expected loader behaviors before coding:
- Existing budget briefings load from the actual enrollment-study deliverable directory, not a missing `dist/briefings` path.
- Transport briefings parse fenced frontmatter into data fields (`persona_id`, `topic`, `source_specs`, `generated_date`).
- Transport analysis docs expose stable IDs/slugs for landing, methodology, and drill-down pages.

- [ ] **Step 2: Run test to verify it fails**

Run: `npm run build`
Expected: warnings that the `briefings` collection base directory does not exist, and transport content is not available through Astro collections.

- [ ] **Step 3: Write minimal implementation**

Implement a small custom Astro loader helper that:
- Reads transport markdown files from `../dist/transportation-analysis/briefings/`
- Removes the top-level fenced wrapper around frontmatter when present
- Parses frontmatter and stores clean markdown bodies
- Exposes normalized collection entries for transport briefings

Also update `site/src/content.config.ts` to:
- Point the existing `briefings` collection at the real enrollment-study briefing output
- Add `transportBriefings`
- Add `transportAnalysis`
- Keep schemas explicit for the transport metadata used by pages

- [ ] **Step 4: Run test to verify it passes**

Run: `npm run build`
Expected: content sync completes without the missing-briefings warning, and the build can resolve transport collections.

- [ ] **Step 5: Commit**

```bash
git add site/src/content.config.ts site/src/lib/transport-content.ts
git commit -m "feat: add transport content loaders"
```

### Task 2: Build Transportation Analysis Pages

**Files:**
- Create: `site/src/pages/transportation-analysis/index.astro`
- Create: `site/src/pages/transportation-analysis/methodology.astro`
- Create: `site/src/pages/transportation-analysis/[slug].astro`
- Create: `site/src/components/TransportComparisonTable.astro`
- Test: `npm run build`

- [ ] **Step 1: Write the failing test**

Define the page behaviors to satisfy:
- `/transportation-analysis/` renders the transport README and the comparison table
- `/transportation-analysis/methodology/` renders the methodology doc
- `/transportation-analysis/<slug>/` renders the individual transport analysis docs
- The comparison table shows all three configurations, range values, and source links

- [ ] **Step 2: Run test to verify it fails**

Run: `npm run build`
Expected: transport routes do not exist yet, and no table component renders the JSON comparison data.

- [ ] **Step 3: Write minimal implementation**

Create a focused table component that:
- Reads `transport-comparison.json`
- Highlights Option A, Option B, and Variant C clearly
- Shows fiscal exposure and percent-of-claimed-savings values
- Links metric rows to the relevant analysis pages

Create the transport pages using the normalized content collections:
- Landing page uses README content + comparison table + links to analyses and briefs
- Methodology page renders the methodology document
- Dynamic analysis page renders all non-README, non-methodology transport docs intended for public drill-down

- [ ] **Step 4: Run test to verify it passes**

Run: `npm run build`
Expected: static transport routes are generated and the JSON-backed table renders without content errors.

- [ ] **Step 5: Commit**

```bash
git add site/src/components/TransportComparisonTable.astro site/src/pages/transportation-analysis
git commit -m "feat: add transportation analysis pages"
```

### Task 3: Build Transport Briefing Index and Detail Pages

**Files:**
- Create: `site/src/pages/transportation-analysis/briefings/index.astro`
- Create: `site/src/pages/transportation-analysis/briefings/[slug].astro`
- Modify: `site/src/pages/personas/[id].astro`
- Test: `npm run build`

- [ ] **Step 1: Write the failing test**

Define the expected behaviors:
- `/transportation-analysis/briefings/` lists the transport general brief and persona-specific briefs
- `/transportation-analysis/briefings/<slug>/` renders each brief cleanly from normalized markdown
- Persona detail pages link to the matching transport brief when one exists

- [ ] **Step 2: Run test to verify it fails**

Run: `npm run build`
Expected: the transport briefing routes do not exist, and persona pages only link to the existing budget briefing collection.

- [ ] **Step 3: Write minimal implementation**

Reuse the visual structure of the existing briefing pages, but:
- Keep transport brief URLs under `/transportation-analysis/briefings/`
- Show transport-specific metadata (`topic`, `source_specs`, `generated_date`)
- Add a transport-brief card or link block on persona detail pages

- [ ] **Step 4: Run test to verify it passes**

Run: `npm run build`
Expected: all transport brief routes build cleanly and persona pages expose the cross-link.

- [ ] **Step 5: Commit**

```bash
git add site/src/pages/transportation-analysis/briefings site/src/pages/personas/[id].astro
git commit -m "feat: add transportation briefing routes"
```

### Task 4: Add Site Navigation and Final Verification

**Files:**
- Modify: `site/src/layouts/BaseLayout.astro`
- Modify: `site/src/pages/index.astro`
- Modify: `site/src/styles/global.css`
- Test: `npm run build`

- [ ] **Step 1: Write the failing test**

Define the expected navigation behaviors:
- Main nav includes Transportation Analysis
- Landing page and transport pages fit the existing site style without layout breakage
- The transport section is discoverable from the homepage and global nav

- [ ] **Step 2: Run test to verify it fails**

Run: `npm run build`
Expected: the new section is still not linked from primary navigation.

- [ ] **Step 3: Write minimal implementation**

Add:
- Main nav entry in `BaseLayout`
- A homepage entry point to the transport analysis section
- Any compact styling needed for the comparison table, source links, and transport section cards

- [ ] **Step 4: Run test to verify it passes**

Run: `npm run build`
Expected: build passes cleanly with the transport section linked from global navigation and homepage entry points.

- [ ] **Step 5: Commit**

```bash
git add site/src/layouts/BaseLayout.astro site/src/pages/index.astro site/src/styles/global.css
git commit -m "feat: link transportation analysis section"
```

### Task 5: Final Verification

**Files:**
- Test: `site/src/content.config.ts`
- Test: `site/src/lib/transport-content.ts`
- Test: `site/src/components/TransportComparisonTable.astro`
- Test: `site/src/pages/transportation-analysis/index.astro`
- Test: `site/src/pages/transportation-analysis/methodology.astro`
- Test: `site/src/pages/transportation-analysis/[slug].astro`
- Test: `site/src/pages/transportation-analysis/briefings/index.astro`
- Test: `site/src/pages/transportation-analysis/briefings/[slug].astro`
- Test: `site/src/pages/personas/[id].astro`
- Test: `site/src/layouts/BaseLayout.astro`
- Test: `site/src/pages/index.astro`
- Test: `site/src/styles/global.css`

- [ ] **Step 1: Run full verification**

Run: `npm run build`
Expected: clean Astro build with no missing-collection warnings and generated transportation-analysis routes.

- [ ] **Step 2: Spot-check generated output**

Review the generated route list for:
- `/transportation-analysis/`
- `/transportation-analysis/methodology/`
- `/transportation-analysis/briefings/`
- multiple `/transportation-analysis/briefings/<slug>/` pages
- multiple `/transportation-analysis/<slug>/` analysis pages

- [ ] **Step 3: Commit**

```bash
git add site
git commit -m "feat: publish transportation analysis section"
```
