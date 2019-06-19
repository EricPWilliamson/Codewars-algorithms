#PASSED but not efficient enough for 15x15 puzzles

# Once you complete this kata, there is a 15x15 Version that you can try. And once you complete that, you can do the Multisize Version which goes up to 50x50.
#
# Description
# For this kata, you will be making a Nonogram solver. :)
#
# If you don't know what Nonograms are, you can look at some instructions and also try out some Nonograms here.
#
# For this kata, you will only have to solve 5x5 Nonograms. :)
#
# Instructions
# You need to complete the Nonogram class and the solve method:
#
# class Nonogram:
#
#     def __init__(self, clues):
#         pass
#
#     def solve(self):
#         pass
# You will be given the clues and you should return the solved puzzle. All the puzzles will be solveable so you will not need to worry about that.
#
# The clues will be a tuple of the horizontal clues, then the vertical clues, which will contain the individual clues. For example, for the Nonogram:
#
#     |   |   | 1 |   |   |
#     | 1 |   | 1 |   |   |
#     | 1 | 4 | 1 | 3 | 1 |
# -------------------------
#   1 |   |   |   |   |   |
# -------------------------
#   2 |   |   |   |   |   |
# -------------------------
#   3 |   |   |   |   |   |
# -------------------------
# 2 1 |   |   |   |   |   |
# -------------------------
#   4 |   |   |   |   |   |
# -------------------------
# The clues are on the top and the left of the puzzle, so in this case:
#
# The horizontal clues are: ((1, 1), (4,), (1, 1, 1), (3,), (1,)),
# and the vertical clues are: ((1,), (2,), (3,), (2, 1), (4,)).
# The horizontal clues are given from left to right. If there is more than one clue for the same column,
#  the upper clue is given first. The vertical clues are given from top to bottom. If there is more than one clue for
#  the same row, the leftmost clue is given first.
#
# Therefore, the clue given to the __init__ method would be
# (((1, 1), (4,), (1, 1, 1), (3,), (1,)), ((1,), (2,), (3,), (2, 1), (4,)))
#  You are given the horizontal clues first then the vertical clues second.
#
# You should return a tuple of the rows as your answer. In this case, the solved Nonogram looks like:
#
#     |   |   | 1 |   |   |
#     | 1 |   | 1 |   |   |
#     | 1 | 4 | 1 | 3 | 1 |
# -------------------------
#   1 |   |   | # |   |   |
# -------------------------
#   2 | # | # |   |   |   |
# -------------------------
#   3 |   | # | # | # |   |
# -------------------------
# 2 1 | # | # |   | # |   |
# -------------------------
#   4 |   | # | # | # | # |
# -------------------------
# In the tuple, you should use 0 for a unfilled square and 1 for a filled square. Therefore, in this case, you should return:
#
# ((0, 0, 1, 0, 0),
#  (1, 1, 0, 0, 0),
#  (0, 1, 1, 1, 0),
#  (1, 1, 0, 1, 0),
#  (0, 1, 1, 1, 1))
# Good Luck!!
#
# If there is anything that is unclear or confusing, just let me know :)

class Nonogram:

    def __init__(self, clues):
        #__init__ allows the class to accept a parameter
        self._clues = clues
        pass


    def get_col(self, c, solution):
        #Gets a vertical column at index c from our 2d matrix, solution.
        row = [x[c] for x in solution]
        return row


    def test_row(self, row, clue):
        #Determine if the proposed row solution matches the clue
        result = [] #Will become the clue that actually matches this row
        seq_cnt = 0 #counts the length of a sequence of 1s
        for val in row:
            if val == 1:
                seq_cnt += 1
            else:
                # Add seq length to result
                if seq_cnt > 0:
                    result += [seq_cnt]
                seq_cnt = 0
        #Add seq length to result
        if seq_cnt > 0:
            result += [seq_cnt]
        return (list(clue) == result)


    def generate_sols(self, row, clue):
        #Generates all valid combos for this row.
        #First generate all possible combos for this row (ignoring the clue):
        row_sols = [[]]
        for val in row:
            if val == -1:
                #We need to double the number of solutions:
                for i in range(len(row_sols)):
                    #add a new row with a 1 appended:
                    row_sols += [row_sols[i] + [1]]
                    #append a 0 to the original:
                    row_sols[i] += [0]
            else:
                for i in range(len(row_sols)):
                    # Just append the known value to all solutions:
                    row_sols[i] += [val]

        #Check row_sols against our clue:
        valid_sols = []
        for sol in row_sols:
            if self.test_row(sol, clue):
                valid_sols += [sol]
        return valid_sols


    def solve(self):
        #Determine width and height of puzzle:
        W = len(self._clues[0])
        H = len(self._clues[1])
        #Initialize our solution, with -1 meaning unknown:
        solution = [[-1]*W for x in range(H)]

        #Repeat the entire loop until every cell has been solved:
        while any(-1 in x for x in solution):
            ###Go through each column, from left to right:
            for c,clue in enumerate(self._clues[0]):
                row = self.get_col(c, solution)
                #generate each possible solution to this row:
                row_sols = self.generate_sols(row, clue)
                #Check if any cells can be locked in:
                for i in range(len(row)):
                    #Dont waste time unless this cell in unknown:
                    if row[i] == -1:
                        #See all posible values for cell i:
                        cell_options = [sol[i] for sol in row_sols]
                        #If there is only one unique value for this cell...
                        if len(set(cell_options)) == 1:
                            #change the value in solution:
                            solution[i][c] = cell_options[0]

            ###Go through each row, from top to bottom:
            for r,clue in enumerate(self._clues[1]):
                row = solution[r]
                # generate each possible solution to this row:
                row_sols = self.generate_sols(row, clue)
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

        # Package the solution into a tuple of tuples:
        return tuple(tuple(row) for row in solution)


# test.it('Test 1')
clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
         ((1,), (2,), (3,), (2, 1), (4,)))

ans = ((0, 0, 1, 0, 0),
       (1, 1, 0, 0, 0),
       (0, 1, 1, 1, 0),
       (1, 1, 0, 1, 0),
       (0, 1, 1, 1, 1))

print(Nonogram(clues).solve() == ans)

# test.it('Test 2')
clues = (((1,), (3,), (1,), (3, 1), (3, 1)),
         ((3,), (2,), (2, 2), (1,), (1, 2)))

ans = ((0, 0, 1, 1, 1),
       (0, 0, 0, 1, 1),
       (1, 1, 0, 1, 1),
       (0, 1, 0, 0, 0),
       (0, 1, 0, 1, 1))

print(Nonogram(clues).solve() == ans)

# test.it('Test 3')
clues = (((3,), (2,), (1, 1), (2,), (4,)),
         ((2,), (3, 1), (1, 2), (3,), (1,)))

ans = ((1, 1, 0, 0, 0),
       (1, 1, 1, 0, 1),
       (1, 0, 0, 1, 1),
       (0, 0, 1, 1, 1),
       (0, 0, 0, 0, 1))

print(Nonogram(clues).solve() == ans)
