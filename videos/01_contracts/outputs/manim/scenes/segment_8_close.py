import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from manim_config import *
from data_loader import CLOSE_NUMBERS


class ThreeNumbersReveal(Scene):
    def construct(self):
        # ----- Title -----
        title = safe_text("Three numbers to take with you",
                          size=SIZE_HEADER, weight=BOLD)
        title.to_edge(UP, buff=0.7)
        self.play(Write(title), run_time=1.2)
        self.wait(0.3)

        # ----- Three columns -----
        x_positions = [-4.5, 0.0, 4.5]
        colors = [HIGHLIGHT_GREEN, HIGHLIGHT_AMBER, HIGHLIGHT_AMBER]

        trackers = []
        big_numbers = []
        captions = []

        for i, ((target, label), x, color) in enumerate(
                zip(CLOSE_NUMBERS, x_positions, colors)):
            tracker = ValueTracker(0)
            trackers.append(tracker)

            # always_redraw big number, positioned at (x, 0.5)
            def make_big(tr=tracker, c=color, x_=x):
                t = safe_text(f"{int(tr.get_value())}",
                              size=SIZE_HERO_NUMBER, color=c,
                              font=FONT_NUMBERS, weight=BOLD)
                t.move_to(np.array([x_, 0.5, 0]))
                return t

            big = always_redraw(make_big)
            big_numbers.append(big)

            # Caption — wrap if long
            cap_text = label
            # word-wrap for narrow columns
            wrapped = self._wrap(cap_text, max_chars=18)
            cap = safe_text(wrapped, size=SIZE_SMALL, color=DIM_TEXT)
            cap.move_to(np.array([x, -1.4, 0]))
            captions.append(cap)

        # Add big numbers (at zero, since trackers are at 0)
        for big in big_numbers:
            self.add(big)

        # ----- Animate each column in sequence -----
        for i, (tracker, cap) in enumerate(zip(trackers, captions)):
            target = CLOSE_NUMBERS[i][0]
            self.play(tracker.animate.set_value(target), run_time=1.2)
            self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)
            self.wait(0.3)

        # ----- Pulse the second caption -----
        second_cap = captions[1]
        self.play(second_cap.animate.scale(1.05), run_time=0.4)
        self.play(second_cap.animate.scale(1.0 / 1.05), run_time=0.4)

        self.wait(2.5)
        self.wait(0.3)

    @staticmethod
    def _wrap(text: str, max_chars: int = 18) -> str:
        """Simple word-wrap to keep captions narrow."""
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            if not cur:
                cur = w
            elif len(cur) + 1 + len(w) <= max_chars:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return "\n".join(lines)


class FinalQuestion(Scene):
    def construct(self):
        # Q1
        q1 = safe_text("Did the GM negotiate this?",
                       size=SIZE_HEADER, weight=BOLD)
        q1.move_to(ORIGIN + UP * 1.5)
        self.play(Write(q1), run_time=1.2)
        self.wait(0.6)

        # Q2
        q2 = safe_text("Or did the CBA?", size=SIZE_HEADER)
        q2.next_to(q1, DOWN, buff=0.4)
        self.play(Write(q2), run_time=1.2)
        self.wait(1.5)

        # Dim both
        self.play(
            q1.animate.set_opacity(0.4),
            q2.animate.set_opacity(0.4),
            run_time=0.6,
        )

        # Punchline
        final = safe_text("Almost always, it was the CBA.",
                          size=SIZE_HEADER, color=HIGHLIGHT_GREEN,
                          weight=BOLD)
        final.next_to(q2, DOWN, buff=0.9)
        self.play(Write(final), run_time=1.5)

        self.wait(3.0)
        self.wait(0.3)
