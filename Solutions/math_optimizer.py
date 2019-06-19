# Class: Optimizer
# Method: reduce
# Parameters: string
# Returns: integer
# Method signature: def reduce(self, expression):

#Note: we only have to worry about (), *, and +   Other operations arent used.

#WIP

import re

class Optimizer(object):
    def findallchars(self, s, c):
        return [pos for pos, char in enumerate(s) if char == c] #handy "findall" operation

    def reduce(self, expression):
        ###Split up strings based on order of operations:
        #Start with last op first:
        substrs = expression.split('+')

        #Check for multiplication by 0:
        for i, s in enumerate(substrs):
            msubs = s.split('*')
            for s in msubs:
                if not bool(re.search('[a-zA-Z1-9]', s)):
                    del substrs[i]

        #Reduce ops involving only integers:
        newstr = ''
        for s in substrs:
            az = bool(re.search('[A-Za-z]', s))
            if bool(re.search('[A-Za-z]', s)):
                newstr += s + '+'
            else:
                newstr += '7+' #Any integer will do, why not 7
        newstr = newstr[0:-1]

        simp_exp = newstr
        ms = self.findallchars(simp_exp, '*')
        ps = self.findallchars(simp_exp, '+')
        num_cycles = len(ms)*10 + len(ps)
        return num_cycles

###Choose a test case:
# # 0)
# math_str = " alpha*beta+5*006 "
# # Returns: 11
# # This can be reduced to "alpha * beta + 30", which has one multiplication and one addition.

# # 1)
# math_str = "a * b * 00 + 1 * 5"
# # Returns: 0
# # This can simply be reduced to "5" which requires no evaluation.

# 2)
math_str = "dx + a * b * 0 + 1 * c"
# Returns: 1

# # 3)
# math_str = "5 * (3 + 4 + c) + (a + c) * (c + d)"
# # Returns: 24
# # This can be reduced to "5 * (7 + c) + (a + c) * (c + d)" which has 4 additions and 2 multiplications.
# # Note that we can not reduce "5 * (7 + c)" to "35 + 5 * c" because that reduction is a property of distributivity,
# # and is not one of the allowed reductions.

###Test it:
foo = Optimizer()
ans = foo.reduce(math_str)
print(ans)

print('done')
