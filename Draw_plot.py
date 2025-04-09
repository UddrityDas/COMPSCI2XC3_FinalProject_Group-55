# Draw_plot.py
import matplotlib.pyplot as plt
import numpy as np

def draw_plot(data_dict, experiment):
    fig, ax = plt.subplots(figsize=(15, 6))
    num_trials = len(next(iter(data_dict.values())))
    num_datasets = len(data_dict)

    bar_width = 0.8 / num_datasets
    colors = ["red", "blue", "green", "purple"][:num_datasets]

    # Bars for each trial
    for i, (label, runtimes) in enumerate(data_dict.items()):
        x_positions = np.arange(num_trials) + (i * bar_width)
        ax.bar(x_positions, runtimes, color=colors[i], width=bar_width, label=label, alpha=0.7)
        # Average line
        avg_runtime = np.mean(runtimes)
        ax.axhline(avg_runtime, color=colors[i], linestyle="--", linewidth=2, alpha=0.9, label=f"Avg ({label})")

    ax.set_xlabel("Trial Number")
    ax.set_ylabel("Runtime (s)")
    ax.set_title("Comparison of Runtime Performance Across Trials")
    ax.set_xticks(np.arange(num_trials) + (bar_width * (num_datasets - 1) / 2))
    ax.set_xticklabels([f"Trial {i+1}" for i in range(num_trials)], rotation=45)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig(f"{experiment}plot.png")
    plt.show()
