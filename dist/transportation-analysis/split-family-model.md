# Split-Family Count Model

**Spec:** SPEC-060 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006
**Date:** 2026-03-31

---

## Summary

Under **Option A** (the administration's recommendation), an estimated **139-169 families** (18-24% of all elementary families) would have children in two different buildings simultaneously. Under **Variant C**, that number is **123-150 families** (16-21%). Under **Option B**, the number is **zero** — every family's children attend the same building.

This is the single most impactful metric for daily family logistics and has not been quantified by the district.

## Methodology

### Approach

For configurations that split grade bands across buildings (Option A, Variant C), families with children on both sides of the grade boundary must send children to two different schools. We estimate this using:

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
| Estimated total families | ~696-773 | Derived from enrollment and sibling rates |

### Grade Boundary Split Probability

For a family with two children in elementary school, the probability that one child is on each side of a grade boundary depends on where the boundary falls within the grade span:

- **Option A boundary (between grades 1 and 2):** 3 grades below (PreK, K, 1), 3 grades above (2, 3, 4) → probability = 0.60
- **Variant C boundary (between grades 2 and 3):** 4 grades below (PreK, K, 1, 2), 2 grades above (3, 4) → probability = 0.53
- **Option B:** No boundary → probability = 0.00

Option A's boundary falls closer to the middle of the grade span, maximizing the number of families affected.

## Results

### Configuration Comparison

| Metric | Option A | Option B | Variant C |
|--------|:--------:|:--------:|:---------:|
| Grade bands | PreK-1 / 2-4 | K-4 (unified) | PreK-2 / 3-4 |
| Boundary split probability | 0.60 | 0.00 | 0.53 |
| **Split families (range)** | **139-169** | **0** | **123-150** |
| **As % of all families** | **18-24%** | **0%** | **16-21%** |
| Students on "lower" side | 449 | — | 667 |
| Students on "upper" side | 622 | — | 404 |

### What This Means in Practice

**Option A:** On any given school morning, roughly **one in five** elementary families would need to get children to two different buildings with potentially different start times. For a single-parent household or a family with one car, this means two drop-offs, two pick-ups, and mismatched schedules — every day for the years their children span the grade boundary.

**Variant C:** Slightly fewer families are split (~12% fewer than Option A) because the boundary falls higher, and fewer students are in grades 3-4 than in the PreK-1 range. But the impact is still substantial: roughly **one in six** families face split logistics.

**Option B:** Zero families face this issue. Every child attends the same K-4 building as their siblings. This is the structural advantage of not splitting grade bands across buildings.

### Sensitivity Analysis

The estimates are most sensitive to the multi-child family rate. If South Portland's rate differs from national averages:

| Multi-child rate | Option A split families | Variant C split families |
|:----------------:|:-----------------------:|:------------------------:|
| 25% (low) | ~115 | ~102 |
| 30% | ~139 | ~123 |
| 35% (midpoint) | ~155 | ~137 |
| 40% | ~169 | ~150 |
| 45% (high) | ~181 | ~161 |

Even at the low end of the range (25% multi-child rate), Option A still creates over 100 split families.

## Limitations

1. **No family-level data:** We cannot identify specific families — only estimate aggregate counts using demographic rates.
2. **National sibling rates:** South Portland's multi-child family rate may differ from national averages. Maine's household composition trends slightly toward smaller families, which would push estimates lower.
3. **Uniform grade-gap assumption:** If sibling grade gaps cluster at 1-2 years (common for closely spaced children), the split probability could be higher for Option A (where the boundary is at grade 1-2) and lower for Variant C.
4. **PreK is optional:** Some PreK families may not continue in the system; including them slightly inflates the Option A and Variant C numbers.
5. **Opt-out behavior:** Some families facing split logistics may choose private school, homeschooling, or voluntary transfers — reducing the count but representing a different kind of harm.

## Data Sources

- Enrollment by grade: `docs/troves/school-geography/schools.json` (2025-26 data)
- Sibling co-enrollment rates: Census Bureau Survey of Income and Program Participation (SIPP); NCES Condition of Education tables
- Calculation script: `pipeline/transport/split_family.py`
- Machine-readable output: `data/split-family-model.json`

## Invitation to Improve

The district has family-level enrollment data that would replace these estimates with exact counts. If the district provides the number of families with children spanning relevant grade boundaries, these estimates can be refined or replaced. The methodology and assumptions are fully transparent so that any correction can be applied directly.
