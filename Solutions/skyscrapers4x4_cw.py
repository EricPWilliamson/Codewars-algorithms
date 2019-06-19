#PASSED
# In a grid of 4 by 4 squares you want to place a skyscraper in each square with only some clues:
#
# The height of the skyscrapers is between 1 and 4
# No two skyscrapers in a row or column may have the same number of floors
# A clue is the number of skyscrapers that you can see in a row or column from the outside
# Higher skyscrapers block the view of lower skyscrapers located behind them
#
#

import numpy as np

def get_row(i, opts):
    #Gets the row corresponding to clue i, and puts it in the order from the clue's perspective.
    if i<4:
        #return a column, top to bottom
        return opts[:,i]
    elif i<8:
        #return a row, right to left
        return opts[i-4,::-1]
    elif i<12:
        #return a column, bottom to top
        return opts[::-1,11-i]
    else:
        #return a row, left to right
        return opts[15-i, :]

def give_row(i, row, opts):
    #Puts a row back in applying any changes made to the row. !!Unnecessary
    if i<4:
        opts[:, i] = row
    elif i<8:
        opts[i-4,::-1] = row
    elif i<12:
        opts[::-1, 11 - i] = row
    else:
        opts[15-i, :] = row
    return opts

def remove_dupes(r, c, opts):
    #If this cell has been solved, eliminate it's duplicates from the rest of its row and column
    n_choices = sum(1 for x in opts[r][c] if x > 0)
    if n_choices == 1:
        #Whats the solved value:
        val = max(opts[r][c])
        for i in range(4):
            #skip cell (r,c)
            if i!=c:
                # eliminate the solved value from here
                opts[r][i] = [0 if x==val else x for x in opts[r][i]]
            if i!=r:
                # eliminate the solved value from here
                opts[i][c] = [0 if x == val else x for x in opts[i][c]]
    return opts

def test_row(sol, clue):
    #Checks if a proposed row solution is valid
    #automatically skip a sol that has zeros
    if 0 in sol:
        return False

    # Check for duplicates:
    for i in range(1,5):
        if sol.count(i)!=1:
            return False

    #Calculate the # of visible building and compare to clue:
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
    #Populate a 4x4 matrix, each cell contains a vector [1,2,3,4] representing the possible options in that location
    opts = np.array([[[1,2,3,4]]*4]*4)
    # opts = np.array([[[1], [3], [4], [2]],
    #                  [[4], [2], [1], [3]],
    #                  [[3], [4], [2], [1]],
    #                  [[2], [1], [3], [4]]])

    #Could be done with basic lists:
    # opts = [[[1, 2, 3, 4]] * 4] * 4
    # opts[0][0] = [1,4]

    # j = 9
    # row = get_row(j,opts)
    # row[2] = [1,2,0,0]
    # new_opts = give_row(j, row, opts)#happens automatically because row shares the opts reference
    # row = np.array(get_row(15,opts)) #Breaks the shared reference between row and opts

    n_solved = 0
    while n_solved<16:
        for i,clue in enumerate(clues):
            #Dont waste time on empty clues
            if clue != 0:
                row = get_row(i, opts)

                ###Special case: clue==4
                if clue == 4:
                    row[:] = [[1,0,0,0],[2,0,0,0],[3,0,0,0],[4,0,0,0]] #Using the [:] avoids breaking the reference to opts
                ###Special case: clue==1
                if clue == 1:
                    row[0] = [4,0,0,0]
                #clue==2?maybe unnecessary
                #clue==3?maybe unnecessary
                #?something about checking how much space the clue needs?

                ###Try all 256 possible combos in the row and determine which ones fit this clue:
                #!This might be SLOW!
                n_good = 0
                good_sols = [[]]*4
                hyp_sol = [0]*4
                for j0 in range(4):
                    hyp_sol[0] = row[0][j0]
                    for j1 in range(4):
                        hyp_sol[1] = row[1][j1]
                        for j2 in range(4):
                            hyp_sol[2] = row[2][j2]
                            for j3 in range(4):
                                hyp_sol[3] = row[3][j3]
                                #Test hypothetical solution:
                                if test_row(hyp_sol, clue):
                                    n_good += 1
                                    # good_sol = list(hyp_sol)#keep this solution in case its the only good one
                                    good_sols = [good_sols[k] + [hyp_sol[k]] for k in range(4)]
                #Are there any values missing from the good_sols? Eliminate them from the row:
                for k in range(4):
                    for j in range(4):
                        if not row[k][j] in good_sols[k]:
                            row[k][j] = 0
                # #only 1 good solution? Apply it:
                # if n_good == 1:
                #     for k, ans in enumerate(good_sol):
                #         row[k] = [ans, 0, 0, 0]
                # #!!What if there are multiple good solutions, but they all have a cell in common... k=0

                ###For each solved square, eliminate it's value from the other spots in its row and column: !maybe unnecessary
                for r in range(4):
                    for c in range(4):
                        opts = remove_dupes(r,c,opts)

        #Determine how many squares of the puzzle are complete
        n_solved = 0
        for r in range(4):
            for c in range(4):
                if sum(1 for x in opts[r][c] if x > 0) == 1:
                    n_solved += 1
        # print(n_solved)

    #Package the solution into a tuple of tuples:
    ans = tuple(tuple([max(item) for item in row]) for row in opts)
    return ans


clues = (
( 2, 2, 1, 3,
  2, 2, 3, 1,
  1, 2, 2, 3,
  3, 2, 1, 3 ),
( 0, 0, 1, 2,
  0, 2, 0, 0,
  0, 3, 0, 0,
  0, 1, 0, 0 )
)


outcomes = (
( ( 1, 3, 4, 2 ),
  ( 4, 2, 1, 3 ),
  ( 3, 4, 2, 1 ),
  ( 2, 1, 3, 4 ) ),
( ( 2, 1, 4, 3 ),
  ( 3, 4, 1, 2 ),
  ( 4, 2, 3, 1 ),
  ( 1, 3, 2, 4 ) )
)

# opts = np.array([[[1], [3], [4], [2]],
    #                  [[4], [2], [1], [3]],
    #                  [[3], [4], [2], [1]],
    #                  [[2], [1], [3], [4]]])

print(solve_puzzle(clues[0]) == outcomes[0])
print(solve_puzzle(clues[1]) == outcomes[1])
