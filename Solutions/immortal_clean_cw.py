"""
In the nation of CodeWars, there lives an Elder who has lived for a long time. Some people call him the Grandpatriarch, but most people just refer to him as the Elder.

There is a secret to his longetivity: he has a lot of young worshippers, who regularly perform a ritual to ensure that the Elder stays immortal:

The worshippers lines up in a magic rectangle, of dimensions m and n.
They channel their will to wish for the Elder. In this magic rectangle, any worshipper can donate time equal to the xor of the column and the row (zero-indexed) he's on, in seconds, to the Elder.
However, not every ritual goes perfectly. The donation of time from the worshippers to the Elder will experience a transmission loss l (in seconds). Also, if a specific worshipper cannot channel more than l seconds, the Elder will not be able to receive this worshipper's donation.
The estimated age of the Elder is so old it's probably bigger than the total number of atoms in the universe. However, the lazy programmers (who made a big news by inventing the Y2K bug and other related things) apparently didn't think thoroughly enough about this, and so their simple date-time system can only record time from 0 to t-1 seconds. If the elder received the total amount of time (in seconds) more than the system can store, it will be wrapped around so that the time would be between the range 0 to t-1.

Given m, n, l and t, please find the number of seconds the Elder has received, represented in the poor programmer's date-time system.

Example:

m=8, n=5, l=1, t=100

Let's draw out the whole magic rectangle:
0 1 2 3 4 5 6 7
1 0 3 2 5 4 7 6
2 3 0 1 6 7 4 5
3 2 1 0 7 6 5 4
4 5 6 7 0 1 2 3

Applying a transmission loss of 1:
0 0 1 2 3 4 5 6
0 0 2 1 4 3 6 5
1 2 0 0 5 6 3 4
2 1 0 0 6 5 4 3
3 4 5 6 0 0 1 2

Adding up all the time gives 105 seconds.

Because the system can only store time between 0 to 99 seconds, the first 100 seconds of time will be lost, giving the answer of 5.
This is no ordinary magic (the Elder's life is at stake), so you need to care about performance. All test cases (900 tests) can be passed within 1 second, but naive solutions will time out easily. Good luck, and do not displease the Elder.
"""

import numpy as np

def add_nxn(n):
    # Returns the tallies by number of bits for a square n x n grid, where n is a power of 2
    b = n.bit_length() - 1
    return np.array([ n //2 ] *b, dtype=np.uint64)


def row_sum(d, subd, i, j, l):
    # Returns the sum of one row of a piece of [d]
    if subd == 1:
        return max([(i ^ j) + d - l, 0])
    idx = i ^ j
    d2 = d + subd - 1
    # Calc sum of sequence from (d+idx*subd-l):(d2+idx*subd-l)
    low = max([(d + idx * subd - l - 1), 0])
    high = max([(d2 + idx * subd - l), 0])
    return high * (high + 1) // 2 - low * (low + 1) // 2


def next_biggest(d, l, r, c, i, j):
    #The square [d] can be broken down into 2**n x 2**n pieces. Goes through [d] and takes the biggest pieces that are
    #  covered by our range
    ex_sum = 0
    while r > 0 and c > 0:
        if c >= r:
            max_bxb = c.bit_length() - 1
            subd = 2 ** max_bxb
            if r <= subd:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * r
            else:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * subd
                ex_sum += next_biggest(d, l, r - subd, subd, i + subd, j)
            c -= subd
            j += subd
        else:
            max_bxb = r.bit_length() - 1
            subd = 2 ** max_bxb
            if c <= subd:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * c
            else:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * subd
                ex_sum += next_biggest(d, l, subd, c - subd, i, j + subd)
            r -= subd
            i += subd
    return ex_sum


def cell_by_cell(bc, n_rows, n_cols, l):
    #Goes through a [d] that isn't completely contained within our range, adding up the final sum
    d = 2 ** bc  # d is both the side length of [d] and the smallest value within
    n_rows = min([d, n_rows])
    n_cols = min([d, n_cols])
    sml = min([n_rows, n_cols])
    big = max([n_rows, n_cols])
    return next_biggest(d, l, sml, big, 0, 0)


def check_square(idx, n, m_row, m_col, is_set, l, t):
    # Checks a square area where we don't have all the rows and columns
    bc = n.bit_length() - 1
    if is_set:
        i_row = idx * n
        i_col = idx * n
    else:
        i_row = 2 * idx * n
        i_col = (2 * idx + 1) * n
    n_rows = min([m_row - i_row, n])
    n_cols = min([m_col - i_col, n])
    # Special case: no hits:
    if n_rows < 1 or n_cols < 1:
        return [], 0
    # Return a pc_list or ex_sum based on conditions:
    if is_set:
        if n_rows >= n and n_cols >= n:
            # Just calculate the entire set:
            return add_nxn(n), 0
        else:
            # Break down the set into its components:
            ex_sum = elder_age_half(n_cols, n_rows, l, t)
            return [], ex_sum
    else:  # The non-sets...
        if n_rows >= n:
            # Add entire columns:
            pc_list = np.zeros(bc + 1, dtype=np.uint64)
            pc_list[bc] += n_cols
            return pc_list, 0
        elif n_cols >= n:
            # Add entire rows:
            pc_list = np.zeros(bc + 1, dtype=np.uint64)
            pc_list[bc] += n_rows
            return pc_list, 0
        else:
            # Go cell by cell
            ex_sum = cell_by_cell(bc, n_rows, n_cols, l)
            return [], ex_sum


def grand_total(pc_list, ex_sum, l, t):
    # Convert pc_list into a single integer and add on ex_sum
    tot = 0
    # Start with the segment of pc_list that might be split by l:
    minb = (l + 1).bit_length() - 1
    d2 = 2 ** (minb + 1) - l
    tot += (d2 * (d2 - 1) // 2) * int(pc_list[minb])
    # Now add the following segments:
    for i, n in enumerate(pc_list[minb + 1:]):
        b = minb + 1 + i
        d2 = 2 ** (b + 1) - l
        d1 = 2 ** (b) - l
        tot += (d2 * (d2 - 1) // 2 - d1 * (d1 - 1) // 2) * int(n)
    return (tot + ex_sum) % t


def elder_age_half(m, n, l, t):
    #The table can be split along the diagonal. Calculates the sum on the larger side of the diagonal.
    # Most parts of the grid contain equal numbers of integers grouped by bit-length (eg. a 4x4 grid of the
    #  numbers 4 thru 7). Keep track of the number of members in each such group using the array pc_list.
    big = max([m, n])
    sml = min([m, n])
    maxbc = (big - 1).bit_length()
    smlbc = sml.bit_length()
    if 2 ** maxbc - 1 <= l:# Special case: l is bigger than the max possible cell value:
        return 0
    ex_sum = 0
    pc_list = np.zeros(maxbc, dtype=np.uint64)
    # Start with the biggest complete 2**b x 2**b square:
    A = add_nxn(2 ** (smlbc - 1))
    pc_list[:len(A)] += A
    # Check sections of the remaining 2**b x 2**b squares:
    for bc in range(smlbc - 1, maxbc):
        d = 2 ** bc
        #Checks a square with numbers of one single bit-length:
        A, x = check_square(0, d, sml, big, False, l, t)
        if any(A):
            pc_list[:len(A)] += A
        ex_sum += x
        # Check the mixed set below that square:
        A, x = check_square(1, d, sml, big, True, l, t)
        if any(A):
            pc_list[:len(A)] += A
        ex_sum += x
    return grand_total(pc_list, ex_sum, l, t)


def elder_age(m, n, l, t):
    #Calculates the final answer to the problem.
    sml = min([m, n])
    return (elder_age_half(m, n, l, t) + elder_age_half(sml, sml, l, t)) % t


############################### Example tests ################################################
class MyTest:
    def describe(self, s):
        print(s)

    def assert_equals(self, output, answer):
        print(output == answer)
        if output != answer:
            print(output)
            print(answer)
            print(output-answer)

test = MyTest()

test.describe('Example tests')
test.assert_equals(elder_age(8,5,1,100), 5)
test.assert_equals(elder_age(8,8,0,100007), 224)
test.assert_equals(elder_age(25,31,0,100007), 11925)
test.assert_equals(elder_age(5,45,3,1000007), 4323)
test.assert_equals(elder_age(31,39,7,2345), 1586)
test.assert_equals(elder_age(545,435,342,1000007), 808451)
test.assert_equals(elder_age(28827050410, 35165045587, 7109602, 13719506), 5456283)

####Tricky CW tests:
# The Elder says:
m=53
n=42
l=18
t=131 #l is large enough to create negative values in row_sum
test.assert_equals(elder_age(m,n,l,t), 106)
