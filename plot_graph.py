import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

#plot graph depending on the method and benchmark function used
def plot_graph(select_method, select_benchmark, plot_later = False):

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
        
        elif (select_benchmark == "uf75"):
            y_axis = np.load('results/rls_uf75_optimum_list.npy')
            x_axis = np.load('results/rls_uf75_run_time_list.npy')

        elif (select_benchmark == "uf250"):
            y_axis = np.load('results/rls_uf250_optimum_list.npy')
            x_axis = np.load('results/rls_uf250_run_time_list.npy')
        
        elif (select_benchmark == "uf75_fitness"):
            y_axis = np.load('results/rls_uf75_best_fitness_list.npy')[1:]
            x_axis = np.load('results/rls_uf75_run_time_list.npy')[1:]

        elif (select_benchmark == "uf250_fitness"):
            y_axis = np.load('results/rls_uf250_best_fitness_list.npy')
            x_axis = np.load('results/rls_uf250_run_time_list.npy')

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

        elif (select_benchmark == "uf75"):
            y_axis = np.load('results/opt_ia_uf75_optimum_list.npy')
            x_axis = np.load('results/opt_ia_uf75_run_time_list.npy')

        elif (select_benchmark == "uf250"):
            y_axis = np.load('results/opt_ia_uf250_optimum_list.npy')
            x_axis = np.load('results/opt_ia_uf250_run_time_list.npy')

        elif (select_benchmark == "uf75_fitness"):
            y_axis = np.load('results/opt_ia_uf75_best_fitness_list.npy')[1:]
            x_axis = np.load('results/opt_ia_uf75_run_time_list.npy')[1:]

        elif (select_benchmark == "uf250_fitness"):
            y_axis = np.load('results/opt_ia_uf250_best_fitness_list.npy')
            x_axis = np.load('results/opt_ia_uf250_run_time_list.npy')

        elif (select_benchmark == "uf75_fitness"):
            y_axis = np.load('results/opt_ia_uf75_best_fitness_list.npy')[1:]
            x_axis = np.load('results/opt_ia_uf75_run_time_list.npy')[1:]

        elif (select_benchmark == "uf250_fitness"):
            y_axis = np.load('results/opt_ia_uf250_best_fitness_list.npy')
            x_axis = np.load('results/opt_ia_uf250_run_time_list.npy')

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
        
        elif (select_benchmark == "uf75"):
            y_axis = np.load('results/symmetric_mexpoHD_uf75_optimum_list.npy')
            x_axis = np.load('results/symmetric_mexpoHD_uf75_run_time_list.npy')

        elif (select_benchmark == "uf250"):
            y_axis = np.load('results/symmetric_mexpoHD_uf250_optimum_list.npy')
            x_axis = np.load('results/symmetric_mexpoHD_uf250_run_time_list.npy')

        elif (select_benchmark == "uf75_fitness"):
            y_axis = np.load('results/symmetric_mexpoHD_uf75_best_fitness_list.npy')[1:]
            x_axis = np.load('results/symmetric_mexpoHD_uf75_run_time_list.npy')[1:]

        elif (select_benchmark == "uf250_fitness"):
            y_axis = np.load('results/symmetric_mexpoHD_uf250_best_fitness_list.npy')
            x_axis = np.load('results/symmetric_mexpoHD_uf250_run_time_list.npy')

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
        
        elif (select_benchmark == "uf75"):
            y_axis = np.load('results/ea_uf75_optimum_list.npy')
            x_axis = np.load('results/ea_uf75_run_time_list.npy')

        elif (select_benchmark == "uf250"):
            y_axis = np.load('results/ea_uf250_optimum_list.npy')
            x_axis = np.load('results/ea_uf250_run_time_list.npy')

        elif (select_benchmark == "uf75_fitness"):
            y_axis = np.load('results/ea_uf75_best_fitness_list.npy')[1:]
            x_axis = np.load('results/ea_uf75_run_time_list.npy')[1:]

        elif (select_benchmark == "uf250_fitness"):
            y_axis = np.load('results/ea_uf250_best_fitness_list.npy')
            x_axis = np.load('results/ea_uf250_run_time_list.npy')

    if (select_benchmark == "uf75") or (select_benchmark == "uf250") or (select_benchmark == "uf75_fitness") or (select_benchmark == "uf250_fitness"):
        plt.xlabel("run time")
        plt.ylabel("optimum found")
        x_axis = np.log10(x_axis)
        plt.plot(x_axis, y_axis, label = select_method)
        plt.legend
    else:
        plt.xlabel("number of bits")
        plt.ylabel("run time by number of evaluations")
        plt.plot(x_axis,y_axis, label = test_label)
        plt.plot(x_axis,control_y, label = control_label)
        plt.legend()
    if plot_later == False:
        file = "plotted_results/"
        file += select_method + "_" + select_benchmark
        plt.savefig(file, dpi=300, bbox_inches = "tight")

if __name__ == "__main__":
    # One max plot
    plt.figure()
    plot_graph("symmetric_mexpoHD", "onemax")
    plt.figure()
    plot_graph("rls", "onemax")
    plt.figure()
    plot_graph("opt_ia", "onemax")
    plt.figure()
    plot_graph("ea", "onemax")
    plt.figure()
    # Two max plot
    plot_graph("symmetric_mexpoHD", "twomax")
    plt.figure()
    # UF75 optimum found plot
    plot_graph("rls", "uf75")
    plt.figure()
    plot_graph("opt_ia", "uf75")
    plt.figure()
    plot_graph("ea", "uf75")
    plt.figure()
    plot_graph("symmetric_mexpoHD", "uf75")
    plt.figure()
    # UF75 fitness plot
    plot_graph("ea", "uf75_fitness")
    plt.figure()
    plot_graph("opt_ia", "uf75_fitness")
    plt.figure()
    plot_graph("rls", "uf75_fitness")
    plt.figure()
    plot_graph("symmetric_mexpoHD", "uf75_fitness")
    plt.figure()
    # UF75 optimum combined plot
    plot_graph("rls", "uf75", plot_later=True)
    plot_graph("opt_ia", "uf75", plot_later=True)
    plot_graph("ea", "uf75", plot_later=True)
    plot_graph("symmetric_mexpoHD", "uf75", plot_later=True)
    plt.legend()
    file = "plotted_results/combined_results"
    plt.savefig(file, dpi=300, bbox_inches = "tight")
    # UF75 best_fitness combined plot
    plt.figure()
    plot_graph("rls", "uf75_fitness", plot_later=True)
    plot_graph("opt_ia", "uf75_fitness", plot_later=True)
    plot_graph("ea", "uf75_fitness", plot_later=True)
    plot_graph("symmetric_mexpoHD", "uf75_fitness", plot_later=True)
    plt.legend()
    file = "plotted_results/combined_fitness_results"
    plt.savefig(file, dpi=300, bbox_inches = "tight")