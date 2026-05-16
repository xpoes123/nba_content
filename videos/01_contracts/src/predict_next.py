"""Predict the NEXT generation of high-value contracts.

The Pritchard pattern (the one openly-negotiated deal in the league that works):
  1. Player is YOUNG (age ≤ 28 at signing)
  2. Currently producing well ABOVE his current salary's market price
  3. Has a deal about to EXPIRE (1-2 years remaining) — the team has to decide
  4. On a team with history of extending pre-breakout (or with cap incentive to)
  5. Not yet broken out in mainstream perception (low usage, low fame)

There are two distinct "next contract" pipelines:

  A. Rookie-scale players entering Year 3 or 4 (extension-eligible).
     If the team extends BEFORE breakout fully prices in, you get a Pritchard.
     If the team waits, you get a Trey Murphy-style market-rate deal.

  B. Minimum-deal vets producing way above the floor (Queta, Spencer, Diabaté).
     Their next deal could be a 3-4yr $8-15M extension. If the team locks them
     up before some other team offers more, it's the next Pritchard.

For each candidate we predict:
  - expected current-market value if they signed today  (E_market)
  - their actual remaining cap hit                       (current)
  - "extension window" flag (in their final 1-2 years)
  - team's pattern of early extension (heuristic)

The output is a ranked list of "most likely to become next Pritchard."
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUT = ROOT / "outputs"

# Teams with documented history of pre-breakout extensions (qualitative):
EARLY_EXTENDERS = {"BOS", "OKC", "IND", "HOU", "MIA", "ATL", "CHO", "MEM"}


def main() -> None:
    df = pd.read_csv(PROC / "values_v4_final.csv")

    # Played enough to evaluate
    df = df[df["MP"] >= 800].copy()

    # Determine years remaining (already in npv csv as 'years')
    df = df.rename(columns={"years": "years_remaining"})

    # Open-market expected salary (current-year basis)
    # E = vet_min + β · WA_z, where β = $4.86M / z-unit from value_v4
    VET_MIN = 2_296_274
    BETA = 4_862_297
    df["E_market_now"] = VET_MIN + BETA * df["WA_z"]
    df["current_underpay"] = df["E_market_now"] - df["salary_25"]

    # Two pipelines:
    df["extension_window"] = df["years_remaining"] <= 2
    df["early_extender"] = df["Tm"].isin(EARLY_EXTENDERS)
    df["young"] = df["Age"] <= 26

    # Score for "next Pritchard" potential
    # weight: current underpay (signal of value), youth (signal of upside),
    # extension window (signal that next deal is imminent), team pattern
    df["next_pritchard_score"] = (
        df["current_underpay"].clip(lower=0) / 1e6  # in millions, current underpay
        * (1.0 + 0.5 * df["young"].astype(int))      # youth bonus
        * (1.0 + 0.4 * df["extension_window"].astype(int))  # imminent decision bonus
        * (1.0 + 0.2 * df["early_extender"].astype(int))   # team pattern bonus
    )

    pd.options.display.float_format = "{:,.1f}".format

    def fmt(d):
        d = d.copy()
        d["salary_25"] = (d["salary_25"] / 1e6).round(2)
        d["E_market_now"] = (d["E_market_now"] / 1e6).round(2)
        d["current_underpay"] = (d["current_underpay"] / 1e6).round(2)
        d["WA_z"] = d["WA_z"].round(2)
        d["next_pritchard_score"] = d["next_pritchard_score"].round(2)
        return d[["Player", "Tm", "Age", "MP", "WA_z",
                  "salary_25", "E_market_now", "current_underpay",
                  "years_remaining", "extension_window", "early_extender",
                  "bucket", "next_pritchard_score"]]

    print("=== PIPELINE A: Rookie-scale players in extension window ===")
    pipe_a = df[
        (df["bucket"] == "rookie_scale")
        & (df["Age"] <= 24)
        & (df["WA_z"] >= 0.5)
        & (df["years_remaining"] <= 3)
    ].sort_values("next_pritchard_score", ascending=False)
    print(fmt(pipe_a.head(10)).to_string(index=False))

    print("\n=== PIPELINE B: Minimum-deal vets producing well above floor ===")
    pipe_b = df[
        (df["bucket"] == "min")
        & (df["WA_z"] >= 0.8)
        & (df["Age"] <= 28)
        & (df["years_remaining"] <= 2)
    ].sort_values("next_pritchard_score", ascending=False)
    print(fmt(pipe_b.head(10)).to_string(index=False))

    print("\n=== PIPELINE C: Mid-career bargains about to renegotiate ===")
    pipe_c = df[
        (df["bucket"] == "open_negotiation")
        & (df["Age"] <= 26)
        & (df["WA_z"] >= 0.8)
        & (df["years_remaining"] <= 2)
    ].sort_values("next_pritchard_score", ascending=False)
    print(fmt(pipe_c.head(10)).to_string(index=False))

    print("\n=== OVERALL TOP 15: most likely 'next Pritchard' candidates ===")
    candidates = df[
        (df["WA_z"] >= 0.6)
        & (df["Age"] <= 27)
        & (df["years_remaining"] <= 3)
        & (df["bucket"] != "max")
    ].sort_values("next_pritchard_score", ascending=False)
    print(fmt(candidates.head(15)).to_string(index=False))

    candidates.to_csv(OUT / "v4_next_pritchard_candidates.csv", index=False)


if __name__ == "__main__":
    main()
