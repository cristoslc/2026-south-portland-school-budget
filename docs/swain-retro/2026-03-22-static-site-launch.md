---
title: "Retro: Static Site Launch"
artifact: RETRO-2026-03-22-static-site-launch
track: standing
status: Active
created: 2026-03-22
last-updated: 2026-03-22
scope: "INITIATIVE-004 / VISION-004 — initial public site build and deploy"
period: "2026-03-22"
linked-artifacts:
  - VISION-004
  - INITIATIVE-004
---

# Retro: Static Site Launch

## Summary

Built and deployed the public-facing static site for the FY27 budget analysis in a single autonomous session. The site went from zero scaffolding to 36 pages live on GitHub Pages in under 30 minutes, including a follow-up dark mode feature. Content is sourced directly from existing `dist/briefings/` and `docs/persona/Active/` via Astro content collections — no content duplication.

## Artifacts

| Artifact | Title | Outcome |
|----------|-------|---------|
| [VISION-004](../vision/Active/(VISION-004)-Public-Budget-Site/(VISION-004)-Public-Budget-Site.md) | Public Budget Site | In progress — site is live, core pages deployed |
| [INITIATIVE-004](../initiative/Active/(INITIATIVE-004)-Public-Budget-Site/(INITIATIVE-004)-Public-Budget-Site.md) | Public Budget Site | In progress — scaffolding and deployment complete; child epics for feedback, visual design, and data assembly remain |

## What was built

- **22 source files** across `site/` and `.github/workflows/`
- **36 pages generated:** landing, 16 briefings, 14 persona profiles, evidence, timeline, about
- **GitHub Pages deployment** with automatic workflow on push
- **Dark mode** with three-state toggle (Auto/Light/Dark), localStorage persistence, and flash prevention

## Reflection

### What went well

- **Content collections as integration layer.** Astro's glob loader pointing to `../dist/briefings/` and `../docs/persona/Active/` means the site reads existing content with zero duplication. New briefings appear automatically on rebuild.
- **Autonomous execution worked.** The user said "I'm going to bed" and the entire site was built, deployed, and verified without intervention. Background agents for git operations kept the main thread productive.
- **Fast iteration cycle.** Astro v6 builds 36 pages in ~800ms. Build-fix-rebuild loops were quick even with content collection issues.
- **GitHub Pages setup via API.** Using `gh api` to enable Pages programmatically avoided needing the user to configure anything in the GitHub UI.

### What was surprising

- **Glob patterns don't match parenthesized directories.** The persona files live in directories like `(PERSONA-001)-Concerned-Elementary-Parent/`, and the glob pattern `**/PERSONA-*.md` failed silently. Switching to `**/*.md` fixed it. This is a microcosm of the evidence pipeline's filename normalization issue ([SPEC-024](../spec/Active/(SPEC-024)-Meaningful-Document-Filenames/(SPEC-024)-Meaningful-Document-Filenames.md)).
- **Astro's `base` config needs a trailing slash.** Without it, all internal links rendered as `/south-portland-school-budget-FY27briefings/` instead of `/south-portland-school-budget-FY27/briefings/`. A one-character fix but it required a full rebuild to catch.
- **TypeScript type annotations aren't allowed in Astro template expressions.** `Record<string, ...>` in a `.map()` inside the template section caused a cryptic esbuild error. Moving it to the frontmatter was the fix.

### What would change

- **Start with a content inventory script.** Before building the site, a quick script that lists all content files with their frontmatter fields would have prevented the glob pattern issue and revealed the exact schema up front.
- **Validate URLs before the first push.** The missing trailing slash produced broken links that only showed up when reading the generated HTML. A post-build link checker would catch this.

### Patterns observed

- **Content-first architecture pays off.** The project's investment in structured briefings with YAML frontmatter meant the site could be built almost entirely as a presentation layer. The hard work was already done in the interpretation pipeline.
- **Background agents for git are effective.** Delegating commit-and-push to background agents kept the main thread focused on building the next feature. This pattern works well for autonomous sessions.
- **Child epics remain undecomposed.** [INITIATIVE-004](../initiative/Active/(INITIATIVE-004)-Public-Budget-Site/(INITIATIVE-004)-Public-Budget-Site.md) lists six child epics (EPIC-013 through EPIC-018) that are still marked "to be created." The site that shipped covers scaffolding (EPIC-013) and core pages (EPIC-015) but the data assembly, feedback, visual design, and continuous deploy epics haven't been formally created. The work outpaced the artifact graph.

## Learnings captured

| Memory file | Type | Summary |
|------------|------|---------|
| feedback_retro_astro_globs.md | feedback | Astro glob loaders fail silently on parenthesized directory names — use `**/*.md` |
| feedback_retro_autonomous_site.md | feedback | Background agents for git + fast build tools = effective autonomous sessions |
