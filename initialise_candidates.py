import numpy as np
from opt_ia_multiprocessing import unif_initialization

# can be either uf75 or uf250
def create_random_candidate(cnf_file):
    file = 'prerequisites/' + cnf_file + '.npy'
    cnf_list = np.load(file)
    maxsat_init = np.array([])
    for i in cnf_list:
        cnf_length = len(i)
        init_candidate = unif_initialization(cnf_length)
        maxsat_init = np.append(maxsat_init, init_candidate)
    file_name = "prerequisites/" + cnf_file + "_init.npy"
    data = np.asarray(maxsat_init)
    np.save(file_name, data)

if __name__ == "__main__":
    create_random_candidate("uf75")
    create_random_candidate("uf250")