# GitHub Header Link And Board Letter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a GitHub source link beside the site title and publish a post-decision school board letter as a transportation supporting resource.

**Architecture:** Add the header link in the shared layout with compact styling that fits the existing header cluster. Publish the board letter through a dedicated transportation route so it can carry memo-specific framing, then link to it from the transportation landing page and the post-decision brief while keeping the post-decision brief as the canonical overview.

**Tech Stack:** Astro 6, Astro page routes, markdown source files, global CSS, Node test runner (`node --test`)

---

### Task 1: Add Header GitHub Link

**Files:**
- Modify: `site/src/layouts/BaseLayout.astro`
- Modify: `site/src/styles/global.css`
- Test: `site/tests/transport-public-copy.test.mjs`

- [ ] **Step 1: Write the failing test**

Add a regression that renders or inspects the shared layout output and asserts:
- the header contains a GitHub repository link
- the link target is `https://github.com/cristoslc/south-portland-school-budget-FY27`
- the link has an accessible label such as `View source on GitHub`

- [ ] **Step 2: Run test to verify it fails**

Run: `cd site && node --test tests/transport-public-copy.test.mjs`
Expected: FAIL because the header currently has no GitHub icon link.

- [ ] **Step 3: Write minimal implementation**

Update the shared title area in `BaseLayout.astro` to include:
- the existing site title
- a compact GitHub icon link beside it
- `target="_blank"` and `rel="noopener noreferrer"`

Update `global.css` so the title cluster:
- stays aligned on desktop and mobile
- keeps the GitHub link visually secondary
- preserves the existing header height and nav layout

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && node --test tests/transport-public-copy.test.mjs`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add site/src/layouts/BaseLayout.astro site/src/styles/global.css site/tests/transport-public-copy.test.mjs
git commit -m "feat: add github link to site header"
```

### Task 2: Publish the Board Letter as a Transportation Resource

**Files:**
- Modify: `dist/transportation-analysis/BOARD-LETTER-DRAFT.md`
- Create: `site/src/pages/transportation-analysis/board-letter.astro`
- Test: `site/tests/transport-content.test.mjs`

- [ ] **Step 1: Write the failing test**

Add a regression asserting:
- the board letter route exists at `/transportation-analysis/board-letter/`
- the public board letter content is post-decision, not pre-vote
- phrases like `scheduled to vote`, `before the vote`, or `if the district adopts` do not appear

- [ ] **Step 2: Run test to verify it fails**

Run: `cd site && node --test tests/transport-content.test.mjs`
Expected: FAIL because there is no dedicated board-letter route or post-decision board-letter rendering yet.

- [ ] **Step 3: Write minimal implementation**

Rewrite `BOARD-LETTER-DRAFT.md` as a post-decision problem-solving memo that:
- states the vote is settled
- asks for implementation clarity, disclosure, timeline, and public communication
- does not argue for reopening the vote
- distinguishes confirmed information from estimates

Create `board-letter.astro` as a dedicated transportation page with:
- transportation back-link
- board-letter title and memo lede
- rendered markdown content
- supporting-resource framing rather than primary landing-page framing

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && node --test tests/transport-content.test.mjs`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dist/transportation-analysis/BOARD-LETTER-DRAFT.md site/src/pages/transportation-analysis/board-letter.astro site/tests/transport-content.test.mjs
git commit -m "feat: publish post-decision transportation board letter"
```

### Task 3: Make the Board Letter Findable From Transportation Pages

**Files:**
- Modify: `site/src/pages/transportation-analysis/index.astro`
- Modify: `dist/transportation-analysis/POST-DECISION-BRIEF.md`
- Modify: `site/src/lib/transport-content.js`
- Test: `site/tests/transport-public-copy.test.mjs`

- [ ] **Step 1: Write the failing test**

Add assertions that:
- the transportation landing page links to `/transportation-analysis/board-letter/`
- the post-decision brief page links to `/transportation-analysis/board-letter/`
- the board letter is presented as a supporting resource, not the main story

- [ ] **Step 2: Run test to verify it fails**

Run: `cd site && node --test tests/transport-public-copy.test.mjs`
Expected: FAIL because the supporting-resource links do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Update the transportation landing page with a supporting-resource card or section that links to the board letter.

Update `POST-DECISION-BRIEF.md` so the rendered public page includes a short supporting-resource link to the board letter.

Extend any render-layer cleanup in `transport-content.js` only if needed so the board-letter link text stays reader-facing and does not reintroduce internal artifact language.

- [ ] **Step 4: Run full verification**

Run:

```bash
cd site && node --test tests/transport-content.test.mjs
cd site && node --test tests/transport-public-copy.test.mjs
cd site && npm run build
```

Expected:
- all tests PASS
- build exits 0
- generated site contains `/transportation-analysis/board-letter/`
- built transport landing and post-decision pages link to the board letter

- [ ] **Step 5: Commit**

```bash
git add site/src/pages/transportation-analysis/index.astro dist/transportation-analysis/POST-DECISION-BRIEF.md site/src/lib/transport-content.js site/tests/transport-public-copy.test.mjs
git commit -m "feat: surface transportation board letter"
```
