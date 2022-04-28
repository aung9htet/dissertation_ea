import numpy as np
from test_cases.onemax import fitness_calculation_onemax, fitness_onemax
from test_cases.twomax import fitness_calculation_twomax, fitness_twomax
from random import choice
import multiprocessing
import sys

# select the n-th bit to flip
def flip_bit(candidate, n):
    new_candidate = candidate[:n]
    if candidate[n] == '0':
        new_candidate += '1'
    else:
        new_candidate += '0'
    new_candidate += candidate[n+1:]
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

# uniformly distributed initialisation
# n = size of the candidate
def unif_initialization(n):
    bit_list = np.random.randint(2, size = n)
    candidate_solution = ''.join(str(bit) for bit in bit_list)
    return candidate_solution

# flips at most Cn bits
def mutation_operator(candidate, c, benchmark_func, run_time):
    n = len(candidate)
    # decide number of bit flips
    if c > 1:
        max_number_flip = n
    else:
        max_number_flip = int(np.ceil(c * n))
    new_candidate = candidate
    count_flip = 0
    continue_flipping = True
    flipped_bit = np.array([])
    # continue mutating if there is no improvements
    while continue_flipping:
        select_bit = choice([i for i in range(0,n) if i not in flipped_bit])
        flipped_bit = np.append(flipped_bit, select_bit)
        count_flip += 1
        new_candidate = flip_bit(new_candidate, select_bit)
        if fitness_calculation(new_candidate, benchmark_func) > fitness_calculation(candidate, benchmark_func):
            continue_flipping = False
        if count_flip >= max_number_flip:
            continue_flipping = False
        run_time += 1
    return new_candidate, run_time

# opt ia with static hypermutation operator
def opt_ia(input_data):

    # set input data
    n = input_data[0]
    c = input_data[1]
    benchmark_func = input_data[2]

    # initialize candidate solution
    current_candidate = unif_initialization(n)
    
    # evaluate f(x)
    local_opt = 0
    termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)

    # set run time
    run_time = 1
    while (termination_condition == False):
        new_candidate, run_time = mutation_operator(current_candidate, c, benchmark_func, run_time)
        if (fitness_calculation(new_candidate, benchmark_func) >= fitness_calculation(current_candidate, benchmark_func)):
            current_candidate = new_candidate
        termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)
    return run_time

# get data ready to be input into the multiprocessing function
def process_input_data(n, c, benchmark_func, repeat):
    data_input = [n, c, benchmark_func]

    # set the shape of the array
    input_data_lst = np.empty((0,3), int)

    # input data
    for i in range(repeat):
        input_data_lst = np.append(input_data_lst, np.array([data_input]), axis = 0)
    
    return input_data_lst

# opt ia method single core      
def opt_ia_singlecore(n, c, benchmark_func, repeat):
    result = 0
    prepare_data = [n, c, benchmark_func]
    for i in range(repeat):
        result += opt_ia(prepare_data)
    result /= repeat
    return result

# opt ia method multi core
def opt_ia_multiprocessing(n, c, benchmark_func, repeat, core = 6):
    result = 0

    # multiprocess the results
    prepare_data = process_input_data(n, c, benchmark_func, repeat)
    with multiprocessing.Pool(core) as pool:
        resultList = pool.map(opt_ia, prepare_data)
    
    # process list of results obtained
    for i in resultList:
        result += i
    result /= repeat
    return result

# save data as npy while working as either multicore or singlecore (for only onemax and twomax)
def get_data(max_bit, c, repeat, benchmark_func = 0, multicore = True):
    sys.stdout.write('The process will go through ' + str(max_bit) + ' bits')
    sys.stdout.flush()
    run_time_lst = np.array([])
    for n in range(5, max_bit+1):
        if multicore == True:
            run_time = opt_ia_multiprocessing(n, c, benchmark_func, repeat, core = 10)
        else:
            run_time = opt_ia_singlecore(n, c, benchmark_func, repeat)
        run_time_lst = np.append(run_time_lst, run_time)
        #To check progress
        sys.stdout.write(f"\r{' '*100}\r")
        sys.stdout.flush()
        sys.stdout.write('Currently working on ' + str(n) + 'th' + ' bit out of ' + str(max_bit) + ' bits')
        sys.stdout.flush()
    if benchmark_func == 0:
        file = "results/opt_ia_onemax_results.npy"
    else:
        file = "results/opt_ia_twomax_results.npy"
    data = np.asarray(run_time_lst)
    np.save(file, data)

# to run the desired code
if __name__ == "__main__":
    get_data(50, 1, 100)