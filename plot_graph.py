import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

#plot graph depending on the method and benchmark function used
def plot_graph(select_method, select_benchmark):

    test_label = select_method

    # for rls
    if (select_method == "rls"):

        # using onemax
        if (select_benchmark == "onemax"):
            control_y = np.array([])
            y_axis = np.load('results/rls_onemax_results.npy')
            for n in range(5, len(y_axis)+5):
                control_value = np.log(n) * n
                control_y = np.append(control_y, control_value)
            control_label = "nlogn"
            x_axis = np.arange(5, len(y_axis)+5)

        # using twomax
        elif (select_benchmark == "twomax"):
            control_y = np.array([])
            y_axis = np.load('results/rls_twomax_results.npy')
            for n in range(5, len(y_axis)+5):
                control_value = np.log(n) * n
                control_y = np.append(control_y, control_value)
            control_label = "nlogn"
            x_axis = np.arange(5, len(y_axis)+5)

    # for opt ia with static hyper mutation operator
    elif (select_method == "opt_ia"):

        # using onemax
        if (select_benchmark == "onemax"):
            control_y = np.array([])
            y_axis = np.load('results/opt_ia_onemax_results.npy')
            for n in range(5, len(y_axis)+5):
                control_value = np.log(n) * np.square(n)
                control_y = np.append(control_y, control_value)
            control_label = "$n^{2}$logn"
            x_axis = np.arange(5, len(y_axis)+5)

        # using twomax
        elif (select_benchmark == "twomax"):
            control_y = np.array([])
            y_axis = np.load('results/opt_ia_twomax_results.npy')
            for n in range(5, len(y_axis)+5):
                control_value = np.log(n) * n
                control_y = np.append(control_y, control_value)
            control_label = "nlogn"
            x_axis = np.arange(5, len(y_axis)+5)

    # for symmetric mexpoHD
    elif (select_method == "symmetric_mexpoHD"):

        # using onemax
        if (select_benchmark == "onemax"):
            control_y = np.array([])
            y_axis = np.load('results/symmetric_mexpoHD_onemax_results.npy')
            for n in range(5, len(y_axis)+5):
                control_value = np.log(n) * n
                control_y = np.append(control_y, control_value)
            control_label = "nlogn"
            x_axis = np.arange(5, len(y_axis)+5)

        # using twomax
        elif (select_benchmark == "twomax"):
            control_y = np.array([])
            y_axis = np.load('results/symmetric_mexpoHD_twomax_results.npy')
            for n in range(5, len(y_axis)+5):
                control_value = np.log(n) * np.power(n, 3/2)
                control_y = np.append(control_y, control_value)
            control_label = "$n^{3/2}$logn"
            x_axis = np.arange(5, len(y_axis)+5)

    elif (select_method == "ea"):

        # using onemax
        if (select_benchmark == "onemax"):
            control_y = np.array([])
            y_axis = np.load('results/ea_onemax_results.npy')
            for n in range(5, len(y_axis)+5):
                control_value = np.log(n) * n
                control_y = np.append(control_y, control_value)
            control_label = "nlogn"
            x_axis = np.arange(5, len(y_axis)+5)

        # using twomax
        elif (select_benchmark == "twomax"):
            control_y = np.array([])
            y_axis = np.load('results/ea_twomax_results.npy')
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
    plt.figure()
    plot_graph("symmetric_mexpoHD", "onemax")
    plt.figure()
    plot_graph("symmetric_mexpoHD", "twomax")
    plt.figure()
    plot_graph("rls", "onemax")
    plt.figure()
    plot_graph("opt_ia", "onemax")
    plt.figure()
    plot_graph("ea", "onemax")
    