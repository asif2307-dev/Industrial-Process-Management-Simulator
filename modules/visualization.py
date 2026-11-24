
import matplotlib.pyplot as plt


def show_gantt_chart(timeline, title="CPU Scheduling"):
    fig, ax = plt.subplots(figsize=(10, 3))

    for item in timeline:
        start = item["start"]
        end = item["end"]
        pid = item["pid"]

        ax.barh(
            0,
            end - start,
            left=start,
            height=0.5,
            edgecolor="black"
        )

        ax.text(
            (start + end) / 2,
            0,
            pid,
            ha="center",
            va="center"
        )

        ax.text(start, -0.4, str(start), ha="center")

    if timeline:
        ax.text(timeline[-1]["end"], -0.4,
                str(timeline[-1]["end"]), ha="center")

    ax.set_title(title)
    ax.set_xlabel("Execution Time")
    ax.set_yticks([])
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()
