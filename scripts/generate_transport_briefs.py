#!/usr/bin/env python3
"""
Generate transport persona briefs (SPEC-066).

Produces 15 persona-specific + 1 general transport brief from the
EPIC-031 configuration comparison data and transportation claims catalog.

Uses the shared LLM client (pipeline/llm_client.py) which calls
claude -p via the Claude Max subscription.
"""

import json
import sys
import os
import re
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.llm_client import call_llm

# === LOAD DATA ===

DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
PERSONA_DIR = DOCS_DIR / "persona" / "Active"
OUTPUT_DIR = PROJECT_ROOT / "dist" / "transportation-analysis" / "briefings"
ANALYSIS_DIR = DOCS_DIR / "analysis"

# Transport comparison data
with open(DATA_DIR / "transport-comparison.json") as f:
    COMPARISON = json.load(f)

# Claims catalog synthesis
CLAIMS_SYNTHESIS = (DOCS_DIR / "troves" / "transportation-claims" / "synthesis.md").read_text()

# Analysis docs (for detailed findings)
ANALYSIS_DOCS = {}
for name in ["split-family-model", "mckinney-vento-exposure", "sea-staffing-assessment",
             "bell-schedule-analysis", "before-after-care-gap", "transport-configuration-comparison"]:
    path = ANALYSIS_DIR / f"{name}.md"
    if path.exists():
        ANALYSIS_DOCS[name] = path.read_text()


def load_personas():
    """Load all persona definitions."""
    personas = {}
    for persona_dir in sorted(PERSONA_DIR.iterdir()):
        if not persona_dir.is_dir():
            continue
        md_files = list(persona_dir.glob("*.md"))
        if not md_files:
            continue
        content = md_files[0].read_text()
        # Extract persona ID from frontmatter
        match = re.search(r'artifact:\s*(PERSONA-\d+)', content)
        if match:
            pid = match.group(1)
            # Extract name from first heading
            name_match = re.search(r'^# (.+?)(?:\s*\(|$)', content, re.MULTILINE)
            name = name_match.group(1).strip() if name_match else pid
            personas[pid] = {
                "id": pid,
                "name": name,
                "content": content,
            }
    return personas


# === PERSONA-SPECIFIC FRAMING ===

PERSONA_FRAMES = {
    "PERSONA-001": "Maria is a concerned elementary parent. Lead with split-family logistics — how many mornings will she spend doing split-building drop-offs? Ground the fiscal exposure in her daily experience. She's the parent who asked about transportation logistics at TC-015.",
    "PERSONA-002": "David is a pragmatic elementary parent focused on numbers. Lead with the net savings calculation — how much of the $1.5-2.2M actually survives after transport costs? He wants the bottom line, not the emotional story.",
    "PERSONA-003": "Sarah is an anxious pre-K parent. Her children are youngest — they face the longest duration of split-building logistics under Option A. PreK is optional, and some families may opt out rather than deal with split logistics.",
    "PERSONA-004": "James is a high school teacher watching from across the district. Frame transportation costs as competing for the same budget that funds his programs. Every dollar spent on expanded bus routes is a dollar not available for academic programs.",
    "PERSONA-005": "Priya is focused on equity. Lead with McKinney-Vento impact — 10% of students are eligible, and displacement triggers federal transport obligations for the most vulnerable families. Who rides longest? Who bears the care gap costs?",
    "PERSONA-006": "Tom is a tax-conscious resident. Lead with fiscal exposure as unfunded mandates eating into claimed savings. He needs to know what the reconfiguration actually costs taxpayers vs. what was promised. The net savings table is his key data point.",
    "PERSONA-007": "Linda is a school board insider. Lead with the governance timeline — questions asked and not answered, the DOT traffic study double standard, and the 3/30 meeting where the Director of Operations confirmed 20 drivers and transport logistics 'underway with partner' but only operationalized AFTER the board votes. She needs the accountability record.",
    "PERSONA-008": "Rachel is a disruption-averse parent. Frame everything through the lens of change minimization. Option B preserves neighborhood schools and zero split families. Option A creates the maximum disruption she fears.",
    "PERSONA-009": "Dana is a local TV news producer. Lead with the headline contradiction: administration recommended a configuration without modeling its transportation impact, then confirmed no modeling will happen before the vote. The numbers make the story concrete.",
    "PERSONA-010": "Alex is a forecaster/writer. Give the analytical deep dive — methodology, assumptions, sensitivity ranges. This persona appreciates the estimation approach and wants to assess the rigor.",
    "PERSONA-011": "Pat is the group chat relay. This brief needs to be shareable — key findings in 2-3 bullet points that can be copy-pasted into a text thread. The headline stat (48-119% of savings offset) is the hook.",
    "PERSONA-012": "Jordan is a high school student. Frame transport costs as money that could go to their programs. Keep it accessible — avoid jargon. The split-family stat is relatable (their younger siblings could be affected).",
    "PERSONA-013": "Casey is a middle school student. Frame simply — 'your younger siblings might have to go to two different schools.' The before/after care gap matters because it affects when parents can pick them up.",
    "PERSONA-014": "Riley is an elementary student. Frame at their level — some kids might have longer bus rides, and some families might have to drop off at two schools instead of one. Keep it simple and concrete.",
    "PERSONA-015": "Chris is a cross-building staff advocate. Lead with the universal driver shortfall — 20 drivers confirmed (3/30 meeting), but every configuration needs 24-30. The 14% SEA cut was decided before anyone counted the drivers. Staff will be asked to do more with less, and the math doesn't work for any option.",
}

SYSTEM_PROMPT = """You are a rigorous, factual analyst producing a transportation impact brief for a specific persona in the South Portland school budget analysis.

TONE AND APPROACH:
- Interventionist framing: fiscal exposure leads, family logistics grounds it, governance context frames it
- Rigorous and factual — let the numbers speak
- Every claim backed by specific data from the analysis
- Disclose known limitations and data gaps
- Include an open invitation to the district to provide refining data
- Do NOT advocate for or against any configuration — present the missing analysis
- The brief should feel like a well-sourced analytical memo, not an opinion piece

STRUCTURE:
1. **Executive Summary** (2-3 sentences in the persona's frame)
2. **Key Finding** (the single most important number for this persona)
3. **Configuration Comparison** (table or structured comparison relevant to this persona's concerns)
4. **What's Missing** (what the district hasn't analyzed, sourced from the claims catalog)
5. **Limitations** (what this analysis can and cannot tell you)
6. **Invitation to Improve** (what district data would make this better)

Keep the brief under 800 words. Be specific — use exact numbers from the data, not vague qualifiers."""


def generate_brief(persona_id, persona_name, persona_content, frame):
    """Generate a transport brief for one persona."""
    # Build the comparison summary
    configs = COMPARISON["configurations"]
    comparison_text = json.dumps(configs, indent=2)

    prompt = f"""Generate a transportation impact brief for {persona_name} ({persona_id}).

## Persona Definition
{persona_content}

## Persona-Specific Framing
{frame}

## Transport Configuration Comparison Data
{comparison_text}

## Key Analysis Findings (V2 — updated with 3/30/2026 meeting data)

### Split Families (SPEC-060)
- Option A: 139-169 families split across buildings (18-24% of elementary families)
- Option B: 0 families split
- Variant C: 123-150 families split (16-21%)

### McKinney-Vento Exposure (SPEC-061)
- 10% of students are MV-eligible (~274 district-wide, ~108 elementary)
- Option A displaces most students (full system reorganization)
- Annual cost: $30K-$128K depending on configuration

### SEA Staffing (SPEC-062) — MAJOR UPDATE
- 20 bus drivers confirmed (Director of Operations Mike Natalie, 3/30/2026 meeting)
- Drivers work 7 AM-4 PM, idle 9:30-1:30 (confirms 3-tier schedule)
- Post-cut: 17-20 drivers available (depending on which SEA positions are cut)
- UNIVERSAL DRIVER SHORTFALL: Option A needs 30, Option B needs 24, Variant C needs 29
- Even the LOWEST-impact option (B) shows a shortfall of 4-7 drivers
- The 14% SEA cut was decided BEFORE anyone counted the drivers or modeled the routes

### Bell Schedules (SPEC-063)
- Current: 3-tier system (HS 8:10, MS 8:30, Elementary 9:05) — confirmed by driver schedule
- Option A/C may need 4th tier (grade-band routing)
- 4th tier creates 30-minute scheduling gap for split families
- Driver idle window (9:30-1:30) leaves no room for a 4th tier without overtime

### Before/After Care (SPEC-064)
- After care FULL at 4/5 schools. Only Kaler (closing) has openings.
- Option A (4-tier): 118-144 new families needing care, $404K-$804K annual cost burden on families
- Option B: $0 care gap

### Net Savings (SPEC-065) — UPDATED
- District costs separated from family-borne costs
- Option A: $946K-$1.68M total fiscal exposure (43-112% of claimed savings)
  - District cost: $803K-$876K | Family cost: $144K-$804K
- Option B: $30K-$80K fiscal exposure (1.4-5.3% of claimed savings)
- Variant C: $797K-$1.45M fiscal exposure (36-97% of claimed savings)
- Sensitivity (FY23 baseline): Option A drops to $743K-$1.48M (34-98%)

### Transport Cost Anomaly
- South Portland per-pupil transport costs rose 50.2% FY23-FY25 ($709→$1,065) vs state average +10.5%
- Diesel cost increases flagged as "considerable" at 3/30 meeting but unquantified
- Transport logistics "underway with partner" but operationalized AFTER board vote, not before

## Governance Timeline (from Transportation Claims Catalog)
{CLAIMS_SYNTHESIS[:2000]}

Generate the brief now. Include frontmatter:
---
schema_version: "1.0"
persona_id: "{persona_id}"
persona_name: "{persona_name}"
topic: "transportation"
generated_date: "2026-03-31"
source_specs: ["SPEC-060", "SPEC-061", "SPEC-062", "SPEC-063", "SPEC-064", "SPEC-065"]
---
"""
    return call_llm(prompt, system_prompt=SYSTEM_PROMPT)


def generate_general_brief():
    """Generate a general-audience transport brief."""
    configs = COMPARISON["configurations"]
    comparison_text = json.dumps(configs, indent=2)

    prompt = f"""Generate a general-audience transportation impact brief for the South Portland elementary reconfiguration.

This brief is for community members who don't fit a specific persona — general residents, casual followers of school budget news, or people encountering this analysis for the first time.

## Transport Configuration Comparison Data
{comparison_text}

## Key Analysis Findings

### The Missing Analysis
The South Portland School Board has been asked to choose between elementary reconfiguration options without transportation analysis. The Director of Operations confirmed transport logistics are "underway with a partner" but will be operationalized AFTER the board votes. At the 3/30/2026 meeting, he also confirmed 20 bus drivers working 7 AM-4 PM.

### Configuration Comparison Summary (V2)
- Option A (admin recommendation): $946K-$1.68M total fiscal exposure (43-112% of claimed savings), 139-169 split families, needs 30 drivers (has 17-20)
- Option B (K-4 proximity): $30K-$80K exposure (1.4-5.3%), zero split families, needs 24 drivers (has 17-20)
- Variant C (citizen alternative): $797K-$1.45M exposure (36-97%), 123-150 split families, needs 29 drivers (has 17-20)
- District costs separated from family-borne costs in all figures

### Key Findings
- UNIVERSAL DRIVER SHORTFALL: All configurations need more drivers than the district has, even after zero cuts to the driver pool
- "Not significant" claim made without modeling (TC-005) — route expansion costs are $624K-$748K/year for grade-band options
- SEA staffing cut (14%) decided before anyone counted drivers or modeled routes
- After care FULL at 4/5 schools; only Kaler (closing) has openings
- South Portland transport costs rose 50.2% FY23-FY25 vs state average 10.5% — cause unknown
- Diesel cost increases flagged as "considerable" at 3/30 meeting

## Governance Timeline
{CLAIMS_SYNTHESIS[:2000]}

Generate the brief. Keep it under 600 words. Use clear, jargon-free language. Include the comparison table.

Include frontmatter:
---
schema_version: "1.0"
persona_id: "general"
persona_name: "General Community Member"
topic: "transportation"
generated_date: "2026-03-31"
source_specs: ["SPEC-060", "SPEC-061", "SPEC-062", "SPEC-063", "SPEC-064", "SPEC-065"]
---
"""
    return call_llm(prompt, system_prompt=SYSTEM_PROMPT)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    personas = load_personas()

    print(f"Loaded {len(personas)} personas")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Generate persona-specific briefs
    generated = 0
    failed = 0

    for pid in sorted(personas.keys()):
        persona = personas[pid]
        frame = PERSONA_FRAMES.get(pid, f"Generate a brief relevant to {persona['name']}'s perspective and concerns.")
        slug = pid.lower().replace("-", "-")

        # Build filename matching existing convention
        name_slug = persona["name"].lower().replace(" ", "-").replace("(", "").replace(")", "")
        filename = f"transport-{pid.lower()}-{name_slug}.md"

        print(f"Generating brief for {persona['name']} ({pid})...", end=" ", flush=True)
        try:
            brief = generate_brief(pid, persona["name"], persona["content"], frame)
            (OUTPUT_DIR / filename).write_text(brief + "\n")
            print("OK")
            generated += 1
        except Exception as e:
            print(f"FAILED: {e}")
            failed += 1

    # Generate general brief
    print("Generating general transport brief...", end=" ", flush=True)
    try:
        general = generate_general_brief()
        (OUTPUT_DIR / "transport-general.md").write_text(general + "\n")
        print("OK")
        generated += 1
    except Exception as e:
        print(f"FAILED: {e}")
        failed += 1

    print(f"\nDone: {generated} generated, {failed} failed")
    print(f"Output: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
