---
title: "Comparable District Transport Impact — Sanford & Biddeford School Closures"
artifact: SPIKE-001
track: container
status: Active
author: Cristos L-C
created: 2026-03-31
last-updated: 2026-03-31
question: "Do Maine DOE transport expenditure trends for Sanford and Biddeford show measurable cost increases following elementary school closures, and if so, what magnitude validates or challenges our $855K route expansion estimate for Option A?"
parent-initiative: INITIATIVE-006
gate: Pre-decision
risks-addressed:
  - Route expansion cost estimate ($855K) is the largest and weakest component of the INITIATIVE-006 fiscal exposure analysis
  - Linear cost scaling assumption may over- or underestimate real fleet economics
evidence-pool: ""
---

# Comparable District Transport Impact — Sanford & Biddeford School Closures

## Summary

<!-- Final-pass section: populated when transitioning to Complete. -->

## Question

Do Maine DOE transport expenditure trends for Sanford and Biddeford show measurable cost increases following elementary school closures, and if so, what magnitude validates or challenges our $855K route expansion estimate for Option A?

### Sub-questions

1. **When did each district close an elementary school?** What year, which school, and what reconfiguration model (redistrict vs. grade-band)?
2. **What does the DOE per-pupil transport expenditure trend show?** Pull FY20-FY25 for both districts. Is there a visible inflection around the closure year?
3. **Can we isolate the closure effect?** Enrollment changes, inflation, and contract renegotiations all affect transport costs. Can we control for these using the peer group baseline or state average trend?
4. **What's the implied route expansion cost?** If transport per-pupil jumped X% post-closure while the state average moved Y%, the delta (X-Y)% applied to South Portland's $2.99M baseline gives a comparables-derived estimate to check against our model's $855K.

## Go / No-Go Criteria

| Criterion | Threshold | Measure |
|-----------|-----------|---------|
| Data availability | FY20-FY25 per-pupil transport data obtainable for both districts | Maine DOE resident expenditure reports |
| Closure event identified | At least one district has a confirmed elementary closure with known year | News sources, district records |
| Signal extractable | Transport cost trend shows a distinguishable pattern vs. state average around closure year | Delta exceeds 5% year-over-year vs. peer baseline |

**Go:** Comparable data produces a transport cost delta that either (a) corroborates our estimate within 50% or (b) provides a credible alternative multiplier.
**No-Go:** Data is too noisy, closures can't be dated, or confounding variables (e.g., simultaneous contract changes) make the signal uninterpretable.

## Pivot Recommendation

If the comparable district approach fails to produce interpretable signal:
- Fall back to **sensitivity analysis** — present the route expansion estimate as a range (0.5x to 1.5x of current $855K) with explicit documentation that no comparable validation was possible.
- Alternatively, check **Gorham** (closest peer by size at 2,815 students) for any recent school reconfigurations.

## Research Plan

### Phase 1: Event identification
- Confirm Sanford and Biddeford elementary closure dates, schools involved, and reconfiguration models
- Sources: news archives, district websites, school board minutes

### Phase 2: DOE data pull
- Pull Maine DOE resident expenditure per-pupil reports for FY20-FY25
- Extract transport line for: Sanford, Biddeford, South Portland, state average
- Also pull enrollment counts for normalization

### Phase 3: Analysis
- Plot transport per-pupil trends for closure districts vs. state average
- Compute closure-year delta (district trend minus state trend)
- Apply delta to South Portland's baseline to derive comparables-based route expansion estimate
- Compare to model-derived $855K

### Phase 4: Write-up
- Document findings with data tables and trend comparison
- State whether the comparable data supports, challenges, or is inconclusive regarding the model estimate

## Findings

### Phase 1: Event Identification (Complete)

**Sanford** — Closed Emerson, Willard, and Lafayette elementary schools in 2013-2014. Consolidated into a new centralized elementary school. This is a proximity-based redistricting model (comparable to South Portland Option B, not Option A).

**Biddeford** — JFK Memorial School closing 2025-2026. New wing at Biddeford Primary School opening spring 2026. This is an active transition — no post-closure DOE data exists yet. Not usable for before/after comparison.

**Implication:** Sanford is the only viable comparable, but the closure was 10+ years ago. FY23-25 DOE data shows the long-run equilibrium, not the immediate shock. Earlier data (FY14-FY17) would be needed to capture the closure-year impact. Those reports are not currently on the Maine DOE website (only FY23-FY25 available).

### Phase 2: DOE Data Pull (Complete)

Source: Maine DOE "Resident Expenditures by Budget Category" reports, FY23-FY25.

**Transport Per-Pupil Expenditure:**

| District | FY23 | FY24 | FY25 | FY23-25 % | vs State |
|----------|------|------|------|-----------|----------|
| State Total | $989 | $1,015 | $1,093 | +10.5% | baseline |
| **South Portland** | **$709** | **$940** | **$1,065** | **+50.2%** | **+39.7pp** |
| Sanford | $688 | $747 | $816 | +18.6% | +8.1pp |
| Biddeford | $737 | $802 | $899 | +22.0% | +11.5pp |
| Portland | $651 | $775 | $626 | -3.9% | -14.4pp |
| Scarborough | $601 | $630 | $691 | +14.8% | +4.3pp |
| Cape Elizabeth | $696 | $674 | $844 | +21.2% | +10.7pp |
| Gorham | $830 | $888 | $946 | +14.1% | +3.6pp |
| Westbrook | $757 | $798 | $986 | +30.4% | +19.9pp |
| Yarmouth | $742 | $683 | $825 | +11.3% | +0.8pp |

**Total Transport Spending (per-pupil x enrollment):**

| District | FY23 | FY25 | Change |
|----------|------|------|--------|
| South Portland | $2.18M | $2.99M | +37.3% |
| State average | — | — | +11.7% |

Data saved to: `data/transport-per-pupil-multiyear.csv`

### Phase 3: Analysis (In Progress)

#### Unexpected finding: South Portland transport cost anomaly

South Portland's transport per-pupil costs rose **50.2% in two years** (FY23 $709 → FY25 $1,065) — nearly 5x the state average increase of 10.5%. Meanwhile, enrollment **fell 8.6%** (3,074 → 2,810). Total spending rose 37.3% ($2.18M → $2.99M).

This is the largest per-pupil transport increase in the peer group by a wide margin. The next closest is Westbrook at +30.4%.

**Possible explanations (requires further investigation):**
1. New bus contract or contract renegotiation
2. Fuel cost pass-throughs hitting smaller districts harder
3. Special education transport cost increases
4. Route structure changes already underway
5. Reporting methodology change in how costs are categorized

**Impact on INITIATIVE-006 analysis:**
- The $2.99M baseline used in the route expansion estimate is already anomalously high vs. FY23
- If the FY23 baseline ($2.18M) is more representative of "normal" transport costs, the route expansion estimate should use that instead — reducing the $855K estimate proportionally
- Alternatively, if costs are rising due to structural factors (e.g., contract terms), the FY25 baseline is correct and route expansion would compound on top of already-rising costs

#### Sanford long-run signal

Sanford's FY23-25 transport trend (+18.6%) is 8.1pp above the state average — suggesting that school closures may create a modest long-run transport premium. However:
- The closures were proximity-based (new centralized school), not grade-band (Option A), so the comparison is imperfect
- 10+ years of compounding makes it impossible to isolate the closure effect from other factors
- Need FY14-FY17 data for the immediate impact, but Maine DOE only posts recent years online

### Remaining Work

- [ ] Attempt to locate FY14-FY17 DOE reports for Sanford closure-year impact (may require FOAA or Wayback Machine)
- [ ] Investigate South Portland FY23→FY25 transport cost spike — what caused the 50% increase?
- [ ] Determine whether the route expansion model should use FY23 or FY25 as baseline

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-31 | — | Created — user-requested spike for [INITIATIVE-006](../../initiative/Active/(INITIATIVE-006)-Independent-Transportation-Analysis/(INITIATIVE-006)-Independent-Transportation-Analysis.md) reliability strengthening |
