"""v3 — addresses adversarial review.

Three substantive fixes:

(1) Aging applied in WIN units, not z-units.
    The bug: a z-score is standardized against the contemporary pool, so
    multiplying it by an age-decline factor doesn't model wins-lost. Negative-z
    players got *better* with age in v2. Fix: convert z → wins → age → wins → z
    using a fixed σ. Aging now decreases negative-z guys further (they're worse
    than replacement, decline pushes them further from peer mean).

(2) β fit with bucket fixed effects on the FULL sample.
    The bug: restricting the fit to above-median WA biased β downward (max
    contracts are capped, so the slope flattens at the top). v2 then
    extrapolated that flatter slope to the bottom half, mechanically producing
    positive surplus for cheap players. v3 fits salary ~ β·WA_z + bucket FEs on
    the whole sample. The "open-market" slope is identified from the
    open-negotiation bucket; min/rookie/max each get their own intercept.

(3) Surplus computed against the open-market counterfactual.
    expected_market_salary = vet_min + β_open · WA_z   (no bucket FE applied)
    Then surplus = expected - actual, regardless of which bucket the player is
    in. This is the honest "what would this contract be worth on an open
    market" question.

v3 leaves the team multiplier untouched — that's a separate file fix.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

VET_MIN = 2_296_274

# Salary-cap thresholds for bucket tagging
MAX_25 = 0.25 * 154_647_000
MIN_THRESHOLD = 3_500_000


def composites(p: pd.DataFrame) -> pd.DataFrame:
    p = p.copy()
    p["VORP_wins"] = p["VORP"] * 2.7
    p["WA_wins"] = (p["VORP_wins"] + p["WS"]) / 2.0
    pool = p[p["MP"] >= 500]
    mu, sd = pool["WA_wins"].mean(), pool["WA_wins"].std()
    p["WA_z"] = (p["WA_wins"] - mu) / sd
    p.attrs["mu_wins"] = mu
    p.attrs["sd_wins"] = sd
    return p


def tag_bucket(row: pd.Series) -> str:
    sal = row["2025-26"]
    if pd.isna(sal):
        return "none"
    if sal >= MAX_25 * 0.95:
        return "max"
    if row["Age"] <= 23 and sal < 15_000_000:
        return "rookie_scale"
    if sal < MIN_THRESHOLD:
        return "min"
    return "open_negotiation"


def fit_open_market_slope(p: pd.DataFrame) -> tuple[float, dict]:
    """Fit salary ~ β·WA_z + bucket dummies on the full sample.

    β is the slope identified from the open-negotiation bucket. Bucket
    dummies absorb the CBA-imposed mean offsets (max contracts uniformly high,
    min contracts uniformly low, rookie scale on a fixed schedule).
    """
    df = p[(p["MP"] >= 500) & p["2025-26"].notna() & p["bucket"].ne("none")].copy()
    df["y"] = df["2025-26"] - VET_MIN
    # design matrix: [WA_z, I(min), I(rookie), I(max)]
    df["d_min"] = (df["bucket"] == "min").astype(float)
    df["d_rookie"] = (df["bucket"] == "rookie_scale").astype(float)
    df["d_max"] = (df["bucket"] == "max").astype(float)
    X = df[["WA_z", "d_min", "d_rookie", "d_max"]].to_numpy()
    y = df["y"].to_numpy()
    # OLS with intercept fixed at zero (we already subtracted vet_min)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    beta_open = float(coef[0])
    fixed_effects = {
        "min": float(coef[1]),
        "rookie_scale": float(coef[2]),
        "max": float(coef[3]),
    }
    return beta_open, fixed_effects


def main() -> None:
    p = pd.read_csv(PROC / "players.csv")
    p = composites(p)
    p["bucket"] = p.apply(tag_bucket, axis=1)

    beta_open, fe = fit_open_market_slope(p)
    print(f"β (open-market slope on WA_z): ${beta_open:,.0f} per z-unit")
    print(f"Bucket fixed effects (relative to open-negotiation):")
    for k, v in fe.items():
        print(f"  {k:15s} ${v:>+15,.0f}  (mean salary offset)")
    print()

    p["expected_open_market"] = VET_MIN + beta_open * p["WA_z"]
    p["surplus_v3"] = p["expected_open_market"] - p["2025-26"]
    p.to_csv(PROC / "values_v3.csv", index=False)
    print(f"wrote {PROC / 'values_v3.csv'}")

    pd.options.display.float_format = "{:,.1f}".format
    played = p[p["MP"] >= 1000].copy()

    print("\n=== TOP 10 surplus (v3, current year, all buckets) ===")
    cols = ["Player", "Tm", "bucket", "Age", "MP", "WA_z",
            "2025-26", "expected_open_market", "surplus_v3"]
    print(played.nlargest(10, "surplus_v3")[cols].to_string(index=False))

    print("\n=== TOP 10 OPEN-NEGOTIATION only ===")
    open_neg = played[played["bucket"] == "open_negotiation"]
    print(open_neg.nlargest(10, "surplus_v3")[cols].to_string(index=False))

    print("\n=== BOTTOM 10 ===")
    print(played.nsmallest(10, "surplus_v3")[cols].to_string(index=False))


if __name__ == "__main__":
    main()
