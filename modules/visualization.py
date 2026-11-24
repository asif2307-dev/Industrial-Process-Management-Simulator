
import matplotlib.pyplot as plt

# Vibrant palette for distinct process identification
PALETTE = [
    "#38bdf8",  # Sky Blue
    "#818cf8",  # Indigo
    "#34d399",  # Emerald
    "#fbbf24",  # Amber
    "#f43f5e",  # Rose
    "#a78bfa",  # Violet
    "#2dd4bf",  # Teal
    "#fb923c",  # Orange
    "#e879f9",  # Fuchsia
    "#60a5fa",  # Blue
]


def plot_gantt_chart(ax, timeline, title="CPU Execution Timeline", dark_mode=True):
    """
    Renders an embedded, industrial-grade Gantt chart directly onto a Matplotlib Axes.
    """
    ax.clear()

    bg_color = "#171e2d" if dark_mode else "#ffffff"
    text_color = "#f8fafc" if dark_mode else "#0f172a"
    subtext_color = "#94a3b8" if dark_mode else "#64748b"
    grid_color = "#334155" if dark_mode else "#e2e8f0"

    ax.set_facecolor(bg_color)
    ax.figure.patch.set_facecolor("#1e293b" if dark_mode else "#f8fafc")

    if not timeline:
        ax.text(
            0.5, 0.5,
            "Awaiting Simulation Run...\nConfigure processes and click 'Run Simulation'",
            color=subtext_color,
            ha="center", va="center",
            fontsize=11, fontweight="medium",
            transform=ax.transAxes
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        return

    # Assign consistent colors to PIDs
    unique_pids = []
    for item in timeline:
        if item["pid"] not in unique_pids and item["pid"] != "IDLE":
            unique_pids.append(item["pid"])

    color_map = {
        pid: PALETTE[i % len(PALETTE)] for i, pid in enumerate(unique_pids)
    }
    color_map["IDLE"] = "#475569" if dark_mode else "#cbd5e1"

    ticks = set()
    prev_end = None

    for item in timeline:
        start = item["start"]
        end = item["end"]
        pid = item["pid"]
        duration = end - start

        # Detect and render idle gap if applicable
        if prev_end is not None and start > prev_end:
            idle_dur = start - prev_end
            ax.barh(
                0, idle_dur, left=prev_end,
                height=0.48, color="#334155",
                edgecolor="#64748b", linestyle="--", linewidth=1
            )
            ax.text(
                (prev_end + start) / 2, 0, "IDLE",
                ha="center", va="center",
                color="#94a3b8", fontsize=8, fontweight="bold"
            )
            ticks.add(prev_end)

        ticks.add(start)
        ticks.add(end)

        bar_color = color_map.get(pid, PALETTE[0])
        ax.barh(
            0, duration, left=start,
            height=0.48, color=bar_color,
            edgecolor="#0f172a", linewidth=1.5
        )

        # Label inside the bar if wide enough, otherwise small
        label = pid
        if duration <= 1:
            label = pid.split("_")[0] if "_" in pid else pid

        ax.text(
            (start + end) / 2, 0, label,
            ha="center", va="center",
            color="#ffffff" if dark_mode else "#0f172a",
            fontsize=10, fontweight="bold"
        )
        prev_end = end

    sorted_ticks = sorted(list(ticks))
    ax.set_xticks(sorted_ticks)
    ax.set_xticklabels([str(t) for t in sorted_ticks], color=subtext_color, fontsize=9)
    ax.set_yticks([])

    ax.set_title(title, color=text_color, fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Timeline (Units / ms)", color=subtext_color, fontsize=9, labelpad=8)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(grid_color)
    ax.grid(axis="x", linestyle=":", color=grid_color, alpha=0.6)


def show_gantt_chart(timeline, title="CPU Scheduling"):
    """
    Standalone popup version for backwards compatibility.
    """
    fig, ax = plt.subplots(figsize=(10, 3.2))
    plot_gantt_chart(ax, timeline, title, dark_mode=False)
    plt.tight_layout()
    plt.show()

