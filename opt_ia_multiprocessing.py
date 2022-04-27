from cProfile import run
import numpy as np
import import_ipynb
import onemax
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from random import choice
import multiprocessing

#select the n-th bit to flip
def flip_bit(candidate, n):
    new_candidate = candidate[:n]
    if candidate[n] == '0':
        new_candidate += '1'
    else:
        new_candidate += '0'
    new_candidate += candidate[n+1:]
    return new_candidate

def fitness(x, i):
    if i == 0: #for onemax
        return onemax.fitness(x)

def fitness_calculation(x, i):
    if i == 0: #for onemax
        return onemax.fitness_calculation(x)

#uniformly distributed initialisation
#n = size of the candidate
def unif_initialization(n):
    bit_list = np.random.randint(2, size = n)
    candidate_solution = ''.join(str(bit) for bit in bit_list)
    return candidate_solution

#Flips at most Cn bits
def mutation_operator(candidate, c, benchmark_func, run_time):
    n = len(candidate)
    #decide number of bit flips
    if c > 1:
        max_number_flip = n
    else:
        max_number_flip = int(np.ceil(c * n))
    new_candidate = candidate
    count_flip = 0
    continue_flipping = True
    flipped_bit = np.array([])
    #continue mutating if there is no improvements
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
        #print("candidate, new_candidate and fitness mutating" , candidate, new_candidate, fitness_calculation(new_candidate, benchmark_func))
    return new_candidate, run_time

def opt_ia(n, c, benchmark_func):
    
    #initialize candidate solution
    current_candidate = unif_initialization(n)
    
    #Evaluate f(x)
    termination_condition = fitness(current_candidate, benchmark_func)
    #Set run time
    run_time = 1
    while (termination_condition == False):
        new_candidate, run_time = mutation_operator(current_candidate, c, benchmark_func, run_time)
        if (fitness_calculation(new_candidate, benchmark_func) >= fitness_calculation(current_candidate, benchmark_func)):
            current_candidate = new_candidate
        termination_condition = fitness(current_candidate, benchmark_func)
    return run_time

def opt_ia_multiprocess(current_bit, c, benchmark_func, repeat, n_workers):
    run_time = 0
    pool = multiprocessing.Pool(n_workers)
    run_times = [pool.apply(opt_ia, args=(current_bit, c, benchmark_func,)) for x in range(repeat)]
    for i in run_times:
        run_time += i
    run_time = run_time/repeat
    return run_time