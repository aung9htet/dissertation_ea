import numpy as np
from test_cases.onemax import fitness_calculation_onemax, fitness_onemax
from test_cases.twomax import fitness_calculation_twomax, fitness_twomax
from random import choice
import multiprocessing
import sys

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

# fitness calculation
def fitness(x, local_opt, i):
    if i == 0: # for onemax
        return fitness_onemax(x), 0
    
    if i == 1: # for twomax
        termination_condition, local_opt = fitness_twomax(x, local_opt)
        return termination_condition, local_opt

def fitness_calculation(x, i):
    if i == 0: # for onemax
        return fitness_calculation_onemax(x)
    if i == 1:
        return fitness_calculation_twomax(x)

# rls method
def rls(input_data):
    
    # set input data
    n = input_data[0]
    benchmark_func = input_data[1]

    # initialize candidate solution
    current_candidate = unif_initialization(n)
    
    # evaluate f(x)
    local_opt = 0
    termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)
    # set run-time
    run_time = 1
    while (termination_condition == False):
        new_candidate = mutation_operator(current_candidate)
        if (fitness_calculation(new_candidate, benchmark_func) >= fitness_calculation(current_candidate, benchmark_func)):
            current_candidate = new_candidate
        termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)
        run_time += 1
    return run_time

# get data ready to be input into the multiprocessing function
def process_input_data(n, benchmark_func, repeat):
    data_input = [n, benchmark_func]

    # set the shape of the array
    input_data_lst = np.empty((0,2), int)

    # input data
    for i in range(repeat):
        input_data_lst = np.append(input_data_lst, np.array([data_input]), axis = 0)
    
    return input_data_lst

# rls method single core      
def rls_singlecore(n, benchmark_func, repeat):
    result = 0
    prepare_data = [n, benchmark_func]
    for i in range(repeat):
        result += rls(prepare_data)
    result /= repeat
    return result

# rls method multi core
def rls_multiprocessing(n, benchmark_func, repeat, core = 6):
    result = 0

    # multiprocess the results
    pool = multiprocessing.Pool(core)
    prepare_data = process_input_data(n, benchmark_func, repeat)
    with pool as p:
        resultList = pool.map(rls, prepare_data)

    # process list of results obtained
    for i in resultList:
        result += i
    result /= repeat
    return result

# save data as npy while working as either multicore or singlecore (for only onemax and twomax)
def get_data(max_bit, repeat, benchmark_func = 0, multicore = True):
    sys.stdout.write('The process will go through ' + str(max_bit) + ' bits')
    sys.stdout.flush()
    run_time_lst = np.array([])
    for n in range(5, max_bit+1):
        if multicore == True:
            run_time = rls_multiprocessing(n, benchmark_func, repeat, core = 10)
        else:
            run_time = rls_singlecore(n, benchmark_func, repeat)
        run_time_lst = np.append(run_time_lst, run_time)
        #To check progress
        sys.stdout.write(f"\r{' '*100}\r")
        sys.stdout.flush()
        sys.stdout.write('Currently working on ' + str(n) + 'th' + ' bit out of ' + str(max_bit) + ' bits')
        sys.stdout.flush()
    if benchmark_func == 0:
        file = "results/rls_onemax_results.npy"
    else:
        file = "results/rls_twomax_results.npy"
    data = np.asarray(run_time_lst)
    np.save(file, data)
    
# to run the desired code
if __name__ == "__main__":
    get_data(100, 100)