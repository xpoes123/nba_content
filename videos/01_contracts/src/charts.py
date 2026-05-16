"""Generate the headline charts for the video."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"

TIER_COLORS = {
    "second_apron": "#c1272d",
    "first_apron": "#e67e22",
    "taxpayer": "#f1c40f",
    "above_cap_below_tax": "#34495e",
    "below_cap": "#95a5a6",
}


def pritchard_chart() -> None:
    df = pd.read_csv(OUT / "pritchard_scenario.csv")
    df = df.sort_values("pritchard_effective_npv_m", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 9))
    colors = [TIER_COLORS[t] for t in df["tier"]]
    bars = ax.barh(df["Tm"], df["pritchard_effective_npv_m"], color=colors)
    ax.set_xlabel("Effective NPV surplus value ($M, over 3 contract years)")
    ax.set_title(
        "The Same Payton Pritchard Contract, On All 30 Teams\n"
        "Naive surplus: $53M.  Effective owner-dollar value ranges from $26M to $379M.",
        fontsize=12,
    )
    for bar, val in zip(bars, df["pritchard_effective_npv_m"]):
        ax.text(val + 4, bar.get_y() + bar.get_height() / 2,
                f"${val:.0f}M", va="center", fontsize=8)
    # legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=c, label=t.replace("_", " "))
        for t, c in TIER_COLORS.items()
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "pritchard_30_teams.png", dpi=140)
    print(f"wrote {OUT / 'pritchard_30_teams.png'}")


def top_unrigged_chart() -> None:
    df = pd.read_csv(OUT / "top_unrigged.csv").head(15)
    df = df.sort_values("surplus_npv_naive", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 7))
    colors = [TIER_COLORS.get(t, "#888") for t in df["tier"]]
    bars = ax.barh(df["Player"] + "  (" + df["Tm"] + ")", df["surplus_npv_naive"] / 1e6, color=colors)
    ax.set_xlabel("NPV surplus value ($M)")
    ax.set_title(
        "Best NBA Contracts — After Stripping Out Max, Rookie Scale, and Minimums\n"
        "These are the contracts GMs actually negotiated, ranked by aging-curve NPV",
        fontsize=12,
    )
    for bar, val in zip(bars, df["surplus_npv_naive"] / 1e6):
        ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
                f"${val:.0f}M", va="center", fontsize=9)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "top_unrigged.png", dpi=140)
    print(f"wrote {OUT / 'top_unrigged.png'}")


def bucket_breakdown_chart() -> None:
    """How surplus value is distributed across CBA-mandated buckets."""
    from headlines import tag_bucket
    df = pd.read_csv(ROOT / "data" / "processed" / "npv.csv")
    df = df[df["MP"] >= 1000].copy()
    df["bucket"] = df.apply(tag_bucket, axis=1)
    by_bucket = df.groupby("bucket").agg(
        n_players=("Player", "count"),
        median_naive_surplus=("surplus_npv_naive", "median"),
        total_naive_surplus=("surplus_npv_naive", "sum"),
    ).reindex(["rookie_scale", "min", "max", "open_negotiation"])
    print(by_bucket)
    by_bucket.to_csv(OUT / "bucket_breakdown.csv")

    fig, ax = plt.subplots(figsize=(9, 5))
    by_bucket["median_naive_surplus"].plot.bar(
        ax=ax, color=["#2980b9", "#16a085", "#c0392b", "#27ae60"]
    )
    ax.set_ylabel("Median NPV surplus value ($)")
    ax.set_title(
        "Where the Surplus Lives: CBA-Mandated Buckets vs Open Negotiation\n"
        "Rookie scale + min deals systematically beat what GMs negotiate freely.",
        fontsize=12,
    )
    ax.axhline(0, color="black", linewidth=0.8)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUT / "bucket_breakdown.png", dpi=140)
    print(f"wrote {OUT / 'bucket_breakdown.png'}")


def main() -> None:
    pritchard_chart()
    top_unrigged_chart()
    bucket_breakdown_chart()


if __name__ == "__main__":
    main()
