import numpy as np
from test_cases.onemax import fitness_calculation_onemax, fitness_onemax
from test_cases.twomax import fitness_calculation_twomax, fitness_twomax
from random import choice
import multiprocessing
import sys

# uniformly distributed initialisation
# n = size of the candidate
def unif_initialization(n):
    bit_list = np.random.randint(2, size = n)
    candidate_solution = ''.join(str(bit) for bit in bit_list)
    return candidate_solution

# mutation operator
def unif_mutation(candidate, benchmark_func, run_time, mutation_potential = 0):
    
    # will be used to check if there is constructive mutation or the number of bit mutation has reached mutation potential
    bit_change_condition = True
    
    # candidate used to check for constructive mutation
    set_candidate = candidate
    
    # to add the flipped bits
    flipped_bit = np.array([])
    while bit_change_condition == True:
        
        # select bit to flip
        bit_change = choice([i for i in range(0,len(candidate)) if i not in flipped_bit])
        flipped_bit = np.append(flipped_bit, bit_change)
        
        # create new candidate to be used
        new_candidate = set_candidate[:bit_change]
        if set_candidate[bit_change] == "0":
            new_candidate += "1"
        else:
            new_candidate += "0"
        new_candidate += set_candidate[bit_change + 1:]
        set_candidate = new_candidate
        
        # compare results
        if fitness_calculation(new_candidate, benchmark_func) > fitness_calculation(candidate, benchmark_func):
            bit_change_condition = False
        if (hamming_distance(new_candidate, candidate) >= mutation_potential):
            bit_change_condition = False
        # add run-time after checking fitness
        run_time += 1
    return new_candidate, run_time

# hamming distance calculation
def hamming_distance(candidate1, candidate2):
    i = 0
    hd = 0
    for char1 in list(candidate1):
        if (char1 != candidate2[i]):
            hd += 1
        i += 1
    return hd

# mutation potential
def symmetric_MexpoHD(n, x, x_origin, best):
    power_numerator = hamming_distance(x, x_origin)
    power_denominator = np.maximum(hamming_distance(best, x_origin), 1)
    power_value = -(power_numerator/power_denominator)
    m1 = np.power(n, power_value)
    m = int(np.ceil(n*m1))
    return m

# decide whether to reset the algorithm or not
def decide_eliminate_candidate(probabilty_to_eliminate):
    p_die = np.random.random_sample()
    result = False
    if p_die > probabilty_to_eliminate:
        result = True
    return result

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

# the benchmark func has the following meaning. 0 is for onemax and 1 for twomax.
# this can also be updated in the fitness and fitness_calculation method to add on more benchmark functions.
def immune_algorithm(input_data):
    
    # set input data
    n = input_data[0]
    C = input_data[1]
    benchmark_func = input_data[2]

    age_threshold = n * np.log(n) * C
    # initialize x
    intialized_candidate = unif_initialization(n)
    x = (intialized_candidate, intialized_candidate, 0); best = x[0]
    y = (intialized_candidate, intialized_candidate, 0)
    # tuple order = (x, origin, age)
    
    # evaluate f(x)
    local_opt = 0
    termination_condition, local_opt = fitness(best, local_opt, benchmark_func)

    # set run time
    run_time = 1
    while (termination_condition == False):
        
        # add age
        x_age = x[2] + 1
        x = (x[0], x[1], x_age)
        
        # mutate x to y and set origin for y
        M = symmetric_MexpoHD(n, x[0], x[1], best)
        mutation_x, run_time = unif_mutation(x[0], benchmark_func, run_time, mutation_potential = M)
        
        # set y.origin = x.origin
        y = (mutation_x, x[1], y[2])
        
        # check fitness between y and x
        if (fitness_calculation(y[0], benchmark_func) > fitness_calculation(x[0], benchmark_func)):
            # set y.age = 0
            y = (y[0], y[1], 0)
            # check best solution
            if (fitness_calculation(y[0], benchmark_func) >= fitness_calculation(best, benchmark_func)):
                # set best solution
                best = y[0]
                termination_condition, local_opt = fitness(best, local_opt, benchmark_func)
        else:
            # set y age as x age 
            y = (y[0], y[1], x[2])
        
        # aging mechanism for x and y
        collection_candidates = [x,y]
        for candidate in collection_candidates:
            # check for age threshold and probability to die set at 0.5
            if ((candidate[2] > age_threshold) and (decide_eliminate_candidate(0.5) == True)):
                # reset the candidate and their age
                reset_candidate = unif_initialization(n) # reinitialize
                x = (reset_candidate, x[0], 0) 
                y = (reset_candidate, y[0], 0)
                
        # best solution selection
        if (fitness_calculation(x[0], benchmark_func) < fitness_calculation(y[0], benchmark_func)):
            x = (y[0], x[1], x[2])
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

# symmetric mexpoHD method single core      
def symmetric_mexpoHD_singlecore(n, c, benchmark_func, repeat):
    result = 0
    prepare_data = [n, c, benchmark_func]
    for i in range(repeat):
        result += immune_algorithm(prepare_data)
    result /= repeat
    return result

# symmetric mexpoHD method multi core
def symmetric_mexpoHD_multiprocessing(n, c, benchmark_func, repeat, core = 6):
    result = 0

    # multiprocess the results
    pool = multiprocessing.Pool(core)
    prepare_data = process_input_data(n, c, benchmark_func, repeat)
    with pool as p:
        resultList = pool.map(immune_algorithm, prepare_data)
    
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
            run_time = symmetric_mexpoHD_multiprocessing(n, c, benchmark_func, repeat, core = 10)
        else:
            run_time = symmetric_mexpoHD_singlecore(n, c, benchmark_func, repeat)
        run_time_lst = np.append(run_time_lst, run_time)
        #To check progress
        sys.stdout.write(f"\r{' '*100}\r")
        sys.stdout.flush()
        sys.stdout.write('Currently working on ' + str(n) + 'th' + ' bit out of ' + str(max_bit) + ' bits')
        sys.stdout.flush()
    if benchmark_func == 0:
        file = "results/symmetric_mexpoHD_onemax_results.npy"
    else:
        file = "results/symmetric_mexpoHD_twomax_results.npy"
    data = np.asarray(run_time_lst)
    np.save(file, data)

# to run the desired code
if __name__ == "__main__":
    get_data(40, 1, 100)