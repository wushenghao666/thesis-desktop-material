from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Adjusted overall averages:
# BaseSpec ≈ 2.42x, SpecSW ≈ 2.97x

BASE_SPEEDUP_CSV = "avg_speedup_values_natural.csv"
MEAN_LATENCY_CSV = "mean_latency_values_natural.csv"

def add_dual_labels(ax):
    xticks = np.arange(6)
    ax.set_xticks(xticks)
    ax.set_xticklabels(["low", "medium", "high", "low", "medium", "high"])
    ax.text(1, -0.20, "stable", transform=ax.get_xaxis_transform(), ha="center", va="top")
    ax.text(4, -0.20, "drift", transform=ax.get_xaxis_transform(), ha="center", va="top")
    ax.axvline(2.5, color="0.85", linewidth=1.0)

def main() -> None:
    spd = pd.read_csv(BASE_SPEEDUP_CSV)
    lat = pd.read_csv(MEAN_LATENCY_CSV)

    workflows = ["request_risk", "log_alert", "media_content"]
    workflow_titles = ["(a) request_risk", "(b) log_alert", "(c) media_content"]
    scenarios = ["stable", "drift"]
    levels = ["low", "medium", "high"]

    colors = {"NoSpec": "#9E9E9E", "BaseSpec": "#4C78A8", "SpecSW": "#F58518"}

    # Mean latency
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.0), sharey=False)
    methods = ["NoSpec", "BaseSpec", "SpecSW"]
    width = 0.24
    for ax, wf, title in zip(axes, workflows, workflow_titles):
        x = np.arange(6)
        vals_by_method = {m: [] for m in methods}
        errs_by_method = {m: [] for m in methods}
        for sc in scenarios:
            for lv in levels:
                rec = lat[(lat.workflow == wf) & (lat.scenario == sc) & (lat.level == lv)].iloc[0]
                for m in methods:
                    vals_by_method[m].append(float(rec[f"{m}_mean"]))
                    errs_by_method[m].append(float(rec[f"{m}_ci95"]))
        for i, m in enumerate(methods):
            ax.bar(
                x + (i - 1) * width,
                vals_by_method[m],
                width=width,
                label=m,
                color=colors[m],
                yerr=errs_by_method[m],
                capsize=2,
                error_kw={"elinewidth": 1.0},
            )
        ax.set_title(title, pad=6)
        add_dual_labels(ax)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.6)
        ax.margins(x=0.03)
    axes[0].set_ylabel("Mean latency (ms)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=[0, 0.04, 1, 0.93])
    fig.savefig("fig_mean_latency_grouped_dualx_natural.png", dpi=220, bbox_inches="tight")
    fig.savefig("fig_mean_latency_grouped_dualx_natural.pdf", bbox_inches="tight")
    plt.close(fig)

    # Avg speedup
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.0), sharey=True)
    methods2 = ["BaseSpec", "SpecSW"]
    width2 = 0.32
    for ax, wf, title in zip(axes, workflows, workflow_titles):
        x = np.arange(6)
        vals_by_method = {m: [] for m in methods2}
        for sc in scenarios:
            for lv in levels:
                for m in methods2:
                    rec = spd[(spd.workflow == wf) & (spd.scenario == sc) & (spd.level == lv) & (spd.method == m)].iloc[0]
                    vals_by_method[m].append(float(rec["avg_speedup"]))
        ax.axhline(1.0, color="0.5", linestyle="--", linewidth=1.0)
        for i, m in enumerate(methods2):
            ax.bar(x + (i - 0.5) * width2, vals_by_method[m], width=width2, label=m, color=colors[m])
        ax.set_title(title, pad=6)
        add_dual_labels(ax)
        ax.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.6)
        ax.margins(x=0.03)
    axes[0].set_ylabel("Avg. speedup")
    ymax = max(float(spd["avg_speedup"].max()) * 1.12, 4.3)
    for ax in axes:
        ax.set_ylim(0, ymax)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=[0, 0.04, 1, 0.93])
    fig.savefig("fig_avg_speedup_grouped_dualx_natural.png", dpi=220, bbox_inches="tight")
    fig.savefig("fig_avg_speedup_grouped_dualx_natural.pdf", bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()
