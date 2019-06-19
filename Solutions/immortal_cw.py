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

# #For n x n square grids, one half's bit count totals can be tallied up as follows:
# bc = 3
# d = 2**bc
# n = 13
# # y = n//4 + (n+1)//4 #2 bit count
# # y = n//8 + (n+1)//8 + (n+2)//8 + (n+3)//8 #3 bit count
# # y = n//16 + (n+1)//16 + (n+2)//16 + (n+3)//16 + (n+4)//16 + (n+5)//16 + (n+6)//16 + (n+7)//16 #4 bit count
# #Expandable eqn:
# count = 0
# for k in range(d//2):
#     count += (n+k)//d
#
# #Summation of numbers within that bc:
# bintot = ((2**bc-1)*2**bc)//2 - (2**(bc-1)*(2**(bc-1)-1))//2

import numpy as np
# import cProfile
#
#
# def do_cprofile(func):
#     def profiled_func(*args, **kwargs):
#         profile = cProfile.Profile()
#         try:
#             profile.enable()
#             result = func(*args, **kwargs)
#             profile.disable()
#             return result
#         finally:
#             profile.print_stats(sort='time')
#     return profiled_func


def add_nxn(n):
    #Returns the tallies by number of bits for a square n x n grid.
    #Special case: n is a power of 2:
    if ((n & (n - 1)) == 0) and n != 0:
        b = n.bit_length()-1
        return np.array([n//2]*b, dtype=np.uint64)

    #!!Avoid this part, it's too slow:
    pc_list = []
    bc = 0
    d = 2**bc
    while d<n:
        bc += 1
        d = 2 ** bc
        # Expandable eqn:
        count = 0
        for k in range(d // 2):
            count += (n + k) // d
        pc_list += [count]
    return np.array(pc_list, dtype=np.uint64)


def cell_by_cell(bc, n_rows, n_cols, l, t):
    #Looks at an incomplete [bc] and tallies up individual cells.
    d = 2**bc
    n_rows = min([d, n_rows])
    n_cols = min([d, n_cols])
    ex_sum = 0
    #Go through each cell in our range:
    for r in range(n_rows):
        for c in range(n_cols):
            real_c = c + d
            #Calc xor and subtract loss
            xorval = (r^real_c)-l
            if xorval>0:
                ex_sum += xorval
    return ex_sum


def row_sum(d,subd,i,j,l):
    #Returns the sum of one row in a chopped [n]
    if subd==1:
        return max([(i^j) + d - l, 0])
    idx = i^j
    d2 = d + subd - 1
    #Calc sum of sequence from (d+idx*subd-l):(d2+idx*subd-l)
    low = max([(d + idx*subd - l - 1), 0])
    high = max([(d2 + idx*subd - l), 0])
    return high*(high+1)//2 - low*(low+1)//2


def new_cell_by_cell(bc, n_rows, n_cols, l, t):
    #Breaks a [bc] in 2**n length boxes to calc total:
    d = 2**bc #d is both the side length of [bc] and the smallest value within
    n_rows = min([d, n_rows])
    n_cols = min([d, n_cols])
    sml = min([n_rows,n_cols])
    big = max([n_rows,n_cols])
    ex_sum = 0

    c = big
    while c>0:
        # Take the next biggest rectangle:
        max_bxb = c.bit_length() - 1
        subd = 2 ** max_bxb
        print(subd)
        # Add each row to sum:
        i = 0  # first row
        j = (big - c) // subd
        r = sml
        while r > subd:
            if subd == 1:#Faster to check this here, rather than in row_sum.
                ex_sum += i^j + d - l #!!Rather slow
            else:
                ex_sum += row_sum(d, subd, i, j, l) * subd
            r -= subd
            i += 1
        ex_sum += row_sum(d, subd, i, j, l) * r
        c -= subd
    return ex_sum


def next_biggest(d,l,r,c,i,j):
    ex_sum = 0
    while r > 0 and c > 0:
        # Start with largest dimension:
        if c >= r:
            max_bxb = c.bit_length() - 1
            subd = 2 ** max_bxb
            if r <= subd:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * r
            else:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * subd
                # Bifurcate into the following state, to get everything below this row:
                # c = subd
                # r -= subd
                # i += subd
                # j = j
                ex_sum += next_biggest(d,l, r-subd, subd, i+subd, j)
            c -= subd
            j += subd
        else:
            max_bxb = r.bit_length() - 1
            subd = 2 ** max_bxb
            if c <= subd:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * c
            else:
                ex_sum += row_sum(d, subd, i // subd, j // subd, l) * subd
                #Bifurcate to get everything to the right of this column:
                ex_sum += next_biggest(d,l, subd, c-subd, i, j+subd)
            r -= subd
            i += subd
    return ex_sum


def cell_by_cell3(bc, n_rows, n_cols, l, t):
    #Breaks a [bc] in 2**n length boxes to calc total. Can rotate to minimize calls to row_sum.
    d = 2**bc #d is both the side length of [bc] and the smallest value within
    n_rows = min([d, n_rows])
    n_cols = min([d, n_cols])
    sml = min([n_rows,n_cols])
    big = max([n_rows,n_cols])
    return next_biggest(d,l, sml,big, 0,0)


def check_square(idx, n, m_row, m_col, is_set, l, t):
    #Checks a square area where we don't have all the rows and columns
    bc = n.bit_length()-1
    if is_set:
        i_row = idx*n
        i_col = idx*n
    else:
        i_row = 2*idx*n
        i_col = (2*idx+1)*n
    n_rows = min([m_row-i_row, n])
    n_cols = min([m_col-i_col, n])
    #Special case: no hits:
    if n_rows < 1 or n_cols < 1:
        return [],0
    #Return a pc_list or ex_sum based on conditions:
    if is_set:
        if n_rows >= n and n_cols >= n:
            #Just calculate the entire set:
            return add_nxn(n), 0
        else:
            #Break down the set into its components:
            ex_sum = elder_age_real(n_cols, n_rows, l, t, skip_small=True)
            return [], ex_sum
    else: #The non-sets...
        if n_rows >= n:
            #Add entire columns:
            pc_list = np.zeros(bc+1, dtype=np.uint64)
            pc_list[bc] += n_cols
            return pc_list, 0
        elif n_cols >= n:
            #Add entire rows:
            pc_list = np.zeros(bc + 1, dtype=np.uint64)
            pc_list[bc] += n_rows
            return pc_list, 0
        else:
            #Go cell by cell
            # ex_sum = new_cell_by_cell(bc, n_rows, n_cols, l, t)
            ex_sum = cell_by_cell3(bc, n_rows, n_cols, l, t)
            return [], ex_sum


def grand_total(pc_list, ex_sum, l, t):
    #Convert pc_list into a single integer and add on ex_sum
    tot = 0
    #Start with the segment of pc_list that might be split by l:
    minb = (l+1).bit_length() - 1
    d2 = 2**(minb+1)-l
    tot += (d2 * (d2 - 1) // 2) * int(pc_list[minb])
    #Now add the following segments:
    for i, n in enumerate(pc_list[minb+1:]):
        b = minb + 1 + i
        d2 = 2 ** (b + 1) - l
        d1 = 2 ** (b) - l
        tot += (d2 * (d2 - 1) // 2 - d1 * (d1 - 1) // 2) * int(n)
    return (tot + ex_sum) % t


def elder_age_real(m,n,l,t,skip_small=False):
    #Finds the age of the wizard.

    #First get basic dimensions:
    big = max([m,n])
    sml = min([m,n])
    maxbc = (big - 1).bit_length()
    smlbc = sml.bit_length()
    # Special case: l is bigger than the max possible cell value:
    if 2**maxbc-1 <= l:
        return 0

    if not skip_small:
        #First tally counts by number of bits for the smaller side:
        pc_list_sml = add_nxn(sml)#!This is slow, avoid using it
    else:
        pc_list_sml = np.zeros(1, dtype=np.uint64)

    ###(NEW) Tally counts for bigger side:
    ex_sum = 0
    pc_list_big = np.zeros(maxbc, dtype=np.uint64)
    #Start with the biggest complete 2**b x 2**b square:
    A = add_nxn(2**(smlbc-1))
    pc_list_big[:len(A)] += A

    #Check sections of the next 2**b x 2**b square:
    for bc in range(smlbc-1,maxbc):
        d = 2**bc
        #Check the 0th [d]:
        A, x = check_square(0, d, sml, big, False, l, t)
        if any(A):
            pc_list_big[:len(A)] += A
        ex_sum += x
        # Check the set below that square:
        A, x = check_square(1, d, sml, big, True, l, t)  # the 1th (dxd) set
        if any(A):
            pc_list_big[:len(A)] += A
        ex_sum += x

    ###Calculate grand total:
    pc_list_big[:len(pc_list_sml)] += pc_list_sml
    return grand_total(pc_list_big, ex_sum, l, t)
    #######################################################################################################

# @do_cprofile
def elder_age(m,n,l,t):
    # return elder_age_real(m, n, l, t)
    #!!use skip_small=True to avoid slow call of add_nxn:
    sml = min([m,n])
    return (elder_age_real(m,n,l,t,True) + elder_age_real(sml,sml,l,t,True)) % t

# def get_counts(m,n):
#     #Just counts the occurances of each integer in the grid.
#     val_list = []
#     for i in range(m):
#         for j in range(n):
#             # add the xor product to our list:
#             val_list += [i ^ j]
#
#     # for x in range(100):
#     #     counts[x] = val_list.count(x)
#
#     counts = [val_list.count(x) for x in range(100)]
#     return counts


########################## my stuff ####################
# ans = elder_age(27, 7, 0, 137100)
# n_cols = 31
# for n_rows in range(30):
#     ans = cell_by_cell(5, n_rows, n_cols, 0, 100000)
#     # print("{0:d}  {1:d}".format(n_rows,ans))
#     print("{0:16b}".format(ans))
#
# for r in range(n_rows):
#     for c in range(n_cols):
#         real_c = c + d
#         # Calc xor and subtract loss
#         xorval = (r ^ real_c) - l
#         if xorval > 0:
#             ex_sum += xorval

# ans = add_nxn(17)

# c = get_counts(5,5)
#
# cmat = np.zeros((100,20))
# for n in range(1,21):
#     c = get_counts(n,n)
#     cmat[:,n-1] = list(c)
#
#
# #copy matrix to clipboard:
# import pandas
# # copy_mat = np.array([nwMet, neMet, swMet, seMet])
# copy_mat = cmat
# pandas.DataFrame(data=copy_mat).to_clipboard(index=False, excel=True)


# ### Print eqn output:
# bc = 1
# d = 2**bc
# for n in range(1,21):
#     # y = n//4 + (n+1)//4 #2 bit count
#     # y = n//8 + (n+1)//8 + (n+2)//8 + (n+3)//8 #3 bit count
#     # y = n//16 + (n+1)//16 + (n+2)//16 + (n+3)//16 + (n+4)//16 + (n+5)//16 + (n+6)//16 + (n+7)//16 #4 bit count
#
#     #Expandable eqn:
#     y = 0
#     for k in range(d//2):
#         y += (n+k)//d
#
#     print(y, end='  ')
# print('')
#
# ###Print n x n values:
# n = 63
# for r in range(n):
#     for c in range(n):
#         print("{:2d}".format(r^c), end='  ')
#     print('')

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

# test.describe('Example tests')
# test.assert_equals(elder_age(8,5,1,100), 5)
# test.assert_equals(elder_age(8,8,0,100007), 224)
# test.assert_equals(elder_age(25,31,0,100007), 11925)
# test.assert_equals(elder_age(5,45,3,1000007), 4323)
# test.assert_equals(elder_age(31,39,7,2345), 1586)
# test.assert_equals(elder_age(545,435,342,1000007), 808451)

###You need to run this test very quickly before attempting the actual tests :)
# test.assert_equals(elder_age(28827050410, 35165045587, 7109602, 13719506), 5456283)
# Takes 905s with row_sum and new_cell_by_cell as the bottlenecks
#Takes ~0.001s with cell_by_cell3

####Tricky CW tests:
# The Elder says:
m=53
n=42
l=18
t=131 #l is large enough to create negative values in row_sum
test.assert_equals(elder_age(m,n,l,t), 106)




# print('<COMPLETEDIN::>')
#
###My performance tests: (Using run, b/c debug is much slower)
# ans = elder_age(28827, 35165, 71, 1371)#Takes 24s with orig cell_by_cell. ~0.02s with new_cell_by_cell

# ans = elder_age(288270504, 351650455, 71096, 137195) #Takes 182s with orig add_nxn. 114s with improved add_nxn. 3.94s with skip_small=True
#Takes 2.476s for row_sum and 1.437s for new_cell_by_cell with single cell addition in add_rows
#Takes xxs for row_sum and xxs for new_cell_by_cell with single cell addition moved to new_cell_by_cell

# ans = elder_age(288270505, 351650455, 71096, 137195)
#Takes 9.644s for row_sum and 6.550s for new_cell_by_cell with single cell addition in add_rows
#Takes 2.509s for row_sum and 8.813s for new_cell_by_cell with single cell addition moved to new_cell_by_cell
#Single cell addition takes at least 2s
#Takes ~0.001s with cell_by_cell3

#Print alert beep
import winsound
frequency = 1500  # Hertz
duration = 100  # milliseconds
for _ in range(3):
    winsound.Beep(frequency, duration)

