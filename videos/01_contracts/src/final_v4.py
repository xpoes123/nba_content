"""Final pipeline using v4 model + corrected team multipliers.

Run after value_v4.py. Produces the headline tables under the adversarial-
review-corrected model:
  - open-market β fit on open-negotiation contracts only
  - aging applied in win units (not z-units)
  - 15% Bayesian shrinkage toward league mean
  - additive (not multiplicative) tax + apron multipliers, with reduced
    apron premiums
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from team_context import effective_multiplier
from value_v4 import composites, tag_bucket, fit_open_market_slope, project_with_shrinkage

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

VET_MIN = 2_296_274
DISCOUNT = 0.05
CONTRACT_YEARS = ["2025-26", "2026-27", "2027-28", "2028-29", "2029-30", "2030-31"]


def main() -> None:
    p = pd.read_csv(PROC / "players.csv")
    p = composites(p)
    p["bucket"] = p.apply(tag_bucket, axis=1)
    beta = fit_open_market_slope(p)
    sigma_wins = p.attrs["sd_wins"]

    print(f"β (open-negotiation slope): ${beta:,.0f} per z-unit")
    print(f"$/win at the mean:          ${beta/sigma_wins:,.0f}")
    print()

    # NPV calculation
    rows = []
    for _, r in p.iterrows():
        if pd.isna(r["Age"]) or pd.isna(r["WA_z"]) or pd.isna(r["2025-26"]):
            continue
        age = int(r["Age"])
        wa_z = float(r["WA_z"])
        npv = 0.0
        years_remaining = 0
        for k, yr in enumerate(CONTRACT_YEARS):
            sal = r[yr]
            if pd.isna(sal) or sal <= 0:
                continue
            years_remaining = k + 1
            proj = project_with_shrinkage(wa_z, age, k, sigma_wins)
            expected = VET_MIN + beta * proj
            npv += (expected - sal) / (1.0 + DISCOUNT) ** k
        rows.append({
            "Player": r["Player"], "Tm": r["Tm"], "Age": age,
            "MP": r["MP"], "WA_z": wa_z, "bucket": r["bucket"],
            "salary_25": r["2025-26"], "years": years_remaining,
            "npv": npv,
        })
    df = pd.DataFrame(rows)

    # team multipliers
    tiers = pd.read_csv(RAW / "team_cap_tiers.csv")
    tiers["multiplier"] = tiers.apply(
        lambda r: effective_multiplier(r["tier"], r["repeater"]), axis=1
    )
    df = df.merge(
        tiers[["Tm", "tier", "multiplier"]],
        on="Tm", how="left"
    )
    df["multiplier"] = df["multiplier"].fillna(1.0)
    df["npv_effective"] = df["npv"] * df["multiplier"]

    played = df[df["MP"] >= 1000].copy()
    played_long = played[played["years"] >= 2]

    def fmt(d):
        d = d.copy()
        d["salary_25"] = (d["salary_25"] / 1e6).round(1)
        d["npv"] = (d["npv"] / 1e6).round(1)
        d["npv_effective"] = (d["npv_effective"] / 1e6).round(1)
        d["WA_z"] = d["WA_z"].round(2)
        return d[["Player", "Tm", "tier", "bucket", "Age", "years", "WA_z",
                  "salary_25", "npv", "npv_effective"]]

    pd.options.display.float_format = "{:,.1f}".format

    print("=== TOP 5 NPV (ALL BUCKETS, team-neutral) ===")
    print(fmt(played_long.nlargest(5, "npv")).to_string(index=False))

    print("\n=== TOP 5 NPV — OPEN-NEGOTIATION ONLY ===")
    open_neg = played_long[played_long["bucket"] == "open_negotiation"]
    print(fmt(open_neg.nlargest(5, "npv")).to_string(index=False))

    print("\n=== TOP 5 NPV EFFECTIVE (team-adjusted) ===")
    print(fmt(played_long.nlargest(5, "npv_effective")).to_string(index=False))

    print("\n=== BOTTOM 5 NPV (team-neutral) ===")
    print(fmt(played_long.nsmallest(5, "npv")).to_string(index=False))

    print("\n=== BOTTOM 5 NPV EFFECTIVE (team-adjusted) ===")
    print(fmt(played_long.nsmallest(5, "npv_effective")).to_string(index=False))

    print("\n=== BUCKET BREAKDOWN — MEDIAN (avoids survivorship in aggregate) ===")
    bb = played_long.groupby("bucket").agg(
        n=("Player", "count"),
        median_npv=("npv", "median"),
        positive_share=("npv", lambda x: (x > 0).mean()),
    )
    bb["median_npv"] = (bb["median_npv"] / 1e6).round(1)
    bb["positive_share"] = (bb["positive_share"] * 100).round(0)
    print(bb.to_string())

    # Save all outputs
    df.to_csv(PROC / "values_v4_final.csv", index=False)
    fmt(played_long.nlargest(10, "npv")).to_csv(OUT / "v4_top10_all.csv", index=False)
    fmt(open_neg.nlargest(10, "npv")).to_csv(OUT / "v4_top10_unrigged.csv", index=False)
    fmt(played_long.nlargest(10, "npv_effective")).to_csv(OUT / "v4_top10_effective.csv", index=False)
    fmt(played_long.nsmallest(10, "npv")).to_csv(OUT / "v4_bottom10.csv", index=False)
    fmt(played_long.nsmallest(10, "npv_effective")).to_csv(OUT / "v4_bottom10_effective.csv", index=False)
    print(f"\nwrote v4 outputs to {OUT}")

    # Pritchard scenario with new multipliers
    pritchard = played_long[played_long["Player"] == "Payton Pritchard"]
    if not pritchard.empty:
        base = pritchard.iloc[0]["npv"]
        sc = tiers.copy()
        sc["pritchard_effective_npv_m"] = (base * sc["multiplier"] / 1e6).round(1)
        sc = sc.sort_values("pritchard_effective_npv_m", ascending=False)
        sc[["Tm", "tier", "repeater", "multiplier", "pritchard_effective_npv_m"]].to_csv(
            OUT / "v4_pritchard_scenario.csv", index=False
        )
        print(f"\n=== PRITCHARD SCENARIO (v4 multipliers) ===")
        print(sc[["Tm", "tier", "multiplier", "pritchard_effective_npv_m"]].head(8).to_string(index=False))
        print(f"  ... and below-cap (BRK): ${sc.iloc[-1]['pritchard_effective_npv_m']:.1f}M")
        print(f"Range: ${sc['pritchard_effective_npv_m'].min():.1f}M to ${sc['pritchard_effective_npv_m'].max():.1f}M ({sc['pritchard_effective_npv_m'].max()/sc['pritchard_effective_npv_m'].min():.1f}× span)")


if __name__ == "__main__":
    main()
