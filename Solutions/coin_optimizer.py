# Class: ChangeOptimizer
# Method: fewestCoins
# Parameters: tuple (integer), integer
# Returns: tuple (integer)
# Method signature: def fewestCoins(self, coinTypes, value):

# Constraints
# - coinTypes has between 1 and 50 elements, inclusive.
# - Each element of coinTypes is between 1 and 100,000,000, inclusive.
# - There will be no repeated values in coinTypes.
# - There will be exactly one element in coinTypes equal to 1.
# - value is between 1 and 1,000,000,000, inclusive.

import math

class ChangeOptimizer(object):
    def fewestCoins(self, coinTypes, value):
        coinTypes = list(coinTypes)
        #Start by trying to use the biggest coins:
        remain = value
        ans1 = [0, 0, 0]
        ans1[2] = math.floor(remain/coinTypes[2])
        remain = remain % coinTypes[2]

        ans1[1] = math.floor(remain/coinTypes[1])
        remain = remain % coinTypes[1]

        ans1[0] = math.floor(remain/coinTypes[0])
        remain = remain % coinTypes[0]

        return tuple(ans1)









# Examples
# 0)
coinTypes = (1, 10, 25)
value = 49
# Returns: ( 9, 4, 0 )
# From the problem statement
# 1)
# (1,3,6,2)
# 11
# Returns: ( 2, 1, 1, 0 )
# From the problem statement
# 2)
# (1,2,3,4,5,6,7,8,9,10)
# 1234567
# Returns: ( 1, 1, 0, 1, 0, 0, 0, 154320, 0, 0 )
# 3)
# (91001,3567,222123,4456,1,732234,123793,982312,14781)
# 65864135
# Returns: ( 0, 0, 0, 0, 14780, 0, 0, 0, 4455 )
# 4)
# (1,10,100,1000,10000)
# 1000000
# Returns: ( 1000000, 0, 0, 0, 0 )
# 5)
# (147323, 544149, 649, 26, 3473340, 267243, 6946680, 587, 13893360, 17103552, 27786720, 60400539, 83360160, 68414208, 72482916, 1, 687, 4758)
# 333440639
# Returns: ( 0, 0, 0, 182, 1, 0, 1, 0, 1, 0, 2, 0, 3, 0, 0, 25, 0, 729 )

###Test it:
foo = ChangeOptimizer()
ans = foo.fewestCoins(coinTypes, value)
print(ans)

print('done')
