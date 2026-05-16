"""Segment 5 — the worst contracts. Scenes 13, 14, 15."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import BOTTOM_5_EFFECTIVE


# Layout constants shared by Scenes 13 + 14
MAX_ABS = 650.0       # rounded ceiling above |Mobley's NPV|
BAR_LENGTH = 7.0      # max bar width in scene units
BAR_HEIGHT = 0.45
ROW_SPACING = 0.9
ZERO_X = 4.2          # x-coordinate of the "0" axis line


def _build_bottom_five_layout():
    """Build (zero_line, zero_label, rows[]) where each row is a dict.

    Each row dict has:
        name_text, tracker (ValueTracker), bar (always_redraw), value_label (always_redraw),
        target_value (float, negative), color
    """
    # Vertical zero axis on the RIGHT side (since bars go LEFT)
    zero_line = Line(
        start=[ZERO_X, 2.2, 0],
        end=[ZERO_X, -2.6, 0],
        color=DIM_TEXT,
        stroke_width=2,
    )
    zero_label = safe_text("0", size=SIZE_SMALL, color=DIM_TEXT)
    zero_label.next_to(zero_line.get_top(), UP, buff=0.15)

    rows = []
    top_y = 1.7
    for i, (player, team, tier, value) in enumerate(BOTTOM_5_EFFECTIVE):
        y = top_y - i * ROW_SPACING
        color = TIER_COLORS[tier]
        tracker = ValueTracker(0.0)

        # Name on the RIGHT side of zero (since bars go LEFT)
        name = safe_text(player, size=SIZE_SMALL, color=TEXT_COLOR)
        name.move_to([ZERO_X + 0.2, y, 0]).align_to([ZERO_X + 0.2, y, 0], LEFT)
        name.shift(RIGHT * 0.0)
        # Ensure name's left edge is at ZERO_X + 0.2
        name.next_to([ZERO_X, y, 0], RIGHT, buff=0.2)

        def make_bar(tracker=tracker, y=y, color=color):
            v = tracker.get_value()
            width = max(abs(v) / MAX_ABS * BAR_LENGTH, 0.0001)
            bar = Rectangle(
                width=width,
                height=BAR_HEIGHT,
                color=color,
                fill_opacity=0.9,
                stroke_width=0,
            )
            # Right edge anchored at ZERO_X; bar extends LEFT
            bar.move_to([ZERO_X - width / 2, y, 0])
            return bar

        def make_value_label(tracker=tracker, y=y):
            v = tracker.get_value()
            width = max(abs(v) / MAX_ABS * BAR_LENGTH, 0.0001)
            label = safe_text(
                f"−${abs(v):.0f}M",
                size=SIZE_SMALL,
                color=TEXT_COLOR,
                font=FONT_NUMBERS,
            )
            label.move_to([ZERO_X - width - 0.5, y, 0])
            return label

        bar = always_redraw(make_bar)
        value_label = always_redraw(make_value_label)

        rows.append({
            "name": name,
            "tracker": tracker,
            "bar": bar,
            "value_label": value_label,
            "target_value": value,
            "color": color,
            "y": y,
        })

    return zero_line, zero_label, rows


class BottomFiveBars(Scene):
    """Horizontal bars descending leftward into the negative."""

    def construct(self):
        title = safe_text(
            "Bottom 5 contracts — effective NPV",
            size=SIZE_HEADER,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.0)

        zero_line, zero_label, rows = _build_bottom_five_layout()

        self.play(Create(zero_line), FadeIn(zero_label), run_time=0.8)

        # Names appear first (faded), then each bar grows
        self.play(
            *[FadeIn(r["name"]) for r in rows],
            run_time=0.6,
        )

        # Add bars + value labels to scene (they start at width ~0)
        for r in rows:
            self.add(r["bar"], r["value_label"])

        # Animate each bar in sequence: 1.2s per bar
        for r in rows:
            self.play(
                r["tracker"].animate.set_value(r["target_value"]),
                run_time=1.2,
            )

        self.wait(2.0)
        self.wait(0.3)


class MobleyAnnotation(Scene):
    """Focus on Mobley with three callout boxes."""

    def construct(self):
        title = safe_text(
            "Bottom 5 contracts — effective NPV",
            size=SIZE_HEADER,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.4)
        self.add(title)

        # Build STATIC layout (no always_redraw — too expensive over long scene)
        zero_line = Line(
            start=[ZERO_X, 2.2, 0],
            end=[ZERO_X, -2.6, 0],
            color=DIM_TEXT,
            stroke_width=2,
        )
        zero_label = safe_text("0", size=SIZE_SMALL, color=DIM_TEXT)
        zero_label.next_to(zero_line.get_top(), UP, buff=0.15)
        self.add(zero_line, zero_label)

        rows = []
        top_y = 1.7
        for i, (player, team, tier, value) in enumerate(BOTTOM_5_EFFECTIVE):
            y = top_y - i * ROW_SPACING
            color = TIER_COLORS[tier]
            width = max(abs(value) / MAX_ABS * BAR_LENGTH, 0.0001)
            name = safe_text(player, size=SIZE_SMALL, color=TEXT_COLOR)
            name.next_to([ZERO_X, y, 0], RIGHT, buff=0.2)
            bar = Rectangle(width=width, height=BAR_HEIGHT, color=color,
                            fill_opacity=0.9, stroke_width=0)
            bar.move_to([ZERO_X - width / 2, y, 0])
            value_label = safe_text(f"-${abs(value):.0f}M", size=SIZE_SMALL,
                                    color=TEXT_COLOR, font=FONT_NUMBERS)
            value_label.move_to([ZERO_X - width - 0.5, y, 0])
            self.add(name, bar, value_label)
            rows.append({
                "name": name, "bar": bar, "value_label": value_label,
                "target_value": value, "color": color, "y": y,
            })

        self.wait(0.5)

        # Mobley is top (index 0)
        mobley = rows[0]
        others = rows[1:]

        # Fade the other 4 bars + their text
        fade_targets = []
        for r in others:
            fade_targets.extend([r["name"], r["bar"], r["value_label"]])
        self.play(
            *[m.animate.set_opacity(0.35) for m in fade_targets],
            run_time=0.8,
        )

        # Pulse Mobley bar
        # Since bar is always_redraw, we pulse the tracker - actually simpler:
        # scale the static visual via direct play on a snapshot. Use a quick
        # value bump trick: scale name + emphasize via flash.
        # Better: temporarily replace bar with static copy for pulse, but the
        # cleanest is to flash a stroke around the Mobley bar.
        mobley_bar_snapshot = Rectangle(
            width=abs(mobley["target_value"]) / MAX_ABS * BAR_LENGTH,
            height=BAR_HEIGHT,
            color=mobley["color"],
            fill_opacity=0.0,
            stroke_color=HIGHLIGHT_AMBER,
            stroke_width=4,
        )
        width = abs(mobley["target_value"]) / MAX_ABS * BAR_LENGTH
        mobley_bar_snapshot.move_to([ZERO_X - width / 2, mobley["y"], 0])
        self.play(
            mobley_bar_snapshot.animate.scale(1.05),
            run_time=0.3,
        )
        self.play(
            mobley_bar_snapshot.animate.scale(1.0 / 1.05),
            run_time=0.3,
        )

        # ----- Three callouts -----
        bar_width = abs(mobley["target_value"]) / MAX_ABS * BAR_LENGTH
        bar_left_x = ZERO_X - bar_width
        bar_center = [ZERO_X - bar_width / 2, mobley["y"], 0]

        # Anchor points on the Mobley bar (different along its width)
        anchor_ul = [bar_left_x + bar_width * 0.25, mobley["y"] + BAR_HEIGHT / 2, 0]
        anchor_ur = [bar_left_x + bar_width * 0.7, mobley["y"] + BAR_HEIGHT / 2, 0]
        anchor_br = [bar_left_x + bar_width * 0.55, mobley["y"] - BAR_HEIGHT / 2, 0]

        def make_callout(text, anchor, target_pos, color):
            t = safe_text(text, size=SIZE_SMALL, color=TEXT_COLOR, weight=BOLD)
            box = Rectangle(
                width=t.width + 0.4,
                height=t.height + 0.3,
                color=color,
                fill_opacity=0.2,
                stroke_color=color,
                stroke_width=2,
            )
            box.move_to(target_pos)
            t.move_to(box.get_center())
            # Connector line from anchor to nearest edge of box
            connector = Line(
                anchor,
                box.get_center(),
                color=color,
                stroke_width=1.5,
            )
            # Trim connector at box boundary by going to closest edge
            # Simpler: line from anchor to box (manim will overlap a bit, ok)
            return VGroup(connector, box, t)

        callout_ul = make_callout(
            "5-year max",
            anchor_ul,
            [bar_left_x + bar_width * 0.25, mobley["y"] + 1.4, 0],
            HIGHLIGHT_AMBER,
        )
        callout_ur = make_callout(
            "Cleveland: 2nd apron",
            anchor_ur,
            [bar_left_x + bar_width * 0.7 + 0.3, mobley["y"] + 2.5, 0],
            HIGHLIGHT_RED,
        )
        callout_br = make_callout(
            "Top-30 production, not top-5",
            anchor_br,
            [bar_left_x + bar_width * 0.55 + 1.5, mobley["y"] - 1.3, 0],
            HIGHLIGHT_AMBER,
        )

        # Make sure callouts stay on screen
        for c in (callout_ul, callout_ur, callout_br):
            # If left edge goes off-screen, nudge right
            if c.get_left()[0] < -7.0:
                c.shift(RIGHT * (-7.0 - c.get_left()[0]))
            if c.get_right()[0] > 7.0:
                c.shift(LEFT * (c.get_right()[0] - 7.0))

        self.play(FadeIn(callout_ul, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(callout_ur, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(callout_br, shift=DOWN * 0.1), run_time=0.6)

        self.wait(2.0)
        self.wait(0.3)


class MaxOnApronPattern(Scene):
    """Pattern: every bottom-5 contract is a max on an apron team."""

    def construct(self):
        # Two-line header
        header1 = safe_text("Every bottom-5 contract:", size=SIZE_HEADER)
        header2 = safe_text(
            "max deal on apron team.",
            size=SIZE_HEADER,
            color=HIGHLIGHT_AMBER,
            weight=BOLD,
        )
        header = VGroup(header1, header2).arrange(DOWN, buff=0.2)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header1), run_time=0.8)
        self.play(Write(header2), run_time=0.8)

        # Rows: player name + team | tier badge
        TIER_LABELS = {
            "second_apron":        "2nd apron",
            "first_apron":         "1st apron",
            "taxpayer":            "taxpayer",
            "above_cap_below_tax": "above cap",
            "below_cap":           "below cap",
        }

        rows = []
        for player, team, tier, _value in BOTTOM_5_EFFECTIVE:
            # Drop trailing asterisk on Curry for display cleanliness
            display_name = player.rstrip("*")
            left = safe_text(
                f"{display_name.split()[-1]} · {team}",
                size=SIZE_BODY,
                color=TEXT_COLOR,
            )

            tier_color = TIER_COLORS[tier]
            badge_text = safe_text(
                TIER_LABELS[tier],
                size=SIZE_SMALL,
                color="#FFFFFF",
                weight=BOLD,
            )
            badge_bg = Rectangle(
                width=badge_text.width + 0.5,
                height=badge_text.height + 0.25,
                color=tier_color,
                fill_opacity=0.95,
                stroke_width=0,
            )
            badge_text.move_to(badge_bg.get_center())
            badge = VGroup(badge_bg, badge_text)

            # Row: left text on LEFT, badge on RIGHT, with fixed total width
            row = VGroup(left, badge)
            # Place them: left text anchored at x=-3, badge anchored at x=+2
            left.move_to([-2.5, 0, 0])
            badge.move_to([2.5, 0, 0])
            rows.append(row)

        # Stack rows vertically
        grid = VGroup(*rows).arrange(DOWN, buff=0.35)
        grid.next_to(header, DOWN, buff=0.7)

        # LaggedStart fade-in
        self.play(
            LaggedStart(
                *[FadeIn(r, shift=RIGHT * 0.2) for r in rows],
                lag_ratio=0.15,
            ),
            run_time=2.5,
        )

        self.wait(2.0)
        self.wait(0.3)
