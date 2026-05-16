"""Segment 6 — 30-team Pritchard chart. Version B: tier-grouped cinematic alt.

Differences from version A:
- Compact left-side tier-color legend draws FIRST (orients the viewer).
- Bars animate IN TIER GROUPS, simultaneously within each tier, in tier order
  (second_apron -> first_apron -> taxpayer -> above_cap_below_tax -> below_cap).
  This emphasizes that team CONTEXT drives the variance, not random noise.
- Subtle horizontal divider lines between tier groups (DIM_TEXT, opacity 0.2).
- GSW (top) gets a glowing pulse, BRK (bottom) gets a quieter pulse.
- Curved bracket connects GSW and BRK with a "7x range" label in HIGHLIGHT_AMBER.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import PRITCHARD_30_TEAMS


# Tier order, top -> bottom
TIER_ORDER = ["second_apron", "first_apron", "taxpayer",
              "above_cap_below_tax", "below_cap"]
TIER_LABELS = {
    "second_apron":        "Second apron",
    "first_apron":         "First apron",
    "taxpayer":            "Taxpayer",
    "above_cap_below_tax": "Above cap",
    "below_cap":           "Below cap",
}


class Pritchard30TeamsB(Scene):
    """Tier-grouped cinematic alt for the 30-team chart."""

    def construct(self):
        # ----- Title -----
        title = safe_text("If Pritchard signed with every other team",
                          size=SIZE_HEADER, color=TEXT_COLOR, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = safe_text("Effective NPV (millions), by team cap tier",
                             size=SIZE_SMALL, color=DIM_TEXT)
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.9)
        self.wait(0.6)

        # ----- Chart geometry -----
        N = len(PRITCHARD_30_TEAMS)
        max_val = max(v for _, _, _, v in PRITCHARD_30_TEAMS)
        bar_max_len = 4.2           # max bar width in screen units
        row_height = 0.185          # vertical spacing per row
        bar_height = 0.135

        # Anchor: left edge of bars (shifted left to make room for the
        # bracket and "7x range" callout on the right)
        bar_left_x = -1.6
        # Top row y-coordinate (just below subtitle)
        top_y = 2.65
        bottom_y = top_y - (N - 1) * row_height

        # ----- Tier legend (left side, drawn first) -----
        legend_items = []
        for tier in TIER_ORDER:
            swatch = Rectangle(width=0.22, height=0.22,
                               color=TIER_COLORS[tier],
                               fill_opacity=0.95, stroke_width=0)
            lbl = safe_text(TIER_LABELS[tier], size=SIZE_TINY,
                            color=TEXT_COLOR)
            lbl.next_to(swatch, RIGHT, buff=0.15)
            legend_items.append(VGroup(swatch, lbl))
        legend = VGroup(*legend_items).arrange(DOWN, buff=0.22,
                                               aligned_edge=LEFT)
        legend.to_edge(LEFT, buff=0.35).shift(DOWN * 0.2)

        legend_title = safe_text("TIER", size=SIZE_TINY,
                                 color=DIM_TEXT, weight=BOLD)
        legend_title.next_to(legend, UP, buff=0.2, aligned_edge=LEFT)

        self.play(
            FadeIn(legend_title, shift=DOWN * 0.1),
            LaggedStart(*[FadeIn(item, shift=RIGHT * 0.15)
                          for item in legend_items],
                        lag_ratio=0.2),
            run_time=2.8,
        )
        self.wait(0.8)

        # ----- Build bars (but don't show them yet) -----
        # Group by tier in the canonical order while preserving data ordering
        all_bars = []   # parallel to PRITCHARD_30_TEAMS
        all_labels = []
        all_values = []
        by_tier = {t: [] for t in TIER_ORDER}

        for i, (team, tier, _npv, val) in enumerate(PRITCHARD_30_TEAMS):
            y = top_y - i * row_height
            width = max(val / max_val * bar_max_len, 0.05)
            bar = Rectangle(width=width, height=bar_height,
                            color=TIER_COLORS[tier],
                            fill_opacity=0.92, stroke_width=0)
            bar.move_to([bar_left_x + width / 2, y, 0])

            team_lbl = safe_text(team, size=SIZE_TINY, color=TEXT_COLOR,
                                 font=FONT_BODY)
            team_lbl.move_to([bar_left_x - 0.25, y, 0]).align_to(
                np.array([bar_left_x - 0.05, y, 0]), RIGHT)

            val_lbl = safe_text(f"${val:.1f}M", size=SIZE_TINY,
                                color=TEXT_COLOR, font=FONT_NUMBERS)
            val_lbl.next_to(bar, RIGHT, buff=0.12)

            all_bars.append(bar)
            all_labels.append(team_lbl)
            all_values.append(val_lbl)
            by_tier[tier].append(i)

        # ----- Tier divider lines (between groups) -----
        divider_lines = []
        for tier_a, tier_b in zip(TIER_ORDER[:-1], TIER_ORDER[1:]):
            if not by_tier[tier_a] or not by_tier[tier_b]:
                continue
            last_idx = by_tier[tier_a][-1]
            next_idx = by_tier[tier_b][0]
            y_a = top_y - last_idx * row_height
            y_b = top_y - next_idx * row_height
            div_y = (y_a + y_b) / 2.0
            line = Line(
                start=[bar_left_x - 0.9, div_y, 0],
                end=[bar_left_x + bar_max_len + 0.6, div_y, 0],
                stroke_color=DIM_TEXT,
                stroke_width=0.8,
                stroke_opacity=0.25,
            )
            divider_lines.append(line)

        # ----- Animate bars tier by tier -----
        for tier in TIER_ORDER:
            idxs = by_tier[tier]
            if not idxs:
                continue
            # Labels appear with the bars (team labels fade in alongside)
            anims = []
            for i in idxs:
                bar = all_bars[i]
                # Grow bar horizontally from its left edge
                bar.stretch(0.001, dim=0, about_edge=LEFT)
                # Save target by re-creating width
                team_lbl = all_labels[i]
                val_lbl = all_values[i]

                target_width = max(
                    PRITCHARD_30_TEAMS[i][3] / max_val * bar_max_len, 0.05,
                )
                anims.append(
                    bar.animate.stretch_to_fit_width(target_width)
                       .move_to([bar_left_x + target_width / 2,
                                 top_y - i * row_height, 0])
                )
                anims.append(FadeIn(team_lbl, shift=RIGHT * 0.05))
                anims.append(FadeIn(val_lbl, shift=LEFT * 0.05))
                self.add(bar)

            # Tier rows simultaneous (within tier) — slower for emphasis
            n_rows = len(idxs)
            rt = 2.2 if n_rows <= 3 else (3.0 if n_rows <= 8 else 5.5)
            self.play(*anims, run_time=rt)
            self.wait(1.1)

        # ----- Draw divider lines after all bars are in -----
        if divider_lines:
            self.play(
                LaggedStart(*[Create(d) for d in divider_lines],
                            lag_ratio=0.15),
                run_time=1.4,
            )
        self.wait(0.9)

        # ----- Locate GSW (top) and BRK (bottom) -----
        gsw_idx = 0          # GSW is first row
        brk_idx = N - 1      # BRK is last row
        gsw_bar = all_bars[gsw_idx]
        brk_bar = all_bars[brk_idx]
        gsw_val_lbl = all_values[gsw_idx]
        brk_val_lbl = all_values[brk_idx]

        # ----- GSW glowing pulse -----
        gsw_glow = Rectangle(
            width=gsw_bar.width + 0.15,
            height=gsw_bar.height + 0.18,
            color=HIGHLIGHT_AMBER,
            stroke_width=2.5,
            fill_opacity=0.0,
        ).move_to(gsw_bar.get_center()).set_stroke(opacity=0.0)

        self.add(gsw_glow)
        self.play(
            gsw_glow.animate.set_stroke(opacity=0.95).scale(1.08),
            gsw_val_lbl.animate.set_color(HIGHLIGHT_AMBER),
            run_time=0.9,
        )
        self.play(
            gsw_glow.animate.set_stroke(opacity=0.0).scale(1.05),
            run_time=0.9,
        )
        # Second pulse for emphasis
        gsw_glow2 = Rectangle(
            width=gsw_bar.width + 0.15,
            height=gsw_bar.height + 0.18,
            color=HIGHLIGHT_AMBER,
            stroke_width=2.5,
            fill_opacity=0.0,
        ).move_to(gsw_bar.get_center()).set_stroke(opacity=0.0)
        self.add(gsw_glow2)
        self.play(
            gsw_glow2.animate.set_stroke(opacity=0.85).scale(1.12),
            run_time=0.7,
        )
        self.play(
            gsw_glow2.animate.set_stroke(opacity=0.0).scale(1.08),
            run_time=0.7,
        )
        self.wait(0.5)

        # ----- BRK quieter pulse -----
        brk_glow = Rectangle(
            width=max(brk_bar.width + 0.12, 0.25),
            height=brk_bar.height + 0.18,
            color=DIM_TEXT,
            stroke_width=2.0,
            fill_opacity=0.0,
        ).move_to(brk_bar.get_center()).set_stroke(opacity=0.0)

        self.add(brk_glow)
        self.play(
            brk_glow.animate.set_stroke(opacity=0.85).scale(1.06),
            brk_val_lbl.animate.set_color(DIM_TEXT),
            run_time=0.9,
        )
        self.play(
            brk_glow.animate.set_stroke(opacity=0.0).scale(1.03),
            run_time=0.9,
        )
        self.wait(0.6)

        # ----- Curved bracket connecting GSW and BRK -----
        # Right edge of the 16:9 frame is ~7.11; keep everything <6.8.
        gsw_y = gsw_bar.get_center()[1]
        brk_y = brk_bar.get_center()[1]
        mid_y = (gsw_y + brk_y) / 2.0

        # Stubs start at the right edge of the longest value label.
        gsw_val_right = gsw_val_lbl.get_right()[0] + 0.15
        brk_val_right = bar_left_x + bar_max_len + 0.6  # align with GSW row
        stub_start_x = max(gsw_val_right, brk_val_right)
        bracket_x = stub_start_x + 0.45

        gsw_anchor = np.array([stub_start_x, gsw_y, 0])
        brk_anchor = np.array([stub_start_x, brk_y, 0])
        gsw_stub_end = np.array([bracket_x, gsw_y, 0])
        brk_stub_end = np.array([bracket_x, brk_y, 0])

        gsw_stub = Line(gsw_anchor, gsw_stub_end,
                        color=HIGHLIGHT_AMBER, stroke_width=2.5)
        brk_stub = Line(brk_anchor, brk_stub_end,
                        color=HIGHLIGHT_AMBER, stroke_width=2.5)

        # Curved spine bulges to the right (small bulge to fit on-screen)
        spine = ArcBetweenPoints(
            gsw_stub_end, brk_stub_end,
            angle=-PI / 6,   # gentle bulge right
            color=HIGHLIGHT_AMBER,
            stroke_width=2.5,
        )

        # "6x range" label, positioned to the right of the bracket
        range_label = safe_text("6x range", size=SIZE_SMALL,
                                color=HIGHLIGHT_AMBER,
                                weight=BOLD, font=FONT_DISPLAY)
        # Approximate spine right-most x: bracket_x + sagitta of arc
        chord = abs(gsw_y - brk_y)
        sagitta = (chord / 2.0) * np.tan((PI / 6) / 2.0)
        spine_right_x = bracket_x + sagitta
        range_label.move_to([spine_right_x + 0.5, mid_y, 0])

        sub_range = safe_text("$2.2M -> $13.3M",
                              size=SIZE_TINY, color=DIM_TEXT,
                              font=FONT_NUMBERS)
        sub_range.next_to(range_label, DOWN, buff=0.1)

        self.play(
            Create(gsw_stub),
            Create(brk_stub),
            run_time=1.0,
        )
        self.play(Create(spine), run_time=1.6)
        self.play(
            FadeIn(range_label, shift=LEFT * 0.2),
            run_time=1.0,
        )
        self.play(FadeIn(sub_range, shift=UP * 0.1), run_time=0.7)

        # ----- Final pulse on range label -----
        self.play(range_label.animate.scale(1.15), run_time=0.4)
        self.play(range_label.animate.scale(1 / 1.15), run_time=0.4)

        # ----- Hold for emphasis -----
        self.wait(4.0)

        self.wait(0.3)
