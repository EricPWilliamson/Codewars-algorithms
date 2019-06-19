"""
Hyper efficient solution from user lechevalier
Completes test in ~165ms
"""

def elder_age(m,n,l,t,s=0):
    if m > n: m, n = n, m
    if m < 2 or not n & (n - 1): # n is a power of 2
        s, p = max(s-l, 0), max(n+s-l-1, 0)
        return (p - s + 1) * (s + p) // 2 * m % t
    p = 1 << n.bit_length() - 1 # Biggest power of 2 lesser than n
    if m < p: return (elder_age(m, p, l, t, s) + elder_age(m, n-p, l, t, s+p)) % t
    return (elder_age(p, p, l, t, s) + elder_age(m-p, n-p, l, t, s) +
            elder_age(p, n-p, l, t, s+p) + elder_age(m-p, p, l, t, s+p)) % t



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

