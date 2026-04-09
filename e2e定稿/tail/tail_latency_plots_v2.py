
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV = "estimated_tail_latency_values_v2.csv"

WORKFLOWS = ["request_risk", "log_alert", "media_content"]
WORKFLOW_TITLES = ["(a) request_risk", "(b) log_alert", "(c) media_content"]
SCENARIOS = ["stable", "drift"]
LEVELS = ["low", "medium", "high"]

COLORS = {"BaseSpec": "#4C78A8", "SpecSW": "#F58518"}

def add_dual_labels(ax):
    xticks = np.arange(6)
    ax.set_xticks(xticks)
    ax.set_xticklabels(["low", "medium", "high", "low", "medium", "high"])
    ax.text(1, -0.20, "stable", transform=ax.get_xaxis_transform(), ha="center", va="top")
    ax.text(4, -0.20, "drift", transform=ax.get_xaxis_transform(), ha="center", va="top")
    ax.axvline(2.5, color="0.85", linewidth=1.0)

def plot_p95_normalized(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.0), sharey=True)
    methods = ["BaseSpec", "SpecSW"]
    width = 0.32

    for ax, wf, title in zip(axes, WORKFLOWS, WORKFLOW_TITLES):
        x = np.arange(6)
        vals_by_method = {m: [] for m in methods}
        for sc in SCENARIOS:
            for lv in LEVELS:
                rec = df[(df.workflow == wf) & (df.scenario == sc) & (df.level == lv)].iloc[0]
                vals_by_method["BaseSpec"].append(float(rec["BaseSpec_p95_norm_to_NoSpec"]))
                vals_by_method["SpecSW"].append(float(rec["SpecSW_p95_norm_to_NoSpec"]))

        ax.axhline(1.0, color="0.5", linestyle="--", linewidth=1.0)
        for i, m in enumerate(methods):
            ax.bar(x + (i - 0.5) * width, vals_by_method[m], width=width, label=m, color=COLORS[m])

        ax.set_title(title, pad=6)
        add_dual_labels(ax)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.6)
        ax.margins(x=0.03)

    axes[0].set_ylabel("Normalized P95 latency (vs. NoSpec)")
    for ax in axes:
        ax.set_ylim(0.45, 1.05)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=[0, 0.04, 1, 0.93])
    fig.savefig("fig_p95_norm_to_nospec_grouped.png", dpi=220, bbox_inches="tight")
    fig.savefig("fig_p95_norm_to_nospec_grouped.pdf", bbox_inches="tight")
    plt.close(fig)

def plot_p99_heatmap(df: pd.DataFrame) -> None:
    columns = [("stable", "low"), ("stable", "medium"), ("stable", "high"),
               ("drift", "low"), ("drift", "medium"), ("drift", "high")]
    arr = np.zeros((3, 6), dtype=float)

    for i, wf in enumerate(WORKFLOWS):
        for j, (sc, lv) in enumerate(columns):
            rec = df[(df.workflow == wf) & (df.scenario == sc) & (df.level == lv)].iloc[0]
            arr[i, j] = float(rec["SpecSW_vs_BaseSpec_p99_pct"])

    fig, ax = plt.subplots(figsize=(12, 3.6))
    vmax = max(18, np.ceil(np.abs(arr).max()))
    im = ax.imshow(arr, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")

    ax.set_xticks(np.arange(6))
    ax.set_xticklabels(["stable\nlow", "stable\nmedium", "stable\nhigh",
                        "drift\nlow", "drift\nmedium", "drift\nhigh"])
    ax.set_yticks(np.arange(3))
    ax.set_yticklabels(WORKFLOWS)
    ax.set_title("SpecSW vs. BaseSpec on P99 tail latency (%)", pad=10)

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            val = arr[i, j]
            txt_color = "white" if abs(val) >= vmax * 0.45 else "black"
            ax.text(j, i, f"{val:+.0f}%", ha="center", va="center", color=txt_color, fontsize=10)

    cbar = fig.colorbar(im, ax=ax, shrink=0.95)
    cbar.set_label("Change in P99 tail latency (%)")

    for x in np.arange(-0.5, 6, 1):
        ax.axvline(x, color="white", linewidth=0.8, alpha=0.8)
    for y in np.arange(-0.5, 3, 1):
        ax.axhline(y, color="white", linewidth=0.8, alpha=0.8)

    fig.tight_layout()
    fig.savefig("fig_p99_specsw_vs_basespec_heatmap.png", dpi=220, bbox_inches="tight")
    fig.savefig("fig_p99_specsw_vs_basespec_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)

def main() -> None:
    df = pd.read_csv(CSV)
    plot_p95_normalized(df)
    plot_p99_heatmap(df)

if __name__ == "__main__":
    main()
