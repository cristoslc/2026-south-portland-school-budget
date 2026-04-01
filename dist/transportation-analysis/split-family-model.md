# Split-Family Count Model

**Spec:** SPEC-060 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006
**Date:** 2026-03-31 | **Version:** Post-decision — reflects 3/30/2026 board vote

---

## Summary

Under the **approved configuration** (Option A: primary PreK-1 / intermediate 2-4, passed 4-2 on March 30, 2026), an estimated **139-169 families** (18-24% of all elementary families) will have children in two different buildings simultaneously. The alternatives considered by the board — Variant C and Option B — are included for comparison. Under Variant C, that number would have been **123-150 families** (16-21%). Under Option B, it would have been **zero** — every family's children would have attended the same building.

This is the single most impactful metric for daily family logistics and has not been quantified by the district.

## Methodology

### Approach

The approved configuration splits grade bands across buildings — primary (PreK-1) and intermediate (2-4). Families with children on both sides of the grade boundary must send children to two different schools. We estimate the number of affected families using:

1. **Enrollment by grade** (2025-26 data from school-geography trove)
2. **Sibling co-enrollment rates** from Census Bureau SIPP surveys and NCES household composition research
3. **Grade boundary probability** — the likelihood that a multi-child family spans the specific grade boundary in a given year

### Key Assumptions

| Parameter | Value | Source |
|-----------|-------|--------|
| Multi-child family rate | 30-40% (midpoint 35%) | Census Bureau SIPP; NCES Condition of Education |
| Avg children per multi-child family | 2.3 | National elementary household data |
| Sibling grade-gap distribution | Approximately uniform across 1-5 years | Simplifying assumption |
| Total K-4 enrollment | 1,013 students | school-geography trove |
| Total with PreK | 1,071 students | school-geography trove |
| Estimated total families | ~705-771 (mid ~736) | Derived from enrollment and sibling rates |

### Grade Boundary Split Probability

For a family with two children in elementary school, the probability that one child is on each side of a grade boundary depends on where the boundary falls within the grade span:

- **Approved configuration boundary (between grades 1 and 2):** 3 grades below (PreK, K, 1), 3 grades above (2, 3, 4) — probability = 0.60
- **Variant C boundary (between grades 2 and 3):** 4 grades below (PreK, K, 1, 2), 2 grades above (3, 4) — probability = 0.533
- **Option B:** No boundary — probability = 0.00

The approved configuration's boundary falls closer to the middle of the grade span, maximizing the number of families affected.

## Results

### Configuration Comparison

| Metric | Approved (Option A) | Option B (considered) | Variant C (considered) |
|--------|:--------:|:--------:|:---------:|
| Grade bands | PreK-1 / 2-4 | K-4 (unified) | PreK-2 / 3-4 |
| Boundary split probability | 0.60 | 0.00 | 0.533 |
| **Split families (range)** | **139-169** | **0** | **123-150** |
| **As % of all families** | **18-24%** | **0%** | **16-21%** |
| Students on "lower" side | 449 | — | 667 |
| Students on "upper" side | 622 | — | 404 |

### What This Means in Practice

**Approved configuration (Option A):** On any given school morning starting fall 2026, roughly **one in five** elementary families will need to get children to two different buildings with potentially different start times. For a single-parent household or a family with one car, this means two drop-offs, two pick-ups, and mismatched schedules — every day for the years their children span the grade boundary.

**Variant C (considered but not selected):** Slightly fewer families would have been split (~12% fewer than the approved configuration) because the boundary falls higher, and fewer students are in grades 3-4 than in the PreK-1 range. The impact would still have been substantial: roughly **one in six** families facing split logistics.

**Option B (considered but not selected):** Zero families would have faced this issue. Every child would have attended the same K-4 building as their siblings. This was the structural advantage of not splitting grade bands across buildings.

### Sensitivity Analysis

The estimates are most sensitive to the multi-child family rate. If South Portland's rate differs from national averages:

| Multi-child rate | Approved config split families | Variant C split families |
|:----------------:|:-----------------------:|:------------------------:|
| 25% (low) | ~115 | ~102 |
| 30% | ~139 | ~123 |
| 35% (midpoint) | ~155 | ~137 |
| 40% | ~169 | ~150 |
| 45% (high) | ~181 | ~161 |

Even at the low end of the range (25% multi-child rate), the approved configuration still creates over 100 split families.

## Sources of Error

This model could be wrong in the following ways:

1. **Multi-child family rate is a national estimate.** Maine trends slightly toward smaller families. If South Portland's actual multi-child rate is 25% instead of 30-40%, the split count drops by roughly 15%. If it is higher (as it could be in a relatively affordable coastal city), the count rises.

2. **Uniform sibling grade-gap assumption.** If sibling grade gaps cluster at 1-2 years (common for closely spaced children), the approved configuration's split probability could be *higher* than 0.60 (since the boundary is at grade 1-2), while Variant C's could be *lower*. Non-uniform distributions could move estimates in either direction by 10-15%.

3. **PreK inclusion inflates the lower-side count.** PreK is optional and not all PreK families will continue. Excluding PreK families would reduce the approved configuration's lower-side count from 449 to approximately 390, modestly reducing the split estimate.

4. **No family-level data exists in this model.** We estimate aggregate counts using demographic rates, not individual family records. Any individual family's situation may differ from the statistical expectation.

5. **Opt-out behavior is unmodeled.** Some families facing split logistics may choose private school, homeschooling, or voluntary transfers. This would reduce the count but represents a different kind of harm — families leaving the system.

**What would fix it:** The district has family-level enrollment data. A query counting families with children spanning the relevant grade boundary would replace this entire model with an exact number.

## Data Sources

- Enrollment by grade: `docs/troves/school-geography/schools.json` (2025-26 data)
- Sibling co-enrollment rates: Census Bureau Survey of Income and Program Participation (SIPP); NCES Condition of Education tables
- Calculation script: `pipeline/transport/split_family.py`
- Machine-readable output: `data/split-family-model.json`

## Invitation to Improve

The district has family-level enrollment data that would replace these estimates with exact counts. If the district provides the number of families with children spanning relevant grade boundaries, these estimates can be refined or replaced. The methodology and assumptions are fully transparent so that any correction can be applied directly.

Community members with access to local demographic data (e.g., South Portland school registration records, PTA membership rolls) could also validate whether the 30-40% multi-child rate is reasonable for this community.
