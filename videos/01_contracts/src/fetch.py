"""Pull raw data from Basketball-Reference for the 2025-26 NBA season.

Outputs to data/raw/:
  - advanced_stats.csv   one row per player (BPM, VORP, WS, etc.)
  - per_game_stats.csv   minutes, games, position
  - contracts.csv        year-by-year salary through end of deal
"""

from __future__ import annotations

import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

SEASON_END_YEAR = 2026  # 2025-26 season
HEADERS = {"User-Agent": "Mozilla/5.0 (research; contracts video)"}
SLEEP = 4.0  # br rate limit is ~20/min; be polite


def fetch(url: str) -> str:
    print(f"GET {url}")
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    time.sleep(SLEEP)
    return r.text


def read_table(html: str, table_id: str) -> pd.DataFrame:
    """Read a table from BR HTML, including tables hidden inside HTML comments."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id=table_id)
    if table is None:
        # BR hides some tables in HTML comments
        for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
            if f'id="{table_id}"' in c:
                table = BeautifulSoup(c, "lxml").find("table", id=table_id)
                if table is not None:
                    break
    if table is None:
        raise RuntimeError(f"table {table_id!r} not found")
    return pd.read_html(StringIO(str(table)))[0]


def fetch_advanced() -> pd.DataFrame:
    url = f"https://www.basketball-reference.com/leagues/NBA_{SEASON_END_YEAR}_advanced.html"
    df = read_table(fetch(url), "advanced")
    # drop repeated header rows
    df = df[df["Rk"] != "Rk"].copy()
    return df


def fetch_per_game() -> pd.DataFrame:
    url = f"https://www.basketball-reference.com/leagues/NBA_{SEASON_END_YEAR}_per_game.html"
    df = read_table(fetch(url), "per_game_stats")
    df = df[df["Rk"] != "Rk"].copy()
    return df


def fetch_contracts() -> pd.DataFrame:
    url = "https://www.basketball-reference.com/contracts/players.html"
    df = read_table(fetch(url), "player-contracts")
    # multi-level columns sometimes; flatten if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[-1] for c in df.columns]
    # drop repeated header rows
    df = df[df["Player"] != "Player"].copy()
    return df


def main() -> None:
    adv = fetch_advanced()
    adv.to_csv(RAW / "advanced_stats.csv", index=False)
    print(f"advanced_stats: {len(adv)} rows")

    pg = fetch_per_game()
    pg.to_csv(RAW / "per_game_stats.csv", index=False)
    print(f"per_game_stats: {len(pg)} rows")

    contracts = fetch_contracts()
    contracts.to_csv(RAW / "contracts.csv", index=False)
    print(f"contracts: {len(contracts)} rows, columns: {list(contracts.columns)}")


if __name__ == "__main__":
    main()
