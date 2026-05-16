"""Composite metric, v2 — fixed scaling and z-score variant.

Bug in v1: averaged raw VORP (pts/100) with WS (wins). Wrong units.
v1 also double-counted the BPM signal: r(VORP, BPM×MP) = 0.989.

v2 gives two composites:
  WA_wins  — (2.7×VORP + WS) / 2     all on wins scale, drops redundant BPM
  WA_z     — (z(VORP) + z(WS)) / 2    unit-free, what the quants asked for

Each is fit independently to salary to get its own $/unit market price.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

VET_MIN = 2_296_274


def composites(p: pd.DataFrame) -> pd.DataFrame:
    p = p.copy()
    p["VORP_wins"] = p["VORP"] * 2.7
    p["BPM_wins"] = p["BPM"] * p["MP"] / (48 * 100) * 2.7
    p["WA_wins"] = (p["VORP_wins"] + p["WS"]) / 2.0
    # z-score on the >=500-MP population so bench guys with tiny samples don't
    # dominate the variance estimate
    pool = p[p["MP"] >= 500]
    mu_v, sd_v = pool["VORP_wins"].mean(), pool["VORP_wins"].std()
    mu_w, sd_w = pool["WS"].mean(), pool["WS"].std()
    p["z_VORP"] = (p["VORP_wins"] - mu_v) / sd_v
    p["z_WS"] = (p["WS"] - mu_w) / sd_w
    p["WA_z"] = (p["z_VORP"] + p["z_WS"]) / 2.0
    return p


def fit_price(p: pd.DataFrame, x_col: str) -> float:
    sub = p[(p[x_col] > p[x_col].quantile(0.5)) & p["2025-26"].notna()].copy()
    y = sub["2025-26"].to_numpy() - VET_MIN
    x = sub[x_col].to_numpy()
    return float((x @ y) / (x @ x))


def main() -> None:
    p = pd.read_csv(PROC / "players.csv")
    p = composites(p)

    beta_wins = fit_price(p, "WA_wins")
    beta_z = fit_price(p, "WA_z")
    print(f"$/composite-wins (wins-scale): ${beta_wins:,.0f}")
    print(f"$/z-unit  (z-score scale):     ${beta_z:,.0f}")
    print()

    # Old composite for comparison
    old = (p["VORP"] + p["WS"] + p["BPM_wins"]) / 3.0  # the buggy original
    p["WA_old"] = old.fillna(0)
    beta_old = fit_price(p, "WA_old")
    print(f"(v1 buggy composite for comparison): ${beta_old:,.0f}")
    print()

    for col, beta, label in [
        ("WA_wins", beta_wins, "WA_wins (fixed-scale)"),
        ("WA_z", beta_z, "WA_z (z-score)"),
        ("WA_old", beta_old, "WA_old (v1 buggy)"),
    ]:
        p[f"E_{col}"] = VET_MIN + beta * p[col]
        p[f"surplus_{col}"] = p[f"E_{col}"] - p["2025-26"]

    pd.options.display.float_format = "{:,.1f}".format
    p_played = p[p["MP"] >= 1000].copy()

    print("\n=== TOP 15: WA_wins (fixed scale) ===")
    cols_wins = ["Player", "Tm", "Age", "MP", "WA_wins", "2025-26", "E_WA_wins", "surplus_WA_wins"]
    print(p_played.nlargest(15, "surplus_WA_wins")[cols_wins].to_string(index=False))

    print("\n=== TOP 15: WA_z (z-score) ===")
    cols_z = ["Player", "Tm", "Age", "MP", "WA_z", "2025-26", "E_WA_z", "surplus_WA_z"]
    print(p_played.nlargest(15, "surplus_WA_z")[cols_z].to_string(index=False))

    print("\n=== TOP 15: WA_old (v1 buggy) ===")
    cols_old = ["Player", "Tm", "Age", "MP", "WA_old", "2025-26", "E_WA_old", "surplus_WA_old"]
    print(p_played.nlargest(15, "surplus_WA_old")[cols_old].to_string(index=False))

    # Specific players the quants asked about
    print("\n=== KORNET / TRE JONES under all three metrics ===")
    for name in ["Luke Kornet", "Tre Jones", "Payton Pritchard", "Nikola JokiÄ\x87",
                 "Shai Gilgeous-Alexander", "Victor Wembanyama"]:
        row = p[p["Player"].str.startswith(name[:8])].head(1)
        if row.empty:
            continue
        r = row.iloc[0]
        print(f"\n  {r['Player']:25s} Age {r['Age']:.0f}, MP {r['MP']:.0f}, Salary ${r['2025-26']/1e6:.1f}M")
        print(f"    WA_old:  {r['WA_old']:.2f}    E[salary] ${r['E_WA_old']/1e6:.1f}M   surplus ${r['surplus_WA_old']/1e6:+.1f}M")
        print(f"    WA_wins: {r['WA_wins']:.2f}    E[salary] ${r['E_WA_wins']/1e6:.1f}M   surplus ${r['surplus_WA_wins']/1e6:+.1f}M")
        print(f"    WA_z:    {r['WA_z']:+.2f}    E[salary] ${r['E_WA_z']/1e6:.1f}M   surplus ${r['surplus_WA_z']/1e6:+.1f}M")

    # Rank stability — Spearman correlation of the three rankings
    s = p_played[["surplus_WA_old", "surplus_WA_wins", "surplus_WA_z"]].rank(ascending=False)
    print("\n=== RANK CORRELATION (Spearman, top-MP-1000 players) ===")
    print(s.corr(method="spearman").round(3))


if __name__ == "__main__":
    main()
