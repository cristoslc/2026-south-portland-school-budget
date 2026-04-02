# Transport Community Lens Briefings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the pre-decision transport persona briefing corpus with a smaller post-decision community-lens briefing set while keeping the post-decision brief as the canonical overview.

**Architecture:** Rewrite the source markdown corpus under `dist/transportation-analysis/briefings/` into seven canonical lens pages, then update the public briefing index and slug rendering to present those pages as the only public briefing set. Verification should prove that old persona slugs are gone from the generated site and that public copy is post-decision, community-facing, and free of old persona framing.

**Tech Stack:** Astro content collections, markdown source files, Node test runner (`node --test`)

---

### Task 1: Replace the Briefing Markdown Corpus

**Files:**
- Modify: `dist/transportation-analysis/briefings/transport-general.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-001-maria.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-002-david.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-003-jess.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-004-marcus.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-005-priya.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-006-tom.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-007-linda.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-008-rachel.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-009-dana.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-010-ben.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-011-meg.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-012-jaylen.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-013-amira.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-014-lila.md`
- Delete: `dist/transportation-analysis/briefings/transport-persona-015-kira.md`
- Create: `dist/transportation-analysis/briefings/transport-families.md`
- Create: `dist/transportation-analysis/briefings/transport-elementary-families.md`
- Create: `dist/transportation-analysis/briefings/transport-staff.md`
- Create: `dist/transportation-analysis/briefings/transport-taxpayers.md`
- Create: `dist/transportation-analysis/briefings/transport-older-students.md`
- Create: `dist/transportation-analysis/briefings/transport-city-school-leadership.md`
- Test: `site/tests/transport-content.test.mjs`

- [ ] **Step 1: Write the failing test**

Add a test asserting that `getTransportBriefing`-style content exposes only:
- `transport-general`
- `transport-families`
- `transport-elementary-families`
- `transport-staff`
- `transport-taxpayers`
- `transport-older-students`
- `transport-city-school-leadership`

Also assert that no briefing ID contains `transport-persona-`.

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/transport-content.test.mjs`
Expected: FAIL because the old persona briefing corpus is still present.

- [ ] **Step 3: Rewrite the markdown corpus**

Write seven post-decision community-lens briefs with consistent frontmatter and structure:
- `What has been decided`
- `What this means for you`
- `What still needs to be worked out`
- `What is confirmed, what is estimated`
- link back to `POST-DECISION-BRIEF.md`

Requirements:
- `transport-general.md` becomes post-decision and community-facing
- all new lens pages use plain audience names, not persona names
- all old persona markdown files are removed from the corpus
- no `Variant C`
- no pre-vote language
- no artifact-language leakage

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test tests/transport-content.test.mjs`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dist/transportation-analysis/briefings site/tests/transport-content.test.mjs
git commit -m "feat: replace transport personas with community lens briefings"
```

### Task 2: Update the Public Briefing Index and Slug Rendering

**Files:**
- Modify: `site/src/pages/transportation-analysis/briefings/index.astro`
- Modify: `site/src/pages/transportation-analysis/briefings/[slug].astro`
- Modify: `site/src/lib/transport-content.js`
- Test: `site/tests/transport-public-copy.test.mjs`

- [ ] **Step 1: Write the failing test**

Add assertions that the built briefing index:
- lists the seven public lens pages
- does not show persona IDs
- does not show old persona slugs
- uses community-facing labels only

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/transport-public-copy.test.mjs`
Expected: FAIL because the current index still reflects the old briefing structure.

- [ ] **Step 3: Implement the minimal rendering changes**

Update the briefing index to group pages as community lenses:
- General Community
- Families
- Elementary Families
- Staff
- Taxpayers
- Older Students
- City and School Leadership

Update slug rendering so:
- badge and description language match the new lens model
- no persona-profile link expectations remain
- any remaining render-layer cleanup supports the new briefing schema without overfitting to removed persona fields

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test tests/transport-public-copy.test.mjs`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add site/src/pages/transportation-analysis/briefings/index.astro \
        site/src/pages/transportation-analysis/briefings/[slug].astro \
        site/src/lib/transport-content.js \
        site/tests/transport-public-copy.test.mjs
git commit -m "feat: present transport briefings as community lenses"
```

### Task 3: Rebuild and Verify Public Output

**Files:**
- Modify: `site/src/pages/index.astro`
- Test: `site/tests/transport-public-copy.test.mjs`
- Test: `site/tests/transport-content.test.mjs`
- Test: `site/tests/transport-comparison.test.mjs`

- [ ] **Step 1: Write the failing test**

Extend public-copy regression coverage to assert:
- no `transport-persona-` paths in built `dist/transportation-analysis/briefings`
- no persona IDs in public briefing cards
- no pre-decision phrases like `being asked to vote`, `before the vote`, `scheduled to vote`

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/transport-public-copy.test.mjs`
Expected: FAIL before the final build/render updates land.

- [ ] **Step 3: Update any remaining public entry points**

Adjust homepage or transport entry copy if needed so it references community lens briefings rather than persona briefings.

- [ ] **Step 4: Run full verification**

Run:

```bash
node --test tests/transport-content.test.mjs
node --test tests/transport-comparison.test.mjs
node --test tests/transport-public-copy.test.mjs
npm run build
```

Expected:
- all tests PASS
- build exits 0
- generated transport briefing output contains only the seven new lens pages

- [ ] **Step 5: Commit**

```bash
git add site/src/pages/index.astro site/tests/transport-public-copy.test.mjs
git commit -m "test: verify post-decision community lens briefing output"
```
