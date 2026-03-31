# Enrollment Study Methodology

**Initiative:** INITIATIVE-005 | **Status:** In Progress

---

## Approach

The enrollment study uses publicly available data from federal (NCES), state (Maine DOE), and local (district budget documents, school board meetings) sources to independently verify and analyze enrollment trends.

## Data Sources

### NCES Common Core of Data (CCD)

The primary enrollment data source. CCD provides annual school-level enrollment counts by grade from the federal government's data collection.

- **Coverage:** All public schools in South Portland
- **Granularity:** Per-school, per-grade enrollment
- **Lag:** Typically 1-2 years behind current year
- **Location:** `data/enrollment/nces-enrollment-by-grade.csv`

### District Budget Documents

Enrollment figures cited in FY27 budget presentations and workshop materials.

- **Coverage:** District-level and building-level enrollment
- **Source:** Evidence pool synthesis (`docs/troves/fy27-budget-documents/synthesis.md`)
- **Limitation:** Figures may use different counting dates (October 1 vs. resident count) than NCES

### School Board Meetings

Enrollment claims, projections, and demographic discussions from public meetings.

- **Coverage:** Verbal claims and slide presentations
- **Source:** Evidence pool synthesis (`docs/troves/school-board-budget-meetings/synthesis.md`)

## Briefing Generation

Persona briefs are generated using the project's interpretation pipeline (`scripts/generate_briefs.py`), which:

1. Loads each persona definition from `docs/persona/Active/`
2. Loads cumulative interpretation state (per-persona narrative built from prior meetings)
3. Loads inter-meeting evidence (new documents since last briefing)
4. Generates a personalized brief via LLM (Claude, via Claude Max subscription)

The pipeline is documented in INITIATIVE-003 (Interpretation Pipeline).

## Limitations

- NCES data lags 1-2 years; current-year enrollment uses district-reported figures
- Enrollment projections (when produced) will use cohort survival modeling, which assumes trend continuation
- South Portland's position as a likely net student importer complicates standard demographic projection models
- The district's enrollment figures may use different counting methodology than NCES

## Reproducibility

Briefing generation: `python3 scripts/generate_briefs.py`
Enrollment data: `data/enrollment/`
