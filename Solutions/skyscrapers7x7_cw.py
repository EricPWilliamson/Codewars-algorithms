#PASSED
# In a grid of 7 by 7 squares you want to place a skyscraper in each square with only some clues:
#
# The height of the skyscrapers is between 1 and 7
# No two skyscrapers in a row or column may have the same number of floors
# A clue is the number of skyscrapers that you can see in a row or column from the outside
# Higher skyscrapers block the view of lower skyscrapers located behind them
# Can you write a program that can solve this puzzle in time?
#
# This kata is based on 4 By 4 Skyscrapers and 6 By 6 Skyscrapers by FrankK. By now, examples should be superfluous; you should really solve Frank's kata first, and then probably optimise some more. A naive solution that solved a 4×4 puzzle within 12 seconds might need time somewhere beyond the Heat Death of the Universe for this size. It's quite bad.
#
# Task
# Create
#
# def solve_puzzle(clues)
# Clues are passed in as a list(28) of integers.
# The return value is a list(7) of list(7) of integers.
#
# All puzzles have one possible solution.
# All this is the same as with the earlier kata.
#
# Caveat: The tests for this kata have been tailored to run in ~10 seconds with the JavaScript reference solution. You'll need to do better than that! Please note the optimization tag.
#
# Conceptis Puzzles have heaps of these puzzles, from 5×5 (they don't even bother with 4×4) up to 7×7 and unsolvable within CodeWars time constraints. Old puzzles from there were used for the tests. They also have lots of other logic, numbers and mathematical puzzles, and their puzzle user interface is generally nice, very nice.
# (It is, however, Flash, and their mobile offerings are far fewer. Desktop PC recommended.)




import numpy as np
import itertools
import cProfile

N = 7

def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort='time')
    return profiled_func


def check_ans(i, ans):
    #Checks ans in the row corresponding to clue i, returns True if the row still has unknown values in it.
    if i<N:
        ans_row = [r[i] for r in ans]
    elif i<2*N:
        ans_row = ans[i-N]
    elif i<3*N:
        ans_row = [ r[3*N-1-i] for r in ans ]
    else:
        ans_row = ans[4*N-1-i]
    return (0 in ans_row)


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


def get_ans_row(i, ans):
    #Gets the row corresponding to clue i, and puts it in the order from the clue's perspective.
    if i<N:
        #return a column, top to bottom
        return [r[i] for r in ans]
    elif i<2*N:
        #return a row, right to left
        # ans_row = ans[i - N]
        return ans[i-N][::-1]
    elif i<3*N:
        #return a column, bottom to top
        # ans_row = [r[3 * N - 1 - i] for r in ans]
        return [r[3*N-1 - i] for r in reversed(ans)]
    else:
        #return a row, left to right
        # ans_row = ans[4 * N - 1 - i]
        return ans[4*N-1 - i]


def generate_permutations(ans_row):
    #Returns an iterator with all possible row permutations given what we know from ans_row.
    n_slots = sum(1 for x in ans_row if x == 0)
    unk_vals = [x for x in range(1,N+1) if x not in ans_row]

    for unk in itertools.permutations(unk_vals, n_slots):
        out = []
        j = 0
        for a in ans_row:
            if a>0:
                out += [a]
            else:
                out += [unk[j]]
                j += 1
        yield out


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


def canned_rows(clue):
    #Returns a precalculated row for opts based solely on clue value (assumes opts is in its original state). Useful for first pass on puzzle.
    if clue == 1:
        return [[0,0,0,0,0,0,7],[1,2,3,4,5,6,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,0]]
    elif clue == 2:
        return [[1,2,3,4,5,6,0],[1,2,3,4,5,0,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
    elif clue == 3:
        return [[1,2,3,4,5,0,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
    elif clue == 4:
        return [[1,2,3,4,0,0,0],[1,2,3,4,5,0,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
    elif clue == 5:
        return [[1,2,3,0,0,0,0],[1,2,3,4,0,0,0],[1,2,3,4,5,0,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
    elif clue == 6:
        return [[1,2,0,0,0,0,0],[1,2,3,0,0,0,0],[1,2,3,4,0,0,0],[1,2,3,4,5,0,0],[1,2,3,4,5,6,0],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
    elif clue == 7:
        return [[1,0,0,0,0,0,0],[0,2,0,0,0,0,0],[0,0,3,0,0,0,0],[0,0,0,4,0,0,0],[0,0,0,0,5,0,0],[0,0,0,0,0,6,0],[0,0,0,0,0,0,7]]
    else:
        return [[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]


def test_row(sol, row, clue):#HUNGRY!!
    #Checks if a proposed row solution is valid.
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


@do_cprofile
def solve_puzzle(clues):
    #Solves a 7x7 skyscraper puzzle.
    #Populate a 7x7 matrix, each cell contains a vector [1,2,3,4,5,6,7] representing the possible options in that location
    opts = np.array([[[1,2,3,4,5,6,7]]*N]*N)
    #Initialize our 7x7 matrix of answers:
    ans = [[0] * N for x in range(N)]


    n_solved = 0
    n_passes = 0
    while n_solved<N*N:
        #!!Try ranking clues by difficulty and only attempt the 5 easiest clues each time!!
        #!!If a clue has already been satisfied, remove it from rotation!!
        for i,clue in enumerate(clues):
            #First make sure we still need to examine this row:
            if check_ans(i, ans):
                # print(i,end=' ')
                row = get_row(i, opts)

                ###Special case: clue==N
                if clue == N:
                    row[:] = [[1,0,0,0,0,0,0],[2,0,0,0,0,0,0],[3,0,0,0,0,0,0],[4,0,0,0,0,0,0],[5,0,0,0,0,0,0],[6,0,0,0,0,0,0],[7,0,0,0,0,0,0]] #Using the [:] avoids breaking the reference to opts
                ###Special case: clue==1
                elif clue == 1:
                    row[0] = [N,0,0,0,0,0,0]
                else:
                    if n_passes ==0:
                        good_sols = canned_rows(clue)
                    else:
                        ###Try all 5040 possible permutations in the row and determine which ones fit this clue: !!Try to avoid permutations that we already know are invalid
                        ans_row = get_ans_row(i, ans)
                        # row_iter = generate_permutations(ans_row)
                        good_sols = [[]]*N
                        # for hyp_sol in itertools.permutations([1,2,3,4,5,6,7], N):
                        for hyp_sol in generate_permutations(ans_row):
                            #Test hypothetical solution:
                            if test_row(hyp_sol, row, clue):
                                #Also check the clue opposite this one:
                                opp_i = get_opposite(i)
                                if test_row(hyp_sol[::-1], get_row(opp_i,opts), clues[opp_i]):
                                    good_sols = [good_sols[k] + [hyp_sol[k]] for k in range(N)] #HUNGRY!!
                    #Are there any values missing from the good_sols? Eliminate them from the row:
                    for k in range(N):
                        for j in range(N):
                            if not row[k][j] in good_sols[k]:
                                row[k][j] = 0

                ###For each solved square, eliminate it's value from the other spots in its row and column: !unnecessary, but may improve speed!
                for r in range(N):
                    for c in range(N):
                        opts = remove_dupes(r,c,opts)

                ###Determine how many squares of the puzzle are complete, and put solved values into ans:
                for r in range(N):
                    for c in range(N):
                        if ans[r][c] == 0:
                            if sum(1 for x in opts[r][c] if x > 0) == 1:
                                n_solved += 1
                                ans[r][c] = max(opts[r][c])
        n_passes += 1
        # print(' ')
        # print(n_solved)

    return ans


####################################### Example Tests ##########################################33
def assert_equals(A,B):
    print(A==B)
    return []

# Test.describe("7x7")
# Test.it("medium")
assert_equals(
  solve_puzzle([7,0,0,0,2,2,3, 0,0,3,0,0,0,0, 3,0,3,0,0,5,0, 0,0,0,0,5,0,4]),
  [ [1,5,6,7,4,3,2],
    [2,7,4,5,3,1,6],
    [3,4,5,6,7,2,1],
    [4,6,3,1,2,7,5],
    [5,3,1,2,6,4,7],
    [6,2,7,3,1,5,4],
    [7,1,2,4,5,6,3] ]
);
# Test.it("very hard")
assert_equals(
  solve_puzzle([0,2,3,0,2,0,0, 5,0,4,5,0,4,0, 0,4,2,0,0,0,6, 5,2,2,2,2,4,1]), # for a _very_ hard puzzle, replace the last 7 values with zeroes
  [ [7,6,2,1,5,4,3],
    [1,3,5,4,2,7,6],
    [6,5,4,7,3,2,1],
    [5,1,7,6,4,3,2],
    [4,2,1,3,7,6,5],
    [3,7,6,2,1,5,4],
    [2,4,3,5,6,1,7] ]
);


########################### My research #######################################

# ####If opts is still untouched, how many viable rows does each clue value produce?
# for clue in range(1,8):
#     row = [[1, 2, 3, 4, 5, 6, 7] for x in range(N)]
#     n_good = 0
#     good_sols = [[]] * N
#     for hyp_sol in itertools.permutations([1,2,3,4,5,6,7], N):
#         #Test hypothetical solution:
#         if test_row(hyp_sol, row, clue):
#             n_good += 1
#             good_sols = [good_sols[k] + [hyp_sol[k]] for k in range(N)] #HUNGRY!!
#     # print("{0:d},{1:d}".format(clue,n_good))
#
#     # Are there any values missing from the good_sols? Eliminate them from the row:
#     for k in range(N):
#         for j in range(N):
#             if not row[k][j] in good_sols[k]:
#                 row[k][j] = 0
#     print(clue)
#     print(row)
#
# row = [[1, 2, 3, 4, 5, 6, 7] for x in range(N)]
# print(row)


