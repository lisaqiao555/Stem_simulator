from simulation import run_simulation
from simulation2 import run_simulation2
import graph
import graph2
import compare_simulation12_graph


if __name__ == "__main__":
    run_simulation()

    df = graph.load_data()
    graph.temperature_line_chart(df)
    graph.error_comparison_chart(df)
    graph.fan_switching_chart(df)
    graph.error_type_distribution_chart(df)

    run_simulation2()

    summary = graph2.load_summary()
    graph2.error_rate_vs_accuracy(summary)
    graph2.error_rate_vs_switching(summary)

    compare_simulation12_graph.mixed_vs_single_comparison()

    print("All simulations and graphs completed.")