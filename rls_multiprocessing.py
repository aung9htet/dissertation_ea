import numpy as np
from test_cases.onemax import fitness_calculation_onemax, fitness_onemax
from test_cases.twomax import fitness_calculation_twomax, fitness_twomax
from test_cases.maxsat import fitness_calculation_maxsat, fitness_maxsat
from random import choice
import multiprocessing
import sys

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

# rls method
def rls(input_data):
    
    # set input data
    n = input_data[0]
    benchmark_func = input_data[1]
    optimum_found = 0
    run_time = 1
    cnf_list = None
    cnf_index = None

    if benchmark_func == 2:
        run_times = np.array([run_time])
        optimums_found = np.array([optimum_found])
        optimum_list = np.array([])
        cnf_file = input_data[2]
        cnf_index = input_data[3]
        sys.stdout.write(f"\r{' '*100}\r")
        sys.stdout.flush()
        sys.stdout.write('Currently working on ' + str(cnf_index + 1) + 'th file out of ' + str(100) + ' files')
        sys.stdout.flush()
        if cnf_file == 0:
            cnf_list = "uf75"
        else:
            cnf_list = "uf250"        
    
    # initialize candidate solution
    current_candidate = unif_initialization(n, cnf_list, cnf_index)

    # evaluate f(x), termination condition different for maxsat and others
    if benchmark_func == 2:
        termination_condition = terminate_maxsat(run_time)
        check_fitness = check_optimum_maxsat(current_candidate, cnf_list, cnf_index)
        if check_fitness == True:
            if not current_candidate in optimum_list:
                optimum_found += 1
                optimum_list = np.append(optimum_list, current_candidate)
    else:
        local_opt = 0
        termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)

    while (termination_condition == False):
        new_candidate = mutation_operator(current_candidate)
        if benchmark_func == 2:
            new_fitness_candidate = calculate_fitness_maxsat(new_candidate, cnf_list, cnf_index)
            current_fitness_candidate = calculate_fitness_maxsat(current_candidate, cnf_list, cnf_index)
        else:
            new_fitness_candidate = fitness_calculation(new_candidate, benchmark_func)
            current_fitness_candidate = fitness_calculation(current_candidate, benchmark_func)
        if (new_fitness_candidate >= current_fitness_candidate):
            current_candidate = new_candidate
        # termination condition different for maxsat and others
        if benchmark_func == 2:
            termination_condition = terminate_maxsat(run_time)
            check_fitness = check_optimum_maxsat(current_candidate, cnf_list, cnf_index)
            if check_fitness == True:
                if not current_candidate in optimum_list:
                    optimum_found += 1
                    optimum_list = np.append(optimum_list, current_candidate)
        else:
            termination_condition, local_opt = fitness(current_candidate, local_opt, benchmark_func)
        run_time += 1
        if benchmark_func == 2:
            run_times = np.append(run_times, run_time)
            optimums_found = np.append(optimums_found, optimum_found)
            sys.stdout.write(f"\r{' '*100}\r")
            sys.stdout.flush()
            sys.stdout.write('Currently working on ' + str(run_time) + ' out of 100,000 runtime for ' +  str(cnf_index + 1) + 'th file out of ' + str(100) + ' files\n')
            sys.stdout.flush()
    if benchmark_func == 2:
        return run_times, optimums_found
    else:
        return run_time

# get data ready to be input into the multiprocessing function. 0 is for uf75, 1 is for uf250
def process_input_data(n, benchmark_func, repeat, cnf_file = 0):
    
    # return array depends on maxsat or not
    if benchmark_func == 2:
        if cnf_file == 0:
            cnf = 'uf75'
        else:
            cnf = 'uf250'
        file = 'prerequisites/' + cnf + '.npy'
        cnf_list = np.load(file)
        
        # set the shape of the array
        input_data_lst = np.empty((0,4), int)
        
        for i in range(repeat):
            for index in range(len(cnf_list)):
                data_input = [n, benchmark_func, cnf_file, index]
                for j in range(repeat):
                    input_data_lst = np.append(input_data_lst, np.array([data_input]), axis = 0)
    else:

        # set the shape of the array
        input_data_lst = np.empty((0,2), int)

        data_input = [n, benchmark_func]
        for i in range(repeat):
            input_data_lst = np.append(input_data_lst, np.array([data_input]), axis = 0)
    
    return input_data_lst

# rls method single core      
def rls_singlecore(n, benchmark_func, repeat, max_runtime = 1000, cnf_file = 0):
    result = 0
    if benchmark_func == 2:
        prepare_data = process_input_data(n, benchmark_func, repeat, cnf_file)

        # max size is 1000 by default
        optimum_total = np.zeros(max_runtime)
        for i in prepare_data:
            run_times, optimum = rls(i)
            optimum_size = len(optimum)
            # add to all behind if best solution is found since best solution would be less than expected
            if optimum_size < max_runtime:
                while (optimum_size < max_runtime):
                    optimum = np.append(optimum, optimum[optimum_size - 1])

            optimum_total = np.add(optimum_total, optimum)
        return run_times[:max_runtime], optimum_total[:max_runtime]
    else:
        prepare_data = process_input_data(n, benchmark_func, repeat)
        for i in prepare_data:
            result += rls(i)
        result /= repeat
        return result

# rls method multi core
def rls_multiprocessing(n, benchmark_func, repeat, max_runtime = 1000, core = 6, cnf_file = 0):
    result = 0

    # multiprocess the results
    if benchmark_func == 2:
        prepare_data = process_input_data(n, benchmark_func, repeat, cnf_file)
    else:
        prepare_data = process_input_data(n, benchmark_func, repeat)
    with multiprocessing.Pool(core) as pool:
        resultList = pool.map(rls, prepare_data)

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
def get_data(max_bit, repeat, benchmark_func = 0, multicore = True, cnf_file = 0):
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
            run_times, optimum_total = rls_multiprocessing(n, benchmark_func, repeat, max_runtime = 100000, core = 10, cnf_file = cnf_file)
        else:
            run_times, optimum_total = rls_singlecore(n, benchmark_func, repeat, max_runtime = 100000, cnf_file = cnf_file)
        # save run times
        run_time_file = "results/rls_" + text + "_run_time_list.npy"
        data = np.asarray(run_times)
        np.save(run_time_file, data)
        # save optimum per run time list
        optimum_file = "results/rls_" + text + "_optimum_list.npy"
        data = np.asarray(optimum_total)
        np.save(optimum_file, data)
    else:
        sys.stdout.write('The process will go through ' + str(max_bit) + ' bits')
        sys.stdout.flush()
        for n in range(5, max_bit+1):
            if multicore == True:
                run_time = rls_multiprocessing(n, benchmark_func, repeat, core = 6)
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
    get_data(50, 1, benchmark_func = 2)