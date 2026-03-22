---
title: "Site Accessibility Standards"
artifact: DESIGN-001
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
linked-initiatives:
  - INITIATIVE-004
linked-visions:
  - VISION-004
depends-on-artifacts:
  - ADR-003
addresses: []
---

# DESIGN-001: Site Accessibility Standards

## Audience

South Portland residents — including senior citizens, parents reading on phones at school pickup, and people with visual impairments. The site must be readable by the broadest possible audience without requiring assistive technology, though it should also work well with screen readers.

## Typography

| Property | Value | Rationale |
|----------|-------|-----------|
| Base font size | 18px | Larger than typical web (16px) for senior readability |
| Line height | 1.75 | Generous spacing for dense budget content |
| Body font | System font stack | Maximum readability across platforms |
| Heading scale | h1: 2.1rem, h2: 1.6rem, h3: 1.25rem, h4: 1.1rem | Clear visual hierarchy |

### Responsive scaling

| Breakpoint | Base size | Rationale |
|-----------|----------|-----------|
| Desktop (>768px) | 18px | Full readability |
| Tablet (768px) | 17px | Slight reduction to fit content |
| Phone (480px) | 16px | Standard mobile size — still readable |

## Color Contrast

All text-on-background pairings must meet **WCAG AA** (4.5:1 for body, 3:1 for large text). Key dark mode pairings:

| Element | Color | Background | Ratio | Grade |
|---------|-------|------------|-------|-------|
| Body text | `#e2e8f0` | `#0f172a` | 13.5:1 | AAA |
| Headings | `#93c5fd` | `#0f172a` | 8.2:1 | AAA |
| Headings (on card) | `#93c5fd` | `#1e293b` | 6.0:1 | AA |
| Muted text | `#94a3b8` | `#0f172a` | 4.6:1 | AA |
| Card description | `#94a3b8` | `#1e293b` | 3.4:1 | AA (large) |

### Dark mode separation

The header, footer, and hero use darker backgrounds than the page body to maintain visual separation:

| Element | Dark bg | Page bg | Contrast |
|---------|---------|---------|----------|
| Header/footer | `#0b1120` | `#0f172a` | Distinct |
| Hero gradient | `#0b1120` to `#162033` | `#0f172a` | Distinct |
| Cards | `#1e293b` | `#0f172a` | Distinct |

## Motion and Animation

- All animations respect `prefers-reduced-motion: reduce` — durations set to 0.01ms
- Scroll-reveal uses IntersectionObserver with a fallback (no IO = show immediately)
- Hover animations use `cubic-bezier(0.34, 1.56, 0.64, 1)` for gentle spring effect
- Theme transitions use 0.3s ease for smooth crossfade without jarring flash

## Mobile Design

- Cards stack to single column below 768px
- Navigation wraps with centered alignment
- Hero stats wrap naturally, switching to horizontal layout on smallest screens
- Section headers stack (title above link) on narrow viewports
- Touch targets (cards, nav links, theme toggle) maintain minimum 44px hit area

## Research Banner

A persistent amber banner appears below the header on every page, clearly stating the site is an independent research project. The banner:

- Uses warm amber palette (distinct from the blue UI chrome)
- Adapts to dark mode with darker amber tones
- Links to the About page for full methodology disclosure
- Font size scales down on mobile but remains readable

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Established during site build and accessibility pass |
