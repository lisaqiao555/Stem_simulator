from simulation import run_simulation
import graph

if __name__ == "__main__":
    run_simulation()

    df = graph.load_data()

    graph.temperature_line_chart(df)
    graph.error_comparison_chart(df)
    graph.fan_switching_chart(df)
    graph.error_type_distribution_chart(df)

    print("Simulation and graphs completed.")