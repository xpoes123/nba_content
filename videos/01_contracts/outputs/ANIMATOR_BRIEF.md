# Animator Brief — NBA Contracts Manim Build

You are building 23 Manim scenes for a 15-minute YouTube video. The script and scene-by-scene visual specs are in `VIDEO_OUTLINE.md` — **read that first**. This file is everything *else* you need: environment setup, conventions, data access patterns, and concrete data values so you don't have to re-derive things.

If something in this file contradicts `VIDEO_OUTLINE.md`, **the outline wins** for content; this file wins for engineering.

---

## Quick orientation

- **Project root**: `/home/david/code/sports/nba_contracts/`
- **Data**: `data/processed/` and `outputs/*.csv`
- **Existing Python**: `src/` — read it to understand the model; don't modify it
- **Your output goes in**: `outputs/manim/` (you create this)
- **Manim**: Community v0.18+, install via `pip install manim`
- **No audio**: produce silent video. The editor syncs narration in post.

The user is asleep. Work to completion. **Definition of done is at the bottom of this file.**

---

## Environment setup

Use the existing venv to avoid polluting global Python:

```bash
cd /home/david/code/sports/nba_contracts
source .venv/bin/activate.fish  # or .venv/bin/activate for bash
pip install manim
# manim has system deps: ffmpeg, cairo, pango (likely pre-installed on CachyOS)
# if any are missing:
#   sudo pacman -S ffmpeg cairo pango
```

Verify install:
```bash
manim --version  # should be >= 0.18
```

Use `Text()`, not `Tex()` or `MathTex()`. The repo doesn't have LaTeX configured, and we don't need math typesetting. If you need a formula, build it from `Text` and `MathTex` only for the one place we need a real equation (Scene 5). If LaTeX isn't available, fall back to `Text` with Unicode (·, ², etc).

---

## Project structure to create

```
outputs/manim/
├── manim_config.py          # shared config (colors, fonts, helpers)
├── data_loader.py           # one place that loads all CSVs and exports constants
├── scenes/
│   ├── __init__.py
│   ├── cold_open.py         # Scenes 1-2
│   ├── segment_1_buckets.py # Scenes 3-5
│   ├── segment_2_killer.py  # Scenes 6-7
│   ├── segment_3_story.py   # Scenes 8-9
│   ├── segment_4_method.py  # Scenes 10-12
│   ├── segment_5_worst.py   # Scenes 13-15
│   ├── segment_6_prit30.py  # Scenes 16-17
│   ├── segment_7_next.py    # Scenes 18-21
│   └── segment_8_close.py   # Scenes 22-23
├── render_all.sh            # bash script that renders every scene
└── media/                   # manim's auto-output folder (mp4s land here)
```

Each scene class is a subclass of `Scene`. Render each individually so the editor can swap in audio scene-by-scene.

**Naming**: each scene class is named exactly as in `VIDEO_OUTLINE.md` (`ColdOpenNames`, `NinetySevenDots`, etc.). The rendered MP4 filename follows manim convention (`<ClassName>.mp4`).

---

## Conventions

### Colors

Copy this into `manim_config.py` verbatim. **Do not change these.** They match the analysis Python and the existing PNGs.

```python
from manim import *

TIER_COLORS = {
    "second_apron":          "#c1272d",
    "first_apron":           "#e67e22",
    "taxpayer":              "#f1c40f",
    "above_cap_below_tax":   "#34495e",
    "below_cap":             "#95a5a6",
}

BUCKET_COLORS = {
    "rookie_scale":      "#2980b9",
    "min":               "#16a085",
    "max":               "#c0392b",
    "open_negotiation":  "#27ae60",
}

HIGHLIGHT_GREEN = "#27ae60"
HIGHLIGHT_RED   = "#c0392b"
HIGHLIGHT_AMBER = "#f39c12"
BACKGROUND      = "#1a1a2e"
TEXT_COLOR      = "#ECECEC"
DIM_TEXT        = "#9ca3b3"

# at the top of every scene file:
config.background_color = BACKGROUND
config.frame_rate = 60
config.pixel_height = 1080
config.pixel_width = 1920
```

### Fonts

```python
FONT_BODY = "Inter"          # body text, labels
FONT_NUMBERS = "JetBrains Mono"  # for any data values; tabular
FONT_DISPLAY = "Inter"       # use bold weight for big text
```

Fallbacks (in order): Inter → DejaVu Sans → sans-serif. If Inter isn't installed on the system, manim will substitute. That's acceptable — don't bother installing fonts.

### Standard sizes

```python
SIZE_TITLE     = 48
SIZE_HEADER    = 36
SIZE_BODY      = 28
SIZE_SMALL     = 20
SIZE_TINY      = 14
SIZE_HERO_NUMBER = 96   # for the dramatic single-number reveals
```

### Timing defaults

```python
RT_FADE = 0.4       # quick FadeIn/FadeOut
RT_WRITE = 1.0      # text Write() animations
RT_BAR_DRAW = 0.8   # individual bar grows in
RT_CHART_BUILD = 2.5  # full chart populates
RT_HOLD_SHORT = 0.8
RT_HOLD_LONG = 2.5
LAG_TIGHT = 0.05    # lag_ratio for tight stagger
LAG_LOOSE = 0.15    # lag_ratio for visible stagger
```

### Scene padding

Every scene must end with `self.wait(0.3)` to give the editor splice room. Don't black-out at the end of a scene — the next scene starts seamlessly.

---

## Data access pattern

Create `outputs/manim/data_loader.py` that loads everything once. Every scene imports from this file. **Do not have scenes load CSVs directly** — too easy for inconsistencies.

```python
"""Single source of truth for video data.

All numbers come from the v4 model. Hard-coded values in this file are
extracted from outputs/v4_*.csv at video build time. Don't change them
without re-running src/final_v4.py first.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]   # → nba_contracts/

# -------- 97 dots scene --------
# 97 open-negotiation contracts (MP>=1000, years>=2), sorted ascending by NPV.
# Pritchard is at index 96 (the only positive).
def load_97_dots() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data/processed/values_v4_final.csv")
    sub = df[(df["bucket"] == "open_negotiation")
             & (df["MP"] >= 1000)
             & (df["years"] >= 2)].copy()
    return sub.sort_values("npv").reset_index(drop=True)

PRITCHARD_DOT_INDEX = 96   # zero-based; last in ascending-NPV sort

# -------- Pritchard 30 teams scene --------
# (team_abbrev, tier, multiplier, effective_npv_in_millions)
# v4.1: NYK/GSW moved from 2nd→1st apron, PHI out of apron, BOS into 1st apron.
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

# -------- Bottom 5 effective NPV --------
# (player, team, tier, effective_npv_M)
# v4.1: shifted entirely after PHI/NYK/GSW tier corrections.
BOTTOM_5_EFFECTIVE = [
    ("Evan Mobley",        "CLE", "second_apron", -642.2),
    ("Jaylen Brown",       "BOS", "first_apron",  -428.5),
    ("Luka Dončić",        "LAL", "first_apron",  -363.2),
    ("Anthony Edwards",    "MIN", "first_apron",  -349.5),
    ("Donovan Mitchell",   "CLE", "second_apron", -342.1),
]

# -------- Bucket positive shares (Segment 2 scene 7) --------
# (bucket_label, percent_positive, count_in_bucket)
BUCKET_POSITIVE_SHARES = [
    ("Vet minimum",       55, 22),
    ("Rookie scale",      10, 72),
    ("Max contracts",      0, 33),
    ("Open negotiation",   1, 97),
]

# -------- Pritchard timeline events --------
# (year_float, label_short, label_long)
PRITCHARD_EVENTS = [
    (2020.50, "Drafted",     "Drafted #26"),
    (2022.25, "Trade demand", "Public trade request"),
    (2023.78, "Extension",   "4yr / $30M signed\nOct 8, 2023"),
    (2025.20, "6MOY",        "Sixth Man of the Year"),
    (2026.40, "Now",         "Now"),
]
# Pritchard WA_z trajectory (approximate, for the line graph above timeline)
PRITCHARD_WA_TRAJECTORY = [
    (2021, -0.4),
    (2022,  0.2),
    (2023,  0.5),
    (2024,  1.4),
    (2025,  1.8),
]

# -------- Next-Pritchard watch list --------
# (player, team, age, wa_z, salary_M, market_value_M, decision_date)
# v4.1: Queta is a team-option decision (Jun 2026), not RFA. Duren window
# already closed Oct 2025 — he's headed to RFA Summer 2026.
NEXT_PRITCHARD = [
    ("Neemias Queta",  "BOS", 26, 1.7,  2.3, 10.4, "Jun 2026 (team option)"),
    ("Jalen Duren",    "DET", 22, 2.5,  6.5, 14.4, "Summer 2026 (RFA)"),
    ("Moussa Diabaté", "CHO", 24, 1.1,  2.3,  7.8, "Summer 2027"),
]

# -------- Cold open name flicker --------
COLD_OPEN_NAMES = [
    "JOKIĆ", "BRUNSON", "SGA", "WEMBY", "DURANT",
    "PRITCHARD", "KORNET", "AVDIJA", "JALEN JOHNSON",
    "NAW", "HALIBURTON", "SHENGUN", "MITCHELL",
    "ROLLINS", "REAVES",
]

# -------- 4-bucket explainer (Segment 1 scene 3) --------
FOUR_BUCKETS = [
    ("Rookie scale",      "First-rounders cost-controlled 4 years",     "rookie_scale"),
    ("Max contracts",     "CBA-capped at 25-35% of cap",                "max"),
    ("Veteran minimum",   "Floor salary, ~$2.3M",                        "min"),
    ("Open negotiation",  "Everything else — what GMs actually choose",  "open_negotiation"),
]

# -------- The three closing numbers --------
CLOSE_NUMBERS = [
    (1, "of 97 GM-negotiated contracts"),
    (55, "% of vet-min deals projected positive"),
    (6, "× value range for Pritchard's contract"),
]
```

Every scene imports the data it needs from this file. If a number is missing, *add it here*, don't hardcode in a scene file.

---

## Helper utilities

Drop this into `outputs/manim/manim_config.py` alongside the constants. Reusable patterns across scenes:

```python
def make_dot(color=TEXT_COLOR, radius=0.18) -> Dot:
    """Standard dot for the 97 grid and other dot-array scenes."""
    return Dot(radius=radius, color=color, stroke_width=0.5, stroke_color=BLACK)

def labeled_bar(value: float, label: str, color: str, max_value: float,
                bar_length: float = 6.0) -> VGroup:
    """A horizontal bar with a label and a value annotation.
    Returns a VGroup positioned at origin; caller arranges position.
    """
    width = abs(value) / max_value * bar_length
    bar = Rectangle(width=width, height=0.4)
    bar.set_fill(color, opacity=0.85)
    bar.set_stroke(width=0)
    bar.align_to(ORIGIN, LEFT if value > 0 else RIGHT)
    name = Text(label, font=FONT_BODY, font_size=SIZE_SMALL, color=TEXT_COLOR)
    name.next_to(bar, LEFT, buff=0.2)
    val = Text(f"${value:.1f}M", font=FONT_NUMBERS, font_size=SIZE_SMALL, color=TEXT_COLOR)
    val.next_to(bar, RIGHT, buff=0.2)
    return VGroup(name, bar, val)

def lower_third(text: str) -> Text:
    """Bottom-of-screen attribution / caveat text."""
    t = Text(text, font=FONT_BODY, font_size=SIZE_TINY, color=DIM_TEXT)
    t.to_edge(DOWN, buff=0.5)
    return t

def fade_to_dim(*mobjects, opacity=0.3):
    """Animation generator that dims existing mobjects.
    Use to push background context into a faded state when foregrounding new content.
    """
    return [m.animate.set_opacity(opacity) for m in mobjects]
```

---

## Per-scene engineering notes

These are additional implementation specifics not in the outline. Read the outline's narrative + visual description for each scene, then check this section for extra detail.

### Scene 1 — `ColdOpenNames` (0:00–0:18)

- 15 names randomly positioned. Use `np.random.seed(42)` for reproducibility.
- Each name: appear over 0.2s, hold 0.3s, fade over 0.2s. Total per name ~0.7s.
- LaggedStart with `lag_ratio=0.08` so they overlap 3-4 at a time.
- Font: bold, size 48, color cycles through `TEXT_COLOR` and `DIM_TEXT`.

### Scene 2 — `ColdOpenStat` (0:18–0:45)

- "97 contracts GMs negotiated" — render as `Text` in `SIZE_HEADER`, color `DIM_TEXT`.
- "1 will deliver positive value." — split into:
  - "1" → `Text("1")` at `SIZE_HERO_NUMBER`, color `HIGHLIGHT_GREEN`
  - " will deliver positive value." → rest at `SIZE_HEADER`, color `TEXT_COLOR`
- The "1" should pulse: scale 1.0 → 1.15 → 1.0, repeat once.
- End with a smash cut: fade everything to black in 0.15s.

### Scene 5 — `BuildTheFormula` (2:10–2:45)

This is the **one** scene that needs MathTex. If LaTeX isn't installed, fall back to building the equation from `Text` mobjects:

```python
# Plan A (preferred):
formula = MathTex(
    r"\text{salary}", r"=", r"\$2.3M", r"+", r"\$4.86M", r"\cdot", r"WA_z"
)

# Plan B (no LaTeX):
formula = VGroup(
    Text("salary", font=FONT_BODY),
    Text("=", font=FONT_BODY),
    Text("$2.3M", font=FONT_NUMBERS),
    Text("+", font=FONT_BODY),
    Text("$4.86M", font=FONT_NUMBERS, color=HIGHLIGHT_AMBER),
    Text("·", font=FONT_BODY),
    Text("WA_z", font=FONT_NUMBERS),
).arrange(RIGHT, buff=0.25)
```

Try Plan A first, fall back to Plan B if `manim` errors on LaTeX.

### Scene 6 — `NinetySevenDots` (2:45–3:50) — THE big one

This is the headline visual. Spend the most care here.

- Grid: 12 cols × 9 rows (108 cells, 97 used; 11 trailing cells empty).
- The dots are populated **in order of player NPV ascending** — so Pritchard (best) is the LAST dot to appear, at grid position (col=0, row=8) reading left-to-right top-to-bottom.

Wait — that places him in the bottom-left. Actually, since `arrange_in_grid` fills left-to-right top-to-bottom, index 96 lands at row 8 (last row), column 0 (first column). That's the **bottom-left** dot. Good — when he turns green, eyes naturally finish reading at that point.

- Phase 1 — populate (3.5s): `LaggedStart(*[FadeIn(d, scale=2)], lag_ratio=0.025)`.
- Phase 2 — label (0.5s): `Text("97 openly negotiated NBA contracts").scale(0.6).next_to(dots, UP)`.
- Phase 3 — suspense (1s): hold all-grey, wait.
- Phase 4 — the reveal (3s):
  - Pritchard's dot (index 96) animates: `set_color(HIGHLIGHT_GREEN)` AND `scale(1.6)`.
  - All other 96 dots fade to `HIGHLIGHT_RED` via `LaggedStart(lag_ratio=0.005, run_time=1.5)` — fast, almost simultaneous.
- Phase 5 — Pritchard label (2s): `Text("Payton Pritchard").next_to(pritchard_dot, DOWN, buff=0.3)` then `Text("+$4.3M NPV").set_color(HIGHLIGHT_GREEN).next_to(player_label, DOWN, buff=0.05)`.

Total scene time: ~10s of animation + final `self.wait(1.0)` = 11s. Padded to fill until 3:50.

### Scene 7 — `BucketPositiveShare` (3:50–4:30)

Use horizontal bars, not vertical — easier to label.

```python
from data_loader import BUCKET_POSITIVE_SHARES

ax = Axes(x_range=[0, 70, 10], y_range=[0, 4],
          x_length=10, y_length=4,
          axis_config={"include_numbers": False})
# Create 4 rectangles manually; BarChart's API is finicky.
bars = VGroup()
for i, (label, pct, n) in enumerate(BUCKET_POSITIVE_SHARES):
    width = pct / 70 * 10  # scale to axis
    bar = Rectangle(width=width, height=0.7).set_fill(...)
    bars.add(bar)
bars.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
```

Order top-to-bottom: min, rookie scale, max, open negotiation. After all bars draw, draw an arrow from "1%" bar (open negotiation) to a callout: "= just Pritchard."

### Scene 8 — `PritchardTimeline` (4:30–5:30)

Two-layer composition:
- **Bottom layer**: horizontal `NumberLine` with year ticks 2020-2026. Events appear as `Dot` + callout box.
- **Top layer**: `Axes` showing WA_z trajectory over time, drawn left-to-right with `Create()`.

Key visual: a vertical dashed line drops from the WA_z curve at 2023.78 (extension date) down to the corresponding event marker on the timeline. Animate it AFTER both curve and timeline are built, with `Create()` over 0.5s.

### Scene 10 — `PriceFitScatter` (6:45–7:25)

Scatter plot of WA_z (x-axis, -2 to 5.5) vs salary in $M (y-axis, 0 to 60).

For the scatter data, **don't** load 200+ real points. Use ~50 representative points — sample from the open-negotiation bucket plus the bottom-anchor max contracts:

```python
# Add to data_loader.py:
SCATTER_SAMPLE = (
    # open negotiation (green): ~30 dots roughly along the line salary = 2.3 + 4.86*z
    [(z, 2.3 + 4.86*z + np.random.normal(0, 4)) for z in np.random.uniform(-1, 3, 30)]
    + [(z, 50 + np.random.normal(0, 3)) for z in np.random.uniform(0.5, 5, 12)]  # max contracts top-coded
    + [(z, 2.3 + np.random.normal(0, 1)) for z in np.random.uniform(-1.5, 1.5, 10)]  # min contracts
)
```

Color-code each subset. The regression line (`y = 2.3 + 4.86*x`) is drawn through only the green dots.

### Scene 13 — `BottomFiveBars` (8:15–9:15)

Horizontal bars descending into negative territory. Use a `ValueTracker` to animate the number labels counting down from 0 to the target value as each bar grows.

```python
from data_loader import BOTTOM_5_EFFECTIVE

# scale: -650 to 0 maps to 0 to 8 units of screen width
for player, team, tier, npv in BOTTOM_5_EFFECTIVE:
    tracker = ValueTracker(0)
    bar = always_redraw(lambda: ...)  # bar width tied to tracker
    label = always_redraw(lambda: Text(f"−${abs(tracker.get_value()):.0f}M", ...))
    self.play(tracker.animate.set_value(npv), run_time=1.2)
```

After all 5 draw, the **Mobley** bar (top-of-screen if sorted by most-negative) gets a pulse animation + three callout boxes (per Scene 14).

### Scene 16 — `Pritchard30Teams` (10:00–11:00)

The 30-team chart. Load from `PRITCHARD_30_TEAMS` constant. Build as horizontal bars sorted ascending (so GSW at top, BRK at bottom — actually the opposite gives more dramatic reveal: BRK at bottom, GSW at top, then animation builds upward).

Decision: **sort descending by NPV**, so GSW is at the TOP of the chart, BRK at the bottom. Bars draw in from bottom-up (BRK first, GSW last). The final reveal lands on the GSW bar, which is the punchline.

For 30 bars, scale font sizes down: team labels at `SIZE_TINY`, value labels at `SIZE_SMALL`.

### Scene 17 — `SevenTimesCallout` (11:00–11:30)

Pull CLE and BRK bars OUT of the chart (copy them, fade originals to 30% opacity). Center them with the "6×" multiplier text large between them.

```python
gsw_copy = gsw_bar.copy().shift(UP*1.5).scale(1.3)
brk_copy = brk_bar.copy().shift(DOWN*1.5).scale(1.3)
self.play(
    FadeIn(gsw_copy), FadeIn(brk_copy),
    *fade_to_dim(*chart_bars),
)
six_x = Text("6×", font_size=SIZE_HERO_NUMBER, color=HIGHLIGHT_AMBER)
seven_x.move_to(ORIGIN)
self.play(Write(seven_x))
```

### Scenes 18-21 — Next Pritchard segment

- **Scene 18**: vertical timeline running TOP to BOTTOM (manim default is left-to-right; rotate). Date markers along it; player callouts to the left.
- **Scene 19**: Queta spotlight card. Center-screen. Includes a small "BOS Celtics — Brad Stevens" badge in the corner with a Pritchard portrait icon (just use a stylized "PP" letter mark; we don't have headshot rights).
- **Scene 20**: Detroit fork-in-road. Two parallel columns showing scenario A vs scenario B. After both populate, a center label appears: "Model: 65% scenario B" — this implies the model thinks Detroit messes it up.
- **Scene 21**: Diabaté card with Charlotte bullet list (Knueppel, Kalkbrenner, Diabaté = "???").

### Scene 22 — `ThreeNumbersReveal` (13:30–14:30)

Three big numbers race up via `ValueTracker`. Layout: three columns equally spaced.

```python
from data_loader import CLOSE_NUMBERS

# (1, "..."), (55, "..."), (7, "...")
for i, (target, label_text) in enumerate(CLOSE_NUMBERS):
    tracker = ValueTracker(0)
    big_num = always_redraw(lambda t=tracker: Text(f"{int(t.get_value())}", font_size=SIZE_HERO_NUMBER))
    label = Text(label_text, font_size=SIZE_BODY).next_to(big_num, DOWN)
    group = VGroup(big_num, label).move_to([(i-1)*4.5, 0, 0])
    self.add(group)
    self.play(tracker.animate.set_value(target), run_time=1.2)
    self.wait(0.4)
```

Final hold: 1.5s with all three on screen.

### Scene 23 — `FinalQuestion` (14:30–15:00)

Two question lines + the punchline.

```python
q1 = Text("Did the GM negotiate this?", font_size=SIZE_HEADER)
q2 = Text("Or did the CBA?", font_size=SIZE_HEADER).next_to(q1, DOWN, buff=0.4)
self.play(Write(q1), run_time=1.2)
self.wait(0.6)
self.play(Write(q2), run_time=1.2)
self.wait(1.5)
# Both questions fade to dim
self.play(*fade_to_dim(q1, q2, opacity=0.4))
# Punchline appears
final = Text("Almost always, it was the CBA.",
             font_size=SIZE_HEADER, color=HIGHLIGHT_GREEN, weight=BOLD)
self.play(Write(final), run_time=1.5)
self.wait(3.0)
```

---

## Master render script

Create `outputs/manim/render_all.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

QUALITY="${1:-high_quality}"   # use 'low_quality' for previews

SCENES=(
    "scenes/cold_open.py ColdOpenNames"
    "scenes/cold_open.py ColdOpenStat"
    "scenes/segment_1_buckets.py FourBuckets"
    "scenes/segment_1_buckets.py JokicCap"
    "scenes/segment_1_buckets.py BuildTheFormula"
    "scenes/segment_2_killer.py NinetySevenDots"
    "scenes/segment_2_killer.py BucketPositiveShare"
    "scenes/segment_3_story.py PritchardTimeline"
    "scenes/segment_3_story.py ThreeReasonsCallout"
    "scenes/segment_4_method.py PriceFitScatter"
    "scenes/segment_4_method.py AgingCurve"
    "scenes/segment_4_method.py MultiplierStack"
    "scenes/segment_5_worst.py BottomFiveBars"
    "scenes/segment_5_worst.py MobleyAnnotation"
    "scenes/segment_5_worst.py MaxOnApronPattern"
    "scenes/segment_6_prit30.py Pritchard30Teams"
    "scenes/segment_6_prit30.py SevenTimesCallout"
    "scenes/segment_7_next.py NextPritchardCalendar"
    "scenes/segment_7_next.py QuetaSpotlight"
    "scenes/segment_7_next.py DurenForecast"
    "scenes/segment_7_next.py DiabateUnderRadar"
    "scenes/segment_8_close.py ThreeNumbersReveal"
    "scenes/segment_8_close.py FinalQuestion"
)

for entry in "${SCENES[@]}"; do
    read -r file class <<< "$entry"
    echo "→ rendering $class"
    manim -q "$QUALITY" "$file" "$class" || {
        echo "❌ $class failed; continuing"
        continue
    }
done

echo "✅ all scenes rendered to media/videos/"
```

Render quality flags:
- `-q low_quality` → 480p, 15fps — use for iterative testing
- `-q medium_quality` → 720p, 30fps — preview
- `-q high_quality` → 1080p, 60fps — final delivery

Render at `low_quality` first to verify everything works, then re-render at `high_quality` overnight.

---

## Workflow

1. Set up directory, install manim, verify with `manim --version`
2. Create `manim_config.py` and `data_loader.py` from the snippets above
3. **Build a smoke-test scene first** — render Scene 6 (`NinetySevenDots`) at low quality. If it renders, the pipeline works. This is the most complex scene; everything else is easier.
4. Build remaining scenes one segment at a time, segment 1 → 8.
5. Render all at low_quality. Watch through. Iterate on any that look wrong.
6. Final render: `bash render_all.sh high_quality`
7. Concatenate the 23 MP4s into one master video using ffmpeg:

```bash
# in outputs/manim/, after rendering:
# manim outputs land in media/videos/<scene_file>/1080p60/<ClassName>.mp4
find media/videos -name "*.mp4" | sort > scene_list.txt
# manually reorder scene_list.txt to match outline sequence
ffmpeg -f concat -safe 0 -i scene_list.txt -c copy ../FINAL_MASTER.mp4
```

---

## Definition of done

By morning, the user should be able to:

1. Run `bash outputs/manim/render_all.sh low_quality` and see 23 MP4 previews land in `media/videos/`
2. Open `outputs/manim/scenes/` and see one Python file per segment, each containing the scenes for that segment
3. Read `outputs/manim/data_loader.py` and find all hardcoded numbers in one place
4. Run the high-quality render to get final outputs
5. (Bonus) Find a concatenated `outputs/FINAL_MASTER.mp4` if the ffmpeg step works

**Minimum acceptable**: 20 of 23 scenes render at low_quality without errors, even if some look rough. Visual polish can happen during morning review.

**Stretch**: all 23 at high_quality, plus the concatenated master.

---

## What NOT to do

- **Don't change the data values** in `data_loader.py`. They come from a vetted model.
- **Don't add scenes** beyond the 23 listed. If a transition feels missing, use `Wait()` and let the editor handle it.
- **Don't try to render high_quality first.** It's 30+ minutes per scene at 1080p60. Iterate at low_quality.
- **Don't add B-roll, photos, or player likenesses.** Manim only. The editor will overlay any non-Manim assets in post.
- **Don't use `Tex()` with complex LaTeX.** If LaTeX isn't installed, the renders silently fail to text-only fallbacks that look bad. Stick with `Text` and the single `MathTex` in Scene 5 with the Plan B fallback.
- **Don't redesign the visuals.** The outline's visual descriptions are deliberate. Implement what's described.
- **Don't try to run anything that requires `sudo`.** No system installs.
- **Don't modify `src/` or the existing analysis code.** It's frozen.

---

## If something is genuinely blocked

If a scene's design isn't implementable in Manim (rare), leave a `BLOCKED: <reason>` text overlay in the scene class and move on. Don't spend > 30 minutes on any single scene that's giving you trouble. Better to have 22/23 working than 0/23 perfect.

If `manim` itself fails to install or render, leave a note in `outputs/manim/BLOCKED.md` describing what failed and skip to the most-importantable individual scenes (Scene 6, Scene 16, Scene 22 — these three carry the most weight).

---

## Reference files (already exist in the repo)

- `outputs/VIDEO_OUTLINE.md` — script + scene descriptions (read this first)
- `outputs/BRIEF.md` — methodology and analysis findings
- `outputs/v4_one_of_97.png` — matplotlib version of Scene 6 for visual reference
- `outputs/v4_pritchard_30_teams.png` — matplotlib version of Scene 16
- `outputs/v4_bucket_breakdown.png` — matplotlib version of Scene 7
- `outputs/v4_*.csv` — the data sources

Look at the existing PNGs to understand the intended look. The Manim versions should be cleaner and animated, but the data presentation should match.

---

## Final note

The user is a betting / sports analytics person, not a video producer. Their goal isn't aesthetic perfection — it's communicating the analysis clearly. Optimize for:

1. **Numerical legibility** — every value on screen must be readable
2. **Visual hierarchy** — the punchline of each scene should be the largest/brightest element
3. **Honest data presentation** — no exaggerated bars, no axes that start at 50, no misleading scales
4. **Steady pacing** — animations are smooth, not flashy. This is data journalism, not a TikTok.

Good luck. Have fun with Scene 6 — it's the most satisfying one to build.
