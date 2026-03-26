# Changelog

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
