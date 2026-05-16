"""Multi-year NPV surplus value for each contract.

For each remaining year of the contract, project WA via the aging curve and
price it at the league $/win baseline. Effective dollars get the team-context
multiplier *for this year*; future years use the same multiplier (a forward-
looking team-context model would adjust as rosters shift, but that's beyond
scope for a 15-min video segment).

Outputs data/processed/npv.csv with naive_npv and effective_npv per player.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from aging import project_wa

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

CONTRACT_YEARS = ["2025-26", "2026-27", "2027-28", "2028-29", "2029-30", "2030-31"]

# Re-import constants without circular import
VET_MIN = 2_296_274
DPW = 5_127_783  # from value.py fit; could re-fit but stable enough for now

DISCOUNT = 0.05  # 5% per year time value


def main() -> None:
    df = pd.read_csv(PROC / "values_team_adjusted.csv")

    naive_npv = np.zeros(len(df))
    eff_npv = np.zeros(len(df))
    years_remaining = np.zeros(len(df), dtype=int)

    for i, row in df.iterrows():
        age = row["Age"]
        wa = row["WA"]
        if pd.isna(age) or pd.isna(wa):
            continue
        multiplier = row["multiplier"] if not pd.isna(row["multiplier"]) else 1.0
        for k, yr in enumerate(CONTRACT_YEARS):
            salary = row[yr]
            if pd.isna(salary) or salary <= 0:
                continue
            years_remaining[i] = k + 1
            proj_wa = project_wa(wa, int(age), k)
            expected = VET_MIN + DPW * max(proj_wa, 0)
            year_surplus = expected - salary
            discount_factor = (1.0 + DISCOUNT) ** k
            naive_npv[i] += year_surplus / discount_factor
            eff_npv[i] += year_surplus * multiplier / discount_factor

    df["years_remaining"] = years_remaining
    df["surplus_npv_naive"] = naive_npv
    df["surplus_npv_effective"] = eff_npv

    df.to_csv(PROC / "npv.csv", index=False)
    print(f"wrote {PROC / 'npv.csv'}")
    print()
    pd.options.display.float_format = "{:,.1f}".format
    cols = ["Player", "Tm", "tier", "Age", "years_remaining", "WA",
            "2025-26", "surplus_npv_naive", "surplus_npv_effective"]

    print("=== TOP 20 BY NAIVE MULTI-YEAR NPV ===")
    eligible = df[df["years_remaining"] >= 2]
    print(eligible.nlargest(20, "surplus_npv_naive")[cols].to_string(index=False))
    print()
    print("=== TOP 20 BY EFFECTIVE NPV (team-context-adjusted) ===")
    print(eligible.nlargest(20, "surplus_npv_effective")[cols].to_string(index=False))


if __name__ == "__main__":
    main()
