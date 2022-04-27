import os
import numpy as np

# to turn binary representation into integer representation of literals for candidate solution
def translate_candidate(candidate):
    translated_candidate = np.array([])
    for i in range(len(candidate)):
        if candidate[i] == '0':
            translated_candidate = np.append(translated_candidate,-(i+1))
        else:
            translated_candidate = np.append(translated_candidate, (i+1))
    return translated_candidate

# calculate fitness of candidates from a chosen cnf
def fitness_calculation(candidate, cnf_array):
    candidate_array = translate_candidate(candidate)
    #get clause from cnf
    result = 0
    for clause in cnf_array:
        #get literal from clause
        for literal in clause:
            #check if literal is part of the candidate
            if literal in candidate_array:
                #add 1 if one of the literal from the clause is in it and thus satisfying the clause
                result += 1
                break
    return result

# calculate if the given solution is the desired candidate solution
def fitness(candidate, cnf_array):
    #one in which all clauses can be satisfied
    best_fitness = len(cnf_array)
    fitness_calc = fitness_calculation(candidate, cnf_array)
    if (fitness_calc == best_fitness):
        return True
    else:
        return False

# test cases
def test_fitness_calculation():
    cnf_array = [[1,2,-3], [1,5,12], [-11,14,5], [16,-2,-9]]
    cnf_array2 = [[1,2,3], [1,5,-12], [-11,-14,-5], [16,-3,9]]
    candidate1 = "0000000000000000"
    candidate2 = "1010101010101010"
    candidate3 = "1111111111111111"
    assert fitness_calculation(candidate1, cnf_array) == 3; "Should be 3"
    assert fitness_calculation(candidate2, cnf_array) == 4; "Should be 4"
    assert fitness_calculation(candidate3, cnf_array) == 4; "Should be 4"
    assert fitness_calculation(candidate1, cnf_array2) == 3; "Should be 3"
    assert fitness_calculation(candidate2, cnf_array2) == 4; "Should be 4"
    assert fitness_calculation(candidate3, cnf_array2) == 3; "Should be 3"
    
def test_fitness():
    cnf_array = [[1,2,-3], [1,5,12], [-11,14,5], [16,-2,-9]]
    cnf_array2 = [[1,2,3], [1,5,-12], [-11,-14,-5], [16,-3,9]]
    candidate1 = "0000000000000000"
    candidate2 = "1010101010101010"
    candidate3 = "1111111111111111"
    assert fitness(candidate1, cnf_array) == False; "Should be False"
    assert fitness(candidate2, cnf_array) == True; "Should be True"
    assert fitness(candidate3, cnf_array) == True; "Should be True"
    assert fitness(candidate1, cnf_array2) == False; "Should be False"
    assert fitness(candidate2, cnf_array2) == True; "Should be True"
    assert fitness(candidate3, cnf_array2) == False; "Should be False"

if __name__ == "__main__":
    test_fitness_calculation()
    test_fitness()
    print("Everything passed")