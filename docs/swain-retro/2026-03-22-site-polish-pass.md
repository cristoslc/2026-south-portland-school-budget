---
title: "Retro: Site Polish Pass"
artifact: RETRO-2026-03-22-site-polish-pass
track: standing
status: Active
created: 2026-03-22
last-updated: 2026-03-22
scope: "INITIATIVE-004 / VISION-004 — accessibility, dark mode fixes, responsive, delight"
period: "2026-03-22"
linked-artifacts:
  - VISION-004
  - INITIATIVE-004
  - ADR-003
  - DESIGN-001
---

# Retro: Site Polish Pass

## Summary

Second session on the static site, focused on fixing dark mode issues, adding a prominent research banner, increasing font sizes for senior readability, improving mobile responsiveness, and adding interaction delight. Also created ADR-003 (Astro content collections decision) and DESIGN-001 (site accessibility standards) to capture standing decisions. Browser-based visual testing caught issues that code review alone missed.

## Artifacts

| Artifact | Title | Outcome |
|----------|-------|---------|
| DESIGN-001 | Site Accessibility Standards | Created — documents typography, contrast, motion, and mobile design standards |
| ADR-003 | Astro Content Collections over Custom SSG | Created — documents the Astro glob loader approach and trade-offs |

## What was fixed

- **Banner hidden under hero** — hero had `margin: -2rem` pulling it over the banner; removed negative margin
- **Card hover underlines** — `<a>` wrapping the whole card caused link underline to leak into all card text; added `a.card` rules to suppress
- **Card h3 color** — headings inside link-cards inherited `--color-sky` instead of `--color-navy`; now uses navy with sky-blue hover transition
- **Font sizes** — base increased from 16px to 18px for senior readability; all secondary text bumped proportionally
- **Mobile responsive** — font sizes scale down at breakpoints, nav wraps, section headers stack, cards go single-column

## Reflection

### What went well

- **Browser testing caught what code review missed.** The banner-under-hero bug was invisible in the CSS — the negative margin was intentional for a visual effect but its interaction with the banner (added later) wasn't predicted. Only a screenshot made it obvious.
- **The three-pass approach worked.** Build -> accessibility fix -> delight was the right sequence. Each pass focused on one concern.
- **ADR and DESIGN docs capture decisions that would otherwise be folklore.** The 18px font decision, the contrast ratios, the Astro choice — these are now findable artifacts instead of implicit knowledge.

### What was surprising

- **The `a.card` link styling cascade was subtle.** When a whole card is an `<a>` tag, every child element inherits link `color` and `text-decoration` behaviors. The fix needed explicit overrides for `h3`, `p`, and `.briefing-meta` inside `a.card`. This is a common pattern but easy to miss when building cards from scratch.
- **Hero negative margins interact badly with later-added elements.** The `-2rem` top margin was a reasonable design choice when the hero was the first thing after the header. Adding the banner between them broke the assumption.

### What would change

- **Always test both themes visually before the first push.** The dark mode heading contrast bug (from the initial build) and the banner-under-hero bug (from the banner addition) were both caught by looking, not by reading CSS.
- **Add a visual regression test.** Even a simple screenshot comparison on deploy would catch theme and layout regressions.

### Patterns observed

- **Civic sites need larger fonts.** The audience is not tech workers — it's parents, retirees, school board members, and students. 18px base with 1.75 line height is noticeably more comfortable than the 16px web default.
- **Dark mode is a second product that needs its own QA pass.** Every color variable, every hardcoded rgba, every gradient — all need dark-mode-specific verification.
- **Standing docs (ADR, DESIGN) are worth creating even for small decisions.** "Why did we use Astro?" and "Why is the font so big?" are questions that will come up. The docs answer them preemptively.

## Learnings captured

| Memory file | Type | Summary |
|------------|------|---------|
| (existing) feedback_retro_dark_mode_a11y.md | feedback | Updated — now covers card link cascade and hero margin interaction |
