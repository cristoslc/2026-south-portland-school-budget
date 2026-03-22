---
title: "Privacy-Respecting Analytics"
artifact: SPEC-028
type: feature
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-epic: ""
parent-initiative: INITIATIVE-004
priority-weight: medium
acceptance-criteria:
  - Site tracks page views and visitor counts without cookies or PII
  - Analytics dashboard accessible to project maintainer
  - No data sent to Google or other ad-tech companies
  - Works with static site (no backend required)
  - Minimal impact on page load performance
depends-on-artifacts:
  - EPIC-014
addresses: []
---

# Privacy-Respecting Analytics

## Problem

Community feedback (EPIC-018) is deferred until the site has real traffic. To know when that threshold is reached and which content resonates, we need basic traffic metrics — but the civic nature of this site demands privacy-respecting analytics. No cookies, no PII, no ad-tech.

## Proposed Solution

Add a lightweight, privacy-respecting analytics service. Options in priority order:

1. **Plausible Analytics** (plausible.io) — open-source, no cookies, GDPR-compliant, ~1KB script. Free for self-hosted; $9/mo cloud.
2. **Umami** (umami.is) — open-source, no cookies, self-hostable. Free.
3. **GoatCounter** (goatcounter.com) — open-source, minimal. Free for non-commercial.
4. **Cloudflare Web Analytics** — free, no cookies, but requires Cloudflare DNS.

## Implementation

Add a single `<script>` tag to `BaseLayout.astro` pointing to the chosen analytics service. No cookies, no localStorage, no fingerprinting.

## Acceptance Criteria

- [ ] Analytics script added to BaseLayout.astro
- [ ] Page views tracked for all 36+ pages
- [ ] Dashboard accessible to project maintainer
- [ ] No cookies set by the analytics script
- [ ] Lighthouse performance score not degraded

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Created as small work under INITIATIVE-004 (no epic wrapper) |
