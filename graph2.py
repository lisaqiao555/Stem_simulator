import os
import pandas as pd
import matplotlib.pyplot as plt


OUTPUT_DIR = "single_simulation2_result"
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "simulation2_summary.csv")


def load_summary():
    return pd.read_csv(SUMMARY_FILE)


def error_rate_vs_accuracy(df):
    plt.figure(figsize=(9, 5))

    for error_type in df["Error_Type"].unique():
        sub = df[df["Error_Type"] == error_type]

        plt.plot(
            sub["Injection_Rate"],
            sub["Average_Raw_Error"],
            marker="o",
            linewidth=2,
            label=f"{error_type} before filter"
        )

        plt.plot(
            sub["Injection_Rate"],
            sub["Average_Filtered_Error"],
            marker="s",
            linestyle="--",
            linewidth=2,
            label=f"{error_type} after filter"
        )

    plt.xlabel("Injection Rate (%)")
    plt.ylabel("Average Temperature Error (°C)")
    plt.title("Impact of Error Injection Rate on Temperature Accuracy")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(
        os.path.join(OUTPUT_DIR, "simulation2_accuracy_impact.png"),
        dpi=300
    )
    plt.close()


def error_rate_vs_switching(df):
    plt.figure(figsize=(9, 5))

    for error_type in df["Error_Type"].unique():
        sub = df[df["Error_Type"] == error_type]

        plt.plot(
            sub["Injection_Rate"],
            sub["Fan_Switch_Before"],
            marker="o",
            linewidth=2,
            label=f"{error_type} before filter"
        )

        plt.plot(
            sub["Injection_Rate"],
            sub["Fan_Switch_After"],
            marker="s",
            linestyle="--",
            linewidth=2,
            label=f"{error_type} after filter"
        )

    plt.xlabel("Injection Rate (%)")
    plt.ylabel("Fan Switching Count")
    plt.title("Impact of Error Injection Rate on System Stability")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(
        os.path.join(OUTPUT_DIR, "simulation2_switching_impact.png"),
        dpi=300
    )
    plt.close()