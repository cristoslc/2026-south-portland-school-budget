# Persona Interpretation Pipeline — Architecture Overview

This document describes the pipeline that transforms evidence pools into per-persona interpretations. It is a living description of the system shape; individual architectural decisions belong in ADRs.

## Pipeline Stages

```
Evidence Pool (raw sources)
    │
    ▼
┌─────────────────────┐
│  Meeting Bundler     │ → groups sources by meeting/workshop milestone
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Per-Meeting         │ → for each meeting × each persona:
│  Interpretation      │     • structured points
│                      │     • journey map
│                      │     • unstructured reactions
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Cumulative Fold     │ → integrates new meeting into running
│                      │   per-persona narrative
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Upcoming-Event      │ → forward-looking brief for next
│  Brief               │   meeting, per persona
└─────────────────────┘
```

## Stage 1: Meeting Bundler

**Input:** Evidence pool sources (transcripts, agendas, presentations, spreadsheets, slide decks).

**Output:** Source groups, each affiliated with a specific meeting or workshop milestone.

**Key design decision:** The atomic unit is the meeting/workshop, not the individual document. Interim artifacts (a spreadsheet posted days before a workshop, a slide deck uploaded after) are bundled with the meeting at which they are presented. This requires semantic understanding of source content and context, not just temporal proximity — a document posted on March 4 may belong to the March 2 workshop or the March 9 one, depending on its content and purpose.

Sources that don't belong to any specific meeting (e.g., a standalone policy document, a state DOE data release) are handled as inter-meeting evidence events and surface in the upcoming-event brief for the next meeting.

**School budget focus:** All evidence is processed, but school budget content is the primary subject matter. City council topics unrelated to the school budget are included as operational context — they matter for the background and political theater, but their specific details receive lighter interpretation than school budget material.

## Stage 2: Per-Meeting Interpretation

**Input:** A meeting bundle (all sources affiliated with one meeting) + all 14 persona definitions.

**Output:** One interpretation per persona per meeting, containing three layers:

### Structured points

Key facts relevant to this persona, what changed from their last known state, emotional stakes and threat level, open questions this meeting raises, and action opportunities (upcoming meetings, public comment periods, votes). These are the findable, quotable, reusable atoms.

### Journey map

A temporal-experiential trace of the persona's experience through the meeting's narrative arc. Not just "what did they learn?" but "what was it like to sit through this meeting as this person?" The journey tracks the sequence of the meeting — the superintendent opens with the budget gap, the closure options are presented, Q&A gets heated — mapped to the persona's cognitive and emotional state at each beat. This requires understanding the meeting as a *narrative* with an arc, not a bag of facts.

### Unstructured reactions

The persona's voice: gut feelings, loose threads, things that don't fit neatly into structured categories. This is where Maria thinks "they pivoted from Skillin to Dyer with NO public discussion" and Tom thinks "3.3% sounds manageable but what happens after revaluation?" and Jaylen thinks "nobody asked a single student what we think." These reactions are the interpretive richness that makes the raw material worth having — they carry the persona's perspective in a way structured points cannot.

## Stage 3: Cumulative Fold

**Input:** New per-meeting interpretation + existing cumulative interpretation for each persona.

**Output:** Updated cumulative interpretation per persona.

**Approach:** Folding, not regeneration. Each new meeting's interpretation is integrated into the existing cumulative view:

- **What shifted** — facts, positions, or emotional states that changed because of this meeting
- **What's confirmed** — things that were uncertain before and are now established
- **What's superseded** — earlier understandings that turned out to be wrong or incomplete (e.g., "Skillin was the closure candidate" → superseded by "Dyer is the closure candidate")
- **Narrative arc** — how the persona's overall story has evolved (Maria went from "general anxiety about cuts" → "my school might close" → "my school IS closing and the decision was made without us")

The fold preserves temporal markers — recording *when* each persona's understanding shifted. This is itself valuable raw material: it captures not just the current state but the journey of understanding across the budget season.

The cumulative interpretation is the authoritative "where does this persona stand?" document at any point in time.

## Stage 4: Upcoming-Event Brief

**Input:** Current cumulative interpretation + inter-meeting evidence events (anything posted since the last meeting that hasn't been bundled yet) + known agenda/details for the upcoming meeting.

**Output:** One forward-looking brief per persona.

**Purpose:** Prepare the persona (and by extension, real stakeholders who match the persona) for the next meeting. The brief synthesizes:

- What happened since the last meeting (new documents, media coverage, public statements)
- Open questions from the cumulative interpretation that might be addressed
- Agenda items and what they mean for this persona
- Specific things to listen for or ask about

**Temporal constraint:** This brief has a real-world deadline — it must exist *before* the meeting it prepares for. This is the only stage with an external scheduling dependency.

**Sequencing:** The upcoming-event brief reads the cumulative interpretation (which reflects all meetings through the most recent one) plus any new inter-meeting evidence. It does not re-interpret past meetings; it builds forward from the current cumulative state.

## Data Flow Summary

```
                    Evidence Pool
                         │
                    Meeting Bundler
                         │
              ┌──────────┼──────────┐
              │          │          │    ... (× 14 personas)
              ▼          ▼          ▼
         Maria's    David's    Jess's
        per-mtg    per-mtg    per-mtg
       interpret.  interpret.  interpret.
              │          │          │
              ▼          ▼          ▼
         Maria's    David's    Jess's
       cumulative  cumulative  cumulative
           fold        fold        fold
              │          │          │
              ▼          ▼          ▼
         Maria's    David's    Jess's
        upcoming   upcoming   upcoming
          brief      brief      brief
```

## Output Artifacts

All outputs are raw material — intermediate artifacts, not publication-ready deliverables. They live in the project's data layer, not in `dist/`. Downstream consumers (briefings, prep guides, narrative timelines, visualizations) select from and format this material as needed.

The specific storage format, file structure, and naming conventions for these artifacts are implementation details to be resolved in child Epics and Specs.
