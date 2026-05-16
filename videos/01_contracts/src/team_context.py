"""Apply team-context multipliers to convert naive surplus into effective surplus.

A dollar of salary doesn't cost a dollar — it costs whatever constraint it's
binding against. The shadow price of cap space depends on the team's tier.

Multipliers below are the *effective* cost of $1 of incremental cap to ownership.
For teams above the tax line, we use the blended-bracket average (~$2.5/$ for
deep taxpayers, $1.50/$ for shallow). Repeater teams get an extra +$1/$ kicker
in the deeper brackets. Apron tiers add a flexibility premium (you can't replace
the player you'd otherwise cut), modeled here as a multiplicative bump.

These multipliers are admittedly approximate — real cap economics are stepwise
within each bracket. For a 15-minute YouTube segment, the tier-level multiplier
captures the right order of magnitude and the qualitative ranking.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

# Adversarial-review fix: tax and apron were composing multiplicatively, which
# inflated effective values 2-3×. Tax is a per-dollar marginal cost; apron is
# operational (lost MLE, frozen picks, no aggregation). Model them additively,
# not multiplicatively, and lower the apron premiums to a defensible band.
#
# (base_multiplier, apron_flexibility_premium)  →  effective = base + premium
TIER_MULTIPLIERS = {
    "below_cap":             (0.5, 0.0),   # cap floor: $ are partially "free"
    "above_cap_below_tax":   (1.0, 0.0),   # standard
    "taxpayer":              (1.5, 0.0),   # most taxpayers in shallow brackets
    "first_apron":           (2.0, 0.3),   # tax + lost MLE/buyout (small premium)
    "second_apron":          (2.5, 0.6),   # tax + frozen picks, no aggregation
}

REPEATER_BONUS = 0.5  # additive +0.5 above tax only — was +1.0 multiplicative


def load_team_tiers() -> pd.DataFrame:
    return pd.read_csv(RAW / "team_cap_tiers.csv")


def effective_multiplier(tier: str, repeater: str) -> float:
    base, premium = TIER_MULTIPLIERS[tier]
    if repeater == "Yes" and tier in {"taxpayer", "first_apron", "second_apron"}:
        base += REPEATER_BONUS
    # additive composition: tax cost (base) + apron operational premium
    return base + premium


def main() -> None:
    values = pd.read_csv(PROC / "values.csv")
    tiers = load_team_tiers()
    tiers["multiplier"] = tiers.apply(
        lambda r: effective_multiplier(r["tier"], r["repeater"]), axis=1
    )
    print("=== TEAM MULTIPLIERS ===")
    print(tiers[["Tm", "tier", "repeater", "multiplier"]].to_string(index=False))

    # join on player's *actual* team this season (the Tm from the stats row)
    # for traded players (Tm == 2TM/3TM) we use the ContractTm (post-trade)
    values["resolved_tm"] = values["Tm"].where(
        ~values["Tm"].isin(["2TM", "3TM", "4TM"]), values["ContractTm"]
    )
    merged = values.merge(
        tiers[["Tm", "tier", "repeater", "multiplier"]].rename(columns={"Tm": "resolved_tm"}),
        on="resolved_tm",
        how="left",
    )

    # effective surplus = naive surplus × team's marginal-dollar multiplier
    # both the production value AND the salary translate to owner-dollars at the
    # same shadow price, so the gap scales with the multiplier. Overpays are
    # amplified the same way (a bad contract on an apron team hurts more).
    merged["effective_cost"] = merged["2025-26"] * merged["multiplier"]
    merged["surplus_effective"] = merged["surplus_naive"] * merged["multiplier"]

    out = merged[[
        "Player", "Tm", "resolved_tm", "tier", "repeater", "multiplier",
        "Age", "Pos", "G", "MP", "WA",
        "2025-26", "effective_cost", "expected_salary",
        "surplus_naive", "surplus_effective",
        "2026-27", "2027-28", "2028-29", "2029-30", "2030-31", "Guaranteed",
    ]].copy()
    out.to_csv(PROC / "values_team_adjusted.csv", index=False)
    print()
    print(f"wrote {PROC / 'values_team_adjusted.csv'}  ({len(out)} rows)")
    print()
    print("=== TOP 15 BY *EFFECTIVE* SURPLUS (current year, team-context-adjusted) ===")
    cols = ["Player", "Tm", "tier", "multiplier", "Age", "MP",
            "WA", "2025-26", "effective_cost", "surplus_effective"]
    top = out.nlargest(15, "surplus_effective")[cols]
    pd.options.display.float_format = "{:,.1f}".format
    print(top.to_string(index=False))


if __name__ == "__main__":
    main()
