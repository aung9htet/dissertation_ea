# dissertation_ea

## Running the results

In the folder, the results can be replicated for each algorithm respectively in:
* symmetric_mexpohd_multiprocessing.py
* rls_multiprocessing.py
* ea_multiprocessing.py
* opt_ia_multiprocessing.py
To work on different version of the benchmark function, the get_data() function can be called/modified in the main function. A description of what the variables will do will be provided below:
* max_bit: meant to be used for onemax and twomax. It decides how many iterations of bit it will run. The bit will start from 5 and increase by increments of 1.
* c: this can be found as a constant for opt_ia, where c is the mutation potential of cn, and symmetric_mexpohd, where c is the age threshold of cnlogn.
* repeat: the number of times the algorithm will be repeated over.
* compare: a list of c will be made where results will be reproduced for comparison
* max_runtime: the maximum run-time allowed before the algorithm will be terminated
* benchmark_func: 0 is for onemax, 1 is for twomax, 2 is for maxsat
* multicore: if true will make use of multicore processing(currently set to 10 worker nodes), if false will use a single core for processing the result(ideal for short runs where the IPC may lower speed.
* cnf_file: 0 is for uf75 and 1 is for uf250

In the folder, the results can be plotted by the use of plot_graph.py. The main function can have the plot_graph() modified to plot different graphs where the variable will define as follows:
* select_method: able to choose between "rls", "symmetric_mexpoHD", "opt_ia" and "ea"
* select_benchmark: able to choose between "onemax", "twomax", "uf75", "uf75_fitness", "uf250" and "uf250_fitness"
* plot_later: if true will save the graph or plotting later, if false will plot the graph after the method finishes running.

In the folder, the wilcoxon_test_results.py can be run for obtaining the statistical analysis of the results comparison between the Symmetric MexpoHD and the other algorithms.
