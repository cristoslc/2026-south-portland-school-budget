# Changelog

## [1.2.0] - 2026-04-06

### Features

#### Progressive event-scoped fold model

EPIC-037 and SPIKE-014 establish the architecture for processing meeting events one at a time instead of in bulk. Research covered three prior-art troves — Kappa architecture, event sourcing, and incremental NLP pipelines — confirming the model is sound. The event loop design supports ordered, resumable fold passes without full re-ingestion.

#### Keyword-triggered reference context injection

SPEC-081 adds a pipeline stage that detects domain keywords in persona briefs and automatically injects relevant reference documents — ADRs, troves, and analysis artifacts — before the LLM call. BDD integration tests verify the trigger rules. This eliminates the need for operators to manually thread context into prompts.

#### Reconfiguration context analysis track

EPIC-036 and SPEC-088–091 build out a dedicated analysis track for the 2024 school reconfiguration. A new site page surfaces reconfiguration context alongside the budget narrative. Briefings for all 15 personas have been regenerated with this context included.

#### Pending state infrastructure

SPEC-082 adds a pending state to the pipeline coordination model. Briefs that are waiting on upstream LLM output now declare pending status explicitly rather than being absent or stale. The lifecycle includes transition rules and a site-visible indicator.

#### Transportation equity evidence and site pages

EPIC-034, SPEC-066, and SPEC-070 complete the transport analysis track. Fifteen persona briefs address Option A transport impacts. A new site section presents walk zone data, per-family cost estimates, and a board letter. The April 2 special budget meeting evidence has been folded in and the transport claims catalog updated.

#### April 2 special budget meeting ingested

The April 2 special budget meeting transcript and supporting materials are fully ingested, normalized, and folded into cumulative summaries. All 15 persona briefs and the post-decision brief have been republished with this evidence.

#### TelVue SPC-TV connector

SPEC-071 adds a connector that extracts VTT captions from the SPC-TV TelVue platform. Three new transcripts were collected using the connector, extending the evidence pool to include School & Public Communications TV coverage.

#### Independent enrollment and transportation studies

INITIATIVE-005 and INITIATIVE-006 are fully decomposed and implemented. The enrollment study includes a school choice transfer flow analysis that found South Portland is a net student importer — decline is demographic, not driven by outbound transfers. The transportation study models all six route configurations with per-family and per-district cost breakdowns.

#### Community lenses section

The site home page now features a community lenses section presenting budget perspectives organized by stakeholder group. Editorial tone has been removed from briefings to meet the no-adversarial-framing policy.

#### Budget collateral page scraper

The budget page connector now captures collateral pages linked from the main district budget page, not just the primary document. This extends automated coverage to supplemental materials posted after initial publication.
- Post-decision brief and board letter published with framing for the April 2 Option A vote outcome
- Duplicate briefing cards removed; 404 redirect added for URL casing variants
- DESIGN-002 design document and JOURNEY-005 community journey artifact added

### Research
- SPIKE-014 — progressive fold event model: three prior-art troves (Kappa architecture, event sourcing, incremental NLP), event loop design complete
- SPIKE-012 and SPIKE-013 — Go verdicts recorded for two research questions
- SPIKE-010 — walk zone audit web research pass complete
- SPIKE-008 — key questions scoring prototype and tracking spreadsheet
- Troves: school-integration-policy (6 sources), sopo-redistricting-tool (2 sources), three progressive-fold prior-art troves

### Supporting Changes
- Swain skills refreshed: design, dispatch, do, doctor, init, keys, release, retro, search, security-check, session, stage, status, sync
- ADR-005 documents keyword-triggered reference context decision
- ADR-004 added for key questions tracking approach
- AGENTS.md, skills-lock.json, and roadmap refreshed
- dist/ reorganized by initiative with README and METHODOLOGY
- Pipeline LLM prompts hardened with editorial tone guardrails
- Stale cumulative summaries regenerated; all briefs republished

## [1.1.0] - 2026-03-25

### Features

#### Full-transcript briefings

The brief generator now ingests complete meeting transcripts — including VTT timestamps — instead of silently truncating at 5K characters. The previous limit caused the LLM to hallucinate that votes and decisions were missing from the record when they were actually present in the source. The 2026-03-23 budget workshop (442K chars, 5+ hours) now loads in full, and all 17 briefs for 2026-03-30 have been regenerated with accurate information about what happened at the end of the meeting.

#### Parallel brief generation

The brief pipeline now runs LLM calls in batches of 3 instead of sequentially. A full 17-brief run completes in ~8.5 minutes (down from ~18). Progress logging shows batch start, per-brief completion with status, and running counts.
- Cumulative persona summaries updated from the 2026-03-23 full reinterpretation (13 personas)

### Supporting Changes
- Swain skills updated to latest upstream (54 files across design, dispatch, do, doctor, init, keys, release, retro, search, security-check, session, stage, status, sync)
- AGENTS.md and skills-lock.json refreshed

## 1.0.0 — 2026-03-25

### Features

#### Question Hub
New Questions section on the site where residents can browse 30 budget questions organized by topic — School Closures, Staffing Cuts, Tax Impact, Programs & Classes, Equity & Fairness, How Decisions Get Made, and What Happens Next. Each question links to a detail page with a plain-language answer, evidence citations from public meeting records and budget documents, and links to related questions. All content written at grade 8.5 reading level.

#### Public Budget Site
Static site with home page, persona-based briefings, 15 community perspectives, evidence/sources page with click-to-expand source collections, budget timeline, changelog, and about/methodology page. Dark mode, responsive design, and research project banner.

#### Persona Interpretation Pipeline
End-to-end pipeline that collects meeting transcripts and budget documents, normalizes them to markdown, interprets each meeting through 15 stakeholder personas, folds interpretations into cumulative narratives, and generates forward-looking briefings. Covers school board meetings, city council meetings, and budget documents from December 2025 through March 2026.

#### Evidence Source Links
Sources page links directly to primary source URLs on spsdme.org, Vimeo, and Diligent. Each source collection card expands to show every collected document and transcript with GitHub links to normalized versions.

#### Question Extraction Pipeline
Automated script that parses open questions from all 16 persona briefings, deduplicates via LLM, categorizes by topic, links to trove evidence sources, and filters to only questions with sourced answers.

- Site freshness indicators and automatic changelog generation
- Google Slides export support and meaningful document filenames in the pipeline
- General public budget briefings alongside persona-specific ones

### Roadmap
- Community feedback integration — accepting and routing resident questions to relevant answer pages
- Privacy-respecting analytics to understand which questions and briefings residents find most useful
- Site data assembly pipeline for automated build-time data generation

### Research
- 6 completed research spikes covering Vimeo API access, Diligent Community scraping, normalization reuse, scheduling, interpretation prompt design, and cumulative fold strategy
- 5 trove collections with 113 sources across budget documents, school board meetings, city council meetings, voter guides, and market segmentation research

### Supporting
- Self-hosted Docker runner for pipeline automation
- Polling LLM pipeline architecture using claude -p subscription auth (no API keys)
- 15 validated community personas spanning parents, teachers, staff, community members, media, and students
- 4 user journeys mapping how residents navigate from concern to understanding
