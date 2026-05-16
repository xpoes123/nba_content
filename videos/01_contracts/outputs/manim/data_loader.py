"""Single source of truth for the video data.

Hardcoded values were extracted from `outputs/v4_*.csv` at video build time.
Don't change them without re-running src/final_v4.py first.
"""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]   # → nba_contracts/

# Load lazily — pandas import is slow inside Manim renders
def load_97_dots():
    import pandas as pd
    df = pd.read_csv(ROOT / "data/processed/values_v4_final.csv")
    sub = df[(df["bucket"] == "open_negotiation")
             & (df["MP"] >= 1000)
             & (df["years"] >= 2)].copy()
    return sub.sort_values("npv").reset_index(drop=True)


PRITCHARD_DOT_INDEX = 96   # zero-based; last (best) in ascending NPV sort
GRID_COLS = 12
GRID_ROWS = 9

# ----- Pritchard 30 teams scene (sorted descending by effective NPV) -----
# v4.1 corrections: NYK/GSW dropped 2nd→1st apron, PHI dropped out of apron,
# BOS moved up to 1st apron (taxpayer above first-apron line).
PRITCHARD_30_TEAMS = [
    ('CLE', 'second_apron',        3.1, 13.3),
    ('GSW', 'first_apron',         2.8, 12.0),
    ('LAL', 'first_apron',         2.8, 12.0),
    ('NYK', 'first_apron',         2.3,  9.9),
    ('HOU', 'first_apron',         2.3,  9.9),
    ('MIN', 'first_apron',         2.3,  9.9),
    ('BOS', 'first_apron',         2.3,  9.9),
    ('LAC', 'taxpayer',            2.0,  8.6),
    ('SAC', 'above_cap_below_tax', 1.0,  4.3),
    ('PHI', 'above_cap_below_tax', 1.0,  4.3),
    ('TOR', 'above_cap_below_tax', 1.0,  4.3),
    ('DEN', 'above_cap_below_tax', 1.0,  4.3),
    ('NOP', 'above_cap_below_tax', 1.0,  4.3),
    ('PHO', 'above_cap_below_tax', 1.0,  4.3),
    ('OKC', 'above_cap_below_tax', 1.0,  4.3),
    ('WAS', 'above_cap_below_tax', 1.0,  4.3),
    ('ORL', 'above_cap_below_tax', 1.0,  4.3),
    ('POR', 'above_cap_below_tax', 1.0,  4.3),
    ('IND', 'above_cap_below_tax', 1.0,  4.3),
    ('MIA', 'above_cap_below_tax', 1.0,  4.3),
    ('CHO', 'above_cap_below_tax', 1.0,  4.3),
    ('DET', 'above_cap_below_tax', 1.0,  4.3),
    ('SAS', 'above_cap_below_tax', 1.0,  4.3),
    ('DAL', 'above_cap_below_tax', 1.0,  4.3),
    ('ATL', 'above_cap_below_tax', 1.0,  4.3),
    ('MIL', 'above_cap_below_tax', 1.0,  4.3),
    ('CHI', 'above_cap_below_tax', 1.0,  4.3),
    ('UTA', 'above_cap_below_tax', 1.0,  4.3),
    ('MEM', 'above_cap_below_tax', 1.0,  4.3),
    ('BRK', 'below_cap',           0.5,  2.2),
]

# ----- Bottom 5 effective NPV -----
# (player, team, tier, effective_npv_M)
# v4.1 corrections: Embiid/Anunoby/Towns/Curry dropped out after tier fixes;
# replaced by next-worst contracts on apron teams.
BOTTOM_5_EFFECTIVE = [
    ("Evan Mobley",        "CLE", "second_apron", -642.2),
    ("Jaylen Brown",       "BOS", "first_apron",  -428.5),
    ("Luka Doncic",        "LAL", "first_apron",  -363.2),
    ("Anthony Edwards",    "MIN", "first_apron",  -349.5),
    ("Donovan Mitchell",   "CLE", "second_apron", -342.1),
]

# ----- Bucket positive shares -----
# (bucket_label, percent_positive, count_in_bucket)
BUCKET_POSITIVE_SHARES = [
    ("Vet minimum",      55, 22),
    ("Rookie scale",     10, 72),
    ("Max contracts",     0, 33),
    ("Open negotiation",  1, 97),
]

# ----- Pritchard timeline events -----
PRITCHARD_EVENTS = [
    (2020.50, "Drafted",      "Drafted #26"),
    (2022.25, "Trade demand", "Public trade request"),
    (2023.78, "Extension",    "4yr / $30M signed\nOct 8, 2023"),
    (2025.20, "6MOY",         "Sixth Man of the Year"),
    (2026.40, "Now",          "Now"),
]
PRITCHARD_WA_TRAJECTORY = [
    (2021, -0.4),
    (2022,  0.2),
    (2023,  0.5),
    (2024,  1.4),
    (2025,  1.8),
]

# ----- Next-Pritchard watch list -----
# v4.1: Queta decision is team option pickup (Jun 2026); Duren is RFA-bound
# Summer 2026 — rookie-ext deadline already closed Oct 2025.
NEXT_PRITCHARD = [
    ("Neemias Queta",  "BOS", 26, 1.7,  2.3, 10.4, "Jun 2026 (option)"),
    ("Jalen Duren",    "DET", 22, 2.5,  6.5, 14.4, "Summer 2026 (RFA)"),
    ("Moussa Diabate", "CHO", 24, 1.1,  2.3,  7.8, "Summer 2027"),
]

# ----- Cold open names -----
COLD_OPEN_NAMES = [
    "JOKIC", "BRUNSON", "SGA", "WEMBY", "DURANT",
    "PRITCHARD", "KORNET", "AVDIJA", "JALEN JOHNSON",
    "NAW", "HALIBURTON", "SHENGUN", "MITCHELL",
    "ROLLINS", "REAVES",
]

# ----- 4-bucket explainer -----
FOUR_BUCKETS = [
    ("Rookie scale",     "First-rounders cost-controlled 4 years",    "rookie_scale"),
    ("Max contracts",    "CBA-capped at 25-35% of cap",                "max"),
    ("Veteran minimum",  "Floor salary, ~$2.3M",                       "min"),
    ("Open negotiation", "Everything else — what GMs actually choose", "open_negotiation"),
]

# ----- The three closing numbers -----
CLOSE_NUMBERS = [
    (1,  "of 97 GM-negotiated contracts"),
    (55, "% of vet-min deals projected positive"),
    (6,  "x value range for Pritchard's contract"),
]

# ----- Scatter sample for PriceFitScatter -----
def make_scatter_sample(seed: int = 42):
    rng = np.random.default_rng(seed)
    open_neg = [(z, 2.3 + 4.86*z + rng.normal(0, 4))
                for z in rng.uniform(-1, 3, 30)]
    maxc = [(z, 50 + rng.normal(0, 3))
            for z in rng.uniform(0.5, 5, 12)]
    minc = [(z, 2.3 + rng.normal(0, 1))
            for z in rng.uniform(-1.5, 1.5, 10)]
    return {"open_neg": open_neg, "max": maxc, "min": minc}
