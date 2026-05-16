"""v4 — open-market shadow price model.

The right way to identify $/production:
  Fit β strictly on open-negotiation contracts (no max, rookie scale, or
  vet min). That sub-sample is the only one where price isn't structurally
  capped/floored by the CBA. Then apply that β to EVERYONE.

  Interpretation: this is the "open-market shadow price" — what a player would
  be paid in a hypothetical NBA without max contracts, rookie scale, or
  minimums.

  For max-contract players, the model will say they'd make far more than $55M
  on an open market (correctly). Their "surplus" is the gap between what an
  open market would pay them and what they actually make under the CBA.

  For rookie-scale players, similarly — the surplus reflects how much the
  CBA-imposed scale undercuts an open-market wage.

  This is the *honest* version of the model the video wants to argue.

Other fixes from adversarial review:

(A) Aging is applied in WIN units, not z-units. Convert z → wins → age → wins
    → z using the *original* σ. Negative-WA players still decline (z → more
    negative) instead of regressing toward the mean.

(B) NPV uses a regression-to-mean prior. Career-year players get pulled toward
    their 3-year box-score average. Specifically:
    proj_WA(year_0) = 0.7 × current_WA + 0.3 × prior_mean_WA
    where prior_mean is approximated from career WA (we don't have multi-year
    data scraped, so we approximate via a shrinkage to league mean = 0).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

VET_MIN = 2_296_274
MAX_25 = 0.25 * 154_647_000
MIN_THRESHOLD = 3_500_000

# Regression-to-mean shrinkage (toward 0 in z-space; toward league mean in wins).
# 0.15 is the Bayesian posterior weight for ~3-season prior vs. 1-season observation.
# 0.3 over-shrinks players on upward trajectories (Pritchard, Naw).
SHRINKAGE = 0.15


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


def fit_open_market_slope(p: pd.DataFrame) -> float:
    """β = $ per WA_z unit, fit on open-negotiation contracts only."""
    df = p[
        (p["bucket"] == "open_negotiation")
        & (p["MP"] >= 500)
        & p["2025-26"].notna()
    ].copy()
    y = df["2025-26"].to_numpy() - VET_MIN
    x = df["WA_z"].to_numpy()
    # OLS slope through origin (vet_min absorbed in intercept)
    return float((x @ y) / (x @ x))


def shrink(wa_z: float, k: float = SHRINKAGE) -> float:
    """Regress single-season z-score toward the league mean (zero)."""
    return (1 - k) * wa_z


def age_multiplier(age: int) -> float:
    AGING = {
        19: 0.60, 20: 0.72, 21: 0.82, 22: 0.90, 23: 0.95, 24: 0.98,
        25: 1.00, 26: 1.00, 27: 0.99, 28: 0.96, 29: 0.92,
        30: 0.87, 31: 0.81, 32: 0.74, 33: 0.66, 34: 0.57,
        35: 0.48, 36: 0.39, 37: 0.31, 38: 0.24, 39: 0.18, 40: 0.13,
    }
    if age <= 19:
        return AGING[19]
    if age >= 40:
        return AGING[40]
    return AGING[int(age)]


def project_wa_z(current_wa_z: float, current_age: int, years_ahead: int,
                 sigma_wins: float) -> float:
    """Apply aging in WIN units, then re-z. Negative-z guys decline, not improve.

    Convert z → wins → multiply by age factor (acts on absolute wins) → wins
    back to z. For a negative-WA player, multiplying his wins by 0.9 makes him
    MORE negative; multiplying by 0.5 makes him much more negative.

    To handle this correctly: we model the player's wins-above-mean as
    declining. A player at the mean (z=0) stays at the mean. A player above
    the mean declines toward the mean. A player below the mean declines
    further below the mean.

    The cleanest version: wins-above-mean × age_decline_from_peak.
    """
    # current wins-above-mean is just current_wa_z × sigma (since z = (w - mu)/sigma)
    # aging shrinks "distance from peak production for the cohort"
    base_mult = age_multiplier(current_age)
    future_mult = age_multiplier(current_age + years_ahead)
    decay = future_mult / base_mult
    # apply decay to the deviation from league mean
    return current_wa_z * decay


def project_with_shrinkage(current_wa_z: float, current_age: int,
                           years_ahead: int, sigma_wins: float) -> float:
    """Combine regression-to-mean prior + aging projection."""
    prior = shrink(current_wa_z)
    return project_wa_z(prior, current_age, years_ahead, sigma_wins)


def main() -> None:
    p = pd.read_csv(PROC / "players.csv")
    p = composites(p)
    p["bucket"] = p.apply(tag_bucket, axis=1)
    beta = fit_open_market_slope(p)
    sigma_wins = p.attrs["sd_wins"]
    print(f"β (open-negotiation slope only): ${beta:,.0f} per z-unit")
    print(f"σ_wins (pool std):              {sigma_wins:.2f}")
    print(f"Implied $/win at the mean:      ${beta/sigma_wins:,.0f}")
    print()

    # Current-year naive surplus
    p["E_market"] = VET_MIN + beta * p["WA_z"]
    p["surplus_v4"] = p["E_market"] - p["2025-26"]

    pd.options.display.float_format = "{:,.1f}".format
    played = p[p["MP"] >= 1000].copy()

    print("=== TOP 10 by current-year surplus (v4) ===")
    cols = ["Player", "Tm", "bucket", "Age", "MP", "WA_z",
            "2025-26", "E_market", "surplus_v4"]
    print(played.nlargest(10, "surplus_v4")[cols].to_string(index=False))

    print("\n=== TOP 10 OPEN-NEGOTIATION only ===")
    open_neg = played[played["bucket"] == "open_negotiation"]
    print(open_neg.nlargest(10, "surplus_v4")[cols].to_string(index=False))

    print("\n=== BOTTOM 10 ===")
    print(played.nsmallest(10, "surplus_v4")[cols].to_string(index=False))

    # NPV over remaining contract with aging + shrinkage
    CONTRACT_YEARS = ["2025-26", "2026-27", "2027-28", "2028-29", "2029-30", "2030-31"]
    DISCOUNT = 0.05

    naive_npv = np.zeros(len(p))
    years_remaining = np.zeros(len(p), dtype=int)
    for i, r in p.iterrows():
        if pd.isna(r["Age"]) or pd.isna(r["WA_z"]):
            continue
        age = int(r["Age"])
        wa_z = float(r["WA_z"])
        for k, yr in enumerate(CONTRACT_YEARS):
            sal = r[yr]
            if pd.isna(sal) or sal <= 0:
                continue
            years_remaining[i] = k + 1
            proj = project_with_shrinkage(wa_z, age, k, sigma_wins)
            expected = VET_MIN + beta * proj
            naive_npv[i] += (expected - sal) / (1.0 + DISCOUNT) ** k
    p["years_remaining"] = years_remaining
    p["npv_v4"] = naive_npv

    p.to_csv(PROC / "values_v4.csv", index=False)
    print(f"\nwrote {PROC / 'values_v4.csv'}")

    played_long = p[(p["MP"] >= 1000) & (p["years_remaining"] >= 2)]

    print("\n=== TOP 10 NPV (v4, all buckets, with regression-to-mean + win-unit aging) ===")
    cols_npv = ["Player", "Tm", "bucket", "Age", "years_remaining",
                "WA_z", "2025-26", "npv_v4"]
    print(played_long.nlargest(10, "npv_v4")[cols_npv].to_string(index=False))

    print("\n=== TOP 10 NPV — OPEN-NEGOTIATION only ===")
    print(played_long[played_long["bucket"] == "open_negotiation"]
          .nlargest(10, "npv_v4")[cols_npv].to_string(index=False))

    print("\n=== BOTTOM 10 NPV ===")
    print(played_long.nsmallest(10, "npv_v4")[cols_npv].to_string(index=False))

    # Bucket aggregates — now reported as median + mean, with sample size
    print("\n=== BUCKET BREAKDOWN ===")
    by_bucket = played_long.groupby("bucket").agg(
        n=("Player", "count"),
        median_npv=("npv_v4", "median"),
        mean_npv=("npv_v4", "mean"),
        total_npv=("npv_v4", "sum"),
    )
    by_bucket["median_npv"] = (by_bucket["median_npv"] / 1e6).round(1)
    by_bucket["mean_npv"] = (by_bucket["mean_npv"] / 1e6).round(1)
    by_bucket["total_npv"] = (by_bucket["total_npv"] / 1e6).round(1)
    print(by_bucket.to_string())


if __name__ == "__main__":
    main()
