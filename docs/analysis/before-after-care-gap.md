# Before/After Care Gap Analysis

**Spec:** SPEC-064 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006
**Date:** 2026-03-31

---

## Summary

Reconfiguration creates new before/after care demand for families split across buildings. Under the **worst-case 4-tier scenario for Option A**, an estimated **118-144 families** face new care needs, creating an aggregate annual cost burden of **$404,000-$804,000** — borne by families, not the district budget.

A critical finding: **after-school care is already FULL at 4 of 5 elementary schools**. The only school with openings is Kaler — the one proposed for closure. Closing Kaler eliminates the only existing care capacity headroom while simultaneously creating new demand.

## Care Infrastructure in South Portland

### SoPo Kids Club (City-Run Program)

The South Portland Recreation Department operates "SoPo Kids Club" inside all five elementary school gyms for grades K-4.

| Service | 5 days/week | 3 days/week |
|---------|:-----------:|:-----------:|
| Before care only (7:00-9:00 AM) | $75/week | $54/week |
| After care only (3:00-6:00 PM) | $95/week | $66/week |
| Before + after care | $155/week | $105/week |

**Annual cost (36 school weeks):** $3,420 (after only) to $5,580 (before + after) per child.

**Source:** [SoPo Kids Club registration](https://southportlandme.myrec.com/info/activities/program_details.aspx?ProgramID=31539)

### Capacity Crisis

As of March 2026, after-school care enrollment status:

| School | After Care Status | Before Care Status |
|--------|:-----------------:|:------------------:|
| Brown | **FULL** | **FULL** |
| Dyer | **FULL** | Available |
| Skillin | **FULL** | Available |
| Small | **FULL** | Available |
| **Kaler** | **Available** | Available |

**The only school with after-care openings is the one proposed for closure.**

This means:
1. Current care demand already exceeds supply at 4 of 5 schools
2. Closing Kaler removes the only remaining capacity
3. Reconfiguration then adds NEW demand from split-building families
4. There is no plan to expand care capacity to meet this demand

### Other Providers

- **Boys & Girls Club of Southern Maine (South Portland):** After-school only (3:00-6:00 PM). Transportation from Small and Brown only. Annual membership model — rates not published.
- **YMCA of Southern Maine:** No school-age care programs in South Portland or Portland area.
- **Private providers:** St. Brigid School (Portland) at $115/week full-time after care as a comparable.

The SoPo Kids Club is effectively the only universal option for South Portland elementary families, and it's at capacity.

## Care Gap by Configuration

### How the Gap Emerges

**Under 3 tiers (all elementary same start time):** Split families still face logistics burden — two different buildings, two drop-offs/pick-ups. About 30% of split families would need additional care to manage the logistics (e.g., using after care at one school to bridge the gap while picking up at the other).

**Under 4 tiers (different start times for grade bands):** Nearly all split families (85%) face a hard scheduling conflict. If primary starts at 8:50 and intermediate at 9:20, a parent cannot be at two buildings simultaneously. One child needs before-care or after-care to cover the gap.

### Results

| Configuration | Scenario | New families needing care | Annual cost burden (aggregate) |
|---------------|----------|:-------------------------:|:------------------------------:|
| **Option A** | 3 tiers | 42-51 | $144,000-$285,000 |
| **Option A** | 4 tiers | 118-144 | **$404,000-$804,000** |
| **Option B** | 3 tiers | 0 | $0 |
| **Variant C** | 3 tiers | 37-45 | $127,000-$251,000 |
| **Variant C** | 4 tiers | 105-128 | $359,000-$714,000 |

### Who Bears the Cost

This is a **transferred cost**, not a savings. The district budget shows reconfiguration saving $1.5-2.2M. But the care costs created by reconfiguration are pushed to families:

- Under Option A (4-tier): families collectively absorb $404,000-$804,000 in new annual care costs
- Per family: $3,420-$5,580/year additional
- This is effectively a **$3,400-$5,600 annual "reconfiguration tax"** on 118-144 working families

Under Option B, this transferred cost is zero.

## The Kaler Paradox

Closing Kaler creates a particularly damaging interaction:

1. Kaler is the only school with care openings
2. Closing Kaler eliminates those openings
3. Kaler's 135 students are redistributed to Brown, Dyer, Small, and Skillin — all of which are already at care capacity
4. Some redistributed families will need care at their new school, where the waitlist is already full
5. Under Option A/Variant C, additional families face new care needs from grade-band splits

The net effect: **care demand increases while care supply decreases**. This is the opposite of what a transition plan should do.

## 57% Were Right to Worry

The administration's own survey (TC-011) found that 57% of parents cited before/after care disruption as a concern. This analysis validates that concern:

- After care is already full
- The only school with openings is being closed
- Reconfiguration creates 37-144 new families needing care (depending on configuration)
- No care expansion plan has been announced
- The care costs are borne entirely by families

## Limitations

- Care gap rate estimates (30% for 3-tier, 85% for 4-tier) are modeled, not surveyed
- Not all affected families would choose paid care — some have informal networks (family, neighbors)
- Cost estimates use city program rates; private alternatives may cost more or less
- Waitlist depth at full schools is unknown — actual unmet demand may be higher
- Analysis covers the SoPo Kids Club as the primary provider; Boys & Girls Club capacity not quantified
- Does not include summer care transition costs

## Data Sources

- Care rates: [SoPo Kids Club](https://southportlandme.myrec.com/info/activities/program_details.aspx?ProgramID=31539) (verified 2026-03-31)
- Split-family counts: `docs/analysis/split-family-model.md` (SPEC-060)
- Bell schedule tiers: `docs/analysis/bell-schedule-analysis.md` (SPEC-063)
- Parent survey data: TC-011 (transportation claims catalog)
- Calculation script: `pipeline/transport/care_gap.py`
- Machine-readable output: `data/before-after-care-gap.json`

## Invitation to Improve

The Recreation Department can provide actual waitlist numbers for each school, which would replace the "FULL" binary with quantified unmet demand. The district can provide data on current care usage rates and family compositions that would refine the gap estimates. If the district plans to expand care capacity as part of reconfiguration, that information would directly improve this analysis.
