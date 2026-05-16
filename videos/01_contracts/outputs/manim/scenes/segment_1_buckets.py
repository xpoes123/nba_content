import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import FOUR_BUCKETS


class FourBuckets(Scene):
    def construct(self):
        # ----- CBA box at top center -----
        cba_label = safe_text("CBA", size=SIZE_HEADER, weight=BOLD)
        cba_box = Rectangle(
            width=cba_label.width + 1.0,
            height=cba_label.height + 0.5,
            color=TEXT_COLOR,
            fill_opacity=0.15,
            stroke_width=2,
        )
        cba_label.move_to(cba_box.get_center())
        cba_group = VGroup(cba_box, cba_label)
        cba_group.to_edge(UP, buff=0.6)

        # ----- Four bucket rectangles -----
        bucket_groups = []
        bucket_width = 2.9
        bucket_height = 2.0
        spacing = 0.25
        total_width = 4 * bucket_width + 3 * spacing
        start_x = -total_width / 2 + bucket_width / 2

        for i, (name, desc, key) in enumerate(FOUR_BUCKETS):
            color = BUCKET_COLORS[key]
            is_open = (key == "open_negotiation")
            stroke_w = 5 if is_open else 2

            rect = Rectangle(
                width=bucket_width,
                height=bucket_height,
                color=color,
                fill_opacity=0.25,
                stroke_width=stroke_w,
            )

            # Wrap name if needed: keep short
            name_text = safe_text(name, size=SIZE_BODY, weight=BOLD, color=TEXT_COLOR)
            # Word-wrap description to ~22 chars/line
            desc_text = self._wrap_text(desc, max_chars=24)

            name_text.scale_to_fit_width(min(bucket_width - 0.3, name_text.width))
            desc_text.scale_to_fit_width(min(bucket_width - 0.3, desc_text.width))

            name_text.move_to(rect.get_top() + DOWN * (name_text.height / 2 + 0.25))
            desc_text.next_to(name_text, DOWN, buff=0.2)

            group = VGroup(rect, name_text, desc_text)

            x = start_x + i * (bucket_width + spacing)
            # Buckets sit below the CBA box; open_negotiation is offset lower
            y = -1.2
            if is_open:
                y = -1.9
            group.move_to([x, y, 0])

            bucket_groups.append((group, rect, key, is_open))

        # ----- Connecting lines from CBA box -----
        lines = []
        for group, rect, key, is_open in bucket_groups:
            start = cba_box.get_bottom()
            end = rect.get_top()
            if is_open:
                line = DashedLine(
                    start,
                    end,
                    color=BUCKET_COLORS[key],
                    stroke_width=3,
                    dash_length=0.15,
                )
            else:
                line = Line(
                    start,
                    end,
                    color=TEXT_COLOR,
                    stroke_width=2,
                )
            lines.append(line)

        # ----- Animations -----
        self.play(FadeIn(cba_group, scale=0.9), run_time=RT_FADE)
        self.wait(0.2)

        # Build per-bucket animation sequence
        bucket_anims = []
        for (group, rect, key, is_open), line in zip(bucket_groups, lines):
            bucket_anims.append(
                AnimationGroup(
                    Create(line),
                    FadeIn(group, shift=DOWN * 0.3),
                    lag_ratio=0.3,
                )
            )

        self.play(LaggedStart(*bucket_anims, lag_ratio=0.15), run_time=3.5)
        self.wait(2.0)
        self.wait(0.3)

    def _wrap_text(self, text, max_chars=24):
        """Wrap text into multiple lines on word boundaries."""
        words = text.split()
        lines = []
        current = ""
        for w in words:
            if len(current) + len(w) + 1 <= max_chars:
                current = (current + " " + w).strip()
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        wrapped = "\n".join(lines)
        return safe_text(wrapped, size=SIZE_SMALL, color=DIM_TEXT)


class JokicCap(Scene):
    def construct(self):
        # ----- Title -----
        title = safe_text(
            "Nikola Jokic — open-market vs CBA-capped",
            size=SIZE_HEADER,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)

        # ----- NumberLine axis (numbers added manually as Text to avoid LaTeX) -----
        axis = NumberLine(
            x_range=[0, 110, 25],
            length=10,
            include_numbers=False,
            color=TEXT_COLOR,
        )
        axis.move_to(DOWN * 2.5)
        # Manually add tick labels as Text
        axis_numbers = VGroup()
        for tick_val in [0, 25, 50, 75, 100]:
            num_t = safe_text(str(tick_val), size=SIZE_SMALL, font=FONT_NUMBERS, color=TEXT_COLOR)
            num_t.next_to(axis.number_to_point(tick_val), DOWN, buff=0.15)
            axis_numbers.add(num_t)

        # axis x->screen mapping
        def x_at(val):
            return axis.number_to_point(val)[0]

        x0 = x_at(0)

        # ----- Open market bar (above axis) -----
        open_value = 100.0
        open_width = x_at(open_value) - x0
        bar_height = 0.7

        open_bar = Rectangle(
            width=open_width,
            height=bar_height,
            color=HIGHLIGHT_GREEN,
            fill_opacity=0.9,
            stroke_width=0,
        )
        # We'll grow from LEFT, so anchor left edge at x0
        open_bar.move_to([x0 + open_width / 2, 0.5, 0])

        open_label = safe_text("Open market: $100M", size=SIZE_SMALL, font=FONT_NUMBERS, color=TEXT_COLOR)
        open_label.next_to(open_bar, DOWN, buff=0.15)

        # ----- CBA cap dashed line at $55M -----
        cap_x = x_at(55)
        cap_line = DashedLine(
            start=[cap_x, 1.5, 0],
            end=[cap_x, -2.0, 0],
            color=HIGHLIGHT_AMBER,
            stroke_width=3,
            dash_length=0.15,
        )
        cap_label = safe_text("CBA cap", size=SIZE_SMALL, color=HIGHLIGHT_AMBER, weight=BOLD)
        cap_label.next_to(cap_line, UP, buff=0.1)

        # ----- CBA max bar (below open bar) -----
        cba_value = 55.0
        cba_width = x_at(cba_value) - x0
        cba_bar = Rectangle(
            width=cba_width,
            height=bar_height,
            color=HIGHLIGHT_RED,
            fill_opacity=0.9,
            stroke_width=0,
        )
        cba_bar.move_to([x0 + cba_width / 2, -1.2, 0])

        cba_label_below = safe_text("CBA max: $55M", size=SIZE_SMALL, font=FONT_NUMBERS, color=TEXT_COLOR)
        cba_label_below.next_to(cba_bar, DOWN, buff=0.15)

        # ----- Animations -----
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=RT_FADE)
        self.play(Create(axis), FadeIn(axis_numbers), run_time=1.2)
        self.wait(0.2)

        # Grow open-market bar from LEFT
        self.play(GrowFromEdge(open_bar, LEFT), run_time=RT_BAR_DRAW)
        self.play(FadeIn(open_label), run_time=RT_FADE)
        self.wait(0.4)

        # Drop the CAP dashed line
        self.play(Create(cap_line), FadeIn(cap_label), run_time=0.8)
        self.wait(0.3)

        # Dim the portion of the green bar BEYOND $55M
        beyond_width = x_at(100) - x_at(55)
        beyond_overlay = Rectangle(
            width=beyond_width,
            height=bar_height,
            color=DIM_TEXT,
            fill_opacity=0.7,
            stroke_width=0,
        )
        beyond_overlay.move_to([x_at(55) + beyond_width / 2, 0.5, 0])
        self.play(FadeIn(beyond_overlay), run_time=RT_FADE)
        self.wait(0.3)

        # CBA capped bar grows in below
        self.play(GrowFromEdge(cba_bar, LEFT), run_time=RT_BAR_DRAW)
        self.play(FadeIn(cba_label_below), run_time=RT_FADE)

        self.wait(2.0)
        self.wait(0.3)


class BuildTheFormula(Scene):
    def construct(self):
        # ----- Build the formula pieces -----
        salary_t = safe_text("salary", size=SIZE_HEADER, font=FONT_BODY)
        eq_t     = safe_text("=", size=SIZE_HEADER, font=FONT_BODY)
        base_t   = safe_text("$2.3M", size=SIZE_HEADER, font=FONT_NUMBERS)
        plus_t   = safe_text("+", size=SIZE_HEADER, font=FONT_BODY)
        coef_t   = safe_text("$4.86M", size=SIZE_HEADER, font=FONT_NUMBERS)
        dot_t    = safe_text("·", size=SIZE_HEADER, font=FONT_BODY)
        waz_t    = safe_text("WA_z", size=SIZE_HEADER, font=FONT_NUMBERS)

        pieces = [salary_t, eq_t, base_t, plus_t, coef_t, dot_t, waz_t]
        formula = VGroup(*pieces).arrange(RIGHT, buff=0.25)
        formula.move_to(ORIGIN)

        # ----- Animation: write each piece left-to-right with pauses -----
        for piece in pieces:
            self.play(Write(piece), run_time=0.4)
            self.wait(0.3)

        self.wait(0.4)

        # ----- Fade $2.3M to DIM_TEXT -----
        self.play(base_t.animate.set_color(DIM_TEXT), run_time=RT_FADE)
        self.wait(0.3)

        # ----- Highlight $4.86M with HIGHLIGHT_AMBER + underline -----
        underline = Underline(coef_t, color=HIGHLIGHT_AMBER, stroke_width=3, buff=0.08)
        self.play(
            coef_t.animate.set_color(HIGHLIGHT_AMBER),
            Create(underline),
            run_time=0.6,
        )
        self.wait(0.3)

        # ----- "OPEN-MARKET SHADOW PRICE" callout above formula -----
        callout = safe_text(
            "OPEN-MARKET SHADOW PRICE",
            size=SIZE_SMALL,
            color=HIGHLIGHT_AMBER,
            weight=BOLD,
        )
        callout.next_to(coef_t, UP, buff=1.0)

        connector = Line(
            callout.get_bottom(),
            coef_t.get_top() + UP * 0.05,
            color=HIGHLIGHT_AMBER,
            stroke_width=1.5,
        )

        self.play(FadeIn(callout, shift=DOWN * 0.1), Create(connector), run_time=0.6)
        self.wait(0.3)

        # ----- Footnote below -----
        footnote = safe_text(
            "fit on open-negotiation contracts only (n=127)",
            size=SIZE_TINY,
            color=DIM_TEXT,
        )
        footnote.next_to(formula, DOWN, buff=0.8)
        self.play(FadeIn(footnote), run_time=RT_FADE)

        self.wait(2.0)
        self.wait(0.3)
