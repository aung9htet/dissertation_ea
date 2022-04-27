from cProfile import run
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from random import choice
import multiprocessing
import time

def print_shit(lol):
    time.sleep(3)
    result = lol
    time.sleep(1)
    return result

def opt_ia_multiprocess():
    result = 0
    pool = multiprocessing.Pool(6)
    with pool as p:
        resultlist = pool.map(print_shit, range(6))
    for i in resultlist:
        result += i
    return result

if __name__ == "__main__":
    print(opt_ia_multiprocess())