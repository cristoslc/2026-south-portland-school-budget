# Bell Schedule Tier Analysis

**Spec:** SPEC-063 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006
**Date:** 2026-03-31

---

## Summary

South Portland currently operates a **3-tier bus system**: high school (8:10 AM), middle school (8:30 AM), elementary (9:05 AM). All five elementary schools share the same bell schedule, allowing a single fleet to run three passes.

**Option B** preserves this 3-tier structure with no complications. **Option A** and **Variant C** introduce grade-band splits that create pressure toward a 4th tier — a configuration that most comparable districts cannot sustain with a single fleet. If forced to 4 tiers, split families face 30-minute scheduling gaps between buildings.

## Current Bell Schedule

| Tier | Level | Start | End | Schools |
|:----:|-------|:-----:|:---:|---------|
| 1 | High School | 8:10 AM | 2:25 PM | SPHS |
| 2 | Middle School | 8:30 AM | 2:45 PM | SPMS |
| 3 | Elementary | 9:05 AM | 3:05 PM | Brown, Dyer, Kaler, Small, Skillin |

**Source:** [SPSD School Start & Dismissal Times](https://www.spsd.org/families/school-start-dismissal-times)

The 35-minute gap between middle school start (8:30) and elementary start (9:05) gives buses adequate turnaround time to complete middle school routes before starting elementary routes. This is a well-established pattern.

**Context:** The middle school currently operates two staggered start times (7:55 and 8:45) which the administration planned to consolidate — but deferred because it requires a $25K DOT traffic study and 6-12 months of permitting (TC-002, TC-013). This same standard was not applied to the elementary reconfiguration, which affects more students and more buildings.

## Configuration Analysis

### Option A: 2 Primary (PreK-1) + 2 Intermediate (2-4)

**Best case (3 tiers):** All 4 elementary buildings on the same 9:05 AM start. Buses serve both primary and intermediate buildings in one pass. Feasible if route times fit, but grade-band routing reduces efficiency — a bus serving Brown (intermediate, 2-4) can't also serve Dyer (primary, PreK-1) on the same run since children from the same neighborhood go to different buildings.

**Likely scenario (4 tiers):** Primary schools start at 8:50, intermediate at 9:20 (or similar split). This requires buses to run 4 passes instead of 3:

| Tier | Start | Level |
|:----:|:-----:|-------|
| 1 | 8:10 | High School |
| 2 | 8:30 | Middle School |
| 3 | 8:50 | Primary (PreK-1) |
| 4 | 9:20 | Intermediate (2-4) |

**Risks:**
- 4 tiers strain fleet capacity. Most comparable districts max out at 3.
- The earliest start (8:10) may need to move earlier, or the latest end later, to fit 4 tiers with adequate turnaround.
- Split families face a 30-minute gap between drop-offs at different buildings.

### Option B: 4 Buildings K-4

**3 tiers (same as current).** All buildings serve the same grades. Bus routing is conceptually identical to today minus one school. Wider catchments add some route time but don't change the tier structure.

| Tier | Start | Level |
|:----:|:-----:|-------|
| 1 | 8:10 | High School |
| 2 | 8:30 | Middle School |
| 3 | 9:05 | Elementary (K-4) |

**Risks:** Minimal. Wider catchments may push some routes to the edge of the tier window, but the structure is proven and operational.

### Variant C: 3 Buildings PreK-2 + 1 Building Grades 3-4

**Higher pressure toward 4 tiers than Option A.** The single grades 3-4 building draws students from the entire city. This creates routes that span the full geographic footprint of South Portland — including across I-295. These city-wide routes are fundamentally different from the neighborhood-based PreK-2 routes and are unlikely to share a tier efficiently.

**If forced to 4 tiers:** Same structure as Option A, with an additional complication: every grade 3-4 family is guaranteed to have a different building than their younger children's PreK-2 school. There is no "lucky" neighborhood that avoids the split.

## Tier Count Comparison

| Configuration | Likely Tiers | Change from Current | Split Family Scheduling Conflict |
|---------------|:------------:|:-------------------:|:--------------------------------:|
| **Option A** | 3-4 | +0 to +1 | 30-min gap if 4 tiers; none if 3 |
| **Option B** | 3 | 0 | None |
| **Variant C** | 3-4 | +0 to +1 | 30-min gap if 4 tiers; none if 3 |

## What a 4th Tier Means for Families

If Option A or Variant C requires 4 tiers:

1. **School day window expands:** The earliest start moves to ~8:10 AM (HS), the latest end to ~3:35 PM. The elementary school day stretches from 7:00 AM (before care) to 6:00 PM (after care) — an 11-hour window.

2. **Split-building families face mismatched schedules:** A family with a kindergartner at a primary school (8:50 start) and a 3rd grader at an intermediate school (9:20 start) must manage two different drop-off times 30 minutes apart, at two different buildings, five days a week.

3. **Before/after care demand increases:** Families who currently need care only because of work schedules now also need it because of sibling scheduling mismatches. See SPEC-064 for care gap quantification.

4. **Driver workday extends:** Four tiers means each bus driver covers more routes per day, potentially pushing into overtime or requiring additional drivers — counteracting the SEA staffing cuts analyzed in SPEC-062.

## The DOT Traffic Study Double Standard

The administration deferred middle school bell time consolidation because it requires a $25K DOT traffic study and 6-12 months of permitting (TC-002). The middle school consolidation affects one building.

The elementary reconfiguration affects four buildings, changes route structures, potentially adds a tier, and alters traffic patterns at multiple school sites. No equivalent traffic study has been mentioned, required, or budgeted for the elementary reconfiguration.

This is the same inconsistency identified in TC-013 of the transportation claims catalog.

## Limitations

- Tier feasibility is assessed qualitatively, not through route-level modeling
- Turnaround time between tiers (~25 minutes) is estimated for South Portland's geography
- Fleet size is unknown — analysis assumes the current fleet can handle 3 tiers
- The middle school bell time consolidation (deferred to fall 2027) could eventually free a tier
- Actual tier determination requires the routing analysis the district has not conducted

## Data Sources

- Current bell schedules: [SPSD website](https://www.spsd.org/families/school-start-dismissal-times) (verified 2026-03-31)
- School geography: `docs/troves/school-geography/schools.json`
- Transportation claims: `docs/troves/transportation-claims/claims.yaml`
- Calculation script: `pipeline/transport/bell_schedule.py`
- Machine-readable output: `data/bell-schedule-analysis.json`

## Invitation to Improve

The district's transportation team knows the current fleet size, route times, and tier constraints. With that data, the feasibility of 3 vs. 4 tiers under each configuration could be definitively assessed rather than estimated. The district has also budgeted for a transportation consultant ($60-125K per TC-012) who could perform this analysis — but the consultant has not been hired and no timeline has been set.
