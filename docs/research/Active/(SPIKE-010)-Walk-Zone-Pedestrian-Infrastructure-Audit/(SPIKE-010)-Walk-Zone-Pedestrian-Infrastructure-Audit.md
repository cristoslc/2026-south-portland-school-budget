---
title: "Walk Zone & Pedestrian Infrastructure Audit"
artifact: SPIKE-010
track: container
status: Active
author: cristos
created: 2026-03-30
last-updated: 2026-03-31
question: "How does the current walk zone policy compare to state minimums and actual pedestrian infrastructure, and how does reconfiguration change the walker/rider classification?"
gate: Pre-MVP
risks-addressed:
  - Walk zone policy may classify students as walkers who cannot safely walk due to infrastructure gaps (I-295, missing sidewalks, winter conditions)
  - Reconfiguration changes which students are within walk distance, potentially reclassifying riders as walkers or vice versa
evidence-pool: ""
linked-artifacts:
  - INITIATIVE-006
  - EPIC-030
---

# Walk Zone & Pedestrian Infrastructure Audit

## Summary

<!-- Populated on transition to Complete -->

## Question

How does the current walk zone policy compare to state minimums and actual pedestrian infrastructure, and how does reconfiguration change the walker/rider classification? Specifically:

1. **Policy baseline:** What is South Portland's current walk zone distance by grade level? How does it compare to Maine state minimums?
2. **Infrastructure reality:** Where do walk zones cross I-295, major arterials without sidewalks, or areas with documented winter pedestrian safety issues?
3. **Reconfiguration impact:** Under each of the three configurations (Option A, Option B, Variant C), how many students shift from walker to rider or rider to walker?
4. **Hazard busing:** Does the district have hazard busing designations? If so, which areas, and are they affected by reconfiguration?

## Go / No-Go Criteria

- **Go:** Walk zone policy is publicly documented AND pedestrian infrastructure data (sidewalk maps, crossing data) is obtainable from city GIS or public works.
- **No-Go:** Walk zone policy is not publicly documented AND the district does not respond to inquiries within the spike timeframe.

## Pivot Recommendation

If walk zone policy details are unobtainable, use Maine state minimums as the baseline and document the gap. Note that the district may have more permissive walk zones than state law requires — the analysis would represent a conservative (minimum busing) estimate.

## Findings

### 1. South Portland Walk Zone Policy

**STATUS: NOT PUBLICLY DOCUMENTED ONLINE**

The SPSD transportation page (https://www.spsdme.org/page/transportation) and Bus FAQ page (https://www.spsdme.org/page/faq) render as JavaScript-only apps that did not yield readable policy text via web scraping. The SPSD policy manual (https://www.spsdme.org/o/policy) is similarly JavaScript-gated.

No walk zone distances were found in any publicly-accessible SPSD document. The district website mentions that schools are "within walking distance for many of our students" but does not define the threshold.

**Comparable reference — Portland Public Schools (neighboring district):**
- Kindergarten: 0.5 miles
- Grades 1-5: 1.0 mile
- Middle school: 2.0 miles
- High school: 2.0 miles
- Safety-based exceptions exist for high-traffic corridors and intersections

Source: https://www.portlandschools.org/about/board-of-education/board-policies/policy/~board/book-e/post/eea-r-procedures-for-the-transportation-of-students

**Next step:** File a request with SPSD Transportation at (207) 767-7714 or submit a public records request for the district's transportation eligibility policy (likely policy code EEA or EEAA in the school board manual). The policy manual may be accessible in person or via direct request even though the website is JavaScript-gated.

### 2. Maine State Law on Student Transportation

**Maine Title 20-A, Section 5401** governs student transportation.

Key provisions:
- **No statewide walk distance minimum.** The statute does NOT set a specific mileage threshold. Instead, it says school boards "shall provide transportation for elementary school students...a part of or the whole distance to and from the nearest suitable school."
- **Board discretion (subsection 11):** "A school board may establish the distance from a school that students must reside to receive transportation." This explicitly delegates walk zone decisions to local boards.
- **Remote location exception (subsection 7):** Parents are responsible for getting students to a public highway if they live in a location "remote from and inaccessible to schools or public highways."
- **One specific threshold:** Students temporarily residing on state property qualify for transportation if living "more than 2 miles from the school."
- Secondary transportation is more discretionary — boards "may" rather than "shall" provide it in some cases.

**Implication:** Maine law gives SPSD full discretion to set walk zone distances. There is no state floor to compare against — the Portland distances (0.5/1.0/2.0 miles) represent one local choice, not a state mandate.

Source: https://www.mainelegislature.org/legis/statutes/20-a/title20-asec5401.html

**Regulatory framework:** Maine DOE regulations are in 05-071 CMR Chapter 83 (School Transportation Operations Program) and Chapter 81 (School Transportation Safety), available via https://www.maine.gov/doe/schools/transportation/laws. These rules govern operational standards but do not set walk distance minimums.

**Recent development:** Governor Mills signed an executive order in January 2026 establishing the Maine School Transportation Safety Commission following two student transportation deaths. This commission is reviewing current laws and practices and may produce new guidance.

Source: https://www.maine.gov/governor/mills/official_documents/executive-orders/2026-01-order-establishing-maine-school-transportation-safety

### 3. I-295 Crossings in South Portland

I-295 runs through South Portland roughly north-south, separating the Maine Mall / western commercial area from the eastern residential neighborhoods. The highway enters South Portland from Scarborough at Exit 1 and continues north through Exit 3 (Westbrook Street/Broadway) and Exit 4 (Route 1/Veterans Memorial Bridge) before crossing the Fore River into Portland.

**Identified crossing points (vehicular roads that bridge over or under I-295):**

1. **Exit 1 area / Maine Turnpike access road:** East-west freeway connector between US 1 (Main Street) and I-95. Provides access to West Broadway. This is a highway interchange — not pedestrian-friendly.

2. **Exit 3 / Westbrook Street & Broadway intersection:** Westbrook Street crosses over/near I-295 at this interchange. The Bike-Pedestrian Committee has recommended an off-road trail along Westbrook Street, beneath the I-295 overpass, across Broadway to Wescott Road (where the SPSD central office is located). A 2025 Westbrook Street Road Safety Demonstration Project tested pedestrian safety improvements at MacArthur Circle West in the Maine Mall area. Broadway/Westbrook Street intersection has a $300,000 PACTS-funded pedestrian safety improvement project in the 2026 work plan (project 030308.00).

3. **Exit 4 / Route 1 overpass:** Currently under a $12.4 million reconstruction project (started March 2025, duration 1+ year) to make the overpass two-way and add southbound I-295 access. The pre-project ramp carried traffic over I-295 on a bridge that is being rebuilt. Pedestrian accessibility during and after construction is uncertain.

4. **Bridge #6258 over I-295:** Referenced in the MaineDOT work plan — Route 701SB begins at this bridge. This is in the northern part of South Portland near the Portland line.

**Critical finding:** There are NO dedicated pedestrian overpasses or underpasses across I-295 in South Portland. All crossings are vehicular road bridges at highway interchanges. The Bike-Ped Committee's recommended trail under the I-295 overpass at Westbrook Street has not yet been built.

**Broadway is the key bottleneck:** Broadway carries 24,240 vehicles daily at its worst section (1,000-foot, four-lane bottleneck between Evans and Lincoln streets). Multiple MaineDOT projects are aimed at relieving Broadway congestion and improving pedestrian safety along it.

Sources:
- Press Herald, 2018: https://www.pressherald.com/2018/07/30/on-broadway-traffic-frustrates-as-south-portland-pursues-solutions/
- Press Herald, March 2025: https://www.pressherald.com/2025/03/15/long-term-road-project-will-detour-traffic-at-veterans-bridge-and-i-295/
- MaineDOT Work Plan 2026-2028: https://www.maine.gov/dot/sites/maine.gov.dot/files/documents/workplan/towns/SouthPortland.pdf
- Westbrook Street demo project: https://southportland.org/m/newsflash/home/detail/348

### 4. South Portland Sidewalk & Pedestrian Infrastructure

**No comprehensive sidewalk inventory or pedestrian master plan was found.**

What does exist:
- **City GIS Hub:** https://city-of-south-portland-southportland.hub.arcgis.com/ — provides general mapping but no sidewalk-specific layer was identified.
- **AxisGIS property viewer:** https://www.axisgis.com/South_PortlandME/ — includes streets, topography, city infrastructure layers. May contain sidewalk data in its layers but this requires interactive exploration.
- **ArcGIS Comprehensive Plan maps:** https://www.arcgis.com/apps/webappviewer/index.html?id=3c82c619da2f4d02ae3960adab2db764 — land use policy areas and zoning, not pedestrian infrastructure.
- **Bicycle-Pedestrian Committee:** Active committee (https://southportland.org/our-city/board-and-committees/bike-ped-committee) with annual reports. The 2023 annual report mentions leveraging AFSP and AARP grants. Committee agendas and Broadway Corridor Projects are linked.
- **Streets & Sidewalks ordinance:** Chapter 23 of city code covers street/sidewalk regulations (https://www.southportland.gov/DocumentCenter/View/1439/CH-23-Streets-and-Sidewalks).
- **Street Design Technical Manual:** Available in the city document center.
- **South Portland 2040 Comprehensive Plan:** Currently in draft (updated July 2025). Studio Luz Architects analyzed vehicle and pedestrian networks as part of the planning process. The Bike-Ped Committee held workshops on how bicycle/pedestrian safety should be treated in the new plan.

**MaineDOT-funded pedestrian projects in South Portland (2026-2028 Work Plan):**

| Project ID | Location | Description | Year | Funding |
|------------|----------|-------------|------|---------|
| 018638.00 | Lincoln Street / Greenbelt Pathway | New bike/ped sidewalk/trail from Evans St to Billy Vachon Dr (0.96 mi) | 2026 | $2,750,000 |
| 024333.00 | Various locations | Priority Corridor Pedestrian-Bicyclist Safety and Access | 2026 | $625,000 |
| 027356.00 | Broadway | Pedestrian safety improvements, Rt 77 to 1.37 mi NE, multiple crossings | 2026 | $1,450,000 |
| 028534.05 | Running Hill Road | New sidewalk/trail from Maine Mall Road west 0.05 mi | 2026 | $200,000 |
| 030273.00 | Citywide | Bike share station implementation | 2026 | $125,000 |
| 030308.00 | Broadway/Westbrook Street | Intersection pedestrian safety improvements (PE only) | 2026 | $300,000 |

**Total pedestrian/bicycle infrastructure investment 2026-2028: ~$5.45M** (excluding bike share)

**Gap:** The city does not appear to publish a formal sidewalk inventory or completeness map. The South Portland 2040 process may produce one, but it is not yet available. The Cash Corner Traffic Calming Study (2022) and Cushing's Point Broadway Corridor Transportation Study (2022) may contain relevant pedestrian data but are not available online.

### 5. Hazard Busing

**STATUS: NO EVIDENCE OF FORMAL HAZARD BUSING DESIGNATIONS IN SOUTH PORTLAND**

Maine state law does not use the term "hazard busing" or "hazardous walking route." The statutory framework (Title 20-A, Section 5401) delegates all walk distance decisions to local school boards without requiring hazard designations.

Other Maine districts (e.g., MSAD 75/RSU 75) do reference "hazardous walking conditions, as determined by the Director of Transportation or Superintendent of Schools" in their policies — but this is a local policy choice, not a state mandate.

The concept of hazard busing is well-established nationally (particularly in states like Pennsylvania, Connecticut, and New Jersey where it has specific statutory meaning). In Maine, the equivalent mechanism is simply the school board's discretion under Section 5401(11) to set distance thresholds and make exceptions.

**Relevance to South Portland:** Even without a formal "hazard busing" label, any areas near I-295, Broadway (24,240 daily vehicles), or other high-traffic corridors would likely need bus service regardless of distance if students cannot safely walk. The absence of a formal hazard designation does not mean the district ignores safety — it may simply handle it informally through route design.

**Next step:** Ask SPSD Transportation directly whether they maintain any hazardous walking route designations or safety-based transportation exceptions beyond the standard distance threshold.

### Data Gaps & How to Fill Them

| Gap | How to Obtain | Priority |
|-----|---------------|----------|
| SPSD walk zone distances by grade | Call Transportation at (207) 767-7714 or FOIA/public records request | **Critical** |
| SPSD hazard busing designations | Same call/request as above | High |
| Sidewalk inventory / completeness map | Contact Public Works at (207) 767-7635 or explore AxisGIS layers interactively | High |
| Cash Corner Traffic Calming Study (2022) | Request from Planning Department | Medium |
| Cushing's Point Broadway Corridor Study (2022) | Request from Planning Department | Medium |
| South Portland 2040 draft transportation chapter | Available at southportland2040.com (check latest CPC meeting materials) | Medium |
| Winter sidewalk plowing routes/coverage | Contact Public Works | Medium |

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-30 | — | Created as child of EPIC-030 under INITIATIVE-006; user-approved |
| Active | 2026-03-31 | — | Web research pass: state law, I-295 crossings, MaineDOT projects, ped infrastructure. SPSD walk zone policy NOT publicly available — requires direct inquiry. |
