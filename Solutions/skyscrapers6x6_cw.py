#PASSED
# In a grid of 6 by 6 squares you want to place a skyscraper in each square with only some clues:
#
# The height of the skyscrapers is between 1 and 6
# No two skyscrapers in a row or column may have the same number of floors
# A clue is the number of skyscrapers that you can see in a row or column from the outside
# Higher skyscrapers block the view of lower skyscrapers located behind them
#
# Can you write a program that can solve each 6 by 6 puzzle?
#
# Pass the clues in an array of 24 items. The clues are in the array around the clock.
#
# If no clue is available, add value 0
# Each puzzle has only one possible solution
# SolvePuzzle() returns matrix int[][]. The first indexer is for the row, the second indexer for the column. Python returns a 6-tuple of 6-tuples, Ruby a 6-Array of 6-Arrays.


import numpy as np
import itertools

N = 6

def get_row(i, opts):
    #Gets the row corresponding to clue i, and puts it in the order from the clue's perspective.
    if i<N:
        #return a column, top to bottom
        return opts[:,i]
    elif i<2*N:
        #return a row, right to left
        return opts[i-N,::-1]
    elif i<3*N:
        #return a column, bottom to top
        return opts[::-1,3*N-1-i]
    else:
        #return a row, left to right
        return opts[4*N-1-i, :]


def get_opposite(i):
    #Gets the clue index opposite ours, since they control the same row.
    if i<N:
        #top row
        return 3*N-1-i
    elif i<2*N:
        #right hand column
        return 5*N-1-i
    elif i<3*N:
        #bottom row
        return 3*N-1-i
    else:
        #left hand column
        return 5*N-1-i


def remove_dupes(r, c, opts):
    #If this cell has been solved, eliminate it's duplicates from the rest of its row and column
    n_choices = sum(1 for x in opts[r][c] if x > 0)
    if n_choices == 1:
        #Whats the solved value:
        val = max(opts[r][c])
        for i in range(N):
            #skip cell (r,c)
            if i!=c:
                # eliminate the solved value from here
                opts[r][i] = [0 if x==val else x for x in opts[r][i]]
            if i!=r:
                # eliminate the solved value from here
                opts[i][c] = [0 if x == val else x for x in opts[i][c]]
    return opts

def test_row(sol, row, clue):
    #Checks if a proposed row solution is valid
    #!Try looking at both clues together, might eliminate more possibilities...
    #Make sure the proposed solution fits the known row clues:
    for i,x in enumerate(sol):
        if x not in row[i]:
            return False
    #Calculate the # of visible building and compare to clue:
    if clue != 0:
        n_vis = 0
        max_height = 0
        for height in sol:
            if height>max_height:
                n_vis += 1
                max_height = height
        if n_vis != clue:
            return False
    #If it makes it here, the solution must be ok
    return True

def solve_puzzle(clues):
    #Populate a 6x6 matrix, each cell contains a vector [1,2,3,4,5,6] representing the possible options in that location
    opts = np.array([[[1,2,3,4,5,6]]*N]*N)

    n_solved = 0
    while n_solved<N*N:
        for i,clue in enumerate(clues):
            print(i,end=' ')
            row = get_row(i, opts)

            #Also get clue opposite this clue:
            opp_i = get_opposite(i)

            ###Special case: clue==N
            if clue == N:
                row[:] = [[1,0,0,0,0,0],[2,0,0,0,0,0],[3,0,0,0,0,0],[4,0,0,0,0,0],[5,0,0,0,0,0],[6,0,0,0,0,0]] #Using the [:] avoids breaking the reference to opts
            ###Special case: clue==1
            elif clue == 1:
                row[0] = [N,0,0,0,0,0]
            else:
                ###Try all 720 possible combos in the row and determine which ones fit this clue:
                #!This might be SLOW!
                n_good = 0
                good_sols = [[]]*N
                for hyp_sol in itertools.permutations([1,2,3,4,5,6], N):
                    #Test hypothetical solution:
                    if test_row(hyp_sol, row, clue):
                        #Also check the clue opposite this one:
                        if test_row(hyp_sol[::-1], get_row(opp_i,opts), clues[opp_i]):
                            n_good += 1
                            good_sols = [good_sols[k] + [hyp_sol[k]] for k in range(N)]
                #Are there any values missing from the good_sols? Eliminate them from the row:
                for k in range(N):
                    for j in range(N):
                        if not row[k][j] in good_sols[k]:
                            row[k][j] = 0

            ###For each solved square, eliminate it's value from the other spots in its row and column: !unnecessary, but may improve speed!
            for r in range(N):
                for c in range(N):
                    opts = remove_dupes(r,c,opts)

        #Determine how many squares of the puzzle are complete
        n_solved = 0
        for r in range(N):
            for c in range(N):
                if sum(1 for x in opts[r][c] if x > 0) == 1:
                    n_solved += 1
        print(' ')
        print(n_solved)

    #Package the solution into a tuple of tuples:
    ans = tuple(tuple([max(item) for item in row]) for row in opts)
    return ans


# Test.describe("Skyscrapers")
# Test.it("can solve 6x6 puzzle 1")PASS
# clues = (3, 2, 2, 3, 2, 1,
#          1, 2, 3, 3, 2, 2,
#          5, 1, 2, 2, 4, 3,
#          3, 2, 1, 2, 2, 4)
#
# expected = ((2, 1, 4, 3, 5, 6),
#             (1, 6, 3, 2, 4, 5),
#             (4, 3, 6, 5, 1, 2),
#             (6, 5, 2, 1, 3, 4),
#             (5, 4, 1, 6, 2, 3),
#             (3, 2, 5, 4, 6, 1))
#
# actual = solve_puzzle(clues)
# print(actual == expected)

# # Test.it("can solve 6x6 puzzle 2")PASS
# clues = (0, 0, 0, 2, 2, 0,
#          0, 0, 0, 6, 3, 0,
#          0, 4, 0, 0, 0, 0,
#          4, 4, 0, 3, 0, 0)
#
# expected = ((5, 6, 1, 4, 3, 2),
#             (4, 1, 3, 2, 6, 5),
#             (2, 3, 6, 1, 5, 4),
#             (6, 5, 4, 3, 2, 1),
#             (1, 2, 5, 6, 4, 3),
#             (3, 4, 2, 5, 1, 6))
#
# actual = solve_puzzle(clues)
# print(actual == expected)

# Test.it("can solve 6x6 puzzle 3")STUCK AT 6 SOLVED
clues = (0, 3, 0, 5, 3, 4,
         0, 0, 0, 0, 0, 1,
         0, 3, 0, 3, 2, 3,
         3, 2, 0, 3, 1, 0)

expected = ((5, 2, 6, 1, 4, 3),
            (6, 4, 3, 2, 5, 1),
            (3, 1, 5, 4, 6, 2),
            (2, 6, 1, 5, 3, 4),
            (4, 3, 2, 6, 1, 5),
            (1, 5, 4, 3, 2, 6))

actual = solve_puzzle(clues)
print(actual == expected)
