#Passed examples, but I'm not satisfied with this.
# Problem Statement
# Pinguos are funny little monsters. Actually, there exist N different types of Pinguos (for
# simplicity numbered from 1 to N). Each midnight, each Pinguo dies. When a Pinguo dies, it gives birth to one or
# more new Pinguos. The types and numbers of these new Pinguos are uniquely determined by the type of the old,
# now dead, Pinguo. Please note that the total count of Pinguos never decreases, as each old Pinguo is replaced by at
#  least one new Pinguo.
#
#
# You are given a transforms (containing N elements) describing for each type of Pinguo what types of Pinguos will
# arise from its dead body. For each i between 1 and N, element i-1 of transforms is a containing a space-separated
# list of integers. These integers are the types of Pinguos that will arise from a dead Pinguo of type i. For
# example, if transforms[6] is "2 3 3", it means that when a Pinguo of type 7 dies, one Pinguo of type 2 and two
# Pinguos of type 3 will arise.
#
#
# It is not hard to see that sometimes the number of Pinguos will grow towards infinity, eventually exceeding all
# bounds. However, there are some cases in which the number of Pinguos reaches a finite constant and then stays the
# same forever. (Note that these are the only two possible cases, as the total number of Pinguos never decreases.
# Also note that in the second case only the total number of Pinguos remains constant, their types may be changing
# every day.)
#
#
# Initially you have a single Pinguo of type 1. You want to know what is the final (finite) number of Pinguos you
# will eventually end up with. Return this number modulo 1,000,000,007. If the count of Pinguos grows beyond all
# bounds, return -1 instead.
#
# Definition
# Class: MonsterFarm
# Method: numMonsters
# Parameters: tuple (string)
# Returns: integer
# Method signature: def numMonsters(self, transforms):
# Limits
# Time limit (s): 840.000
# Memory limit (MB): 64
# Constraints
# - transforms will contain between 1 and 50 elements, inclusive.
# - Each element of transforms will contain between 1 and 50 characters, inclusive.
# - Each element of transforms will be a list of integers separated by single spaces, with no extra leading or trailing spaces.
# - Each integer in transforms will be between 1 and the number of elements in transforms, inclusive, with no leading zeros.

class MonsterFarm(object):
    def numMonsters(self, transforms):
        pop = [1]

        for i in range(1000):
            newpop = []
            for parent in pop:
                s = transforms[parent-1]
                for child in s.split(' '):
                    newpop += [int(child)]
            if newpop == pop:
                return len(newpop)
            #The lists arent the same, but is the population makeup still changing? If not, probably infinite:
            if list(set(newpop)) == list(set(pop)):
                return -1
            pop = newpop


        return len(pop)









foo = MonsterFarm()

# Examples
# 0)
# {"1"}
# Returns: 1
# After the Pinguo dies, you will always get another one of the same type. The total number of Pinguos is 1 forever.
# 1)
# {"1 1"}
# Returns: -1
# As the number of Pinguos doubles every day, the growth of their population will never terminate.
# 2)
# {"2", "3", "1"}
# Returns: 1
# The type of the Pinguo changes every day, but the total number of Pinguos stays the same.
# 3)
# {"1", "3 4", "2", "2"}
# Returns: 1
# You start with a Pinguo of type 1, and this is what you will have forever. However, note that if you had started with a Pinguo of type 2, your number of Pinguos would eventually grow beyond all bounds.
# 4)
transforms = ("2 2", "3", "4 4 4", "5", "6", "7 7 7 7", "7")
# Returns: 24
# 5)
transforms = ("2 3","5 7","2 4","5","6","4","7")
# Returns: 5

ans = foo.numMonsters(transforms)

print(ans)
