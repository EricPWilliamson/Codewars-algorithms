#PASSED
# For a given list [x1, x2, x3, ..., xn] compute the last (decimal) digit of x1 ^ (x2 ^ (x3 ^ (... ^ xn))).
#
# E. g.,
# last_digit([3, 4, 2]) == 1
# because 3 ^ (4 ^ 2) = 3 ^ 16 = 43046721.
#
# Beware: powers grow incredibly fast. For example, 9 ^ (9 ^ 9) has more than 369 millions of digits. lastDigit has to deal with such numbers efficiently.
#
# Corner cases: we assume that 0 ^ 0 = 1 and that lastDigit of an empty list equals to 1.
#
# This kata generalizes Last digit of a large number; you may find useful to solve it beforehand.




def final_cycle(n1, n2, i):
    #Was main function from the simpler last digit problem
    # t1 = timer()

    if n2==0: #Special case where exponent is 0
        return 1

    #we just need the last digit of n1:
    n1_end = n1 % 10
    #Each value of n1_end produces a different repeating cycle (sometimes a cycle of one value)
    if n1_end == 0:
        return 0
    elif n1_end == 1:
        return 1
    elif n1_end == 2:
        cycle = [2,4,8,6]
    elif n1_end == 3:
        cycle = [3,9,7,1]
    elif n1_end == 4:
        cycle = [4,6,4,6]
    elif n1_end == 5:
        return 5
    elif n1_end == 6:
        return 6
    elif n1_end == 7:
        cycle = [7,9,3,1]
    elif n1_end == 8:
        cycle = [8,4,2,6]
    elif n1_end == 9:
        cycle = [9,1,9,1]

    return cycle[i-1]

def new_cycle(n1,n2):
    #Calculates (n1**n2) % 4 to determine i,new_n2 where i indicates cycle[i-1] the next iteration needs to use
    if n2==0: #Special case: exponent is 0
        return 1,1
    elif n1==0: #Special case: n1 is zero, but exponent isnt
        return 4,0
    if n1==1:
        return 1,1

    # get the last two digits of n1:
    n1_end = n1 % 10
    n1_2nd = n1//10 % 10
    #Each pair of final digits has a different pattern.
    if n1_end%2 == 0: #Final digit is any even number:
        # Pattern could be 200000... or 0000000...
        if n2==1: #The first position is the only place that can be non-zero
            if n1_end%4 == 0: #multiples of 4
                if n1_2nd%2 == 0: #even tens digit
                    return 4,2
                else:
                    return 2,2
            else: #non multiples of 4
                if n1_2nd%2 == 0: #even tens digit
                    return 2,2
                else:
                    return 4,2
        else: #Beyond the first position, it's all zeros
            return 4,2
    else: #Final digit is any odd number
        if n1_end==3 or n1_end==7:
            #Pattern is 3131...
            #           1111...
            if n1_2nd%2 == 1: #odd 2nd digit, so 11111...
                return 1,3
            else: #odd 2nd digit, so 313131...
                if n2%2==1:
                    return 3,3
                else:
                    return 1,3
        else: #Final digit is 1,5, or 9
            #Pattern is 1111...
            #           3131...
            if n1_2nd%2 == 0: #even 2nd digit, so 11111...
                return 1,3
            else: #odd 2nd digit, so 313131...
                if n2%2==1:
                    return 3,3
                else:
                    return 1,3


def last_digit(lst):
    # Your Code Here
    if not lst: #Special case: empty list
        return 1
    if len(lst) == 1: #Special case: list of one
        return lst[0] % 10

    # n2 = lst[-1]
    # n1 = lst[-2]
    # res = new_cycle(n1,n2)
    # n1 = lst[-3]
    # n2 = res
    # res = orig_last_digit(n1,n2)
    #!!Could be faster if we check lst[0] for special digits first

    n2 = lst[-1]
    i = n2 % 4
    for n1 in reversed(lst[1:-1]): #!!Is this range correct?
        i,n2 = new_cycle(n1,n2)
    #For the final calculation, we use the i value
    return final_cycle(lst[0],n2,i)


# for d in range(11):
#     N = 10*d + 1
#     print(N)
#     for x in range(1,90):
#         print((N**x) % 4, end=',')
#     print('\n')

###MOD 4:
# twos:
# 2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

#twelves:
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

#22s:
# 2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0


###MOD 100:
# twos = [4,8,16,32,64,28,56,12,24,48,96,92,84,68,36,72,44,88]
# 2,\
# 4,8,16,32,64,28,56,12,24,48,96,92,84,68,36,72,44,88,76,52,\
# 4,8,16,32,64,28,56,12,24,48,96,92,84,68,36,72,44,88,76,52,\
# 4,8,16,32,64,28,56,12,24,48,96,92,84,68,36,72,44,88
# twelves:
# 12,44,28,36,32,84,8,96,52,24,88,56,72,64,68,16,92,4,48,76,\
# 12,44,28,36,32,84,8,96,52,24,88,56,72,64,68,16,92,4,48,76,\
# 12,44,28,36,32,84,8,96,52,24,88,56,72,64,68,16,92,4,48

# test.it('Basic tests')
# test_data = [
#     ([], 1),
#     ([0, 0], 1),
#     ([0, 0, 0], 0),
#     ([1, 2], 1),
#     ([3, 4, 5], 1),
#     ([4, 3, 6], 4),
#     ([7, 6, 21], 1),
#     ([12, 30, 21], 6),
#     ([2, 2, 2, 0], 4),
#     ([937640, 767456, 981242], 0),
#     ([123232, 694022, 140249], 6),
#     ([499942, 898102, 846073], 6)
# ]
# for test_input, test_output in test_data:
#     print(last_digit(test_input) == test_output)

# print(last_digit([2,2,2,0]) == 4)

# [12, 18]
# 2 should equal 4
# print(last_digit([12,18]) == 4)

# # [3, 3, 1]
# # 3 should equal 7
# print(last_digit([3,3,1]) == 7)

# # [329507]
# # Wrong solution for [329507]: 3 should equal 7
# print(last_digit([329507]))
