"""Charts for v4 (adversarial-review-corrected model)."""

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
    df = pd.read_csv(OUT / "v4_pritchard_scenario.csv")
    df = df.sort_values("pritchard_effective_npv_m", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 9))
    colors = [TIER_COLORS[t] for t in df["tier"]]
    bars = ax.barh(df["Tm"], df["pritchard_effective_npv_m"], color=colors)
    ax.set_xlabel("Effective NPV surplus value ($M)")
    ax.set_title(
        "Same Payton Pritchard Contract, On All 30 Teams (v4)\n"
        "Team-neutral NPV: $4.3M.  Effective owner-dollar value ranges $2.2M to $15.5M.",
        fontsize=12,
    )
    for bar, val in zip(bars, df["pritchard_effective_npv_m"]):
        ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                f"${val:.1f}M", va="center", fontsize=8)
    from matplotlib.patches import Patch
    legend = [Patch(facecolor=c, label=t.replace("_", " "))
              for t, c in TIER_COLORS.items()]
    ax.legend(handles=legend, loc="lower right", fontsize=9)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "v4_pritchard_30_teams.png", dpi=140)
    print(f"wrote {OUT / 'v4_pritchard_30_teams.png'}")


def one_of_97_chart() -> None:
    """97 dots — 1 green, 96 red. The headline visual."""
    df = pd.read_csv(ROOT / "data" / "processed" / "values_v4_final.csv")
    open_neg = df[(df["bucket"] == "open_negotiation") & (df["MP"] >= 1000) & (df["years"] >= 2)].copy()
    open_neg = open_neg.sort_values("npv")
    n = len(open_neg)
    cols = 12
    rows = (n + cols - 1) // cols
    fig, ax = plt.subplots(figsize=(12, rows * 0.7))
    for i, (_, r) in enumerate(open_neg.iterrows()):
        x = i % cols
        y = rows - 1 - (i // cols)
        color = "#27ae60" if r["npv"] > 0 else "#c0392b"
        ax.scatter(x, y, c=color, s=180, edgecolors="black", linewidths=0.5)
        if r["npv"] > 0:
            ax.annotate(r["Player"], (x, y), xytext=(0, 13), textcoords="offset points",
                        fontsize=8, ha="center", fontweight="bold")
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)
    ax.axis("off")
    ax.set_title(
        f"Of {n} openly negotiated NBA contracts (1000+ MP, 2+ yrs remaining),\n"
        "exactly 1 is projected positive NPV: Payton Pritchard",
        fontsize=13,
    )
    plt.tight_layout()
    plt.savefig(OUT / "v4_one_of_97.png", dpi=140, bbox_inches="tight")
    print(f"wrote {OUT / 'v4_one_of_97.png'}")


def bucket_positive_share() -> None:
    """Positive-NPV share by bucket — replaces the original total-aggregate chart."""
    df = pd.read_csv(ROOT / "data" / "processed" / "values_v4_final.csv")
    sub = df[(df["MP"] >= 1000) & (df["years"] >= 2)]
    by_bucket = sub.groupby("bucket").agg(
        n=("Player", "count"),
        median_npv=("npv", "median"),
        pos_share=("npv", lambda x: (x > 0).mean() * 100),
    ).reindex(["min", "rookie_scale", "max", "open_negotiation"])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: median NPV
    colors = ["#16a085", "#2980b9", "#c0392b", "#27ae60"]
    by_bucket["median_npv_m"] = by_bucket["median_npv"] / 1e6
    axes[0].bar(by_bucket.index, by_bucket["median_npv_m"], color=colors)
    axes[0].set_ylabel("Median NPV ($M)")
    axes[0].set_title("Median surplus by contract bucket")
    axes[0].axhline(0, color="black", linewidth=0.8)
    for i, (idx, v) in enumerate(by_bucket["median_npv_m"].items()):
        axes[0].text(i, v + (3 if v > 0 else -8), f"${v:.0f}M", ha="center", fontsize=10)

    # Right: positive share
    axes[1].bar(by_bucket.index, by_bucket["pos_share"], color=colors)
    axes[1].set_ylabel("% with positive NPV")
    axes[1].set_title("Share of contracts projecting positive value")
    axes[1].set_ylim(0, 70)
    for i, (idx, v) in enumerate(by_bucket["pos_share"].items()):
        n = by_bucket.iloc[i]["n"]
        axes[1].text(i, v + 1.5, f"{v:.0f}%\n(n={n:.0f})", ha="center", fontsize=10)

    plt.suptitle(
        "Where the surplus actually lives: CBA-mandated buckets vs GM negotiation",
        fontsize=13,
    )
    plt.tight_layout()
    plt.savefig(OUT / "v4_bucket_breakdown.png", dpi=140)
    print(f"wrote {OUT / 'v4_bucket_breakdown.png'}")


def main() -> None:
    pritchard_chart()
    one_of_97_chart()
    bucket_positive_share()


if __name__ == "__main__":
    main()
