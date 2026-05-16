"""Shared Manim config + reusable helpers for the NBA contracts video.

Every scene file should `from manim_config import *` at the top.
"""
from manim import *

# ---------------- Color palette ----------------
TIER_COLORS = {
    "second_apron":        "#c1272d",
    "first_apron":         "#e67e22",
    "taxpayer":            "#f1c40f",
    "above_cap_below_tax": "#34495e",
    "below_cap":           "#95a5a6",
}

BUCKET_COLORS = {
    "rookie_scale":     "#2980b9",
    "min":              "#16a085",
    "max":              "#c0392b",
    "open_negotiation": "#27ae60",
}

HIGHLIGHT_GREEN = "#27ae60"
HIGHLIGHT_RED   = "#c0392b"
HIGHLIGHT_AMBER = "#f39c12"
BACKGROUND      = "#1a1a2e"
TEXT_COLOR      = "#ECECEC"
DIM_TEXT        = "#9ca3b3"

# ---------------- Fonts ----------------
FONT_BODY    = "Inter"
FONT_NUMBERS = "JetBrains Mono"
FONT_DISPLAY = "Inter"

# ---------------- Sizes ----------------
SIZE_TITLE       = 48
SIZE_HEADER      = 36
SIZE_BODY        = 28
SIZE_SMALL       = 20
SIZE_TINY        = 14
SIZE_HERO_NUMBER = 96

# ---------------- Timing ----------------
RT_FADE        = 0.4
RT_WRITE       = 1.0
RT_BAR_DRAW    = 0.8
RT_CHART_BUILD = 2.5
RT_HOLD_SHORT  = 0.8
RT_HOLD_LONG   = 2.5
LAG_TIGHT      = 0.05
LAG_LOOSE      = 0.15

# ---------------- Global config ----------------
# Only set background; let CLI -q flag control resolution/framerate
config.background_color = BACKGROUND


# ---------------- Helpers ----------------
def make_dot(color=TEXT_COLOR, radius=0.18) -> Dot:
    return Dot(radius=radius, color=color, stroke_width=0.5, stroke_color=BLACK)


def lower_third(text: str) -> Text:
    t = Text(text, font=FONT_BODY, font_size=SIZE_TINY, color=DIM_TEXT)
    t.to_edge(DOWN, buff=0.4)
    return t


def fade_to_dim(*mobjects, opacity=0.3):
    return [m.animate.set_opacity(opacity) for m in mobjects]


def labeled_bar_h(value: float, label: str, color: str, max_value: float,
                  bar_length: float = 6.0, sign_neg: bool = False) -> VGroup:
    """Horizontal bar grouping: [label] [bar] [value]."""
    width = max(abs(value) / max_value * bar_length, 0.05)
    bar = Rectangle(width=width, height=0.4, color=color, fill_opacity=0.9,
                    stroke_width=0)
    name = Text(label, font=FONT_BODY, font_size=SIZE_SMALL, color=TEXT_COLOR)
    name.next_to(bar, LEFT, buff=0.2)
    sign = "-" if sign_neg or value < 0 else ""
    val = Text(f"{sign}${abs(value):.1f}M", font=FONT_NUMBERS,
               font_size=SIZE_SMALL, color=TEXT_COLOR)
    val.next_to(bar, RIGHT, buff=0.2)
    return VGroup(name, bar, val)


def title_card(text: str, color=TEXT_COLOR) -> Text:
    t = Text(text, font=FONT_BODY, font_size=SIZE_TITLE, color=color, weight=BOLD)
    return t


def safe_text(text: str, size: int = SIZE_BODY, color=TEXT_COLOR,
              font: str = FONT_BODY, weight=NORMAL) -> Text:
    """Text with sensible defaults — use everywhere instead of bare Text()."""
    return Text(text, font=font, font_size=size, color=color, weight=weight)
