#PASSED but not efficient enough for multidimensional puzzles
# Task
# Complete the function solve(clues) that solves 15-by-15 Nonogram puzzles.
#
# Your algorithm has to be clever enough to solve all puzzles in time.
#
# As in 5x5 Nonogram Solver, the input format will look like this:
#
# input = tuple(column_clues, row_clues)
#
# each of (row_clues, column_clues) = tuple(
#   tuple(num_of_ones_in_a_row, ...),
#   ...
# )

# Notes
# Some puzzles may have lines with no cells filled. Most Nonogram games show the clues for such lines as a single zero,
#  but the clue for such a line is represented as a zero-length tuple for the sake of this Kata.


import itertools

def partitions(n, k):
    #https://stackoverflow.com/questions/28965734/general-bars-and-stars
    #Usage: Example usage 3 [0]s and 4 slots
    # for p in partitions(3, 4):
    #     print(p)
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]


def sort_clues(clues):
    #Judges the difficulty of each clue by calculating the number of free [0]s and sorts them easiest to hardest.
    #Usage: clue_i = clues[v[i][0]][v[i][1]]
    # Determine width and height of puzzle:
    W = len(clues[0])
    H = len(clues[1])
    ###Look at each clue and determine diff:
    diffs = []
    #Start with column clues:
    for clue in clues[0]:
        if clue:
            marbles = H - sum(clue) - (len(clue) - 1)  # Number of extra [0]s
        else:
            #Empty clues are the easiest
            marbles = 0
        diffs += [marbles]
    #Now do row clues:
    for clue in clues[1]:
        if clue:
            marbles = W - sum(clue) - (len(clue) - 1)  # Number of extra [0]s
        else:
            #Empty clues are easiest
            marbles = 0
        diffs += [marbles]
    ###Create vector of indices, sorted on difficulty:
    diff_order = sorted((e, i) for i, e in enumerate(diffs))
    v = []
    for x in diff_order:
        i = x[1]
        if i<W:
            v += [[0,i]]
        else:
            v += [[1,i-W]]
    return v


def get_col(c, solution):
    # Gets a vertical column at index c from our 2d matrix, solution.
    row = [x[c] for x in solution]
    return row


def smart_generate_sols(row, clue):
    # Generates all valid combos for this row
    # Find all combos that fit this row's clue, using the stars and bars method
    sol_list = []
    bins = len(clue)+1 #Number of slots for extra [0]s
    marbles = len(row) - sum(clue) - (len(clue)-1) #Number of extra [0]s
    for p in partitions(marbles, bins):
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

    return sol_list


def solve(clues):
    # Determine width and height of puzzle:
    W = len(clues[0])
    H = len(clues[1])
    # Initialize our solution, with -1 meaning unknown:
    solution = [[-1] * W for x in range(H)]

    ###Sort clues by difficulty, easiest first:
    v = sort_clues(clues)
    ########## Repeat the entire loop until every cell has been solved:
    itercount = 0
    while any(-1 in x for x in solution) and itercount <50:
        itercount += 1
        ###Go though each clue, starting with easiest ones:
        for cv in v:
            clue = clues[cv[0]][cv[1]]
            ###Verticals:
            if cv[0] == 0:
                c = cv[1]
                # Ignore empty clues:
                if clue:
                    row = get_col(c, solution)
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        # generate each possible solution to this row:
                        row_sols = smart_generate_sols(row, clue)
                        # row_sols = generate_sols(row, clue)

                        # Check if any cells can be locked in:
                        for i in range(len(row)):
                            # Dont waste time unless this cell in unknown:
                            if row[i] == -1:
                                # See all posible values for cell i:
                                cell_options = [sol[i] for sol in row_sols]
                                # If there is only one unique value for this cell...
                                if len(set(cell_options)) == 1:
                                    # change the value in solution:
                                    solution[i][c] = cell_options[0]
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(W):
                        solution[i][c] = 0

            ###Horizontal rows:
            else:
                r = cv[1]
                # Ignore empty clues:
                if clue:
                    row = solution[r]
                    # Dont waste time on rows that are already solved
                    if -1 in row:
                        # generate each possible solution to this row:
                        # row_sols = generate_sols(row, clue)
                        row_sols = smart_generate_sols(row, clue)
                        # Check if any cells can be locked in:
                        for i in range(len(row)):
                            # Dont waste time unless this cell in unknown:
                            if row[i] == -1:
                                # See all posible values for cell i:
                                cell_options = [sol[i] for sol in row_sols]
                                # If there is only one unique value for this cell...
                                if len(set(cell_options)) == 1:
                                    # change the value in solution:
                                    solution[r][i] = cell_options[0]
                else:
                    # An empty clue means the row is all [0]s:
                    for i in range(H):
                        solution[r][i] = 0

    ####################### Old, unsorted method ###################
    # # Repeat the entire loop until every cell has been solved:
    # itercount = 0
    # while any(-1 in x for x in solution) and itercount <50:
    #     itercount += 1
    #     ###!!Go though each column, starting with whichever has the least marbles
    #     ###Go through each column, from left to right:
    #     for c, clue in enumerate(clues[0]):
    #         #Ignore empty clues:
    #         if clue:
    #             row = get_col(c, solution)
    #             #Dont waste time on rows that are already solved
    #             if -1 in row:
    #                 # generate each possible solution to this row:
    #                 row_sols = smart_generate_sols(row, clue)
    #                 # row_sols = generate_sols(row, clue)
    #
    #                 # Check if any cells can be locked in:
    #                 for i in range(len(row)):
    #                     # Dont waste time unless this cell in unknown:
    #                     if row[i] == -1:
    #                         # See all posible values for cell i:
    #                         cell_options = [sol[i] for sol in row_sols]
    #                         # If there is only one unique value for this cell...
    #                         if len(set(cell_options)) == 1:
    #                             # change the value in solution:
    #                             solution[i][c] = cell_options[0]
    #         else:
    #             #An empty clue means the row is all [0]s:
    #             for i in range(W):
    #                 solution[i][c] = 0
    #
    #     ###Go through each row, from top to bottom:
    #     for r, clue in enumerate(clues[1]):
    #         # Ignore empty clues:
    #         if clue:
    #             row = solution[r]
    #             # Dont waste time on rows that are already solved
    #             if -1 in row:
    #                 # generate each possible solution to this row:
    #                 # row_sols = generate_sols(row, clue)
    #                 row_sols = smart_generate_sols(row,clue)
    #                 # Check if any cells can be locked in:
    #                 for i in range(len(row)):
    #                     # Dont waste time unless this cell in unknown:
    #                     if row[i] == -1:
    #                         # See all posible values for cell i:
    #                         cell_options = [sol[i] for sol in row_sols]
    #                         # If there is only one unique value for this cell...
    #                         if len(set(cell_options)) == 1:
    #                             # change the value in solution:
    #                             solution[r][i] = cell_options[0]
    #         else:
    #             # An empty clue means the row is all [0]s:
    #             for i in range(H):
    #                 solution[r][i] = 0
    ######################################################################################################

    # Package the solution into a tuple of tuples:
    return tuple(tuple(row) for row in solution)


# test.describe('15x15 Nonograms')
# test.it('Sample Tests')
solution = (
    (0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0),
    (1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0),
    (1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1),
    (1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1),
    (1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0),
    (0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0),
    (1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0),
    (1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1),
    (1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1),
    (0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1)
)
clues = (
    (
        (4, 3), (1, 6, 2), (1, 2, 2, 1, 1), (1, 2, 2, 1, 2), (3, 2, 3),
        (2, 1, 3), (1, 1, 1), (2, 1, 4, 1), (1, 1, 1, 1, 2), (1, 4, 2),
        (1, 1, 2, 1), (2, 7, 1), (2, 1, 1, 2), (1, 2, 1), (3, 3)
    ), (
        (3, 2), (1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 1, 1, 3), (1, 1, 2, 1),
        (2, 3, 1, 2), (9, 3), (2, 3), (1, 2), (1, 1, 1, 1),
        (1, 4, 1), (1, 2, 2, 2), (1, 1, 1, 1, 1, 1, 2), (2, 1, 1, 2, 1, 1), (3, 4, 3, 1)
    )
)
print(solve(clues) == solution)
