import os
from itertools import islice
import numpy as np

# select lib for the project from uf75 and uf250. if project doesnt exist return empty array.
def process_satlib(select_lib):
    str_clauses = ""
    cnf_lst = []
    
    # select line for lib
    if select_lib == "uf75":
        directory = (r'C:..\\satlib\\UF75.325.100')
        max_clause = 333
    elif select_lib == "uf250":
        directory = (r'..\\satlib\\uf250-1065\\UF250.1065.100')
        max_clause = 1073
    else:
        return cnf_lst
  
    # string manipulation to get the clauses part only
    for file in os.listdir(directory):
        assert directory
        assert file
        with open(os.path.join(directory, file), 'r') as f:
            for line in islice(f, 8, max_clause):
                str_clauses += line.strip()
                str_clauses += " "
            literal_lst = get_literal(str_clauses)
            clause_lst = get_clause(literal_lst)
            str_clauses = ""
            cnf_lst.append(clause_lst)
    cnf_lst = np.array(cnf_lst)
    return cnf_lst

# get a list of literals from an unprocessed string
def get_literal(str_clauses):
    # get array of number
    literal_lst = np.array([])
    literal_str = ""
    for character in str_clauses:
        # add character to become number
        if character.isspace():
            if literal_str.isspace() == False:
                literal_lst = np.append(literal_lst, int(literal_str))
            literal_str = ""
        else:
            literal_str += character
    return literal_lst

# divide a list of unprocessed string into a list of clauses
def get_clause(literal_lst):
    clauses_lst = np.empty((0,3), int)
    clause = np.array([])
    for literal in literal_lst:
        if literal == 0:
            clauses_lst = np.append(clauses_lst, np.array([clause]), axis = 0)
            clause = np.array([])
        else:
            clause = np.append(clause, literal)
    return clauses_lst

# save processed lib for the project from uf75 and uf250
def save_as_npy(select_lib):
    if select_lib == "uf75":
        data = np.asarray(process_satlib("uf75"))
        np.save('uf75.npy', data)
    elif select_lib == "uf250":
        data = np.asarray(process_satlib("uf250"))
        np.save('uf250.npy', data)

if __name__ == "__main__":
    save_as_npy("uf75")
    print("UF75 test cases are processed and saved ...")
    save_as_npy("uf250")
    print("UF250 test cases are processed and saved ...")
    print("All test cases has been processed and saved as npy file!")