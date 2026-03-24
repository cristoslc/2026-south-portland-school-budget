# South Portland 2026 School Budget Analysis

**[Read the briefings on the website &rarr;](https://cristoslc.github.io/south-portland-school-budget-FY27/)**

Independent analysis of the South Portland School Department's proposed FY27 (2026-2027) budget. The district faces an **$8.4 million structural gap** and has proposed **eliminating 78 positions** and **closing one elementary school** to bridge it. This project translates the raw budget into forms that residents can actually use.

This is a research project, not a software application. It is not affiliated with or endorsed by the South Portland School Department or City of South Portland.

## Start Here

The easiest way to read the briefings is on the website: **[cristoslc.github.io/south-portland-school-budget-FY27](https://cristoslc.github.io/south-portland-school-budget-FY27/)**

The site includes all briefings, persona profiles, evidence summaries, a budget timeline, and methodology documentation. It supports dark mode and is designed for readability on all devices.

### Briefings (also available as raw markdown)

The `dist/briefings/` folder contains the same briefings as raw markdown files.

| Briefing | Audience |
|----------|----------|
| [General Budget Briefing](dist/briefings/general-budget-briefing.md) | Anyone -- covers the full budget picture |
| [General Upcoming Briefing](dist/briefings/general-upcoming-briefing.md) | Anyone -- what to watch at the next budget meeting |
| [Maria (Concerned Elementary Parent)](dist/briefings/persona-001-maria-concerned-elementary-parent.md) | Parents worried about school closures and classroom impact |
| [David (Pragmatic Elementary Parent)](dist/briefings/persona-002-david-pragmatic-elementary-parent.md) | Parents focused on logistics -- redistricting, transportation, transitions |
| [Jess (Anxious Pre-K Parent)](dist/briefings/persona-003-jess-anxious-prek-parent.md) | Incoming families navigating uncertainty |
| [Marcus (High School Teacher)](dist/briefings/persona-004-marcus-high-school-teacher.md) | Teachers facing staffing cuts and workload changes |
| [Priya (Equity-Focused Community Member)](dist/briefings/persona-005-priya-equity-focused-community-member.md) | Advocates tracking how cuts affect underserved students |
| [Tom (Tax-Conscious Resident)](dist/briefings/persona-006-tom-tax-conscious-resident.md) | Taxpayers evaluating the fiscal picture and mil rate impact |
| [Linda (School Board Insider)](dist/briefings/persona-007-linda-school-board-insider.md) | Board members and governance participants |
| [Rachel (Disruption-Averse Parent)](dist/briefings/persona-008-rachel-disruption-averse-parent.md) | Parents prioritizing stability and minimal disruption |
| [Dana (Local TV News Producer)](dist/briefings/persona-009-dana-local-tv-news-producer.md) | Journalists covering the story for broadcast |
| [Ben (Forecaster Writer)](dist/briefings/persona-010-ben-forecaster-writer.md) | Long-form journalists and newsletter writers |
| [Meg (Group Chat Relay)](dist/briefings/persona-011-meg-group-chat-relay.md) | Parents who distill meetings into social media and group chats |
| [Jaylen (High School Student)](dist/briefings/persona-012-jaylen-high-school-student.md) | High school students affected by staffing and program cuts |
| [Amira (Middle School Student)](dist/briefings/persona-013-amira-middle-school-student.md) | Middle schoolers navigating transition-year uncertainty |
| [Lila (Elementary Student)](dist/briefings/persona-014-lila-elementary-student.md) | Elementary students experiencing school closures firsthand |

## Research Documentation

The `docs/` folder contains the research artifacts behind the briefings.

### Evidence Pools

Primary source research, organized by topic. Each pool has a manifest, individual source notes, and a thematic synthesis.

- **[FY27 Budget Documents](docs/troves/fy27-budget-documents/synthesis.md)** -- Meeting packets, presentations, and spreadsheets from the district (12 sources, Dec 2025 - Mar 2026)
- **[School Board Budget Meetings](docs/troves/school-board-budget-meetings/synthesis.md)** -- Transcripts and analysis of board meetings where the budget was discussed (4 meetings, Jan - Mar 2026)
- **[City Council Meetings 2026](docs/troves/city-council-meetings-2026/synthesis.md)** -- Council meeting transcripts covering budget-adjacent municipal context (7 meetings, Jan - Mar 2026)

### Personas

Fourteen [validated stakeholder personas](docs/persona/list-persona.md) representing the range of people affected by this budget -- parents, teachers, taxpayers, board members, journalists, community advocates, and students from elementary through high school. Each persona defines key questions, information needs, and concerns that guide the briefing content.

### User Journeys

Four [draft user journeys](docs/journey/list-journey.md) mapping how different stakeholders move from initial awareness to informed participation:

- Understanding what's changing at my kid's school
- Evaluating the budget as a fiscal document
- Tracing equity through the budget
- Navigating the budget as a governance participant

### Vision

- **[VISION-001: Budget Analysis](docs/vision/Active/(VISION-001)-SP-Budget-Analysis/(VISION-001)-SP-Budget-Analysis.md)** -- Scope, audience, success metrics, and non-goals for the analysis itself.
- **[VISION-002: Evidence Pipeline](docs/vision/Active/(VISION-002)-Evidence-Pipeline/(VISION-002)-Evidence-Pipeline.md)** *(WIP)* -- Automated pipeline to keep evidence pools current as new meetings and documents are published. See below.

## Evidence Pipeline (WIP)

VISION-002 defines an automated pipeline that detects new meeting materials, downloads them, normalizes to markdown, and stages them into evidence pools -- replacing the current manual collection process. The pipeline has three layers, built progressively:

**Implemented:**
- **Source connectors** -- Vimeo VTT download (API-based) and Diligent Community agenda scraping (Playwright-based)
- **Normalizers** -- VTT transcript parsing, PDF text extraction, HTML cleaning, XLSX conversion
- **Pipeline runner** -- Orchestrates discovery → download → normalization → evidence pool integration
- **Scheduling** -- Cron-based pipeline runs with incremental processing (only new/changed sources)
- **Meeting bundles** -- Groups evidence pool sources into per-meeting bundles with schema validation

**In progress (Draft specs):**
- **Per-meeting interpretation** -- Generate 14 persona-specific interpretations per meeting bundle, each with structured analysis points, emotional journey maps, and persona-voice reactions
- **Cumulative narratives** -- Log-structured fold system that integrates new meeting interpretations into running per-persona narratives, preserving how each persona's understanding evolves over time
- **Briefings** -- Forward-looking persona briefs plus public general briefings for the full budget picture and the next meeting

Pipeline code lives in `pipeline/` (library modules) and `scripts/` (CLI entry points).

## Raw Data

The `data/` folder contains source materials -- meeting transcripts (VTT), budget PDFs, presentation slides, and agendas. See [`data/README.md`](data/README.md) for a full inventory with dates and source links. Binary files (PDFs, spreadsheets, VTTs) are gitignored; the data README serves as the manifest.

## Scripts

CLI entry points in `scripts/`:

- `pipeline.py` -- Run the full evidence pipeline (discovery → download → normalize → pool integration)
- `parse_vtt.py` -- Parse Vimeo auto-generated transcript files
- `build_evidence_pool.py` -- Build structured evidence pools from source documents
- `add_key_points.py` -- Extract and annotate key points from sources
- `bundle_meetings.py` -- Group evidence pool sources into per-meeting bundles
- `validate_bundle.py` -- Validate meeting bundle schema compliance
- `interpret_meeting.py` -- Generate persona-specific interpretations for a meeting bundle *(WIP)*
- `fold_meeting.py` -- Fold new interpretations into cumulative narratives *(WIP)*
- `generate_briefs.py` -- Generate persona and general public briefings *(WIP)*

## Timeline

This analysis covers the FY27 budget as proposed through March 2026. Key upcoming dates:

- **Mar 16** -- Open Conversation with District Leadership
- **Mar 23** -- Budget Workshop II
- **Mar 30** -- Budget Workshop III
- **Apr 14** -- City Council Budget Workshop #1

The budget process typically runs March through June, ending with a public referendum vote.

## How This Project Is Built

This project uses [swain](https://github.com/cristoslc/swain), an AI-agent skill framework designed for software product development -- not municipal government or civic advocacy. Swain provides structured workflows for things like vision documents, user personas, evidence pools, and implementation specs. Repurposing it for school budget analysis means the terminology and artifact structure can feel odd: budget stakeholders are modeled as "user personas," meeting transcripts go through "evidence pool" pipelines, and briefings are treated as product deliverables. It works, but if you browse the `docs/` folder and wonder why a budget analysis project has software-style artifacts, that's why.

## Disclaimer

This is an independent, volunteer analysis. It is not affiliated with or endorsed by the South Portland School Department or City of South Portland.
