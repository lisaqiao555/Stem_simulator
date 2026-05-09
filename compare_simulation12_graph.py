import os
import pandas as pd
import matplotlib.pyplot as plt


MIX_DIR = "mix_simulation1_result"
SINGLE_DIR = "single_simulation2_result"

MIX_FILE = os.path.join(MIX_DIR, "cps_sensor_simulation_results.csv")
SUMMARY_FILE = os.path.join(SINGLE_DIR, "simulation2_summary.csv")

OUTPUT_FILE = os.path.join(SINGLE_DIR, "simulation12_mixed_vs_single_comparison.png")


def count_switches(series):
    return int((series != series.shift()).sum() - 1)


def mixed_vs_single_comparison():
    mix_df = pd.read_csv(MIX_FILE)
    summary_df = pd.read_csv(SUMMARY_FILE)

    mix_before = count_switches(mix_df["Fan_Before"])
    mix_after = count_switches(mix_df["Fan_After"])

    high_rate = summary_df[summary_df["Injection_Rate"] == 60]

    categories = ["Mixed", "Noise", "Missing", "Spike"]

    before_values = [mix_before]
    after_values = [mix_after]

    for error_type in ["noise", "missing", "spike"]:
        row = high_rate[high_rate["Error_Type"] == error_type].iloc[0]
        before_values.append(row["Fan_Switch_Before"])
        after_values.append(row["Fan_Switch_After"])

    x = range(len(categories))
    width = 0.35

    plt.figure(figsize=(8, 5))

    plt.bar(
        [i - width / 2 for i in x],
        before_values,
        width=width,
        label="Before Filter"
    )

    plt.bar(
        [i + width / 2 for i in x],
        after_values,
        width=width,
        label="After Filter"
    )

    plt.xticks(x, categories)
    plt.ylabel("Fan Switching Count")
    plt.title("Mixed vs Single Error Impact on System Stability")
    plt.legend()
    plt.grid(axis="y")

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    plt.close()

    print(f"Comparison graph saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    mixed_vs_single_comparison()