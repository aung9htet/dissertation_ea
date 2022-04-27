import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

def plot_graph(select_method, select_benchmark):
    test_label = select_method
    if ((select_method == "rls") and (select_benchmark == "onemax")):
        control_y = np.array([])
        y_axis = np.load('results/rls_onemax_results.npy')
        for n in range(5, len(y_axis)+5):
            control_value = np.log(n) * n
            control_y = np.append(control_y, control_value)
        control_label = "nlogn"
        x_axis = np.arange(5, len(y_axis)+5)
    plt.xlabel("number of bits")
    plt.ylabel("run time by number of evaluations")
    plt.plot(x_axis,y_axis, label = test_label)
    plt.plot(x_axis,control_y, label = control_label)
    plt.legend()
    file = "plotted_results/"
    file += select_method + "_" + select_benchmark
    plt.savefig(file, dpi=300, bbox_inches = "tight")

if __name__ == "__main__":
    plot_graph("rls", "onemax")
    