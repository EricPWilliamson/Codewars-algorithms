#FAILED - cant get efficiency high enough
# If you haven't already done so, you should do the 5x5 and 15x15 Nonogram solvers first.
#
# In this kata, you have to solve nonograms from any size up to one with an average side length of 50. The nonograms
#  are not all square. However, they all will be valid and should only have one solution.
#
# I highly recommend not to try and use a brute force solution as some of the grids are very big. Also, you may not be
#  able to solve all the grids by deduction alone so may have to guess one or two squares. :P
#
# You will be given three arguments: The clues, the width, and the height:
#
# # clues is given in the same format as the previous two nonogram katas:
# clues = (tuple((column_clues,) for column_clues in column),
#          tuple((row_clues,) for row_clues in row))
#
# # width is the width of the puzzle (distance from left to right)
# width = width_of_puzzle
#
# # height is the height of the puzzle (distance from top to bottom)
# height = height_of_puzzle
# and you will have to finish the function:
#
# def solve(clues, width, height):
#     pass
# You should return either a tuple of tuples for Python or an array of array for JS of the solved grid.
#
# For example, the second example test case looks like:
#
# Img
#
# Therefore, you would be given the arguments:
#
# clues = (((3,), (4,), (2, 2, 2), (2, 4, 2), (6,), (3,)),
#          ((4,), (6,), (2, 2), (2, 2), (2,), (2,), (2,), (2,), (), (2,), (2,)))
# width = 6
# height = 11
# Zero will be given as an empty tuple in python, or empty array in JS.
#
# Test sizes:
# You will be given 60 random tests in total. There will be:
#
# 35 small tests: 3 < the average of the side lengths <= 25
# 15 medium tests: 25 < the average of the side lengths <= 35
# 10 big tests: 40 <= the average of the side lengths <= 50
# Good luck :)


import time
from timeit import default_timer as timer
import math
import itertools

def partitions(n, k):
    #https://stackoverflow.com/questions/28965734/general-bars-and-stars
    #Usage: Example usage 3 [0]s and 4 slots
    # for p in partitions(3, 4):
    #     print(p)
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]


def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


def stars_bars(marbles,bins):
    n = marbles + bins -1
    k = marbles
    n_combos = nCr(n,k)
    return n_combos


def sort_clues(clues):
    #Judges the difficulty of each clue by calculating the number potental combinations.
    #Usage: clue_i = clues[v[i][0]][v[i][1]]
    # Determine width and height of puzzle:
    W = len(clues[0])
    H = len(clues[1])
    ###Look at each clue and determine diff:
    diffs = []
    #Start with column clues:
    for clue in clues[0]:
        bins = len(clue) + 1  # Number of slots for extra [0]s
        if clue:
            marbles = H - sum(clue) - (len(clue) - 1)  # Number of extra [0]s
        else:
            #Empty clues are the easiest
            marbles = 0
        # diffs += [marbles]
        n_combos = int(stars_bars(marbles, bins))
        diffs += [n_combos]
    #Now do row clues:
    for clue in clues[1]:
        bins = len(clue) + 1  # Number of slots for extra [0]s
        if clue:
            marbles = W - sum(clue) - (len(clue) - 1)  # Number of extra [0]s
        else:
            #Empty clues are easiest
            marbles = 0
        # diffs += [marbles]
        n_combos = int(stars_bars(marbles, bins))
        diffs += [n_combos]
    ###Create vector of indices, sorted on difficulty:
    diff_order = sorted((e, i) for i, e in enumerate(diffs))
    v = []
    for x in diff_order:
        i = x[1]
        if i<W:
            v += [[0,i]]
        else:
            v += [[1,i-W]]

    #Split v into easy batch and hard batch:
    #get the index where difficulty surpasses 100 variations:
    cut = next((i for i,x in enumerate(diff_order) if x[0] > 100), len(v))
    return v[0:cut], v[cut:]
    # return v


def get_col(c, solution):
    # Gets a vertical column at index c from our 2d matrix, solution.
    row = [x[c] for x in solution]
    return row


def test_inc_sol(hyp_sol, clue):
    #Tests a partially complete hypothetical row solution against our given clue.
    ###Calculate what kind of clue would match the known portion of this hypothetical solution
    hyp_clue = [0]
    n_extra = 0
    for i,cell in enumerate(hyp_sol):
        if cell == -1: # We run through the solution until we hit an unknown
            n_extra = len(hyp_sol) - i
            break
        elif cell == 0: # We have a gap here, so start a new segment (if we haven't already started one)
            if hyp_clue[-1] > 0:
                hyp_clue += [0]
        else: # This cell is filled, so add to the latest segment:
            hyp_clue[-1] += 1
    ###Compare the hyp_clue to our actual clue:
    if len(hyp_clue) > len(clue)+1:#More than one extra element means we've added an unnecessary segment
        return False
    for i in range(len(hyp_clue)-1):
        if i < len(hyp_clue) - 1:  # make sure we're not at the end of hyp_clue
            if hyp_clue[i] != clue[i]:  # This part of the clue must be an exact match
                return False
    #The final element of hyp_clue is special:
    if hyp_clue[-1] > 0: #we can ignore the last element if its [0]
        if len(hyp_clue)>len(clue): #make sure we havent added too many segments
            return False
        elif hyp_clue[-1] > clue[len(hyp_clue)-1]: #This final segment may yet be added to, so it's ok if its less than the value in clue
            return False
    ###Make sure we still have room to fit the rest of our clue:
    if len(hyp_clue)<=len(clue):
        # How many cells do we need to complete the latest segment?
        n_needed = clue[len(hyp_clue)-1] - hyp_clue[-1]
        #If we still have additional segments in clue...
        for i in range(len(hyp_clue), len(clue)):
            n_needed += 1 #At least one cell for gap
            n_needed += clue[i] #and the new segment
        if n_needed>n_extra:
            return False

    #Since the code ran to here, we must not have any failures
    return True


def smarter_add_to_sol(sol, i, clue):
    #Takes an incomplete proposed solution and adds proposed solutions for cell i, creating a pair if both combinations are allowed:
    if sol[i] != -1: #we already solved this cell
        return [sol]
    new_sols = []
    #Try putting 0 in cell i, and see if we still match our clue:
    hyp_sol = list(sol)
    hyp_sol[i] = 0
    if test_inc_sol(hyp_sol, clue):
        new_sols += [hyp_sol]
    #Now try putting a 1 in cell i, and test it:
    hyp_sol = list(sol)
    hyp_sol[i] = 1
    if test_inc_sol(hyp_sol, clue):
        new_sols += [hyp_sol]
    return new_sols


def smarter_generate_sols(row, clue):
    #Generates valid combos by looking at known values and clue in each step.
    # !!!This is usually slower than smart_add_to_sol :(
    sol_list = [row]
    for i in range(len(row)):
        new_sols = []
        for sol in sol_list:
            new_sols += smarter_add_to_sol(sol, i, clue)
        sol_list = list(new_sols)
    return sol_list


def smart_generate_sols(row, clue):
    # Generates all valid combos for this row
    #!!make this more efficient by first looking at cells that have already been solved. Should be able to drastically reduce the number of solutions we have to check...
    # Find all combos that fit this row's clue, using the stars and bars method
    sol_list = []
    bins = len(clue)+1 #Number of slots for extra [0]s
    marbles = len(row) - sum(clue) - (len(clue)-1) #Number of extra [0]s
    n_guesses = 0
    for p in partitions(marbles, bins):
        n_guesses += 1
        sol = []
        for i in range(len(clue)):
            sol += [0] * p[i]    #Variable [0]s
            sol += [1] * clue[i] #Block of [1]s fitting clue
            sol += [0]           #Gap
        #Remove the extra gap
        sol = sol[:-1]
        #Add the final group of variable [0]s
        sol += [0] * p[bins-1]

        #Lastly check that this solution matches our existing known values in row:
        # any(-1 in x for x in solution)
        if not any((x!=y and x!=-1) for x,y in zip(row,sol)):
            sol_list += [sol[:]]
    # print(n_guesses)
    return sol_list


def crunch_row(row, clue):
    #Looks at one row and its clue and tries to see if any cells can be definatively determined.
    new_row = list(row)
    ### generate each possible solution to this row: ###SLOW###
    t1 = timer()
    # row_sols = smarter_generate_sols(row, clue)
    row_sols = smart_generate_sols(row, clue)
    # row_sols = generate_sols(row, clue)
    t2 = timer()
    # print((t2 - t1) * 1000)
    #########################################################

    # Check if any cells can be locked in:
    for i in range(len(row)):
        # Dont waste time unless this cell in unknown:
        if row[i] == -1:
            # See all posible values for cell i:
            cell_options = [sol[i] for sol in row_sols]
            # If there is only one unique value for this cell...
            if len(set(cell_options)) == 1:
                # change the value in solution:
                new_row[i] = cell_options[0]
    return new_row


def solve(clues, width, height):
    # Determine width and height of puzzle:
    W = len(clues[0])
    H = len(clues[1])
    # Initialize our solution, with -1 meaning unknown:
    solution = [[-1] * W for x in range(H)]

    ###Sort clues by difficulty, easiest first:
    # v = sort_clues(clues)
    v_easy,v_hard = sort_clues(clues)
    ########## Repeat the entire loop until every cell has been solved:
    #!!First go through the easy clues a few times!!
    for x in range(10):
        for cv in v_easy:
            clue = clues[cv[0]][cv[1]]
            ###Verticals:
            if cv[0] == 0:
                c = cv[1]
                # Ignore empty clues:
                if clue:
                    row = get_col(c, solution)
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        new_row = crunch_row(row, clue)
                        for i in range(H):
                            solution[i][c] = new_row[i]
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(H):
                        solution[i][c] = 0
            ###Horizontal rows:
            else:
                r = cv[1]
                # Ignore empty clues:
                if clue:
                    row = solution[r]
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        new_row = crunch_row(row, clue)
                        solution[r] = list(new_row)
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(W):
                        solution[r][i] = 0
    itercount = 0
    while any(-1 in x for x in solution) and itercount <50:
        itercount += 1
        ###Go though each clue, starting with easiest ones:
        # for cv in v:
        for cv in v_easy:
            clue = clues[cv[0]][cv[1]]
            ###Verticals:
            if cv[0] == 0:
                c = cv[1]
                # Ignore empty clues:
                if clue:
                    row = get_col(c, solution)
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        new_row = crunch_row(row, clue)
                        for i in range(H):
                            solution[i][c] = new_row[i]
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(H):
                        solution[i][c] = 0
            ###Horizontal rows:
            else:
                r = cv[1]
                # Ignore empty clues:
                if clue:
                    row = solution[r]
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        new_row = crunch_row(row, clue)
                        solution[r] = list(new_row)
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(W):
                        solution[r][i] = 0
        for cv in v_hard:
            clue = clues[cv[0]][cv[1]]
            ###Verticals:
            if cv[0] == 0:
                c = cv[1]
                # Ignore empty clues:
                if clue:
                    row = get_col(c, solution)
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        new_row = crunch_row(row, clue)
                        for i in range(H):
                            solution[i][c] = new_row[i]
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(H):
                        solution[i][c] = 0
            ###Horizontal rows:
            else:
                r = cv[1]
                # Ignore empty clues:
                if clue:
                    row = solution[r]
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        new_row = crunch_row(row, clue)
                        solution[r] = list(new_row)
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(W):
                        solution[r][i] = 0

    # Package the solution into a tuple of tuples:
    return tuple(tuple(row) for row in solution)

########### Tests #############
def do_tests():
    puzzles = get_puzzles()

    for puzzle in puzzles:
        args, solution, it = puzzle
        # test.it(it)
        print(solve(*args) == solution)


def get_puzzles():
    v_clues = ((1, 1), (4,), (1, 1, 1), (3,), (1,))
    h_clues = ((1,), (2,), (3,), (2, 1), (4,))
    args = ((v_clues, h_clues), 5, 5)

    ans = ((0, 0, 1, 0, 0),
           (1, 1, 0, 0, 0),
           (0, 1, 1, 1, 0),
           (1, 1, 0, 1, 0),
           (0, 1, 1, 1, 1))

    t1 = (args, ans, '5 x 5 puzzle')

    v_clues = ((3,), (4,), (2, 2, 2), (2, 4, 2), (6,), (3,))
    h_clues = ((4,), (6,), (2, 2), (2, 2), (2,), (2,), (2,), (2,), (), (2,), (2,))
    args = ((v_clues, h_clues), 6, 11)

    ans = ((0, 1, 1, 1, 1, 0),
           (1, 1, 1, 1, 1, 1),
           (1, 1, 0, 0, 1, 1),
           (1, 1, 0, 0, 1, 1),
           (0, 0, 0, 1, 1, 0),
           (0, 0, 0, 1, 1, 0),
           (0, 0, 1, 1, 0, 0),
           (0, 0, 1, 1, 0, 0),
           (0, 0, 0, 0, 0, 0),
           (0, 0, 1, 1, 0, 0),
           (0, 0, 1, 1, 0, 0))

    t2 = (args, ans, '6 x 11 puzzle')

    v_clues = ((1, 1, 3), (3, 2, 1, 3), (2, 2), (3, 6, 3),
               (3, 8, 2), (15,), (8, 5), (15,),
               (7, 1, 4, 2), (7, 9,), (6, 4, 2,), (2, 1, 5, 4),
               (6, 4), (2, 6), (2, 5), (5, 2, 1),
               (6, 1), (3, 1), (1, 4, 2, 1), (2, 2, 2, 2))
    h_clues = ((2, 1, 1), (3, 4, 2), (4, 4, 2), (8, 3),
               (7, 2, 2), (7, 5), (9, 4), (8, 2, 3),
               (7, 1, 1), (6, 2), (5, 3), (3, 6, 3),
               (2, 9, 2), (1, 8), (1, 6, 1), (3, 1, 6),
               (5, 5), (1, 3, 8), (1, 2, 6, 1), (1, 1, 1, 3, 2))
    args = ((v_clues, h_clues), 20, 20)

    ans = ((1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
           (0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1),
           (1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0),
           (0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0),
           (0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1),
           (0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1),
           (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0),
           (0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0),
           (0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0),
           (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0),
           (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
           (0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1),
           (1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1),
           (1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
           (1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
           (0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
           (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0),
           (0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0),
           (0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1),
           (0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1))

    t3 = (args, ans, '20 x 20 puzzle')

    tests = [t1, t2, t3]
    return tests


do_tests()
