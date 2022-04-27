from cProfile import run
import numpy as np
import import_ipynb
import onemax
import time
import queue
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sys
from random import choice
from multiprocessing import Queue, Process

#uniformly distributed initialisation
#n = size of the candidate
def unif_initialization(n):
    bit_list = np.random.randint(2, size = n)
    candidate_solution = ''.join(str(bit) for bit in bit_list)
    return candidate_solution

#mutation operator
def unif_mutation(candidate, benchmark_func, run_time, mutation_potential = 0):
    
    #Will be used to check if there is constructive mutation or the number of bit mutation has reached mutation potential
    bit_change_condition = True
    
    #candidate used to check for constructive mutation
    set_candidate = candidate
    
    #To add the flipped bits
    flipped_bit = np.array([])
    while bit_change_condition == True:
        
        #Select bit to flip
        bit_change = choice([i for i in range(0,len(candidate)) if i not in flipped_bit])
        flipped_bit = np.append(flipped_bit, bit_change)
        
        #Create new candidate to be used
        new_candidate = set_candidate[:bit_change]
        if set_candidate[bit_change] == "0":
            new_candidate += "1"
        else:
            new_candidate += "0"
        new_candidate += set_candidate[bit_change + 1:]
        set_candidate = new_candidate
        
        #Compare results
        if (hamming_distance(new_candidate, candidate) >= mutation_potential):
            bit_change_condition = False
        if fitness_calculation(new_candidate, benchmark_func) >= fitness_calculation(candidate, benchmark_func):
            continue_flipping = False
        #Add run-time after checking fitness
        run_time += 1
    return new_candidate, run_time

#hamming distance calculation
def hamming_distance(candidate1, candidate2):
    i = 0
    hd = 0
    for char1 in list(candidate1):
        if (char1 != candidate2[i]):
            hd += 1
        i += 1
    return hd

#mutation potential
def symmetric_MexpoHD(n, x, x_origin, best):
    power_numerator = hamming_distance(x, x_origin)
    power_denominator = np.maximum(hamming_distance(best, x_origin), 1)
    power_value = -(power_numerator/power_denominator)
    m1 = np.power(n, power_value)
    m = int(np.ceil(n*m1))
    return m

def decide_eliminate_candidate(probabilty_to_eliminate):
    p_die = np.random.random_sample()
    result = False
    if p_die < probabilty_to_eliminate:
        result = True
    return result

#fitness calculations
def fitness(x, i):
    if i == 0: #for onemax
        return onemax.fitness(x)

def fitness_calculation(x, i):
    if i == 0: #for onemax
        return onemax.fitness_calculation(x)

# The benchmark func has the following meaning. 0 is for onemax and 1 for twomax.
# This can also be updated in the fitness and fitness_calculation method to add on more benchmark functions.
def immune_algorithm(n, age_threshold, benchmark_func):
    
    #initialize x
    intialized_candidate = unif_initialization(n)
    x = (intialized_candidate, intialized_candidate, 0); best = x[0]
    y = (intialized_candidate, intialized_candidate, 0)
    # tuple order = (x, origin, age)
    
    #Evaluate f(x)
    termination_condition = fitness(best, benchmark_func)
    #Set run time
    run_time = 1
    while (termination_condition == False):
        
        #add age
        x_age = x[2] + 1
        x = (x[0], x[1], x_age)
        
        #mutate x to y and set origin for y
        M = symmetric_MexpoHD(n, x[0], x[1], best)
        mutation_x, run_time = unif_mutation(x[0], benchmark_func, run_time, mutation_potential = M)
        
        #Set y.origin = x.origin
        y = (mutation_x, x[1], y[2])
        
        #check fitness between y and x
        if (fitness_calculation(y[0], benchmark_func) > fitness_calculation(x[0], benchmark_func)):
            #set y.age = 0
            y = (y[0], y[1], 0)
            #Check best solution
            if (fitness_calculation(y[0], benchmark_func) >= fitness_calculation(best, benchmark_func)):
                #Set best solution
                best = y[0]
                termination_condition = fitness(best, benchmark_func)
        else:
            #add y age
            y = (y[0], y[1], x[2])
        
        #Add run_time after checking the fitness
        run_time += 1
        
        #aging mechanism for x and y
        collection_candidates = [x,y]
        for candidate in collection_candidates:
            #check for age threshold and probability to die set at 0.5
            if ((candidate[2] > age_threshold) and (decide_eliminate_candidate(0.5) == True)):
                #reset the candidate and their age
                reset_candidate = unif_initialization(n) #reinitialize
                x = (reset_candidate, x[0], 0) 
                y = (reset_candidate, y[0], 0)
                
        # best solution selection
        if (fitness_calculation(x[0], benchmark_func) < fitness_calculation(y[0], benchmark_func)):
            x = (y[0], x[1], x[2])
    return run_time

def worker(queue, run_times):
    while not queue.empty():
        task = queue.get()
        run_time = immune_algorithm(task[0], task[1], task[2])
        run_times.put(run_time)

def divide_task(set_args):
    run_time = 0
    repeat = set_args[3]
    queue = Queue()
    run_times = Queue()
    processes = []
    number_of_processes = 40

    for i in range(repeat):
        queue.put([set_args[0], set_args[1], set_args[2]])

    for w in range(number_of_processes):
        process = Process(target = worker, args = (queue, run_times))
        processes.append(process)
        process.start()
    
    for p in processes:
        p.join()

    while not run_times.empty():
        run_time += run_times.get()
    return run_time

#starts from 5 bits until the max_bit
#repeat is the number of time repeated and the average time taken from it will be used
def plot_graph_onemax(max_bit, repeat):
    y_axis = np.array([])
    control_y = np.array([])
    sys.stdout.write('The process will go through ' + str(max_bit) + ' bits')
    sys.stdout.flush()
    for n in range(5,max_bit+6):
        control_value = np.log(n) * np.square(n)
        control_y = np.append(control_y, control_value)
        run_time = divide_task([n, 100, 0, repeat])
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
    plt.plot(x_axis,y_axis, label = "Symmetric MexpoHD")
    plt.plot(x_axis,control_y, label = "$n^{2}$logn")
    plt.legend()