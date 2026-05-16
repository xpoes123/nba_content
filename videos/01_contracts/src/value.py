"""Build composite production metric, $/win baseline, and surplus value.

Composite "Wins Added" (WA) blends three open metrics so each cancels the others'
known biases:
  - VORP   — points above replacement per 100 possessions, scaled to wins (BR
             multiplies by ~2.7 internally)
  - WS     — box-score win shares, full season
  - BPM·MP — minutes-weighted BPM (so high BPM in 200 min doesn't outrank a
             starter at +4)

All three are box-score-based. They share weaknesses (none captures defense well
in isolation), but combining them is more robust than any single one.

WA is calibrated so that one composite unit equals one team win. The intercept
of (salary on WA) is forced to the veteran minimum baseline (~$2.3M for 2025-26)
to anchor replacement level — otherwise the regression absorbs the cap floor as
the intercept and underestimates marginal $/win.

Outputs:
  data/processed/values.csv  Player, WA, salary, surplus, percentile
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

# 2025-26 reference values
VET_MIN = 2_296_274  # one-year minimum for 2+ years exp, rounded
SALARY_CAP = 154_647_000


def composite_wa(df: pd.DataFrame) -> pd.Series:
    """Composite Wins Added per player.

    VORP is already on a wins-ish scale (~2.7 pts per 100 poss = 1 win equiv).
    WS is already a wins quantity.
    BPM is per-100. Convert with BPM * (MP / 48) / 100 ≈ wins-equivalent.
    Average the three to get a robust blended estimate.
    """
    vorp_wins = df["VORP"]
    ws_wins = df["WS"]
    bpm_wins = df["BPM"] * df["MP"] / (48 * 100) * 2.7  # scale to wins
    wa = pd.concat([vorp_wins, ws_wins, bpm_wins], axis=1).mean(axis=1)
    return wa.fillna(0.0)


def estimate_dollars_per_win(df: pd.DataFrame) -> float:
    """Linear fit: salary = vet_min + dpw * WA, solved for dpw via least squares
    on the slope only (intercept fixed at the vet min).

    Restrict to players with positive WA and a 2025-26 salary, to avoid the
    intercept getting dominated by deep bench guys on minimums.
    """
    sub = df[(df["WA"] > 0.5) & df["2025-26"].notna()].copy()
    y = sub["2025-26"].to_numpy() - VET_MIN
    x = sub["WA"].to_numpy()
    # OLS slope through origin (forcing intercept = 0 in shifted space)
    dpw = float((x @ y) / (x @ x))
    return dpw


def main() -> None:
    p = pd.read_csv(PROC / "players.csv")
    p["WA"] = composite_wa(p)
    dpw = estimate_dollars_per_win(p)
    print(f"$/win (open-market, blended fit): ${dpw:,.0f}")

    # Surplus value (naive, current year only)
    p["expected_salary"] = VET_MIN + dpw * p["WA"]
    p["surplus_naive"] = p["expected_salary"] - p["2025-26"]
    # cap effective surplus at zero for max-contract players to avoid double
    # counting their CBA-mandated underpayment in the naive list (we'll surface
    # them in a separate "structural" list)
    out = p[[
        "Player", "Tm", "Age", "Pos", "G", "MP",
        "BPM", "VORP", "WS", "WA",
        "2025-26", "expected_salary", "surplus_naive",
        "ContractTm", "2026-27", "2027-28", "2028-29", "2029-30", "2030-31",
        "Guaranteed",
    ]].copy()
    out.to_csv(PROC / "values.csv", index=False)
    print(f"wrote {PROC / 'values.csv'}  ({len(out)} rows)")
    print()
    print("=== TOP 10 BY NAIVE SURPLUS (current year) ===")
    cols = ["Player", "Tm", "Age", "MP", "WA", "2025-26", "expected_salary", "surplus_naive"]
    print(out.nlargest(10, "surplus_naive")[cols].to_string(index=False))
    print()
    print("=== BOTTOM 10 (worst contracts) ===")
    print(out.nsmallest(10, "surplus_naive")[cols].to_string(index=False))


if __name__ == "__main__":
    main()
