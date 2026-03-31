# School Choice Transfer Flows — Synthesis

**Trove:** school-choice-transfers
**Date:** 2026-03-31
**Linked spec:** SPEC-052

---

## Data Availability

**District-level transfer data is not publicly available.** Maine DOE does not publish superintendent agreement transfer counts by district. The data exists in the NEO system but is not part of public reporting. A FOAA request to the district or to Maine DOE could yield this data but would take time.

**What IS available:**

1. **Home instruction counts by district** (Maine DOE, publicly downloadable)
2. **Census school-age population** (ACS 5-year estimates)
3. **NCES CCD public enrollment** (already in the project)
4. **Statewide rates** for private school (8.9%), charter school (1.2%), and homeschool (6.0%) participation

## Home Instruction (Homeschool) Data

South Portland home instruction students, from Maine DOE:

| Year | Students | Notes |
|------|:--------:|-------|
| 2020 | 36 | Pre-COVID baseline |
| 2021 | 72 | COVID spike (doubled) |
| 2022 | 52 | Partial return |
| 2023 | 35 | Below pre-COVID |
| 2024 | 46 | Slight uptick |
| 2025 | 46 | Stable |
| 2026 | 54 | Increasing — budget uncertainty? |

**Key observations:**
- COVID drove a temporary doubling (36 → 72) that has largely reversed
- FY26 shows a new uptick to 54 — coinciding with the budget crisis and closure discussions
- Home instruction represents ~2% of the school-age population — well below the statewide 6% rate
- South Portland's lower-than-average homeschool rate may reflect its diverse, lower-income demographics (homeschooling correlates with higher income and white demographics)

## Indirect Estimation: Public vs. Total School-Age Population

| Metric | Value | Source |
|--------|-------|--------|
| Under-18 population | 3,951 | Census ACS 2024 5-year |
| Ages 5-9 | ~2,159 (8.02%) | Census ACS 2024 5-year |
| Ages 10-19 | ~4,906 (18.23%) | Census ACS (includes 18-19) |
| Public school enrollment (K-12) | 2,816 | NCES CCD 2024-25 |
| Home instruction | 54 | Maine DOE 2025-26 |

**Estimated school-age population vs. enrollment (sensitivity analysis):**

The under-18 census count (3,951) includes ages 0-4, who are not school-age. The gap estimate is highly sensitive to the assumed under-5 share of population:

| Under-5 assumption | Est. school-age (5-17) | Public enrollment | Gap | Interpretation |
|:-------------------:|:---------------------:|:-----------------:|:---:|:---------------|
| 4.0% of pop | 2,873 | 2,816 | +3 | Breakeven — roughly 1:1 |
| 5.0% of pop | 2,604 | 2,816 | -266 | **Net importer** of students |
| 6.0% of pop | 2,335 | 2,816 | -535 | **Strong net importer** |

**Key finding: South Portland is likely a net importer of students, not a net exporter.** At reasonable under-5 assumptions (5-6% of population for a community with 20.7% seniors), public school enrollment *exceeds* the resident school-age population. This means more students are transferring IN to South Portland schools than transferring out — consistent with being a larger district with comprehensive programming adjacent to smaller towns.

**This changes the enrollment narrative.** The district's declining enrollment is not driven by families choosing to leave the district. It appears to be driven by demographic decline (fewer school-age children in the community) — which makes it more structural and harder to reverse through programmatic improvements.

**Applying statewide rates as a secondary estimate:**
- Private school (8.9% statewide): ~250-280 students out
- Charter school (1.2% statewide): ~34-38 students out
- Homeschool (actual): 54 students out
- **Total estimated outflow:** ~340-370 students
- **Implied inflow (to explain enrollment exceeding resident population):** ~480-750+ students from neighboring districts

**Caution:** This analysis uses ACS 5-year estimates (averaging 2019-2024), which may not reflect the most recent population changes. The age bracket misalignment between census (5-9, 10-19) and school grades (K-12) introduces uncertainty. These are order-of-magnitude estimates, not precise counts.

## Implications for Enrollment Modeling

1. **School choice outflow is NOT the primary enrollment driver.** South Portland appears to be a net receiver of students. The enrollment decline is demographic (fewer children), not behavioral (families leaving).

2. **But closure could change the equation.** Even if South Portland is currently a net importer, losing 2-3% of enrollment to outflow triggered by reduced confidence (~70-85 students) would be significant — especially if the students who leave are from families with the most options (higher income, car access).

3. **The cohort survival model should model this as a risk scenario.** SPEC-059 should include a "confidence shock" scenario: what happens if net inflow decreases or reverses after closure.

4. **Direct transfer data remains the gold standard.** A FOAA request to the district for superintendent agreement transfer counts (in and out) by year would replace this indirect estimation with actual numbers. The request should be straightforward — this is public data.

## Data Files

- Home instruction data extracted from Maine DOE Excel download (not saved as raw file — data captured in this synthesis)
- Census data from Census Reporter ACS 2024 5-year profile for South Portland (FIPS: 2371990)

## Gaps

- **Superintendent agreement transfer counts** (in and out) — requires FOAA request
- **Private school enrollment by sending town** — not publicly reported
- **Charter school enrollment by sending district** — Maine DOE charter enrollment page was inaccessible
- **Net in-migration of students** (families moving to South Portland for schools) — not separable from census data
