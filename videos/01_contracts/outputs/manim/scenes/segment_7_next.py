"""Segment 7 — the next Pritchard. Scenes 18, 19, 20, 21."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import NEXT_PRITCHARD


class NextPritchardCalendar(Scene):
    """Vertical timeline (top-to-bottom) with three decision windows."""

    def construct(self):
        title = safe_text(
            "Upcoming decision windows",
            size=SIZE_HEADER,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Horizontal number line, then rotate 90deg to make it vertical
        timeline = NumberLine(
            x_range=[2026.4, 2027.9, 0.25],
            length=7,
            color=DIM_TEXT,
            stroke_width=3,
            include_ticks=True,
            tick_size=0.08,
            include_numbers=False,
        )
        # Rotate so it runs top-to-bottom (lower year at top)
        # Default horizontal goes left->right (low->high). Rotate by -PI/2
        # so low values end up at the TOP and high values at the BOTTOM.
        timeline.rotate(-PI / 2)
        timeline.move_to([-4, -0.3, 0])

        self.play(Create(timeline), run_time=1.2)

        decisions = [
            (2026.4, "Jun 2026",    "Queta — Boston team option"),
            (2026.6, "Summer 2026", "Duren — DET restricted FA"),
            (2027.6, "Summer 2027", "Diabate — CHO RFA window"),
        ]

        callout_groups = []
        for year_float, header_text, body_text in decisions:
            dot_pos = timeline.n2p(year_float)
            dot = Dot(point=dot_pos, radius=0.16, color=HIGHLIGHT_GREEN,
                      stroke_width=2, stroke_color=BACKGROUND)

            # Callout on the RIGHT side
            header = safe_text(header_text, size=SIZE_BODY, weight=BOLD,
                               color=HIGHLIGHT_GREEN)
            body = safe_text(body_text, size=SIZE_SMALL, color=TEXT_COLOR)
            content = VGroup(header, body).arrange(DOWN, buff=0.12,
                                                   aligned_edge=LEFT)
            box = Rectangle(
                width=content.width + 0.5,
                height=content.height + 0.4,
                color=DIM_TEXT,
                fill_color=BACKGROUND,
                fill_opacity=0.9,
                stroke_width=1.5,
            )
            # Position callout on right side at the same y as the dot
            callout = VGroup(box, content)
            callout.move_to([2.5, dot_pos[1], 0])
            content.move_to(box.get_center())

            connector = Line(
                dot_pos,
                [box.get_left()[0], dot_pos[1], 0],
                color=DIM_TEXT,
                stroke_width=2,
            )

            # Pulse animation: build manually via Succession
            pulse_dot = Dot(point=dot_pos, radius=0.16, color=HIGHLIGHT_GREEN)

            group = VGroup(connector, callout)
            callout_groups.append((dot, pulse_dot, group))

        # Build LaggedStart of (dot pulse + callout fade-in) for each decision
        anims = []
        for dot, pulse_dot, group in callout_groups:
            anims.append(
                AnimationGroup(
                    GrowFromCenter(dot),
                    FadeIn(group, shift=LEFT * 0.2),
                    lag_ratio=0.0,
                )
            )

        self.play(
            LaggedStart(*anims, lag_ratio=0.4),
            run_time=3.0,
        )

        # Brief pulse on all dots together
        self.play(
            *[Indicate(dot, color=HIGHLIGHT_GREEN, scale_factor=1.4)
              for dot, _, _ in callout_groups],
            run_time=0.8,
        )

        self.wait(2.0)
        self.wait(0.3)


class QuetaSpotlight(Scene):
    """Center-screen card for Neemias Queta."""

    def construct(self):
        title = safe_text(
            "Neemias Queta — BOS",
            size=SIZE_TITLE,
            weight=BOLD,
            color=BUCKET_COLORS["min"],
        )
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # Stat lines
        line1 = safe_text(
            "Age 26   ·   WA z = 1.7 (top 4%)",
            size=SIZE_BODY,
            color=TEXT_COLOR,
        )

        salary_label = safe_text("Salary: ", size=SIZE_BODY, color=TEXT_COLOR)
        salary_val = safe_text("$2.3M", size=SIZE_BODY,
                               font=FONT_NUMBERS, color=TEXT_COLOR)
        market_label = safe_text("    Market value: ", size=SIZE_BODY,
                                 color=TEXT_COLOR)
        market_val = safe_text("$10.4M", size=SIZE_BODY,
                               font=FONT_NUMBERS, color=HIGHLIGHT_GREEN)
        line2 = VGroup(salary_label, salary_val, market_label, market_val)
        line2.arrange(RIGHT, buff=0.05)

        underpaid_label = safe_text("Underpaid by ", size=SIZE_BODY,
                                    color=TEXT_COLOR)
        underpaid_val = safe_text("$8.0M", size=SIZE_BODY,
                                  font=FONT_NUMBERS,
                                  color=HIGHLIGHT_GREEN, weight=BOLD)
        underpaid_tail = safe_text(" (single year)", size=SIZE_BODY,
                                   color=DIM_TEXT)
        line3 = VGroup(underpaid_label, underpaid_val, underpaid_tail)
        line3.arrange(RIGHT, buff=0.05)

        stats = VGroup(line1, line2, line3).arrange(DOWN, buff=0.4)
        stats.next_to(title, DOWN, buff=0.8)

        self.play(
            LaggedStart(
                FadeIn(line1, shift=UP * 0.1),
                FadeIn(line2, shift=UP * 0.1),
                FadeIn(line3, shift=UP * 0.1),
                lag_ratio=0.4,
            ),
            run_time=1.8,
        )

        # Decision-window badge
        badge_text = safe_text(
            "Jun 2026 — team option decision",
            size=SIZE_SMALL,
            color="#FFFFFF",
            weight=BOLD,
        )
        badge_bg = Rectangle(
            width=badge_text.width + 0.6,
            height=badge_text.height + 0.35,
            color=HIGHLIGHT_AMBER,
            fill_opacity=0.95,
            stroke_width=0,
        )
        badge_text.move_to(badge_bg.get_center())
        badge = VGroup(badge_bg, badge_text)
        badge.next_to(stats, DOWN, buff=0.7)

        self.play(FadeIn(badge, shift=UP * 0.1), run_time=0.7)

        # PP badge bottom-right
        pp_circle = Circle(radius=0.5, color=BUCKET_COLORS["min"],
                           fill_opacity=0.2, stroke_width=2)
        pp_text = safe_text("PP", size=SIZE_SMALL, weight=BOLD,
                            color=BUCKET_COLORS["min"])
        pp_text.move_to(pp_circle.get_center())
        pp_caption = safe_text(
            "Same template, same team, same GM",
            size=SIZE_TINY,
            color=DIM_TEXT,
        )
        pp_group = VGroup(pp_circle, pp_text)
        pp_caption.next_to(pp_group, LEFT, buff=0.2)
        pp_full = VGroup(pp_caption, pp_group)
        pp_full.to_corner(DR, buff=0.6)

        self.play(FadeIn(pp_full, shift=LEFT * 0.2), run_time=0.7)

        self.wait(2.5)
        self.wait(0.3)


class DurenForecast(Scene):
    """Two-column scenario forecast for Jalen Duren."""

    def construct(self):
        title = safe_text(
            "Jalen Duren — DET",
            size=SIZE_HEADER,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # Left column — counterfactual: what Detroit could have done before Oct 20, 2025
        left_header = safe_text(
            "Counterfactual: ext. by Oct 2025",
            size=SIZE_BODY,
            color=HIGHLIGHT_GREEN,
            weight=BOLD,
        )
        left_body1 = safe_text(
            "4yr / $80M @ age 22",
            size=SIZE_SMALL,
            font=FONT_NUMBERS,
            color=TEXT_COLOR,
        )
        left_body2 = safe_text(
            "-> would have been next Pritchard",
            size=SIZE_SMALL,
            color=HIGHLIGHT_GREEN,
            weight=BOLD,
        )
        left_col = VGroup(left_header, left_body1, left_body2).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )
        left_col.move_to([-3.5, 0.5, 0])

        # Right column — what actually happened
        right_header = safe_text(
            "What happened: deadline closed",
            size=SIZE_BODY,
            color=HIGHLIGHT_RED,
            weight=BOLD,
        )
        right_body1 = safe_text(
            "All-Star Feb 2026 -> RFA market $35M/yr",
            size=SIZE_SMALL,
            font=FONT_NUMBERS,
            color=TEXT_COLOR,
        )
        right_body2 = safe_text(
            "Detroit must match -> no surplus",
            size=SIZE_SMALL,
            color=HIGHLIGHT_RED,
            weight=BOLD,
        )
        right_col = VGroup(right_header, right_body1, right_body2).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )
        right_col.move_to([3.5, 0.5, 0])
        # Re-align: center each column on its x
        for col, cx in [(left_col, -3.5), (right_col, 3.5)]:
            col.move_to([cx, col.get_center()[1], 0])

        # Vertical divider
        divider = Line(
            start=[0, 1.4, 0],
            end=[0, -1.2, 0],
            color=DIM_TEXT,
            stroke_width=2,
        )

        self.play(Create(divider), run_time=0.5)

        # Pair-by-pair LaggedStart
        pairs = [
            (left_header, right_header),
            (left_body1, right_body1),
            (left_body2, right_body2),
        ]
        anims = []
        for l, r in pairs:
            anims.append(
                AnimationGroup(
                    FadeIn(l, shift=RIGHT * 0.2),
                    FadeIn(r, shift=LEFT * 0.2),
                )
            )
        self.play(
            LaggedStart(*anims, lag_ratio=0.3),
            run_time=2.0,
        )

        # Center label
        center_label = safe_text(
            "Model: 65% scenario B",
            size=SIZE_HEADER,
            color=HIGHLIGHT_AMBER,
            weight=BOLD,
        )
        center_label.move_to([0, -2.2, 0])
        self.play(FadeIn(center_label, shift=UP * 0.2), run_time=0.8)

        self.wait(2.5)
        self.wait(0.3)


class DiabateUnderRadar(Scene):
    """Under-the-radar pick: Moussa Diabate."""

    def construct(self):
        title = safe_text(
            "Moussa Diabate — CHO",
            size=SIZE_TITLE,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.8)

        stats = safe_text(
            "Age 24   ·   WA z = 1.1   ·   $2.3M vet min",
            size=SIZE_BODY,
            font=FONT_NUMBERS,
            color=TEXT_COLOR,
        )
        stats.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(stats), run_time=0.6)

        # List header
        list_header = safe_text(
            "Charlotte already extended cheap:",
            size=SIZE_BODY,
            color=TEXT_COLOR,
            weight=BOLD,
        )
        list_header.next_to(stats, DOWN, buff=0.7)
        self.play(FadeIn(list_header, shift=UP * 0.1), run_time=0.5)

        # Build bullet rows
        bullets = [
            ("Knueppel — 4yr rookie", TEXT_COLOR, False),
            ("Kalkbrenner — 4yr min", TEXT_COLOR, False),
            ("Diabate — ???", HIGHLIGHT_AMBER, True),
        ]

        rows = []
        for text_str, text_color, is_pulse in bullets:
            dot = Dot(radius=0.08, color=text_color)
            txt = safe_text(text_str, size=SIZE_BODY, color=text_color,
                            weight=(BOLD if is_pulse else NORMAL))
            row = VGroup(dot, txt).arrange(RIGHT, buff=0.3)
            rows.append((row, txt, is_pulse))

        rows_group = VGroup(*[r[0] for r in rows]).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )
        rows_group.next_to(list_header, DOWN, buff=0.4)

        # LaggedStart fade in
        self.play(
            LaggedStart(
                *[FadeIn(r[0], shift=RIGHT * 0.2) for r in rows],
                lag_ratio=0.3,
            ),
            run_time=1.5,
        )

        # Pulse the "???" row twice
        pulse_txt = rows[-1][1]
        for _ in range(2):
            self.play(pulse_txt.animate.scale(1.1), run_time=0.3)
            self.play(pulse_txt.animate.scale(1.0 / 1.1), run_time=0.3)

        # Caption
        caption = safe_text(
            "Under-the-radar pick",
            size=SIZE_BODY,
            color=HIGHLIGHT_AMBER,
            weight=BOLD,
        )
        caption.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.6)

        self.wait(2.0)
        self.wait(0.3)
