#!/usr/bin/env python3
"""Append Key Points sections to VTT transcript source files."""

import os

BASE_DIR = "/Users/cristos/Documents/projects/2026-south-portland-school-budget"
SOURCES_DIR = os.path.join(BASE_DIR, "docs/evidence-pools/city-council-meetings-2026/sources")

KEY_POINTS = {
    "001-council-meeting-2026-01-06.md": """
## Key Points

- Council entered executive session to discuss police/fire union contracts and Jetport tree-cutting agreement
- Toss the Tanks campaign urged council to create a working committee on Hill Street Tank Farm redevelopment as part of 2026 goals
- Resident proposed a public music/arts festival at Bug Light Park for September 2026 (pilot) and 2027 (larger city-partnered event)
- Cemetery management ordinance (Chapter 18) passed with amendment; council directed staff to create a public donation fund for cemetery maintenance
- Council rules amended regarding reconsideration motions and voting procedures
- City manager previewed upcoming meetings: Mahoney City Center Committee (Jan 13), housing ordinance updates, FY25 audit presentation (Feb 3), TI TIF extension (Feb 3), and budget guidance workshop with school board (Feb 10)
- Mayor noted school board chair DeAngelos announced a school budget citizen forum for January 22
- Mayor highlighted the statewide property tax relief task force, noting the first report was due in January with final report at year's end
- City council and city manager are monitoring state-level property tax reform efforts
""",

    "002-council-workshop-2026-01-13.md": """
## Key Points

- Mahoney City Center Committee presented its project recommendation to the council, with SMRT Architects providing cost estimates for the proposed city center and for refurbishing current city facilities
- The workshop covered the full history and process leading to the Mahoney recommendation, including the committee's December vote
- Housing ordinance updates presented by Planning Director Milan Neveda, covering state-mandated zoning changes
- Three specific questions posed to council regarding housing law implementation
- Two additional workshop proposals discussed: adding Central Fire Station to historic resources inventory, and changing dog off-leash hours at Willard Beach
- Public comment period drew significant community input on both Mahoney and housing topics
- Council provided guidance to city manager on Mahoney project direction and housing ordinance approach
""",

    "003-council-meeting-2026-01-20.md": """
## Key Points

- Working waterfront petition reported: 2,597 signatures collected (2,163 validated) from comprehensive plan workshop — met threshold for citizen initiative if formalized
- Economic Development Director presented 2025 Business Award winners, ceremony scheduled for February 25 at South Portland High School
- Miscellaneous zoning ordinance amendments passed (first reading) to comply with state housing law changes
- Council discussed density, multifamily housing, and streamlining development review processes in the context of state housing requirements
- Council continued filling committee/board appointment backlog
- Executive session held for real estate matter
""",

    "004-council-meeting-2026-02-03.md": """
## Key Points

- FY2025 financial audit presented: clean (unmodified) opinion, but material weakness in school department reconciliations (repeat finding); 34 audit journal entries (very high); ~$400K in grant funds moved to general fund due to ineligibility/overspending
- School department had six finance directors in five years; new director bringing stability and improved reconciliation procedures
- School budget was over-expended and non-compliant with legally adopted budget (repeat finding)
- City fund balance increased $5.8M, driven by auto excise tax over-collection ($1.7M) and staff vacancy savings; excess of ~$8.5M available for CIP
- Texas Instruments presented request for 20-year TIF extension under new state law (LD 1739); staff proposed combining TI TIF with expiring Growth Area and Transit TIFs into a new Mall Area TOD district
- TI TIF generates ~$1.2M/year; under extension, 75% must support transit-oriented development/affordable housing; CEA limited to 12.5% of property taxes
- Council adopted 2026 goals, including consideration of tank farm redevelopment
- Community safety resolution regarding federal immigration enforcement passed
- Coal storage zoning ordinance first reading
- School Board Chair DeAngelos urged council to provide clear budget guidance at Feb 10 joint meeting
- Poverty abatement request approved
""",

    "005-council-workshop-2026-02-10.md": """
## Key Points

- Joint council-school board budget guidance workshop — the pivotal budget meeting of the period
- Interim Superintendent Entwistle presented three budget scenarios: Option A (status quo, ~19% school tax increase), Option B (6% increase with $3.5M gap), Option C (9.8% increase with $1.1M gap)
- Enrollment declined from ~3,050 to 2,748 since 2017; 82 positions added in same period
- Three structural initiatives proposed: elementary reconfiguration ($2M savings), middle/high school efficiencies ($1M each)
- Elementary reconfiguration would create three intermediate schools (grades 2-4) and two primary schools (pre-K-1)
- Middle school start-time consolidation requires $25K DOT traffic study with 6-12 month permitting timeline
- Council guidance for school: range of 3-6%, majority gravitating toward 5-6%
- Councilor Walker was the outlier at 6%+ citing importance of education investment
- Councilor Matthews noted historically school increases never exceeded 3% during his 12-year board tenure
- City finance director outlined FY27 pressures: 10% health insurance increase, rising solid waste costs, 6.8% water rate increase, ARPA positions sunsetting
- School fund balance essentially zero; potential FY26 deficit may require city-side fund balance to cover temporarily
- Council guidance for city: 3-5% with majority at 4%; general opposition to new positions/programs unless revenue-neutral
- Councilor West proposed $2M/year capital building fund citing $194M in deferred capital needs
- Climate resilience overlay zone presented in second half of workshop
- Significant public comment on school budget: teachers' union president, parents, and taxpayers all voiced concerns
- Community tensions evident between need for education investment and taxpayer burden, especially for seniors on fixed incomes
""",

    "006-council-meeting-2026-02-17.md": """
## Key Points

- Immigration enforcement community impact dominated public comment — multiple residents described fear, inability to work, disrupted school attendance, and economic hardship among immigrant families
- Business microloan/grant program for ICE-affected businesses investigated via GP-COG survey; staff recommended not moving forward at this time due to insufficient South Portland-specific data
- TIF reserves identified as potential funding source for future business support programs
- PFML (Paid Family Medical Leave) state coverage transfer to private plan approved via consent calendar
- Committee annual reports continued from Feb 3 meeting
- Public comment included Walgreens Cash Corner closure concerns — last nearby pharmacy; resident urged thoughtful planning for the vacant space
- Bike/Ped Committee chair presented annual report highlights and urged council to reinstate practice of inviting committee chairs to present
- Council continued extensive appointment calendar backlog
- CDBG FY27 annual action plan discussed: ~$411K expected, including Broadway corridor pedestrian safety ($288K), domestic violence services, Meals on Wheels, homelessness prevention
""",

    "007-council-meeting-2026-03-05.md": """
## Key Points

- Mahoney/City Facilities/Public Safety Facilities workshop — council addressed four key questions on facility project direction
- Council eliminated library from Mahoney project scope (Order #155)
- Council directed staff to seek alternative police station locations outside Mahoney (Order #156); Cash Corner/Walgreens site mentioned as possibility
- Mahoney City Center Committee charge updated (Order #157)
- Central Fire Station historic inventory nomination discussed — inclusion would not prevent demolition
- Bond referendum for public safety facilities potentially targeted for November 2026
- Council open to split referendum and exploring other City Hall/Hamlin locations beyond A1++ option
- Temporary Emergency Rental Assistance proposal advanced for Mar 10 workshop: staff recommended $150K from undesignated fund balance to nonprofits
- Multiple residents testified about immigration enforcement impact and need for rental assistance
- CDBG Annual Action Plan approved ($411K): Broadway pedestrian safety, social services
- Bike/Ped Committee chair (Rosemary DeAngelos, also school board chair) presented annual report and urged committee recognition
- Budget workshop schedule confirmed: April 14 (School & misc.), April 28 (remaining depts.), May 12 (parking lot)
""",
}

for filename, key_points_text in KEY_POINTS.items():
    filepath = os.path.join(SOURCES_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Only add if not already present
    if "## Key Points" not in content:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(key_points_text)
        print(f"  Added Key Points to {filename}")
    else:
        print(f"  Key Points already present in {filename}")

print("\nDone!")
