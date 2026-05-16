"""Segment 3 — the Pritchard story. Scenes 8, 9."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import PRITCHARD_EVENTS, PRITCHARD_WA_TRAJECTORY


class PritchardTimeline(Scene):
    """Two-layer: WA_z trajectory (top) + event timeline (bottom)."""

    def construct(self):
        # ----- Title -----
        title = safe_text("Pritchard: the trajectory + the timing",
                          size=SIZE_HEADER, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.0)

        # ----- TOP: WA_z trajectory axes -----
        axes = Axes(
            x_range=[2021, 2026, 1],
            y_range=[-0.5, 2.0, 0.5],
            x_length=10,
            y_length=2.2,
            tips=False,
            axis_config={
                "color": DIM_TEXT,
                "stroke_width": 2,
                "include_numbers": False,
            },
        )
        axes.move_to(UP * 1.3)

        # Manual axis labels (avoid LaTeX)
        axis_labels = VGroup()
        for x_val in [2021, 2022, 2023, 2024, 2025]:
            lbl = safe_text(str(x_val), size=12, color=DIM_TEXT)
            lbl.next_to(axes.c2p(x_val, -0.5), DOWN, buff=0.08)
            axis_labels.add(lbl)
        for y_val in [0.0, 1.0, 2.0]:
            lbl = safe_text(f"{y_val:.1f}", size=12, color=DIM_TEXT,
                            font=FONT_NUMBERS)
            lbl.next_to(axes.c2p(2021, y_val), LEFT, buff=0.1)
            axis_labels.add(lbl)

        y_label = safe_text("WA_z", size=SIZE_TINY, color=DIM_TEXT)
        y_label.next_to(axes.y_axis, UP, buff=0.1)

        x_values = [pt[0] for pt in PRITCHARD_WA_TRAJECTORY]
        y_values = [pt[1] for pt in PRITCHARD_WA_TRAJECTORY]
        wa_line = axes.plot_line_graph(
            x_values=x_values,
            y_values=y_values,
            line_color=HIGHLIGHT_GREEN,
            vertex_dot_radius=0.06,
            stroke_width=3,
        )

        # ----- BOTTOM: NumberLine -----
        timeline = NumberLine(
            x_range=[2020, 2027, 1],
            length=11,
            color=DIM_TEXT,
            include_numbers=False,
            include_tip=False,
        )
        timeline.move_to(DOWN * 2.0)

        # Manual timeline number labels
        timeline_labels = VGroup()
        for yr in range(2020, 2028):
            lbl = safe_text(str(yr), size=14, color=DIM_TEXT,
                            font=FONT_NUMBERS)
            lbl.next_to(timeline.n2p(yr), DOWN, buff=0.15)
            timeline_labels.add(lbl)

        # Draw axes + numberline
        self.play(
            Create(axes),
            FadeIn(axis_labels),
            FadeIn(y_label),
            Create(timeline),
            FadeIn(timeline_labels),
            run_time=1.5,
        )

        # Draw WA trajectory line
        self.play(Create(wa_line), run_time=2.0)

        # ----- Build event callouts -----
        callouts = []
        event_dots = []
        # Alternate above/below: place callouts above line. Stagger vertical offsets to avoid overlap.
        vertical_offsets = [0.5, 1.0, 0.6, 1.1, 0.55]

        for i, (year, label_short, label_long) in enumerate(PRITCHARD_EVENTS):
            anchor = timeline.n2p(year)
            dot = Dot(anchor, radius=0.09, color=HIGHLIGHT_AMBER)

            short_t = safe_text(label_short, size=SIZE_SMALL,
                                color=TEXT_COLOR, weight=BOLD)
            long_t = safe_text(label_long, size=SIZE_TINY, color=DIM_TEXT)
            text_group = VGroup(short_t, long_t).arrange(DOWN, buff=0.08)

            v_off = vertical_offsets[i]
            text_group.move_to(anchor + UP * (v_off + text_group.height / 2 + 0.1))

            connector = Line(
                anchor + UP * 0.08,
                text_group.get_bottom() + DOWN * 0.02,
                color=DIM_TEXT,
                stroke_width=1.5,
            )

            callout = VGroup(connector, dot, text_group)
            callouts.append(callout)
            event_dots.append(dot)

        self.play(
            LaggedStart(*[FadeIn(c) for c in callouts], lag_ratio=0.4),
            run_time=3.5,
        )

        self.wait(0.8)

        # ----- KEY MOMENT: dashed line from WA curve at 2023.78 -----
        ext_year = 2023.78
        # Interpolate y on WA curve at x=2023.78 (between 2023→0.5 and 2024→1.4)
        # frac = 0.78 → y = 0.5 + 0.78*(1.4-0.5) = 0.5 + 0.702 = 1.202
        ext_y_wa = 0.5 + 0.78 * (1.4 - 0.5)
        top_point = axes.c2p(ext_year, ext_y_wa)
        bottom_point = event_dots[2].get_center()

        dashed = DashedLine(
            top_point,
            bottom_point,
            color=HIGHLIGHT_AMBER,
            stroke_width=3,
            dash_length=0.12,
        )

        ext_label = safe_text("Extension signed HERE",
                              size=SIZE_SMALL,
                              color=HIGHLIGHT_AMBER,
                              weight=BOLD)
        ext_label.next_to(top_point, RIGHT, buff=0.2)
        # Make sure label doesn't go off-screen; nudge if needed
        if ext_label.get_right()[0] > 6.8:
            ext_label.next_to(top_point, LEFT, buff=0.2)

        # Highlight pulse on extension dot
        self.play(
            Create(dashed),
            event_dots[2].animate.set_color(HIGHLIGHT_AMBER).scale(1.4),
            run_time=1.0,
        )
        self.play(Write(ext_label), run_time=0.8)

        self.wait(2.0)
        self.wait(0.3)


class ThreeReasonsCallout(Scene):
    """Three numbered reasons Pritchard's deal was unique, with mini grid."""

    def construct(self):
        title = safe_text("Why Pritchard? Three reasons.",
                          size=SIZE_HEADER, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)

        reasons = [
            ("1", "Extended BEFORE the breakout", HIGHLIGHT_AMBER),
            ("2", "Length compounds (3 yrs x $7M)", HIGHLIGHT_AMBER),
            ("3", "Price anchored LOW, not just early", HIGHLIGHT_GREEN),
        ]

        lines = []
        for num, desc, color in reasons:
            circle = Circle(radius=0.4, color=color, fill_opacity=0.8,
                            stroke_width=0)
            num_t = safe_text(num, size=SIZE_BODY, color=BACKGROUND, weight=BOLD)
            num_t.move_to(circle.get_center())
            num_group = VGroup(circle, num_t)

            desc_t = safe_text(desc, size=SIZE_BODY, color=TEXT_COLOR)
            line = VGroup(num_group, desc_t).arrange(RIGHT, buff=0.4)
            lines.append(line)

        group = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        group.move_to(ORIGIN).shift(LEFT * 1.5 + DOWN * 0.2)

        # Sequence: line 1
        self.play(FadeIn(lines[0], shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.5)

        # line 2
        self.play(FadeIn(lines[1], shift=RIGHT * 0.2), run_time=0.7)
        self.wait(1.5)

        # line 3
        self.play(FadeIn(lines[2], shift=RIGHT * 0.2), run_time=0.7)
        self.wait(0.5)

        # Highlight box behind line 3
        highlight = Rectangle(
            width=lines[2].width + 0.5,
            height=lines[2].height + 0.3,
            color=HIGHLIGHT_GREEN,
            fill_opacity=0.2,
            stroke_width=0,
        )
        highlight.move_to(lines[2].get_center())
        self.add(highlight)
        self.bring_to_back(highlight)
        self.play(FadeIn(highlight), run_time=0.5)

        # ----- 2x2 grid of mini player icons to the right of line 3 -----
        # All three "comparable" players were also extended pre-breakout, but
        # at market-rate prices. Only Pritchard's price+timing combo produced
        # surplus.
        players = [
            ("Avdija $13.75M/yr",   False),
            ("J. Johnson $30M/yr",  False),
            ("Pritchard $7.5M/yr",  True),
        ]

        icons = []
        for name, is_good in players:
            color = HIGHLIGHT_GREEN if is_good else HIGHLIGHT_RED
            circle = Circle(radius=0.25, color=color, fill_opacity=0.8,
                            stroke_width=0)
            # mark above
            if is_good:
                # check shape: V from two lines
                p1 = circle.get_top() + UP * 0.15 + LEFT * 0.18
                p2 = circle.get_top() + UP * 0.05
                p3 = circle.get_top() + UP * 0.25 + RIGHT * 0.18
                mark = VGroup(
                    Line(p1, p2, color=HIGHLIGHT_GREEN, stroke_width=4),
                    Line(p2, p3, color=HIGHLIGHT_GREEN, stroke_width=4),
                )
            else:
                # X mark
                c = circle.get_top() + UP * 0.18
                off = 0.12
                mark = VGroup(
                    Line(c + LEFT*off + DOWN*off, c + RIGHT*off + UP*off,
                         color=HIGHLIGHT_RED, stroke_width=4),
                    Line(c + LEFT*off + UP*off, c + RIGHT*off + DOWN*off,
                         color=HIGHLIGHT_RED, stroke_width=4),
                )

            name_t = safe_text(name, size=SIZE_TINY, color=TEXT_COLOR)
            name_t.next_to(circle, DOWN, buff=0.12)

            icon = VGroup(mark, circle, name_t)
            icons.append(icon)

        # Arrange in 2x2 grid
        grid = VGroup(*icons).arrange_in_grid(rows=2, cols=2,
                                              buff=(0.6, 0.5))
        grid.next_to(lines[2], RIGHT, buff=0.8)
        # If grid goes off-screen, nudge down/right adjust
        if grid.get_right()[0] > 6.8:
            grid.shift(LEFT * (grid.get_right()[0] - 6.6))

        self.play(
            LaggedStart(*[FadeIn(ic, shift=UP * 0.15) for ic in icons],
                        lag_ratio=0.2),
            run_time=1.5,
        )

        self.wait(2.0)
        self.wait(0.3)
