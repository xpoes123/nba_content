"""Aging curves to project future Wins Added.

Public NBA aging research (Vaci et al. 2019, Bayesian fits on BR data;
APBRmetrics community curves) converges on a few stylized facts:
  - Peak production lands at ~age 26-27 for most skills
  - Offense peaks earlier; defense/rebounding peak later and decay slower
  - Decline from 28-32 is roughly linear at ~5-8% per year
  - Decline from 33+ accelerates non-linearly
  - Individual variance is enormous; the curve is a population mean, not a forecast

We use a piecewise multiplier on current-year WA. For a player at age `a`, his
projected WA at future age `a+k` is current WA × multiplier(a+k) / multiplier(a).
This keeps the curve shape but pegs every player to his current performance level.
"""

from __future__ import annotations

# Population aging multipliers (relative to peak = 1.00).
# Hand-calibrated to match the Vaci/APBRmetrics consensus shape.
AGING = {
    19: 0.60, 20: 0.72, 21: 0.82, 22: 0.90, 23: 0.95, 24: 0.98,
    25: 1.00, 26: 1.00, 27: 0.99, 28: 0.96, 29: 0.92,
    30: 0.87, 31: 0.81, 32: 0.74, 33: 0.66, 34: 0.57,
    35: 0.48, 36: 0.39, 37: 0.31, 38: 0.24, 39: 0.18, 40: 0.13,
}


def age_multiplier(age: int) -> float:
    if age <= 19:
        return AGING[19]
    if age >= 40:
        return AGING[40]
    return AGING[int(age)]


def project_wa(current_wa: float, current_age: int, years_ahead: int) -> float:
    """Project a player's WA `years_ahead` years from now."""
    future_age = current_age + years_ahead
    return current_wa * age_multiplier(future_age) / age_multiplier(current_age)
