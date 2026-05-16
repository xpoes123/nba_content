"""Segment 2 — the killer stat. Scenes 6, 7."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import (
    PRITCHARD_DOT_INDEX, GRID_COLS, GRID_ROWS,
    BUCKET_POSITIVE_SHARES,
)


class NinetySevenDots(Scene):
    """The headline visual. 97 dots, 96 turn red, 1 stays green."""

    def construct(self):
        N = 97

        # ----- Build the 12x9 grid -----
        dots = VGroup(*[make_dot(color=DIM_TEXT, radius=0.16) for _ in range(N)])
        dots.arrange_in_grid(rows=GRID_ROWS, cols=GRID_COLS, buff=0.42)
        dots.move_to(ORIGIN).shift(DOWN * 0.3)

        # Phase 1: populate
        self.play(
            LaggedStart(*[FadeIn(d, scale=2) for d in dots],
                        lag_ratio=0.025),
            run_time=3.5,
        )

        # Phase 2: label
        label = safe_text("97 openly negotiated NBA contracts",
                          size=SIZE_HEADER, color=TEXT_COLOR, weight=BOLD)
        label.next_to(dots, UP, buff=0.5)
        sub = safe_text("MP >= 1000 min, 2+ years remaining",
                        size=SIZE_SMALL, color=DIM_TEXT)
        sub.next_to(label, DOWN, buff=0.15)
        self.play(Write(label), FadeIn(sub, shift=UP*0.1), run_time=1.2)

        # Phase 3: suspense
        self.wait(1.2)

        # Phase 4: the reveal
        pritchard_dot = dots[PRITCHARD_DOT_INDEX]
        other_dots = [d for i, d in enumerate(dots) if i != PRITCHARD_DOT_INDEX]

        self.play(
            pritchard_dot.animate.set_color(HIGHLIGHT_GREEN).scale(1.7),
            LaggedStart(*[d.animate.set_color(HIGHLIGHT_RED) for d in other_dots],
                        lag_ratio=0.005),
            run_time=1.8,
        )

        # Subtle pulse on Pritchard
        self.play(pritchard_dot.animate.scale(1.15), run_time=0.25)
        self.play(pritchard_dot.animate.scale(1/1.15), run_time=0.25)

        # Phase 5: Pritchard label
        player_name = safe_text("Payton Pritchard",
                                 size=SIZE_BODY, color=HIGHLIGHT_GREEN, weight=BOLD)
        npv_label = safe_text("+$4.3M NPV",
                              size=SIZE_SMALL, color=HIGHLIGHT_GREEN,
                              font=FONT_NUMBERS)
        # Place to the side since Pritchard is bottom-left
        info = VGroup(player_name, npv_label).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        info.next_to(pritchard_dot, RIGHT, buff=0.6).shift(DOWN*0.4)
        # arrow
        arrow = Arrow(start=info.get_left() + LEFT*0.05,
                      end=pritchard_dot.get_center() + RIGHT*0.2,
                      color=HIGHLIGHT_GREEN, buff=0.1, stroke_width=3)
        self.play(GrowArrow(arrow), Write(player_name), run_time=0.8)
        self.play(FadeIn(npv_label, shift=UP*0.1), run_time=0.5)

        self.wait(1.5)
        self.wait(0.3)


class BucketPositiveShare(Scene):
    """Four horizontal bars showing % positive by bucket."""

    def construct(self):
        title = safe_text("% projected positive, by contract bucket",
                          size=SIZE_HEADER, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0)

        bucket_keys = ["min", "rookie_scale", "max", "open_negotiation"]
        rows = list(zip(BUCKET_POSITIVE_SHARES, bucket_keys))

        max_pct = 70.0
        bar_max_length = 8.5
        row_height = 0.7
        row_buff = 0.4

        bar_objs = []
        label_objs = []
        value_objs = []
        callout_objs = []

        n_rows = len(rows)
        total_h = n_rows * row_height + (n_rows - 1) * row_buff
        top_y = total_h / 2 - row_height / 2 - 0.3

        for i, ((bucket_label, pct, n), key) in enumerate(rows):
            y = top_y - i * (row_height + row_buff)
            width = max(pct / max_pct * bar_max_length, 0.04)
            bar = Rectangle(width=width, height=row_height,
                            color=BUCKET_COLORS[key], fill_opacity=0.92,
                            stroke_width=0)
            bar.move_to([-bar_max_length/2 + width/2 + 1.0, y, 0])

            lbl = safe_text(bucket_label, size=SIZE_BODY, color=TEXT_COLOR)
            lbl.next_to(bar, LEFT, buff=0.3).align_to(bar, LEFT).shift(LEFT*1.3)
            lbl.move_to([-bar_max_length/2 - 1.5, y, 0])

            val = safe_text(f"{pct}%", size=SIZE_BODY,
                            color=TEXT_COLOR, font=FONT_NUMBERS, weight=BOLD)
            val.next_to(bar, RIGHT, buff=0.25)

            extra = safe_text(f"(n={n})", size=SIZE_SMALL,
                              color=DIM_TEXT, font=FONT_NUMBERS)
            extra.next_to(val, RIGHT, buff=0.25)
            callout_objs.append(extra)

            bar_objs.append(bar)
            label_objs.append(lbl)
            value_objs.append(val)

        for i in range(n_rows):
            self.play(
                FadeIn(label_objs[i], shift=RIGHT*0.2),
                GrowFromEdge(bar_objs[i], LEFT),
                run_time=0.55,
            )
            self.play(
                FadeIn(value_objs[i]),
                FadeIn(callout_objs[i]),
                run_time=0.3,
            )

        # Callout on open_negotiation row
        opennego_bar = bar_objs[3]
        callout = safe_text('= just Pritchard',
                            size=SIZE_BODY, color=HIGHLIGHT_GREEN,
                            weight=BOLD)
        callout.next_to(callout_objs[3], RIGHT, buff=0.4)
        arrow = Arrow(start=callout.get_left() + LEFT*0.05,
                      end=opennego_bar.get_right() + RIGHT*0.05,
                      color=HIGHLIGHT_GREEN, buff=0.05, stroke_width=3)
        # Actually point from callout area to the bar; layout is OK either way
        self.play(Write(callout), run_time=0.7)

        self.wait(2.0)
        self.wait(0.3)
