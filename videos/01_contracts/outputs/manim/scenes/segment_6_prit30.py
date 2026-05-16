"""Segment 6 — Pritchard's contract across all 30 teams. Scenes 16, 17."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import PRITCHARD_30_TEAMS


# ---- Shared layout parameters ----
ROW_HEIGHT = 0.18
ROW_BUFF = 0.04
MAX_BAR_LEN = 8.0
MAX_VAL = 13.3
BAR_LEFT_X = -2.5  # x at which all bars start (left edge of bar)


def _build_prit30(scene_width_ok=True):
    """Build the 30-row layout. Returns dict of mobjects:
        title, subtitle, rows (list of dicts), all_group
    Rows ordered top→bottom = PRITCHARD_30_TEAMS (GSW first / top, BRK last / bottom).
    """
    title = safe_text("Same contract, 30 teams: effective NPV",
                      size=SIZE_HEADER, weight=BOLD)
    title.to_edge(UP, buff=0.35)

    subtitle = safe_text("Sorted descending by effective value",
                         size=SIZE_SMALL, color=DIM_TEXT)
    subtitle.next_to(title, DOWN, buff=0.15)

    n = len(PRITCHARD_30_TEAMS)
    # Vertical space below subtitle
    top_y = subtitle.get_bottom()[1] - 0.25
    bottom_y = -3.95
    avail = top_y - bottom_y
    step = avail / n  # ~ row pitch
    # Force pitch close to ROW_HEIGHT + ROW_BUFF if possible
    pitch = min(step, ROW_HEIGHT + ROW_BUFF)
    # Actually let's just lay them out using the available space evenly
    pitch = step

    rows = []
    for i, (team, tier, _orig_npv, eff_npv) in enumerate(PRITCHARD_30_TEAMS):
        y = top_y - (i + 0.5) * pitch
        width = max(eff_npv / MAX_VAL * MAX_BAR_LEN, 0.05)
        bar = Rectangle(width=width, height=ROW_HEIGHT,
                        color=TIER_COLORS[tier], fill_opacity=0.95,
                        stroke_width=0)
        # Place so left edge is at BAR_LEFT_X
        bar.move_to([BAR_LEFT_X + width / 2, y, 0])

        lbl = safe_text(team, size=SIZE_TINY, color=TEXT_COLOR,
                        font=FONT_BODY)
        lbl.move_to([BAR_LEFT_X - 0.55, y, 0])

        val = safe_text(f"${eff_npv:.1f}M", size=SIZE_TINY,
                        color=TEXT_COLOR, font=FONT_NUMBERS)
        val.next_to(bar, RIGHT, buff=0.12)

        rows.append({
            "team": team,
            "tier": tier,
            "eff": eff_npv,
            "bar": bar,
            "label": lbl,
            "value": val,
            "y": y,
        })

    all_group = VGroup(title, subtitle,
                       *[r["label"] for r in rows],
                       *[r["bar"] for r in rows],
                       *[r["value"] for r in rows])

    return {"title": title, "subtitle": subtitle,
            "rows": rows, "all_group": all_group}


class Pritchard30Teams(Scene):
    """30 horizontal bars: Pritchard's effective NPV across all 30 teams."""

    def construct(self):
        built = _build_prit30()
        title = built["title"]
        subtitle = built["subtitle"]
        rows = built["rows"]

        # Header
        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.4)

        # Bars draw bottom-up: BRK first, GSW last.
        # rows is top→bottom (GSW idx 0, BRK idx 29). Reverse to animate bottom-up.
        anims = []
        for r in reversed(rows):
            grp = VGroup(r["label"], r["bar"], r["value"])
            # GrowFromEdge on the whole group makes the label/value fly in too;
            # use a small combo: FadeIn label/value + GrowFromEdge bar.
            anims.append(AnimationGroup(
                FadeIn(r["label"], shift=RIGHT * 0.05),
                GrowFromEdge(r["bar"], LEFT),
                FadeIn(r["value"], shift=LEFT * 0.05),
                lag_ratio=0.0,
            ))

        self.play(LaggedStart(*anims, lag_ratio=0.04), run_time=4.0)

        # Callouts: BRK (last row, bottom) and GSW (first row, top)
        gsw = rows[0]
        brk = rows[-1]

        gsw_callout = safe_text("$13.3M", size=SIZE_SMALL,
                                color=TIER_COLORS["second_apron"],
                                font=FONT_NUMBERS, weight=BOLD)
        gsw_callout.move_to(gsw["bar"].get_right() + RIGHT * 1.7)

        gsw_arrow = Arrow(
            start=gsw_callout.get_left() + LEFT * 0.05,
            end=gsw["value"].get_right() + RIGHT * 0.1,
            color=TIER_COLORS["second_apron"],
            buff=0.05, stroke_width=3, max_tip_length_to_length_ratio=0.25,
        )

        brk_callout = safe_text("$2.2M", size=SIZE_SMALL,
                                color=TIER_COLORS["below_cap"],
                                font=FONT_NUMBERS, weight=BOLD)
        brk_callout.move_to(brk["value"].get_right() + RIGHT * 1.2)

        brk_arrow = Arrow(
            start=brk_callout.get_left() + LEFT * 0.05,
            end=brk["value"].get_right() + RIGHT * 0.1,
            color=TIER_COLORS["below_cap"],
            buff=0.05, stroke_width=3, max_tip_length_to_length_ratio=0.3,
        )

        self.play(
            GrowArrow(gsw_arrow), FadeIn(gsw_callout, shift=LEFT * 0.1),
            run_time=0.6,
        )
        self.play(
            GrowArrow(brk_arrow), FadeIn(brk_callout, shift=LEFT * 0.1),
            run_time=0.6,
        )

        self.wait(2.0)
        self.wait(0.3)


class SevenTimesCallout(Scene):
    """Pull GSW and BRK out, show '7x' callout."""

    def construct(self):
        built = _build_prit30()
        rows = built["rows"]
        bg_group = built["all_group"]

        # Add background already dimmed
        bg_group.set_opacity(0.3)
        self.add(bg_group)

        # Make copies of GSW and BRK rows (label+bar+value)
        gsw = rows[0]
        brk = rows[-1]

        def make_copy(r, target_x, color_key):
            label_c = r["label"].copy().set_opacity(1.0)
            bar_c = r["bar"].copy().set_opacity(1.0)
            val_c = r["value"].copy().set_opacity(1.0)
            grp = VGroup(label_c, bar_c, val_c)
            grp.scale(1.4)
            grp.move_to([target_x, -1.6, 0])
            return grp, label_c, bar_c, val_c

        gsw_grp, gsw_lbl, gsw_bar, gsw_val = make_copy(gsw, -3.5, "second_apron")
        brk_grp, brk_lbl, brk_bar, brk_val = make_copy(brk, 3.5, "below_cap")

        # Big labels above each copy
        gsw_big = safe_text("CLE",
                            size=SIZE_HEADER,
                            color=TIER_COLORS["second_apron"],
                            weight=BOLD)
        gsw_big_val = safe_text("$13.3M",
                                size=SIZE_BODY,
                                color=TIER_COLORS["second_apron"],
                                font=FONT_NUMBERS, weight=BOLD)
        gsw_header = VGroup(gsw_big, gsw_big_val).arrange(DOWN, buff=0.12)
        gsw_header.next_to(gsw_grp, UP, buff=0.4)

        brk_big = safe_text("BRK",
                            size=SIZE_HEADER,
                            color=TIER_COLORS["below_cap"],
                            weight=BOLD)
        brk_big_val = safe_text("$2.2M",
                                size=SIZE_BODY,
                                color=TIER_COLORS["below_cap"],
                                font=FONT_NUMBERS, weight=BOLD)
        brk_header = VGroup(brk_big, brk_big_val).arrange(DOWN, buff=0.12)
        brk_header.next_to(brk_grp, UP, buff=0.4)

        # Pull copies out
        self.play(
            FadeIn(gsw_grp, scale=1.1),
            FadeIn(brk_grp, scale=1.1),
            run_time=0.9,
        )
        self.play(
            FadeIn(gsw_header, shift=DOWN * 0.15),
            FadeIn(brk_header, shift=DOWN * 0.15),
            run_time=0.7,
        )

        # Big "6x" in the center
        seven = safe_text("6x", size=SIZE_HERO_NUMBER,
                          color=HIGHLIGHT_AMBER, weight=BOLD)
        seven.move_to([0, 1.2, 0])
        seven.scale(0.3)

        self.play(
            seven.animate.scale(1.0 / 0.3),
            run_time=0.9,
        )

        # Tagline
        tagline = safe_text("Same contract. Same player. 6x the value.",
                            size=SIZE_HEADER, color=TEXT_COLOR, weight=BOLD)
        tagline.move_to([0, -0.4, 0])

        self.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.7)

        self.wait(2.5)
        self.wait(0.3)
