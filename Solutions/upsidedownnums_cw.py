#PASSED -- full test took 5996ms
# Consider the numbers 6969 and 9116. When you rotate them 180 degrees (upside down), these numbers remain the same.
# To clarify, if we write them down on a paper and turn the paper upside down, the numbers will be the same. Try it and
# see! Some numbers such as 2 or 5 don't yield numbers when rotated.
#
# Given a range, return the count of upside down numbers within that range. For example, solve(0,10) = 3, because there
#  are only 3 upside down numbers >= 0 and < 10. They are 0, 1, 8.
#
# More examples in the test cases.
#
# Good luck!
#
# If you like this Kata, please try Life without primes
#
# Please also try the performance version of this kata at Upside down numbers - Challenge Edition

#Conversions:
# 0->0
# 1->1
# 6->9
# 8->8
# 9->6

# from timeit import default_timer as timer

def get_digits(number):
    #Takes an integer and lists the digits in an array. Starts with the one's place.
    if number == 0: #zero needs to be handled specially
        return [0]
    digits = []
    while number:
        digit = number % 10
        #Discard this number from algorithm right away if it has any non-flippable digits:
        if digit in [2,3,4,5,7]:
            return []

        digits += [digit]
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

def solve(a, b):
    # t1 = timer()
    counter = 0
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




# get_digits(10)


# Test.it("Basic tests")
print(solve(0,10)==3)
print(solve(10,100)==4)
print(solve(100,1000)==12)
print(solve(1000,10000)==20)
print(solve(10000,15000)==6)
print(solve(15000,20000)==9)
print(solve(60000,70000)==15)
print(solve(60000,130000)==55)
