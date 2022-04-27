import numpy as np

def fitness_calculation_onemax(candidate):
    result = 0
    for i in candidate:
        result += int(i)
    return result

def fitness_onemax(candidate):
    if (fitness_calculation_onemax(candidate) == len(candidate)):
        return True
    else:
        return False

def test_fitness_calculation():
    candidate1 = "0000000000000000"
    candidate2 = "1010101010101010"
    candidate3 = "1111111111111111"
    assert fitness_calculation_onemax(candidate1) == 0; "Should be 0"
    assert fitness_calculation_onemax(candidate2) == 8; "Should be 8"
    assert fitness_calculation_onemax(candidate3) == 16; "Should be 16"

def test_fitness():
    candidate1 = "0000000000000000"
    candidate2 = "1010101010101010"
    candidate3 = "1111111111111111"
    assert fitness_onemax(candidate1) == False; "Should be false"
    assert fitness_onemax(candidate2) == False; "Should be false"
    assert fitness_onemax(candidate3) == True; "Should be true"
    
if __name__ == "__main__":
    test_fitness_calculation()
    test_fitness()
    print("Everything passed")