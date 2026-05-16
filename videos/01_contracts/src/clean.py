"""Clean and join raw data into a single player-season frame.

Produces data/processed/players.csv with one row per player containing:
  - identity:    name, age, team, position
  - playing:     games, minutes, started
  - production:  BPM, VORP, WS, OWS, DWS, PER, USG, TS%
  - contract:    cap hits for 2025-26 through 2030-31, total guaranteed
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)


def _to_dollars(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .replace({"nan": None, "": None})
        .astype(float)
    )


def load_advanced() -> pd.DataFrame:
    df = pd.read_csv(RAW / "advanced_stats.csv")
    df = df.rename(columns={"Team": "Tm"})
    # for traded players, BR emits one row per stint plus a "2TM"/"3TM" aggregate row.
    # keep only the aggregate when present, else the single team row.
    agg = df[df["Tm"].isin(["2TM", "3TM", "4TM"])]
    single = df[~df["Player"].isin(agg["Player"])]
    out = pd.concat([agg, single], ignore_index=True)
    keep = [
        "Player", "Age", "Tm", "Pos", "G", "GS", "MP",
        "PER", "TS%", "USG%", "OWS", "DWS", "WS", "WS/48",
        "OBPM", "DBPM", "BPM", "VORP",
    ]
    out = out[keep].copy()
    out["Age"] = pd.to_numeric(out["Age"], errors="coerce")
    for c in ["G", "GS", "MP"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    for c in ["PER", "TS%", "USG%", "OWS", "DWS", "WS", "WS/48",
              "OBPM", "DBPM", "BPM", "VORP"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def load_contracts() -> pd.DataFrame:
    df = pd.read_csv(RAW / "contracts.csv")
    # BR injects section-divider rows (Player==NaN, salary cells == 'Salary'); drop them
    df = df.dropna(subset=["Player"]).copy()
    year_cols = ["2025-26", "2026-27", "2027-28", "2028-29", "2029-30", "2030-31"]
    for c in year_cols:
        df[c] = _to_dollars(df[c])
    df["Guaranteed"] = _to_dollars(df["Guaranteed"])
    # traded players show one contract row per team they passed through; the salary
    # numbers are identical across rows, so collapse to one row per player
    df = df.drop_duplicates(subset=["Player"], keep="last")
    return df[["Player", "Tm"] + year_cols + ["Guaranteed"]].copy()


def main() -> None:
    adv = load_advanced()
    con = load_contracts()
    # join on player name; team can differ (e.g., a traded player's contract row
    # lists current team, but stats show 2TM aggregate). Keep contract team as "ContractTm".
    merged = adv.merge(
        con.rename(columns={"Tm": "ContractTm"}),
        on="Player",
        how="left",
    )
    # players with stats but no contract row = on minimum / two-way / pending
    print(f"players with stats: {len(adv)}")
    print(f"players with contract: {len(con)}")
    print(f"merged rows: {len(merged)}")
    print(f"merged w/ 2025-26 salary: {merged['2025-26'].notna().sum()}")

    merged.to_csv(PROC / "players.csv", index=False)
    print(f"wrote {PROC / 'players.csv'}")


if __name__ == "__main__":
    main()
