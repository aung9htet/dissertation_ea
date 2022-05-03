import numpy as np
from test_cases.onemax import fitness_calculation_onemax, fitness_onemax
from test_cases.twomax import fitness_calculation_twomax, fitness_twomax
from test_cases.maxsat import fitness_calculation_maxsat, fitness_maxsat
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

# termination for maxsat is dependent on the number runs and thus is represented as shown
def terminate_maxsat(run_time):
    # number of runs is set at 40000 as discussed with Dr Pietro Oliveto
    if run_time >= 100000:
        return True
    else:
        return False

# cnf file is to choose from uf75 and uf250 while cnf index is to chose which test cases of the 100 instances that will be used
def check_optimum_maxsat(x, cnf_file, cnf_index):
    file = 'prerequisites/' + cnf_file + '.npy'
    cnf_list = np.load(file)
    cnf = cnf_list[cnf_index]
    check_fitness = fitness_maxsat(x, cnf)
    if check_fitness == True:
        return True

# fitness calculation for max sat
def calculate_fitness_maxsat(x, cnf_file, cnf_index):
    file = 'prerequisites/' + cnf_file + '.npy'
    cnf_list = np.load(file)
    cnf = cnf_list[cnf_index]
    calculate_fitness = fitness_calculation_maxsat(x, cnf)
    return calculate_fitness

# uniformly distributed initialisation
# n = size of the candidate
def unif_initialization(n, cnf_list, cnf_index, initialise_single_candidate = True):
    if cnf_list is not None and initialise_single_candidate is True:
        cnf_files = np.load("prerequisites/" + cnf_list + "_init.npy")
        candidate_solution = cnf_files[cnf_index]
    else:
        bit_list = np.random.randint(2, size = n)
        candidate_solution = ''.join(str(bit) for bit in bit_list)
    return candidate_solution

# flips at most Cn bits
def mutation_operator(candidate, c, benchmark_func, run_time, optimum_found, cnf_list = None, cnf_index = None, run_times = None, optimums_found = None):
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
        if benchmark_func == 2:
            new_fitness_candidate = calculate_fitness_maxsat(new_candidate, cnf_list, cnf_index)
            current_fitness_candidate = calculate_fitness_maxsat(candidate, cnf_list, cnf_index)
        else:
            new_fitness_candidate = fitness_calculation(new_candidate, benchmark_func)
            current_fitness_candidate = fitness_calculation(candidate, benchmark_func)
        if new_fitness_candidate > current_fitness_candidate:
            continue_flipping = False
        if count_flip >= max_number_flip:
            continue_flipping = False
        run_time += 1
        if terminate_maxsat(run_time) == True:
            continue_flipping = False
        if benchmark_func == 2:
            run_times = np.append(run_times, run_time)
            optimums_found = np.append(optimums_found, optimum_found)
            sys.stdout.write(f"\r{' '*100}\r")
            sys.stdout.flush()
            sys.stdout.write('Currently working on ' + str(run_time) + ' out of 100,000 runtime for ' +  str(cnf_index + 1) + 'th file out of ' + str(100) + ' files\n')
            sys.stdout.flush()
    if benchmark_func == 2:
        return new_candidate, run_times, optimums_found, run_time, optimum_found
    else:
        return new_candidate, run_time

# opt ia with static hypermutation operator
def opt_ia(input_data):

    # set input data
    n = input_data[0]
    c = input_data[1]
    benchmark_func = input_data[2]
    optimum_found = 0
    run_time = 1
    cnf_list = None
    cnf_index = None

    # required variables for maxsat
    if benchmark_func == 2:
        optimum_list = []
        run_times = np.array([run_time])
        optimums_found = np.array([optimum_found])
        cnf_file = input_data[3]
        cnf_index = input_data[4]
        sys.stdout.write(f"\r{' '*100}\r")
        sys.stdout.flush()
        sys.stdout.write('Currently working on ' + str(cnf_index) + 'th file out of ' + str(100) + ' files')
        sys.stdout.flush()
        if cnf_file == 0:
            cnf_list = "uf75"
        else:
            cnf_list = "uf250"

    # initialize candidate solution
    current_candidate = unif_initialization(n, cnf_list, cnf_index)
    
    # evaluate f(x)
    if benchmark_func == 2:
        termination_condition = terminate_maxsat(run_time)
        check_fitness = check_optimum_maxsat(current_candidate, cnf_list, cnf_index)
        if check_fitness == True:
            if not current_candidate in optimum_list:
                optimum_found += 1
                optimum_list.append(current_candidate)
    else:
        local_opt = 0
        termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)

    while (termination_condition == False):
        if benchmark_func == 2:
            new_candidate, run_times, optimums_found, run_time, optimum_found = mutation_operator(current_candidate, c, benchmark_func, run_time, optimum_found, cnf_list, cnf_index, run_times, optimums_found)
            new_fitness_candidate = calculate_fitness_maxsat(new_candidate, cnf_list, cnf_index)
            current_fitness_candidate = calculate_fitness_maxsat(current_candidate, cnf_list, cnf_index)
        else:
            new_candidate, run_time = mutation_operator(current_candidate, c, benchmark_func, run_time, optimum_found)
            new_fitness_candidate = fitness_calculation(new_candidate, benchmark_func)
            current_fitness_candidate = fitness_calculation(current_candidate, benchmark_func)
        
        # check fitness of new candidates
        if new_fitness_candidate >= current_fitness_candidate:
            current_candidate = new_candidate

        # check termination condition
        if benchmark_func == 2:
            termination_condition = terminate_maxsat(run_time)
            check_fitness = check_optimum_maxsat(current_candidate, cnf_list, cnf_index)
            if check_fitness == True:
                if not current_candidate in optimum_list:
                    optimum_found += 1
                    optimum_list.append(current_candidate)
        else:
            termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)
    if benchmark_func == 2:
        return run_times, optimums_found
    else:
        return run_time

# get data ready to be input into the multiprocessing function
def process_input_data(n, c, benchmark_func, repeat, cnf_file = 0):

    # return array depends on maxsat or not
    if benchmark_func == 2:
        if cnf_file == 0:
            cnf = 'uf75'
        else:
            cnf = 'uf250'
        file = 'prerequisites/' + cnf + '.npy'
        cnf_list = np.load(file)
        
        # set the shape of the array
        input_data_lst = np.empty((0,5), int)
        
        for i in range(repeat):
            for index in range(len(cnf_list)):
                data_input = [n, c, benchmark_func, cnf_file, index]
                for j in range(repeat):
                    input_data_lst = np.append(input_data_lst, np.array([data_input]), axis = 0)
    else:
        data_input = [n, c, benchmark_func]

        # set the shape of the array
        input_data_lst = np.empty((0,3), int)

        # input data
        for i in range(repeat):
            input_data_lst = np.append(input_data_lst, np.array([data_input]), axis = 0)
        
    return input_data_lst

# opt ia method single core      
def opt_ia_singlecore(n, c, benchmark_func, repeat, max_runtime = 1000, cnf_file = 0):
    result = 0
    if benchmark_func == 2:
        prepare_data = process_input_data(n, c, benchmark_func, repeat, cnf_file = 0)

        # max size is 1000 by default
        optimum_total = np.zeros(max_runtime)
        for i in prepare_data:
            run_times, optimum = opt_ia(i)
            optimum_size = len(optimum)
            # add to all behind if best solution is found since best solution would be less than expected
            if optimum_size < max_runtime:
                while (optimum_size < max_runtime):
                    optimum = np.append(optimum, optimum[optimum_size - 1])

            optimum_total = np.add(optimum_total, optimum)
        return run_times[:max_runtime], optimum_total[:max_runtime]
    else:
        prepare_data = process_input_data(n, c, benchmark_func, repeat)
        for i in prepare_data:
            result += opt_ia(i)
        result /= repeat
        return result

# opt ia method multi core
def opt_ia_multiprocessing(n, c, benchmark_func, repeat, max_runtime = 1000, core = 6, cnf_file = 0):
    result = 0

    # multiprocess the results
    if benchmark_func == 2:
        prepare_data = process_input_data(n, c, benchmark_func, repeat, cnf_file)
    else:
        prepare_data = process_input_data(n, c, benchmark_func, repeat)
    with multiprocessing.Pool(core) as pool:
        resultList = pool.map(opt_ia, prepare_data)
    sys.stdout.flush()
    sys.stdout.write('Completed calculating results. Now processing...')
    sys.stdout.flush()

    # process list of results obtained
    if benchmark_func == 2:
        optimum_total = np.zeros(max_runtime)
        for i in resultList:
            run_times, optimum =  i
            optimum_size = len(optimum)

            # add to all behind if best solution is found since best solution would be less than expected
            if optimum_size < max_runtime:
                optimum_fill = np.empty(max_runtime - (optimum_size))
                optimum_fill.fill(optimum[optimum_size - 1])
                optimum = np.append(optimum, optimum_fill)

            optimum_total = np.add(optimum_total, optimum[:max_runtime])
        sys.stdout.write('Results processed.')
        sys.stdout.flush()
        return run_times[:max_runtime], optimum_total[:max_runtime]
    else:
        for i in resultList:
            result += i
        result /= repeat
        return result

# save data as npy while working as either multicore or singlecore (for only onemax and twomax)
def get_data(max_bit, c, repeat, benchmark_func = 0, multicore = True, cnf_file = 0):
    run_time_lst = np.array([])
    if benchmark_func == 2:
        sys.stdout.write('The process will work on maxsat')
        sys.stdout.flush()
        if cnf_file == 0:
            n = 75
            text = 'uf75'
        else:
            n = 250
            text = 'uf250'
        if multicore == True:
            run_times, optimum_total = opt_ia_multiprocessing(n, c, benchmark_func, repeat, max_runtime = 100000, core = 10, cnf_file = cnf_file)
        else:
            run_times, optimum_total = opt_ia_singlecore(n, c, benchmark_func, repeat, max_runtime = 100000, cnf_file = cnf_file)
        # save run times
        sys.stdout.write('Saving results')
        sys.stdout.flush()
        run_time_file = "results/opt_ia_" + text + "_run_time_list.npy"
        data = np.asarray(run_times)
        np.save(run_time_file, data)
        # save optimum per run time list
        optimum_file = "results/opt_ia_" + text + "_optimum_list.npy"
        data = np.asarray(optimum_total)
        np.save(optimum_file, data)
    else:
        sys.stdout.write('The process will go through ' + str(max_bit) + ' bits')
        sys.stdout.flush()
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
    get_data(50, 1, 1, benchmark_func=2)