import numpy as np

# fitness calculation of candidate solution for two max
def fitness_calculation_twomax(candidate):
    result_one = 0 #all ones
    for i in candidate:
        result_one += int(i)
    result_two = len(candidate) - result_one # all zeros
    result = np.maximum(result_one, result_two)
    return result

# check if the fitness is of the desired solution
# the solution should fine both optima of the two max
def fitness_twomax(candidate, local_opt):
    
    #calculate result
    result_one = 0
    for i in candidate:
        result_one += int(i)
    result_two = len(candidate) - result_one
    
    result = False
    #decide if both optimas is found
    if (local_opt == 1): #optimum with all zeros found
        if result_one == len(candidate):
            result = True
    elif (local_opt == 2): #optimum with all ones found
        if result_two == len(candidate):
            result = True
    else:
        if result_one == len(candidate):
            local_opt = 2
        elif result_two == len(candidate):
            local_opt = 1
    return result, local_opt

# test cases
def test_fitness_calculation():
    candidate1 = "0000000000000000"
    candidate2 = "1010101010101010"
    candidate3 = "1111111111111111"
    assert fitness_calculation_twomax(candidate1) == 16; "Should be 16"
    assert fitness_calculation_twomax(candidate2) == 8; "Should be 8"
    assert fitness_calculation_twomax(candidate3) == 16; "Should be 16"

def test_fitness():
    candidate1 = "0000000000000000"
    candidate2 = "1010101010101010"
    candidate3 = "1111111111111111"
    termination_condition, local_opt = fitness_twomax(candidate1, 2)
    assert termination_condition == True; "Should be true"
    termination_condition, local_opt = fitness_twomax(candidate2, 0)
    assert termination_condition == False; "Should be false"
    termination_condition, local_opt = fitness_twomax(candidate3, 1)
    assert termination_condition == True; "Should be true"
    
if __name__ == "__main__":
    test_fitness_calculation()
    test_fitness()
    print("Everything passed")