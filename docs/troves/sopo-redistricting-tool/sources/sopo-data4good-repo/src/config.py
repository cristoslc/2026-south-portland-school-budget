"""
Central configuration for the South Portland redistricting model.

Closing Skillin is excluded: remaining 4-school capacity (1,020) covers
all 1,013 K-4 students. The four viable closure scenarios are Brown, Dyer,
Small, and Kaler.

PreK is a pilot program (currently at Dyer + Kaler only). It is modeled as
a pre-assigned capacity overhead — not subject to geographic zone optimization.
"""
import os

SCHOOLS = {
    "Brown":   {"lat": 43.63469222922709, "lng": -70.2488528529349,  "capacity": 260},
    "Dyer":    {"lat": 43.62188281730617, "lng": -70.27491180480025, "capacity": 240},
    "Small":   {"lat": 43.64131092018083, "lng": -70.23385021390395, "capacity": 280},
    "Skillin": {"lat": 43.62597508507279, "lng": -70.30537634309235, "capacity": 380},
    "Kaler":   {"lat": 43.62867422728908, "lng": -70.26881539114758, "capacity": 240},
}

# Per-school per-grade enrollment (current, March 2026)
# Note: original school "Totals" excluded PreK (pilot). PreK shown separately.
GRADE_ENROLLMENT = {
    "Brown":   {"prek": 0,  "k": 29, "g1": 44, "g2": 46, "g3": 38, "g4": 37},
    "Dyer":    {"prek": 29, "k": 35, "g1": 28, "g2": 39, "g3": 25, "g4": 39},
    "Kaler":   {"prek": 29, "k": 26, "g1": 33, "g2": 30, "g3": 26, "g4": 20},
    "Small":   {"prek": 0,  "k": 33, "g1": 39, "g2": 39, "g3": 42, "g4": 46},
    "Skillin": {"prek": 0,  "k": 68, "g1": 56, "g2": 64, "g3": 58, "g4": 73},
}

PREK_PER_SCHOOL = 29   # max PreK per building (community school mode)
PREK_PER_CENTER = 58   # max PreK per grade center (2 classes merged)

# Grade-band totals for proportional block allocation
# Geographic zone optimization runs on K-4 (community) or K-1 / 2-4 (grade centers)
TOTAL_K4  = sum(g["k"]+g["g1"]+g["g2"]+g["g3"]+g["g4"] for g in GRADE_ENROLLMENT.values())  # 1013
TOTAL_K1  = sum(g["k"]+g["g1"]                           for g in GRADE_ENROLLMENT.values())  # 391
TOTAL_G24 = sum(g["g2"]+g["g3"]+g["g4"]                 for g in GRADE_ENROLLMENT.values())  # 622
TOTAL_ENROLLMENT = TOTAL_K4   # legacy alias used by existing imports

# PreK overhead per scenario — community school, CURRENT pilot state
# Dyer + Kaler have 29 each today. If one closes, their 29 goes to Small.
PREK_COMMUNITY_CURRENT = {
    "brown_closed": {"Dyer": 29, "Kaler": 29},
    "kaler_closed": {"Dyer": 29, "Small": 29},
    "dyer_closed":  {"Kaler": 29, "Small": 29},
    "small_closed": {"Dyer": 29, "Kaler": 29},
}

SCENARIOS = [
    {"name": "brown_closed", "closed": "Brown"},
    {"name": "dyer_closed",  "closed": "Dyer"},
    {"name": "small_closed", "closed": "Small"},
    {"name": "kaler_closed", "closed": "Kaler"},
]

# Grade-center reconfiguration: which buildings serve PreK-1 vs Grades 2-4
RECONFIG_SCENARIOS = {
    "brown_closed": {"prek1_schools": ["Dyer",  "Kaler"], "g24_schools": ["Small",  "Skillin"]},
    "kaler_closed": {"prek1_schools": ["Dyer",  "Small"], "g24_schools": ["Brown",  "Skillin"]},
    "dyer_closed":  {"prek1_schools": ["Kaler", "Small"], "g24_schools": ["Brown",  "Skillin"]},
    "small_closed": {"prek1_schools": ["Dyer",  "Kaler"], "g24_schools": ["Brown",  "Skillin"]},
}

WALK_THRESHOLD_MILES  = 0.75
WALK_THRESHOLD_METERS = WALK_THRESHOLD_MILES * 1609.34

STUDY_AREA = "South Portland, Maine, USA"

SCHOOL_COLORS = {
    "Brown":      "#E74C3C",
    "Dyer":       "#3498DB",
    "Small":      "#2ECC71",
    "Skillin":    "#F39C12",
    "Kaler":      "#9B59B6",
    "UNASSIGNED": "#CCCCCC",
}

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR      = os.path.join(BASE_DIR, "cache")
OUTPUT_DIR     = os.path.join(BASE_DIR, "outputs")
BLOCKS_GEOJSON = os.path.join(BASE_DIR, "Polygons.geojson")
