"""Segment 2 — the killer stat. Version B: more cinematic alternative.

Differences from version A:
- Grid builds from center outward via radial sort (elegant bloom).
- Longer hold beats let the suspense breathe.
- Red dots dim to opacity ~0.45 after the reveal so Pritchard pops harder.
- Pritchard dot scales 2.0x and gets a subtle glow ring that fades in/out.
- Player label sits in a callout-style box (Rectangle backing, fill_opacity 0.2).
- Final punchline: all other dots fade out, Pritchard alone with "+$4.3M NPV".
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import PRITCHARD_DOT_INDEX, GRID_COLS, GRID_ROWS


class NinetySevenDotsB(Scene):
    """Cinematic alt take on the headline 97-dots visual."""

    def construct(self):
        N = 97

        # ----- Build the 12x9 grid -----
        dots = VGroup(*[make_dot(color=DIM_TEXT, radius=0.16) for _ in range(N)])
        dots.arrange_in_grid(rows=GRID_ROWS, cols=GRID_COLS, buff=0.42)
        dots.move_to(ORIGIN).shift(DOWN * 0.3)

        # ----- Phase 1: radial-sorted populate (bloom from center) -----
        center = dots.get_center()
        # Pair each dot with its distance from grid center, sort ascending
        indexed = sorted(
            enumerate(dots),
            key=lambda pair: np.linalg.norm(pair[1].get_center() - center),
        )
        ordered_dots = [d for _, d in indexed]

        self.play(
            LaggedStart(
                *[FadeIn(d, scale=2.2) for d in ordered_dots],
                lag_ratio=0.035,
            ),
            run_time=4.2,
        )

        # ----- Phase 2: title labels -----
        label = safe_text("97 openly negotiated NBA contracts",
                          size=SIZE_HEADER, color=TEXT_COLOR, weight=BOLD)
        label.next_to(dots, UP, buff=0.55)
        sub = safe_text("MP >= 1000 min, 2+ years remaining",
                        size=SIZE_SMALL, color=DIM_TEXT)
        sub.next_to(label, DOWN, buff=0.18)
        self.play(Write(label), FadeIn(sub, shift=UP * 0.1), run_time=1.3)

        # ----- Phase 3: long suspense beat -----
        self.wait(2.0)

        # ----- Phase 4: the reveal -----
        pritchard_dot = dots[PRITCHARD_DOT_INDEX]
        other_dots = [d for i, d in enumerate(dots) if i != PRITCHARD_DOT_INDEX]

        # Re-sort the red wave radially from Pritchard so the color floods outward
        p_center = pritchard_dot.get_center()
        other_sorted = sorted(
            other_dots,
            key=lambda d: np.linalg.norm(d.get_center() - p_center),
        )

        self.play(
            pritchard_dot.animate.set_color(HIGHLIGHT_GREEN).scale(2.0),
            LaggedStart(
                *[d.animate.set_color(HIGHLIGHT_RED) for d in other_sorted],
                lag_ratio=0.012,
            ),
            run_time=2.2,
        )

        # ----- Phase 4b: glow ring + dim the reds -----
        glow = Circle(
            radius=pritchard_dot.width * 0.95,
            color=HIGHLIGHT_GREEN,
            stroke_width=3,
            stroke_opacity=0.0,
            fill_opacity=0.0,
        ).move_to(pritchard_dot.get_center())

        self.play(
            glow.animate.set_stroke(opacity=0.85).scale(1.6),
            *[d.animate.set_opacity(0.45) for d in other_dots],
            run_time=0.9,
        )
        self.play(
            glow.animate.set_stroke(opacity=0.0).scale(1.3),
            run_time=0.7,
        )

        # ----- Phase 5: callout-box label for Pritchard -----
        player_name = safe_text("Payton Pritchard",
                                size=SIZE_BODY, color=HIGHLIGHT_GREEN, weight=BOLD)
        npv_label = safe_text("+$4.3M NPV",
                              size=SIZE_SMALL, color=HIGHLIGHT_GREEN,
                              font=FONT_NUMBERS)
        info_inner = VGroup(player_name, npv_label).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT,
        )
        box = Rectangle(
            width=info_inner.width + 0.5,
            height=info_inner.height + 0.4,
            color=HIGHLIGHT_GREEN,
            fill_opacity=0.2,
            stroke_width=2,
        )
        box.move_to(info_inner.get_center())
        callout = VGroup(box, info_inner)
        # Place to the right of Pritchard (he's bottom-LEFT)
        callout.next_to(pritchard_dot, RIGHT, buff=0.7).shift(UP * 0.2)

        arrow = Arrow(
            start=callout.get_left() + LEFT * 0.02,
            end=pritchard_dot.get_center() + RIGHT * 0.25,
            color=HIGHLIGHT_GREEN, buff=0.1, stroke_width=3,
        )
        self.play(GrowArrow(arrow), FadeIn(box, scale=0.9), run_time=0.7)
        self.play(Write(player_name), run_time=0.6)
        self.play(FadeIn(npv_label, shift=UP * 0.08), run_time=0.5)

        # ----- Phase 6: hold to read -----
        self.wait(1.6)

        # ----- Phase 7: punchline — fade everything except Pritchard + tag -----
        red_group = VGroup(*other_dots)
        self.play(
            FadeOut(red_group),
            FadeOut(label),
            FadeOut(sub),
            FadeOut(arrow),
            run_time=1.1,
        )

        # Move Pritchard + his callout to center stage for the punchline
        target_dot_pos = ORIGIN + LEFT * 1.6
        offset = target_dot_pos - pritchard_dot.get_center()
        self.play(
            pritchard_dot.animate.shift(offset),
            callout.animate.shift(offset),
            run_time=0.9,
        )

        # Tiny final pulse
        self.play(pritchard_dot.animate.scale(1.18), run_time=0.25)
        self.play(pritchard_dot.animate.scale(1 / 1.18), run_time=0.25)

        self.wait(1.4)
        self.wait(0.3)
