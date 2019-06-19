#PASSED
#  Define a function
#
# def last_digit(n1, n2):
#   return
# that takes in two numbers a and b and returns the last decimal digit of a^b. Note that a and b may be very large!
#
# For example, the last decimal digit of 9^7 is 9, since 9^7 = 4782969. The last decimal digit of (2^200)^(2^300), which has over 10^92 decimal digits, is 6.
#
# The inputs to your function will always be non-negative integers.


from timeit import default_timer as timer

def last_digit(n1, n2):
    #Is our main fcn.
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
        cycle = [4,6]
    elif n1_end == 5:
        return 5
    elif n1_end == 6:
        return 6
    elif n1_end == 7:
        cycle = [7,9,3,1]
    elif n1_end == 8:
        cycle = [8,4,2,6]
    elif n1_end == 9:
        cycle = [9,1]

    i = (n2 % len(cycle))-1

    # t2 = timer()
    # print("{:.2f}ms".format(1000 * (t2 - t1)))
    return cycle[i]
















# Test.it("Example tests")
print(last_digit(4, 1) == 4)
print(last_digit(4, 2) == 6)
print(last_digit(9, 7) == 9)
print(last_digit(10, 10 ** 10) == 0)
print(last_digit(2 ** 200, 2 ** 300) == 6) #Gets laggy
print(last_digit(3715290469715693021198967285016729344580685479654510946723, 68819615221552997273737174557165657483427362207517952651) == 7)

# Test.it("x ** 0")
for nmbr in range(1, 9):
    a = nmbr ** nmbr
    print("Testing %d and %d" % (a, 0))
    print(last_digit(a, 0)== 1) # "x ** 0 must return 1"

