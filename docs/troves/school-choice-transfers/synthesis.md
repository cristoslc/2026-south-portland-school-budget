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

**Estimated non-public enrollment:**
- Total school-age (5-17, estimated): ~3,600-3,800 (adjusting the under-18 figure for ages 0-4)
- Public enrollment: 2,816
- Home instruction: 54
- **Gap (private + charter + inter-district transfers out):** ~730-930 students

**Caveat:** This is a rough estimate. The census age brackets don't align perfectly with school grades. The 5-year ACS data averages 2019-2024. Some of the "gap" may also be explained by pre-K age children in the under-18 count who aren't yet enrolled.

**Applying statewide rates as a cross-check:**
- Private school (8.9% statewide): ~320-340 students
- Charter school (1.2% statewide): ~43-46 students
- Homeschool (actual): 54 students
- **Total estimated non-public:** ~420-440 students
- **Residual (inter-district transfers or estimation error):** ~290-490 students

## Implications for Enrollment Modeling

1. **School choice is a meaningful enrollment driver.** An estimated 730-930 South Portland school-age children are not enrolled in South Portland public schools. This is 20-25% of the school-age population.

2. **The closure decision could increase outflow.** If families lose confidence in the district due to closure and reconfiguration, even a small increase in private school or inter-district transfer rates (e.g., 2% shift = ~70 students) would deepen the enrollment decline and reduce per-pupil state revenue.

3. **The cohort survival model should include a school choice sensitivity scenario.** SPEC-059 (scenario brackets) should model what happens if closure triggers 2-5% additional outflow to non-public options.

4. **Direct transfer data would strengthen this analysis.** A FOAA request to the district for superintendent agreement transfer counts (in and out) by year would provide the actual net transfer flow rather than this indirect estimation.

## Data Files

- Home instruction data extracted from Maine DOE Excel download (not saved as raw file — data captured in this synthesis)
- Census data from Census Reporter ACS 2024 5-year profile for South Portland (FIPS: 2371990)

## Gaps

- **Superintendent agreement transfer counts** (in and out) — requires FOAA request
- **Private school enrollment by sending town** — not publicly reported
- **Charter school enrollment by sending district** — Maine DOE charter enrollment page was inaccessible
- **Net in-migration of students** (families moving to South Portland for schools) — not separable from census data
