---
title: "Astro Content Collections over Custom SSG"
artifact: ADR-003
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
linked-epics: []
linked-specs: []
linked-initiatives:
  - INITIATIVE-004
linked-visions:
  - VISION-004
depends-on-artifacts: []
addresses: []
---

# ADR-003: Astro Content Collections over Custom SSG

## Context

VISION-004 calls for a static site that presents budget briefings and persona profiles to South Portland residents. The content already exists as structured markdown with YAML frontmatter in `dist/briefings/` (16 briefings) and `docs/persona/Active/` (14 persona profiles). The site needs to render this content without duplicating it.

Three approaches were considered:

1. **Custom Python SSG** — generate HTML directly from the existing pipeline scripts
2. **Jekyll/Hugo** — established static site generators with markdown support
3. **Astro with content collections** — modern SSG with native content collection loaders that can point to external directories

## Decision

Use **Astro v6 with glob-based content collections** that point directly at the existing content directories (`../dist/briefings/` and `../docs/persona/Active/`).

## Rationale

- **Zero content duplication.** The glob loader reads directly from the source directories. When the interpretation pipeline generates new briefings, a site rebuild picks them up automatically.
- **Schema validation.** Astro's Zod-based content schemas catch frontmatter issues at build time, not at runtime.
- **Fast builds.** 36 pages build in ~800ms — fast enough for the GitHub Actions deploy workflow.
- **GitHub Pages native.** Astro has first-class support for GitHub Pages with the `site`/`base` config and `actions/deploy-pages`.
- **Component model.** Astro's `.astro` component format keeps layout, pages, and content separate without requiring a JS framework.

## Trade-offs

- **Glob pattern sensitivity.** Astro's glob loader silently returns zero results when directory names contain parentheses (the swain artifact naming convention). Workaround: use `**/*.md` instead of specific filename patterns.
- **Node.js dependency.** The rest of the project is Python. The site adds `node_modules/` and `package-lock.json` to the repo.
- **Astro-specific knowledge.** Content collection config, frontmatter coercion, and template expression limitations (no TypeScript type annotations in template blocks) require Astro-specific knowledge.

## Consequences

- The `site/` directory is self-contained — all Astro code lives there.
- Content flows one direction: pipeline -> `dist/briefings/` -> site build. The site never modifies content.
- GitHub Pages deployment is triggered by pushes to `site/`, `dist/briefings/`, or `docs/persona/`.

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Decided during initial site build |
