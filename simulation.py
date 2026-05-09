import os
import pandas as pd

from sensors import true_temperature
from errors import inject_error
from filter import moving_average_filter
from controller import fan_control
from config import SIMULATION_STEPS


OUTPUT_DIR = "mix_simulation1_result"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "cps_sensor_simulation_results.csv")


def run_simulation():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rows = []
    raw_values = []

    for step in range(1, SIMULATION_STEPS + 1):
        true_temp = true_temperature(step)
        raw_temp, error_type = inject_error(true_temp)

        raw_values.append(raw_temp)

        rows.append({
            "Step": step,
            "True_Temperature": true_temp,
            "Raw_Temperature": raw_temp,
            "Error_Type": error_type
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
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Simulation 1 complete. Saved to {OUTPUT_FILE}")