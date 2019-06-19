"""
https://www.codewars.com/kata/sliding-puzzle-solver/train/python
"""

import numpy as np

def swap_cells(x,puz):
    """Swap 0 and x."""
    #Get the coords of 0 and x
    zero_i = np.where(puz==0)
    target_i = np.where(puz==x)
    #Make sure this is a valid swap:
    dist = np.abs(zero_i[0][0]-target_i[0][0]) + np.abs(zero_i[1][0]-target_i[1][0])
    if dist != 1:
        raise Exception('Tried to swap with non-adjacent cell.')
    #Perform the swap:
    puz[zero_i] = x
    puz[target_i] = 0
    return puz

def slide_puzzle(ar):
    """Main fcn"""
    puz = np.array(ar)

    # ###Example 1:
    # #Get 1 in right position:
    # puz = swap_cells(8,puz)
    # puz = swap_cells(2,puz)
    # puz = swap_cells(4,puz)
    # puz = swap_cells(1,puz)
    # #Get 2 in right position:
    # puz = swap_cells(2,puz)
    # #Move 5:
    # puz = swap_cells(8,puz)
    # puz = swap_cells(5,puz)
    # #Get 5 in right position:
    # puz = swap_cells(6,puz)
    # puz = swap_cells(8,puz)
    # puz = swap_cells(5,puz)
    # #Get 6 in right position:
    # puz = swap_cells(6,puz)
    # #Done
    # return [8,2,4,1,2,8,5,6,8,5,6]

    ###Example 2:
    sol = []
    #Get 1 in the right place:
    sol += [8,6,3,10,1]
    #March 2 to home:
    sol += [2,13,5,2,13,5,7,6,3,10,2]
    #Get 3 home:
    sol += [7,6,15,8,4,10,3]

    ###Execute solution
    for x in sol:
        puz = swap_cells(x,puz)
    print(puz)

    return None #unsolvable puzzle


#############################################
def validate_solution(puzzle, solution):
    puz = np.array(puzzle)
    for x in solution:
        puz = swap_cells(x,puz)
    flat_puz = np.reshape(puz,-1)
    for i,x in enumerate(flat_puz[:-1]):
        if i+1 != x:
            print('FAILED')
            return False
    print('PASSED')
    return True
#############################################

# test.describe('Example Tests')
puzzle1 = [
    [4,1,3],
    [2,8,0],
    [7,6,5]
]
puzzle2 = [
    [10, 3, 6, 4],
    [ 1, 5, 8, 0],
    [ 2,13, 7,15],
    [14, 9,12,11]
]
puzzle3 = [
    [ 3, 7,14,15,10],
    [ 1, 0, 5, 9, 4],
    [16, 2,11,12, 8],
    [17, 6,13,18,20],
    [21,22,23,19,24]
]
# validate_solution(puzzle1,slide_puzzle([x[:] for x in puzzle1]))
validate_solution(puzzle2,slide_puzzle([x[:] for x in puzzle2]))
# validate_solution(puzzle3,slide_puzzle([x[:] for x in puzzle3]))

