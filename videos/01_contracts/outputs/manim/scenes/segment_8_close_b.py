"""Segment 8 — Close. Version B of Scene 22 (ThreeNumbersRevealB).

Stylistic take vs version A:
- Each number debuts FULL-SCREEN at center (hero scale), then minimizes upward
  into a stacked row to make room for the next.
- Slot-machine ValueTracker reveal with a small overshoot before settling.
- Colored ribbon backgrounds behind each number, keyed to bucket colors.
- Final beat: three numbers re-flow horizontally at large scale with a single
  unifying caption: "of 97  ·  % positive  ·  6x range".
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import CLOSE_NUMBERS


# Map each closing number to a bucket color that anchors it visually.
RIBBON_COLORS = [
    BUCKET_COLORS["open_negotiation"],  # 1 of 97 (GM-negotiated bucket)
    BUCKET_COLORS["min"],                # 55% of vet-min
    HIGHLIGHT_AMBER,                     # 6x range
]


class ThreeNumbersRevealB(Scene):
    def construct(self):
        # ---------------- Intro card ----------------
        intro = safe_text("Three numbers to take with you.",
                          size=SIZE_HEADER, weight=BOLD)
        intro.move_to(ORIGIN)
        sub_intro = safe_text("from 97 GM-negotiated contracts",
                              size=SIZE_SMALL, color=DIM_TEXT)
        sub_intro.next_to(intro, DOWN, buff=0.35)
        self.play(FadeIn(intro, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(sub_intro, shift=UP * 0.15), run_time=0.6)
        self.wait(2.6)
        self.play(
            FadeOut(intro, shift=UP * 0.2),
            FadeOut(sub_intro, shift=UP * 0.2),
            run_time=0.5,
        )

        # ---------------- Reveal each number ----------------
        # Final stacked positions (top → bottom) once all three are visible.
        slot_ys = [2.0, 0.4, -1.2]
        small_scale = 0.42  # scale applied to the hero card when it moves up

        cards = []  # list of VGroups (ribbon + number + label) in stacked form

        for i, (target, label_text) in enumerate(CLOSE_NUMBERS):
            color = RIBBON_COLORS[i]

            # Build the hero card at center, full size.
            ribbon = RoundedRectangle(
                corner_radius=0.18,
                width=9.0,
                height=3.4,
                fill_color=color,
                fill_opacity=0.18,
                stroke_color=color,
                stroke_width=2.5,
            )
            ribbon.move_to(ORIGIN)

            tracker = ValueTracker(0.0)
            suffix = "%" if target == 55 else ("x" if target == 6 else "")

            number = always_redraw(
                lambda t=tracker, s=suffix: safe_text(
                    f"{int(round(t.get_value()))}{s}",
                    size=SIZE_HERO_NUMBER,
                    color=TEXT_COLOR,
                    font=FONT_NUMBERS,
                    weight=BOLD,
                ).move_to(ribbon.get_center() + UP * 0.35)
            )

            label = safe_text(label_text, size=SIZE_BODY, color=DIM_TEXT)
            label.next_to(ribbon.get_center() + DOWN * 0.9, ORIGIN, buff=0)

            self.play(
                FadeIn(ribbon, scale=0.96),
                FadeIn(label, shift=UP * 0.2),
                run_time=0.7,
            )
            self.add(number)

            # Slot-machine feel: overshoot, then settle.
            overshoot = target + max(2, int(target * 0.25))
            self.play(
                tracker.animate.set_value(overshoot),
                run_time=1.2,
                rate_func=rush_into,
            )
            self.play(
                tracker.animate.set_value(target * 0.85),
                run_time=0.35,
                rate_func=smooth,
            )
            self.play(
                tracker.animate.set_value(target),
                run_time=0.5,
                rate_func=smooth,
            )
            # Hold long enough for narration to land each number.
            # Per-beat narration is ~6-8s; balance hold between hero size and
            # the post-minimize wait below.
            self.wait(5.8)

            # Freeze the number into a static Text so we can transform/scale it.
            self.remove(number)
            static_number = safe_text(
                f"{int(target)}{suffix}",
                size=SIZE_HERO_NUMBER,
                color=TEXT_COLOR,
                font=FONT_NUMBERS,
                weight=BOLD,
            ).move_to(number.get_center())
            self.add(static_number)

            card = VGroup(ribbon, static_number, label)

            # Build the minimized target (stacked row at top of screen).
            target_card = card.copy()
            target_card.scale(small_scale)
            # Position in the slot; for the first two slots only (third stays large).
            if i < 2:
                target_card.move_to([0, slot_ys[i], 0])
                self.play(
                    Transform(card, target_card),
                    run_time=0.9,
                )
                self.wait(0.4)
                cards.append(card)
            else:
                # Third card: don't shrink yet — hold large briefly, then we'll
                # do a unified re-flow.
                cards.append(card)
                self.wait(0.8)

        # ---------------- Final unified arrangement ----------------
        # Re-flow all three into a single horizontal triplet at the bottom-center,
        # and add a unifying caption above.
        self.wait(0.3)

        # Caption above the triplet.
        caption = safe_text(
            "of 97   ·   % positive   ·   6x range",
            size=SIZE_HEADER,
            color=DIM_TEXT,
            weight=BOLD,
        )
        caption.to_edge(UP, buff=0.9)

        # Build target triplet positions.
        triplet_targets = []
        col_xs = [-4.5, 0.0, 4.5]
        for i, (target, label_text) in enumerate(CLOSE_NUMBERS):
            color = RIBBON_COLORS[i]
            suffix = "%" if target == 55 else ("x" if target == 6 else "")

            ribbon_t = RoundedRectangle(
                corner_radius=0.18,
                width=3.8,
                height=3.2,
                fill_color=color,
                fill_opacity=0.18,
                stroke_color=color,
                stroke_width=2.5,
            )
            num_t = safe_text(
                f"{int(target)}{suffix}",
                size=SIZE_HERO_NUMBER,
                color=TEXT_COLOR,
                font=FONT_NUMBERS,
                weight=BOLD,
            )
            num_t.scale(0.85)
            num_t.move_to(ribbon_t.get_center() + UP * 0.35)

            lbl_t = safe_text(label_text, size=SIZE_SMALL, color=DIM_TEXT)
            # Wrap-ish behavior: keep label inside the card width.
            if lbl_t.width > 3.5:
                lbl_t.scale(3.5 / lbl_t.width)
            lbl_t.next_to(ribbon_t.get_center() + DOWN * 1.05, ORIGIN, buff=0)

            tgt = VGroup(ribbon_t, num_t, lbl_t)
            tgt.move_to([col_xs[i], -0.6, 0])
            triplet_targets.append(tgt)

        anims = [Write(caption)]
        for src, tgt in zip(cards, triplet_targets):
            anims.append(Transform(src, tgt))

        self.play(*anims, run_time=2.0)
        self.wait(6.5)

        # Final flourish: pulse the ribbons together.
        pulses = []
        for c in cards:
            ribbon = c[0]
            pulses.append(Indicate(ribbon, scale_factor=1.05, color=ribbon.get_color()))
        self.play(*pulses, run_time=1.2)
        self.wait(5.0)

        # Gentle fade-out at the end.
        self.play(
            FadeOut(caption, shift=UP * 0.2),
            *[FadeOut(c, shift=DOWN * 0.2) for c in cards],
            run_time=0.7,
        )
        self.wait(0.3)
