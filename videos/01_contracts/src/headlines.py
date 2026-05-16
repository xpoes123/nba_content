"""Generate the video's headline outputs.

Six CSVs land in outputs/:
  1. top_current_year.csv         — best 2025-26 surplus, naive
  2. top_npv.csv                  — best multi-year NPV, naive
  3. top_effective_npv.csv        — best multi-year NPV, team-context-adjusted
  4. top_unrigged.csv             — top NPV after stripping max + rookie-scale + min
  5. worst_contracts.csv          — bottom NPV (overpays)
  6. pritchard_scenario.csv       — same Pritchard contract on every team

A contract is flagged "structurally suppressed" if it falls into one of three
buckets the CBA caps below open-market value:
  - max:          first-year salary >= 25% of cap, OR named max designations
  - rookie_scale: 4-year rookie scale (first pick years 1-4 of career, drafted R1)
  - min:          veteran minimum or 2-way (first-year salary < $3M)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

MIN_MP = 1000  # filter sample-size noise from headline tables

# 2025-26 max salary tiers
MAX_25 = 0.25 * 154_647_000  # ~$38.7M (0-6 years exp)
MAX_30 = 0.30 * 154_647_000  # ~$46.4M (7-9 years)
MAX_35 = 0.35 * 154_647_000  # ~$54.1M (10+ years)
MIN_THRESHOLD = 3_500_000  # rough vet-min cutoff for 2025-26


def tag_bucket(row: pd.Series) -> str:
    sal = row["2025-26"]
    age = row["Age"]
    if pd.isna(sal):
        return "no_contract"
    if sal >= MAX_25 * 0.95:  # near or at max
        return "max"
    # rookie scale heuristic: age <= 23 + salary on R1-scale-like ramp + <=4 years
    # we don't have draft year directly, so use age proxy
    if age <= 23 and sal < 15_000_000 and row.get("years_remaining", 0) <= 4:
        return "rookie_scale"
    if sal < MIN_THRESHOLD:
        return "min"
    return "open_negotiation"


def main() -> None:
    df = pd.read_csv(PROC / "npv.csv")
    df["bucket"] = df.apply(tag_bucket, axis=1)
    df_played = df[df["MP"] >= MIN_MP].copy()

    cols_basic = [
        "Player", "Tm", "tier", "Age", "MP", "WA",
        "2025-26", "expected_salary", "surplus_naive",
    ]
    cols_npv = [
        "Player", "Tm", "tier", "Age", "years_remaining", "WA",
        "2025-26", "surplus_npv_naive", "surplus_npv_effective", "bucket",
    ]

    # 1. Top current year naive
    df_played.nlargest(20, "surplus_naive")[cols_basic + ["bucket"]].to_csv(
        OUT / "top_current_year.csv", index=False
    )

    # 2. Top multi-year NPV naive
    df_npv = df_played[df_played["years_remaining"] >= 2]
    df_npv.nlargest(20, "surplus_npv_naive")[cols_npv].to_csv(
        OUT / "top_npv.csv", index=False
    )

    # 3. Top multi-year NPV effective
    df_npv.nlargest(20, "surplus_npv_effective")[cols_npv].to_csv(
        OUT / "top_effective_npv.csv", index=False
    )

    # 4. Top NPV after stripping rigged contracts
    open_neg = df_npv[df_npv["bucket"] == "open_negotiation"]
    open_neg.nlargest(20, "surplus_npv_naive")[cols_npv].to_csv(
        OUT / "top_unrigged.csv", index=False
    )

    # 5. Worst contracts (bottom NPV)
    df_played.nsmallest(20, "surplus_npv_naive")[cols_npv].to_csv(
        OUT / "worst_contracts.csv", index=False
    )

    # 6. Pritchard scenario across all teams
    tiers = pd.read_csv(ROOT / "data" / "raw" / "team_cap_tiers.csv")
    from team_context import effective_multiplier
    tiers["multiplier"] = tiers.apply(
        lambda r: effective_multiplier(r["tier"], r["repeater"]), axis=1
    )
    pritchard = df_played[df_played["Player"] == "Payton Pritchard"].iloc[0]
    base_surplus = pritchard["surplus_npv_naive"]
    scenarios = tiers.copy()
    scenarios["pritchard_effective_npv_m"] = (base_surplus * scenarios["multiplier"]) / 1e6
    scenarios = scenarios.sort_values("pritchard_effective_npv_m", ascending=False)
    scenarios.to_csv(OUT / "pritchard_scenario.csv", index=False)

    # Print summary
    pd.options.display.float_format = "{:,.1f}".format
    print("\n=== 1. TOP 20 CURRENT-YEAR SURPLUS (MP >= 1000) ===")
    print(pd.read_csv(OUT / "top_current_year.csv").to_string(index=False))
    print("\n=== 2. TOP 20 NPV NAIVE ===")
    print(pd.read_csv(OUT / "top_npv.csv").to_string(index=False))
    print("\n=== 3. TOP 20 NPV EFFECTIVE (TEAM-ADJUSTED) ===")
    print(pd.read_csv(OUT / "top_effective_npv.csv").to_string(index=False))
    print("\n=== 4. TOP 20 OPEN-NEGOTIATION ONLY (un-rigged) ===")
    print(pd.read_csv(OUT / "top_unrigged.csv").to_string(index=False))
    print("\n=== 5. WORST 20 CONTRACTS ===")
    print(pd.read_csv(OUT / "worst_contracts.csv").to_string(index=False))
    print("\n=== 6. PRITCHARD SCENARIO ACROSS 30 TEAMS ===")
    print(pd.read_csv(OUT / "pritchard_scenario.csv").to_string(index=False))


if __name__ == "__main__":
    main()
