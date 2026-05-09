import os
import pandas as pd
import matplotlib.pyplot as plt


OUTPUT_DIR = "mix_simulation1_result"
CSV_FILE = os.path.join(OUTPUT_DIR, "cps_sensor_simulation_results.csv")


def load_data():
    df = pd.read_csv(CSV_FILE)

    df["Raw_Temperature"] = df["Raw_Temperature"].interpolate()
    df["Filtered_Temperature"] = df["Filtered_Temperature"].interpolate()

    return df


def temperature_line_chart(df):
    plt.figure(figsize=(10, 5))

    plt.plot(df["Step"], df["True_Temperature"], label="True Temperature")
    plt.plot(df["Step"], df["Raw_Temperature"], label="Raw Sensor Data")
    plt.plot(df["Step"], df["Filtered_Temperature"], label="Filtered Data")

    plt.axhline(26, linestyle="--", label="Fan ON Threshold (26°C)")
    plt.axhline(24, linestyle="--", label="Fan OFF Threshold (24°C)")

    plt.xlabel("Step")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Comparison Before and After Filtering")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "figure1_temperature_comparison.png"), dpi=300)
    plt.close()


def error_comparison_chart(df):
    df["Raw_Error"] = abs(df["Raw_Temperature"] - df["True_Temperature"])
    df["Filtered_Error"] = abs(df["Filtered_Temperature"] - df["True_Temperature"])

    plt.figure(figsize=(6, 4))
    plt.bar(
        ["Before Filter", "After Filter"],
        [df["Raw_Error"].mean(), df["Filtered_Error"].mean()],
        color=["orange", "green"]
    )

    plt.ylabel("Average Error (°C)")
    plt.title("Average Temperature Error Before and After Filtering")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "figure2_error_comparison.png"), dpi=300)
    plt.close()


def fan_switching_chart(df):
    raw_switch = (df["Fan_Before"] != df["Fan_Before"].shift()).sum() - 1
    filtered_switch = (df["Fan_After"] != df["Fan_After"].shift()).sum() - 1

    plt.figure(figsize=(6, 4))
    plt.bar(
        ["Before Filter", "After Filter"],
        [raw_switch, filtered_switch],
        color=["red", "blue"]
    )

    plt.ylabel("Number of Fan State Changes")
    plt.title("Fan Switching Behaviour Before and After Filtering")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "figure3_fan_switching.png"), dpi=300)
    plt.close()


def error_type_distribution_chart(df):
    error_counts = df["Error_Type"].value_counts()

    plt.figure(figsize=(6, 4))
    plt.bar(
        error_counts.index,
        error_counts.values,
        color=["green", "orange", "purple", "red"][:len(error_counts)]
    )

    plt.xlabel("Error Type")
    plt.ylabel("Count")
    plt.title("Distribution of Simulated Sensor Error Types")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "figure4_error_distribution.png"), dpi=300)
    plt.close()