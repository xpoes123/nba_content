import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
import numpy as np
from manim_config import *
from data_loader import make_scatter_sample


class PriceFitScatter(Scene):
    def construct(self):
        # ----- Axes -----
        ax = Axes(
            x_range=[-2, 5.5, 1],
            y_range=[0, 60, 10],
            x_length=9,
            y_length=5,
            tips=False,
            axis_config={
                "color": DIM_TEXT,
                "stroke_width": 2,
                "include_numbers": False,
            },
        )
        ax.shift(DOWN * 0.3)

        # Manual axis tick labels (avoid LaTeX)
        tick_labels = VGroup()
        for xv in range(-2, 6):
            lbl = safe_text(str(xv), size=SIZE_TINY, color=DIM_TEXT,
                            font=FONT_NUMBERS)
            lbl.next_to(ax.c2p(xv, 0), DOWN, buff=0.12)
            tick_labels.add(lbl)
        for yv in range(0, 61, 10):
            lbl = safe_text(str(yv), size=SIZE_TINY, color=DIM_TEXT,
                            font=FONT_NUMBERS)
            lbl.next_to(ax.c2p(-2, yv), LEFT, buff=0.12)
            tick_labels.add(lbl)

        x_label = safe_text("Wins Added (z-score)", size=SIZE_SMALL, color=DIM_TEXT)
        x_label.next_to(ax.x_axis, DOWN, buff=0.5)
        y_label = safe_text("Salary ($M)", size=SIZE_SMALL, color=DIM_TEXT)
        y_label.rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.5)

        title = safe_text(
            "Price = $2.3M + $4.86M·WA_z",
            size=SIZE_HEADER,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.4)

        self.play(Create(ax), FadeIn(tick_labels), FadeIn(x_label),
                  FadeIn(y_label), FadeIn(title))

        # ----- Data -----
        samples = make_scatter_sample(42)

        def clamp(z, s):
            # Keep dots inside plot bounds for safety
            z = max(-2, min(5.5, z))
            s = max(0, min(60, s))
            return z, s

        open_dots = []
        for z, s in samples["open_neg"]:
            z, s = clamp(z, s)
            open_dots.append(
                Dot(ax.c2p(z, s), radius=0.08,
                    color=BUCKET_COLORS["open_negotiation"])
            )
        max_dots = []
        for z, s in samples["max"]:
            z, s = clamp(z, s)
            max_dots.append(
                Dot(ax.c2p(z, s), radius=0.08, color=BUCKET_COLORS["max"])
            )
        min_dots = []
        for z, s in samples["min"]:
            z, s = clamp(z, s)
            min_dots.append(
                Dot(ax.c2p(z, s), radius=0.08, color=BUCKET_COLORS["min"])
            )

        # ----- Open negotiation dots (fit sample) -----
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in open_dots],
                lag_ratio=0.02,
                run_time=1.2,
            )
        )

        # ----- Regression line -----
        line = ax.plot(lambda x: 2.3 + 4.86 * x,
                       x_range=[-2, 5],
                       color=HIGHLIGHT_GREEN)
        self.play(Create(line), run_time=1.2)

        # ----- Slope annotation -----
        end_point = ax.c2p(5, min(60, 2.3 + 4.86 * 5))
        slope_label = safe_text("$4.86M / SD", size=SIZE_SMALL,
                                color=HIGHLIGHT_AMBER, font=FONT_NUMBERS)
        slope_label.move_to(end_point + LEFT * 1.4 + UP * 0.4)
        self.play(FadeIn(slope_label))

        # ----- Max dots + callout -----
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in max_dots],
                lag_ratio=0.04,
                run_time=1.0,
            )
        )
        cluster_center = ax.c2p(2.5, 50)
        callout = safe_text(
            "max contracts cap at ~$55M — would flatten the slope",
            size=SIZE_SMALL,
            color=DIM_TEXT,
        )
        callout.next_to(title, DOWN, buff=0.15)
        arrow = Arrow(
            start=callout.get_bottom() + DOWN * 0.05,
            end=cluster_center + UP * 0.2,
            color=DIM_TEXT,
            buff=0.1,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.05,
        )
        self.play(FadeIn(callout), Create(arrow))

        # ----- Min dots -----
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in min_dots],
                lag_ratio=0.04,
                run_time=0.8,
            )
        )

        self.wait(2)
        self.wait(0.3)


class AgingCurve(Scene):
    def construct(self):
        ax = Axes(
            x_range=[19, 40, 2],
            y_range=[0, 1.1, 0.2],
            x_length=9,
            y_length=4.5,
            tips=False,
            axis_config={
                "color": DIM_TEXT,
                "stroke_width": 2,
                "include_numbers": False,
            },
        )
        ax.shift(DOWN * 0.2)

        tick_labels = VGroup()
        for xv in range(19, 40, 2):
            lbl = safe_text(str(xv), size=SIZE_TINY, color=DIM_TEXT,
                            font=FONT_NUMBERS)
            lbl.next_to(ax.c2p(xv, 0), DOWN, buff=0.12)
            tick_labels.add(lbl)
        for yv in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            lbl = safe_text(f"{yv:.1f}", size=SIZE_TINY, color=DIM_TEXT,
                            font=FONT_NUMBERS)
            lbl.next_to(ax.c2p(19, yv), LEFT, buff=0.12)
            tick_labels.add(lbl)

        x_label = safe_text("Age", size=SIZE_SMALL, color=DIM_TEXT)
        x_label.next_to(ax.x_axis, DOWN, buff=0.5)
        y_label = safe_text("Production multiplier", size=SIZE_SMALL, color=DIM_TEXT)
        y_label.rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.5)

        title = safe_text("Aging curve", size=SIZE_HEADER, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        def aging_fn(age):
            if age <= 26:
                return 0.65 + 0.05 * (age - 19)
            elif age <= 32:
                return 1.0 - 0.075 * (age - 26)
            else:
                return max(0.05, 0.55 - 0.10 * (age - 32))

        curve = ax.plot(aging_fn, x_range=[19, 39], color=HIGHLIGHT_AMBER)

        self.play(Create(ax), FadeIn(tick_labels), FadeIn(x_label),
                  FadeIn(y_label), FadeIn(title))
        self.play(Create(curve), run_time=1.5)

        # ----- Caption -----
        caption = safe_text(
            "Production declines ~5%/yr after age 28",
            size=SIZE_SMALL,
            color=DIM_TEXT,
        )
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption))

        # ----- Moving dot via ValueTracker -----
        age_tracker = ValueTracker(22)

        dot = always_redraw(
            lambda: Dot(
                ax.c2p(age_tracker.get_value(), aging_fn(age_tracker.get_value())),
                radius=0.12,
                color=HIGHLIGHT_GREEN,
            )
        )

        age_label = always_redraw(
            lambda: safe_text(
                f"Age {age_tracker.get_value():.0f}  ·  {aging_fn(age_tracker.get_value()):.2f}×",
                size=SIZE_SMALL,
                color=TEXT_COLOR,
                font=FONT_NUMBERS,
            ).next_to(
                ax.c2p(age_tracker.get_value(),
                       aging_fn(age_tracker.get_value())),
                UP,
                buff=0.2,
            )
        )

        self.add(dot, age_label)
        self.wait(0.4)

        self.play(age_tracker.animate.set_value(35), run_time=4.0, rate_func=linear)

        self.wait(2)
        self.wait(0.3)


class MultiplierStack(Scene):
    def construct(self):
        title = safe_text(
            "Effective cost per $1 of salary",
            size=SIZE_HEADER,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        tiers = [
            ("Below cap", 0.5, BUCKET_COLORS["min"]),
            ("Above cap", 1.0, TIER_COLORS["above_cap_below_tax"]),
            ("Taxpayer", 1.5, TIER_COLORS["taxpayer"]),
            ("1st apron", 2.3, TIER_COLORS["first_apron"]),
            ("2nd apron", 3.5, TIER_COLORS["second_apron"]),
        ]

        max_mult = max(t[1] for t in tiers)
        max_bar_height = 4.0
        bar_width = 1.4
        spacing = 0.4
        n = len(tiers)
        total_width = n * bar_width + (n - 1) * spacing
        start_x = -total_width / 2 + bar_width / 2

        # Baseline y for bar bottoms
        baseline_y = -2.3

        bars = []
        mult_labels = []
        name_labels = []

        for i, (name, mult, color) in enumerate(tiers):
            h = (mult / max_mult) * max_bar_height
            x = start_x + i * (bar_width + spacing)
            bar = Rectangle(
                width=bar_width,
                height=h,
                color=color,
                fill_opacity=0.9,
                stroke_width=0,
            )
            bar.move_to([x, baseline_y + h / 2, 0])
            bars.append(bar)

            mlabel = safe_text(
                f"{mult}×",
                size=SIZE_BODY,
                font=FONT_NUMBERS,
                color=TEXT_COLOR,
            )
            mlabel.next_to(bar, UP, buff=0.2)
            mult_labels.append(mlabel)

            nlabel = safe_text(name, size=SIZE_SMALL, color=DIM_TEXT)
            nlabel.next_to(bar, DOWN, buff=0.25)
            name_labels.append(nlabel)

        # Static baseline indicator line (1× reference)
        ref_y = baseline_y + (1.0 / max_mult) * max_bar_height
        ref_line = DashedLine(
            start=[start_x - bar_width, ref_y, 0],
            end=[start_x + total_width, ref_y, 0],
            color=DIM_TEXT,
            stroke_width=1.5,
        )
        ref_label = safe_text("1× (no premium)", size=SIZE_TINY, color=DIM_TEXT)
        ref_label.next_to(ref_line.get_end(), RIGHT, buff=0.1)

        self.play(FadeIn(ref_line), FadeIn(ref_label))

        # Show name labels first so they appear under bars as they grow
        self.play(
            LaggedStart(
                *[FadeIn(nl) for nl in name_labels],
                lag_ratio=0.1,
                run_time=0.6,
            )
        )

        # Animate bars growing from bottom + multiplier labels fading in
        anims = []
        for bar, mlabel in zip(bars, mult_labels):
            anims.append(
                AnimationGroup(
                    GrowFromEdge(bar, DOWN),
                    FadeIn(mlabel, shift=UP * 0.2),
                    lag_ratio=0.3,
                )
            )
        self.play(LaggedStart(*anims, lag_ratio=0.2, run_time=2.5))

        self.wait(2)
        self.wait(0.3)
