import os
import random
import pandas as pd

from sensors import true_temperature
from filter import moving_average_filter
from controller import fan_control
from config import SIMULATION_STEPS


OUTPUT_DIR = "single_simulation2_result"
RATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
ERROR_TYPES = ["noise", "missing", "spike"]


def inject_single_error(value, error_type, rate):
    if random.random() > rate:
        return value, "normal"

    if error_type == "noise":
        return round(value + random.uniform(-1.5, 1.5), 2), "noise"

    if error_type == "missing":
        return None, "missing"

    if error_type == "spike":
        return round(value + random.choice([-1, 1]) * random.uniform(3, 5), 2), "spike"

    return value, "normal"


def count_switches(series):
    return int((series != series.shift()).sum() - 1)


def run_one_case(error_type, rate):
    rows = []
    raw_values = []

    for step in range(1, SIMULATION_STEPS + 1):
        true_temp = true_temperature(step)
        raw_temp, actual_error = inject_single_error(true_temp, error_type, rate)

        raw_values.append(raw_temp)

        rows.append({
            "Step": step,
            "Injection_Rate": int(rate * 100),
            "Target_Error_Type": error_type,
            "True_Temperature": true_temp,
            "Raw_Temperature": raw_temp,
            "Actual_Error": actual_error
        })

    filtered_values = moving_average_filter(raw_values)

    raw_state = "OFF"
    filtered_state = "OFF"

    for i, row in enumerate(rows):
        raw_state = fan_control(row["Raw_Temperature"], raw_state)
        filtered_state = fan_control(filtered_values[i], filtered_state)

        row["Filtered_Temperature"] = filtered_values[i]
        row["Fan_Before"] = raw_state
        row["Fan_After"] = filtered_state

    df = pd.DataFrame(rows)

    df["Raw_Error"] = abs(df["Raw_Temperature"] - df["True_Temperature"])
    df["Filtered_Error"] = abs(df["Filtered_Temperature"] - df["True_Temperature"])

    return df


def run_simulation2():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    random.seed(42)

    summary_rows = []

    for error_type in ERROR_TYPES:
        excel_file = os.path.join(OUTPUT_DIR, f"simulation2_{error_type}.xlsx")

        with pd.ExcelWriter(excel_file) as writer:
            for rate in RATES:
                df = run_one_case(error_type, rate)

                sheet_name = f"Rate_{int(rate * 100)}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                summary_rows.append({
                    "Error_Type": error_type,
                    "Injection_Rate": int(rate * 100),
                    "Average_Raw_Error": round(df["Raw_Error"].mean(), 3),
                    "Average_Filtered_Error": round(df["Filtered_Error"].mean(), 3),
                    "Fan_Switch_Before": count_switches(df["Fan_Before"]),
                    "Fan_Switch_After": count_switches(df["Fan_After"]),
                    "Injected_Error_Count": int((df["Actual_Error"] == error_type).sum())
                })

        print(f"Saved {excel_file}")

    summary_df = pd.DataFrame(summary_rows)
    summary_file = os.path.join(OUTPUT_DIR, "simulation2_summary.csv")
    summary_df.to_csv(summary_file, index=False)

    print(f"Simulation 2 complete. Summary saved to {summary_file}")