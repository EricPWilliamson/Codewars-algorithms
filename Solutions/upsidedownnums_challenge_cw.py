# Welcome to the Challenge Edition of Upside-Down Numbers
# In the original kata by @KenKamau you were limited to integers below 2^17. Here, you will be given strings of digits of up to 42 characters in length (upper bound is 10^42 - 1).
#
# Your task is essentially the same, but an additional challenge is creating a fast, efficient solution.
#
# Input:
# Your function will receive two strings, each comprised of digits representing a positive integer.
#
# Output:
# Your function must return the number of valid upside down numbers within the range between the two numbers, inclusive.
#
# What is an Upside-Down Number?
# An upside down number is an integer that appears the same when rotated 180 degrees, as illustrated below.
#
# 1961 - OK, 88 - OK, 101 - OK, 25 - No
#
# Example:
#
# x = '0'
# y = '25'
# upsidedown(x,y) #4
# # the valid numbers in the range are 0, 1, 8, and 11
# Additional Notes:
# All inputs will be valid.
# The first argument will always be less than the second argument (ie. the range will always be valid).

###First attempt: The '100000','12345678900000000' example couldn't finish after an entire hour. 100,1000 took about 1ms
# Trying to generate and test so many numbers is dumb.
###2nd attempt: only generate #s we know are flippable...


# from timeit import default_timer as timer

def get_digits(number):
    #Takes an integer and lists the digits in an array. Starts with the one's place. number must be greater than 0
    digits = []
    while number:
        digit = number % 10
        #Discard this number from algorithm right away if it has any non-flippable digits:
        if digit in [2,3,4,5,7]:
            return []

        digits += [digit]#!!Can we save time by producing the flipped number here?!!
        # remove last digit from number (as integer)
        number //= 10
    return digits


def flip_num(digits):
    #Takes an array representing the digits of the number and spits out an integer represting the flipped number.
    fnum = 0
    factor = 1
    for d in reversed(digits):
        if d == 6:
            fnum += 9 * factor
        elif d == 9:
            fnum += 6 * factor
        else:
            fnum += d * factor
        factor *= 10
    return fnum


def test_companions(co_str, a_s):
    # Checks digits in the 2nd half of our number to make sure they exceed the maximum:
    if not co_str: #handles empty co_str special case
        return True
    if len(co_str) < (len(a_s)//2):
        return True
    #Take the entire latter half of a_s:
    test_min = int(a_s[-(len(a_s)//2):])
    return (int(co_str) >= test_min)

def near_min_new(a_s, i, co_str):
    #Calculates the number of flippable numbers close to our max value. Just looks at digit i, uses recursion for inner digits if necessary.
    counter = 0
    n = int(a_s[i])
    L = len(a_s) - 2*i
    ###Handle special cases
    if L == 1:
        counter += sum(1 for x in [0,1,8] if x>n)
        if test_companions(co_str, a_s):
            counter += sum(1 for x in [0,1,8] if x==n)
        return counter

    if i==0:
        V = [1, 6, 8, 9]
        W = [1, 9, 8, 6]
    else:
        V = [0, 1, 6, 8, 9]
        W = [0, 1, 9, 8, 6]

    for x, companion in zip(V, W):
        if n < x:
            # We dont need to look any further.
            d = L
            if L % 2 == 1:  # odd num of digits
                counter += int( 3 * 5**((d-3)/2) )
            else: #even num of digits
                counter += int( 5**((d-2)/2) )
        elif (n == x):
            new_cs = str(companion) + co_str
            if test_companions(new_cs,a_s):
                if(L>2):
                    # make sure we can add the companion without going over the limit:
                    # if [c for c in a_s[i + 1:i + L - 1] if c != "0"] \
                    #         or int(a_s[i + L - 1]) <= companion:
                    # Need to check more chars of a_s
                    counter += near_min_new(a_s, i+1, new_cs)
                else:
                    counter += 1
        else:
            pass
            # no gains
    return counter


def near_min(a_s, i):
    #Calculates the number of flippable numbers close to our max value. Just looks at digit i, uses recursion for inner digits if necessary.
    counter = 0
    n = int(a_s[i])
    L = len(a_s) - 2*i
    ###Handle special cases
    if L == 1:
        return sum(1 for x in [0,1,8] if x>=n)

    if i==0:
        V = [1, 6, 8, 9]
        W = [1, 9, 8, 6]
    else:
        V = [0, 1, 6, 8, 9]
        W = [0, 1, 9, 8, 6]

    for x, companion in zip(V, W):
        if n < x:
            # We dont need to look any further.
            d = L
            if L % 2 == 1:  # odd num of digits
                counter += int( 3 * 5**((d-3)/2) )
            else: #even num of digits
                counter += int( 5**((d-2)/2) )
        elif (n == x):
            if(L>2):
                # Need to check more chars of a_s
                counter += near_min(a_s, i+1)
            else:
                counter += 1
        else:
            pass
            # no gains
    return counter


def near_max(b_s, i):
    #Calculates the number of flippable numbers close to our max value.
    #!!probably will fail if L becomes small
    counter = 0
    n = int(b_s[i])
    L = len(b_s) - 2 * i
    ###Handle special cases
    if L == 1:
        return sum(1 for x in [0, 1, 8] if x <= n)
    elif L == 2:
        n = int(b_s[i:i+2])
        if i==0:
            V = [11, 69, 88, 96]
        else:
            V = [00, 11, 69, 88, 96]
        return sum(1 for x in V if x<=n)

    if i==0:
        V = [1, 6, 8, 9]
        W = [1, 9, 8, 6]
    else:
        V = [0, 1, 6, 8, 9]
        W = [0, 1, 9, 8, 6]

    #Just look at b_s[i]:
    for x,companion in zip(V,W):
        if n > x:
            d = L
            # We dont need to look any further.
            if L % 2 == 1:  # odd num of digits
                counter += int( 3 * 5**((d-3)/2) )
            else: #even num of digits
                counter += int( 5**((d-2)/2) )
        elif (n == x) and (L>2):
            # make sure we can add the companion without going over the limit:
            if [c for c in b_s[i+1:i+L-1] if c!="0"] \
                    or int(b_s[i+L-1]) >= companion:   #we have a non-zero digit preceeding the companion or The companion digit is just below max
                # Need to check more chars of b_s
                counter += near_max(b_s, i+1)
        else:
            pass
            # no gains
    return counter


def upsidedown(a_s, b_s):
    # t1 = timer()
    if False: #!!len(b_s) < 6: ###First attempt:
        #Convert strings to ints:
        a = int(a_s)
        b = int(b_s)
        if a == 0: #Zero is a special case...
            counter = 1
            a = 1
        else:
            counter = 0
        #Count reversable numbers:
        for n in range(a,b):
            # print(n)
            #Put the digits of this number into a list:
            digits = get_digits(n)
            if digits: #Only numbers with flippable digits may pass
                ###Check if the flipped number matches the orig:
                fnum = flip_num(digits)
                if fnum == n:
                    counter += 1

        # t2 = timer()
        # print("{:.2f}ms".format(1000*(t2-t1)))
        return counter
    else: ###Second attempt:
        counter = 0
        #Deal with the smallest digit size:
        # counter += near_min(a_s,0)
        counter += near_min_new(a_s, 0, '')

        # we can use always use all digits in len(a_s)+1 and len(b_s)-1
        for d in range(len(a_s)+1, len(b_s)):
            if d==1: #special case for 1 digit nums
                counter += 3
            elif (d % 2)==1: #odd num digits
                counter += int( 3 * 4 * 5**((d-3)/2) )
            else: #even num digits
                counter += int( 4 * 5**((d-2)/2) )

        #Deal with the last digit size:
        counter += near_max(b_s, 0)

        # t2 = timer()
        # print("{:.2f}ms".format(1000 * (t2 - t1)))
        return counter



# # test.describe('Example Tests')
# print(upsidedown('0','10')==3)
# print(upsidedown('6','25')==2)
# print(upsidedown('10','100')==4) #Smallest 2 digit # to smallest 3 digit #. So all 2 digit #s are counted
# print(upsidedown('100','1000')==12) #All 3 digit #s are counted
# print(upsidedown('100000','12345678900000000')==718650) #All 6 digit #s, through 16 digit #s counted. About 400,000 17 digit #s counted.
#
# #My own tests:
# print(upsidedown('100','1001')==13)
# print(upsidedown('100','1002')==13)

######################### Tricky CW tests: #########################################

# print(upsidedown('9090908074312','617239057843276275839275848') - 2919867187)
#New min fcn puts us under by 312
#Orig min fcn puts us over by 1
# print('6172390578432')
# print('7')
# print('6275839275848')
# 909090
# 8
# 074312

# print(upsidedown('534','101')) #WTF!!
# 534
# 101
# Should equal -2

# print(upsidedown('26008611','668618434') - 952)
# # 26008611
# # 668618434
# # 0.02ms
# # 953 should equal 952
#
# print(upsidedown('819','5505608') - 259)
# # 819
# # 5505608
# # 0.01ms
# # 258 should equal 259

print(upsidedown('908','12005') - 28)
# 908
# 12005
# 0.01ms
# 26 should equal 28

# print(upsidedown('','') - N)
# # 173
# # 3625316
# # 0.01ms
# # 264 should equal 265
