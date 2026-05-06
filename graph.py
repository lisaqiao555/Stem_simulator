import pandas as pd
import matplotlib.pyplot as plt


CSV_FILE = "cps_sensor_simulation_results.csv"


def load_data():
    df = pd.read_csv(CSV_FILE)

    # fill missing values for plotting only
    df["Raw_Temperature"] = df["Raw_Temperature"].interpolate()
    df["Filtered_Temperature"] = df["Filtered_Temperature"].interpolate()

    return df


# -----------------------------
# Figure 1: Temperature Line Chart
# -----------------------------
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
    plt.savefig("figure1_temperature_comparison.png", dpi=300)
    plt.close()


# -----------------------------
# Figure 2: Error Comparison
# Figure 2 compares the average temperature error before and after filtering. 
# The results indicate that the filtering method slightly reduces the deviation between measured and true temperature values, 
# demonstrating limited improvement in accuracy.
# -----------------------------
def error_comparison_chart(df):
    df["Raw_Error"] = abs(df["Raw_Temperature"] - df["True_Temperature"])
    df["Filtered_Error"] = abs(df["Filtered_Temperature"] - df["True_Temperature"])

    plt.figure(figsize=(6, 4))

    plt.bar(
        ["Before Filter", "After Filter"],
        [df["Raw_Error"].mean(), df["Filtered_Error"].mean()],
        color=["orange", "green"]   # ⭐ different colors
    )

    plt.ylabel("Average Error (°C)")
    plt.title("Average Temperature Error Before and After Filtering")

    plt.tight_layout()
    plt.savefig("figure2_error_comparison.png", dpi=300)
    plt.close()


# -----------------------------
# Figure 3: Fan Switching from on->off
# Figure 3 illustrates the number of fan state changes before and after filtering. 
# The results show that filtering significantly reduces switching frequency, 
# indicating improved system stability and reduced oscillatory behaviour.
# -----------------------------
def fan_switching_chart(df):
    raw_switch = (df["Fan_Before"] != df["Fan_Before"].shift()).sum() - 1
    filtered_switch = (df["Fan_After"] != df["Fan_After"].shift()).sum() - 1

    plt.figure(figsize=(6, 4))

    plt.bar(
        ["Before Filter", "After Filter"],
        [raw_switch, filtered_switch],
        color=["red", "blue"]   # ⭐ different colors
    )

    plt.ylabel("Number of Fan State Changes")
    plt.title("Fan Switching Behaviour Before and After Filtering")

    plt.tight_layout()
    plt.savefig("figure3_fan_switching.png", dpi=300)
    plt.close()


# -----------------------------
# Figure 4: Error Distribution
# -----------------------------
def error_type_distribution_chart(df):
    error_counts = df["Error_Type"].value_counts()

    plt.figure(figsize=(6, 4))

    colors = ["green", "orange", "purple", "red"]  # ⭐ multiple colors

    plt.bar(error_counts.index, error_counts.values, color=colors[:len(error_counts)])

    plt.xlabel("Error Type")
    plt.ylabel("Count")
    plt.title("Distribution of Simulated Sensor Error Types")

    plt.tight_layout()
    plt.savefig("figure4_error_distribution.png", dpi=300)
    plt.close()