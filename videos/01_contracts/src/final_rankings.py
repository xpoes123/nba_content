"""Final rankings using the z-score composite + aging + team context.

Run this after value_v2.py — it uses the same WA_z definition, applies aging
curves over remaining contract years, and applies the team cap-tier multiplier.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from aging import project_wa
from team_context import effective_multiplier
from value_v2 import composites, fit_price
from headlines import tag_bucket

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

VET_MIN = 2_296_274
DISCOUNT = 0.05
CONTRACT_YEARS = ["2025-26", "2026-27", "2027-28", "2028-29", "2029-30", "2030-31"]


def main() -> None:
    p = pd.read_csv(PROC / "players.csv")
    p = composites(p)
    beta_z = fit_price(p, "WA_z")

    # join contracts already merged via clean.py — players.csv has cap-hit cols
    # apply aging + npv
    rows = []
    for _, r in p.iterrows():
        if pd.isna(r["Age"]) or pd.isna(r["WA_z"]) or pd.isna(r["2025-26"]):
            continue
        age = int(r["Age"])
        wa_z = float(r["WA_z"])
        naive_npv = 0.0
        years_remaining = 0
        for k, yr in enumerate(CONTRACT_YEARS):
            sal = r[yr]
            if pd.isna(sal) or sal <= 0:
                continue
            years_remaining = k + 1
            proj = project_wa(wa_z, age, k)  # z-score scales with the curve
            expected = VET_MIN + beta_z * max(proj, 0)
            naive_npv += (expected - sal) / (1.0 + DISCOUNT) ** k
        rows.append({
            "Player": r["Player"],
            "Tm": r["Tm"],
            "Age": age,
            "MP": r["MP"],
            "WA_z": wa_z,
            "salary_25": r["2025-26"],
            "years": years_remaining,
            "npv_naive": naive_npv,
        })
    df = pd.DataFrame(rows)

    # join team multipliers
    tiers = pd.read_csv(RAW / "team_cap_tiers.csv")
    tiers["multiplier"] = tiers.apply(
        lambda r: effective_multiplier(r["tier"], r["repeater"]), axis=1
    )
    df["resolved_tm"] = df["Tm"]
    df = df.merge(
        tiers[["Tm", "tier", "multiplier"]].rename(columns={"Tm": "resolved_tm"}),
        on="resolved_tm", how="left"
    )
    df["multiplier"] = df["multiplier"].fillna(1.0)
    df["npv_effective"] = df["npv_naive"] * df["multiplier"]
    df["bucket"] = df.apply(lambda r: tag_bucket(pd.Series({
        "2025-26": r["salary_25"], "Age": r["Age"], "years_remaining": r["years"],
    })), axis=1)

    df = df[df["MP"] >= 1000].copy()
    pd.options.display.float_format = "{:,.1f}".format

    def fmt(d):
        d = d.copy()
        d["salary_25"] = (d["salary_25"] / 1e6).round(1)
        d["npv_naive"] = (d["npv_naive"] / 1e6).round(1)
        d["npv_effective"] = (d["npv_effective"] / 1e6).round(1)
        d["WA_z"] = d["WA_z"].round(2)
        return d[["Player", "Tm", "tier", "Age", "years", "WA_z",
                  "salary_25", "npv_naive", "npv_effective", "bucket"]]

    print("\n========================================")
    print("TOP 5 BEST CONTRACTS (NPV, ALL BUCKETS)")
    print("========================================")
    print(fmt(df.nlargest(5, "npv_naive")).to_string(index=False))

    print("\n========================================")
    print("TOP 5 BEST CONTRACTS (UN-RIGGED — no max/rookie/min)")
    print("========================================")
    open_neg = df[df["bucket"] == "open_negotiation"]
    print(fmt(open_neg.nlargest(5, "npv_naive")).to_string(index=False))

    print("\n========================================")
    print("TOP 5 BEST BY EFFECTIVE NPV (team-adjusted)")
    print("========================================")
    print(fmt(df.nlargest(5, "npv_effective")).to_string(index=False))

    print("\n========================================")
    print("BOTTOM 5 WORST CONTRACTS (NPV, naive)")
    print("========================================")
    print(fmt(df.nsmallest(5, "npv_naive")).to_string(index=False))

    print("\n========================================")
    print("BOTTOM 5 WORST CONTRACTS (effective, team-adjusted)")
    print("========================================")
    print(fmt(df.nsmallest(5, "npv_effective")).to_string(index=False))


if __name__ == "__main__":
    main()
