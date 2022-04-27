from cProfile import run
import numpy as np
import import_ipynb
import onemax
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from random import choice
import multiprocessing

#uniformly distributed initialisation
#n = size of the candidate
def unif_initialization(n):
    bit_list = np.random.randint(2, size = n)
    candidate_solution = ''.join(str(bit) for bit in bit_list)
    return candidate_solution

def mutation_operator(candidate):
    n = len(candidate)
    bit_to_flip = np.random.randint(1, n+1)
    new_candidate = candidate[0:bit_to_flip - 1]
    if (candidate[bit_to_flip - 1] == '1'):
        new_candidate += '0'
    else:
        new_candidate += '1'
    if (bit_to_flip < n):
        new_candidate += candidate[bit_to_flip:]
    return new_candidate

def fitness(x, i):
    if i == 0: #for onemax
        return onemax.fitness(x)

def fitness_calculation(x, i):
    if i == 0: #for onemax
        return onemax.fitness_calculation(x)

def rls(n, benchmark_func):
    
    #initialize candidate solution
    current_candidate = unif_initialization(n)
    
    #Evaluate f(x)
    termination_condition = fitness(current_candidate, benchmark_func)
    #set run-time
    run_time = 1
    while (termination_condition == False):
        new_candidate = mutation_operator(current_candidate)
        if (fitness_calculation(new_candidate, benchmark_func) >= fitness_calculation(current_candidate, benchmark_func)):
            current_candidate = new_candidate
        termination_condition = fitness(current_candidate, benchmark_func)
        run_time += 1
    return run_time

#starts from 5 bits until the max_bit
#repeat is the number of time repeated and the average time taken from it will be used
def plot_graph_onemax(max_bit, repeat):
    y_axis = np.array([])
    control_y = np.array([])
    sys.stdout.write('The process will go through ' + str(max_bit) + ' bits')
    sys.stdout.flush()
    for n in range(5,max_bit+6):
        control_value = np.log(n) * n
        control_y = np.append(control_y, control_value)
        run_time = 0
        for i in range(repeat):
            run_time += rls(n, 0)
        run_time = run_time/repeat
        y_axis = np.append(y_axis, run_time)
        #To check progress
        sys.stdout.write(f"\r{' '*100}\r")
        sys.stdout.flush()
        sys.stdout.write('Currently working on ' + '\x1b[7;37;42m' + str(n) + 'th' + '\x1b[0m' + ' bit out of ' + str(max_bit + 5) + ' bits')
        sys.stdout.flush()
    x_axis = np.arange(5,max_bit+6)
    plt.xlabel("number of bits")
    plt.ylabel("run time by number of evaluations")
    plt.plot(x_axis,y_axis, label = "rls")
    plt.plot(x_axis,control_y, label = "nlogn")
    plt.legend()