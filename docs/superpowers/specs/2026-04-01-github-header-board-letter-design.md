# GitHub Header Link And Board Letter Design

## Goal

Add a GitHub repository link to the site header and make the school board letter easy to find as a transportation supporting resource.

## Scope

This work covers two public-site changes:

1. A GitHub icon link in the header next to the site title.
2. A post-decision board letter page inside the transportation section.

This work does not add the board letter to main navigation.

## Design

### Header GitHub Link

The header should gain a compact GitHub icon button beside the `SP Budget Watch` title in the existing title area in [BaseLayout.astro](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/spec-070-transport-site/site/src/layouts/BaseLayout.astro).

Requirements:

- Link target: `https://github.com/cristoslc/south-portland-school-budget-FY27`
- Open in a new tab with safe external-link attributes
- Visually secondary to the site title
- Accessible label such as `View source on GitHub`
- Styled in the existing header visual language, not as a new nav item

### Board Letter Positioning

The board letter should live as a transportation supporting resource, not as a top-level section.

Public location:

- `/transportation-analysis/board-letter/`

Source of truth:

- [BOARD-LETTER-DRAFT.md](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/spec-070-transport-site/dist/transportation-analysis/BOARD-LETTER-DRAFT.md)

### Board Letter Content Direction

The current letter is still partly shaped by the pre-decision context. It should be rewritten as a post-decision problem-solving memo.

Requirements:

- The vote is already settled
- The letter should not argue for reopening the vote
- The main asks should be about implementation, disclosure, timeline, and public communication
- Tone should be practical, firm, and non-adversarial
- The letter should align with the current transportation pages on confirmed vs estimated claims

Recommended structure:

1. What has already been decided
2. What now needs public clarity
3. Specific requests for the board and district
4. Link back to the transportation analysis and post-decision brief

### Findability

The board letter should be linked from:

- the transportation landing page
- the post-decision brief
- optionally the briefing index as a supporting resource block if the page layout supports it cleanly

The transport landing page should present it as a supporting resource, not as the primary reader path.

## Files Likely To Change

- [BaseLayout.astro](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/spec-070-transport-site/site/src/layouts/BaseLayout.astro)
- [global.css](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/spec-070-transport-site/site/src/styles/global.css)
- [BOARD-LETTER-DRAFT.md](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/spec-070-transport-site/dist/transportation-analysis/BOARD-LETTER-DRAFT.md)
- [transportation-analysis/index.astro](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/spec-070-transport-site/site/src/pages/transportation-analysis/index.astro)
- [transportation-analysis/[slug].astro](/Users/cristos/Documents/projects/south-portland-school-budget-FY27/.claude/worktrees/spec-070-transport-site/site/src/pages/transportation-analysis/[slug].astro) or a new dedicated page if cleaner
- a new route for the board letter page if it should not share the generic analysis template

## Open Choice

Implementation can either:

1. Treat the board letter as another analysis page under the existing generic dynamic route, if the page works cleanly with the current template.
2. Create a dedicated `board-letter.astro` page if the letter needs different framing or surrounding navigation.

I recommend the second option if the page needs a clearer supporting-resource presentation than the generic analysis template provides.
