import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from manim import *
from manim_config import *
from data_loader import COLD_OPEN_NAMES


class ColdOpenNames(Scene):
    def construct(self):
        np.random.seed(42)

        animations = []
        for i, name in enumerate(COLD_OPEN_NAMES):
            x = np.random.uniform(-6, 6)
            y = np.random.uniform(-3, 3)
            color = TEXT_COLOR if i % 2 == 0 else DIM_TEXT
            t = safe_text(name, size=48, color=color, weight=BOLD)
            t.move_to(np.array([x, y, 0.0]))
            animations.append(
                Succession(
                    FadeIn(t, run_time=0.2),
                    Wait(0.3),
                    FadeOut(t, run_time=0.2),
                )
            )

        self.play(LaggedStart(*animations, lag_ratio=0.08))
        self.wait(0.4)
        self.wait(0.3)


class ColdOpenStat(Scene):
    def construct(self):
        line1 = safe_text(
            "97 contracts GMs negotiated",
            size=SIZE_HEADER,
            color=DIM_TEXT,
        )
        line1.move_to(UP * 0.8)

        big_one = safe_text("1", size=SIZE_HERO_NUMBER, color=HIGHLIGHT_GREEN, weight=BOLD)
        rest = safe_text(" will deliver positive value.", size=SIZE_HEADER, color=TEXT_COLOR)
        line2 = VGroup(big_one, rest).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        line2.next_to(line1, DOWN, buff=0.8)

        # 1) Write line1
        self.play(Write(line1), run_time=1.5)
        # 2) wait
        self.wait(0.5)
        # 3) FadeIn line2 small-to-large
        line2.save_state()
        line2.scale(0.4)
        self.play(
            line2.animate.restore(),
            FadeIn(line2),
            run_time=0.6,
        )
        # Pulse the "1" twice: scale up then back, twice (4 plays total)
        self.play(big_one.animate.scale(1.15), run_time=0.4)
        self.play(big_one.animate.scale(1.0 / 1.15), run_time=0.4)
        self.play(big_one.animate.scale(1.15), run_time=0.4)
        self.play(big_one.animate.scale(1.0 / 1.15), run_time=0.4)
        # 4) hold
        self.wait(1.5)
        # 5) fade out
        self.play(FadeOut(line1), FadeOut(line2), run_time=0.4)

        self.wait(0.3)
