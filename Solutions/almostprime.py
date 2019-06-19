# Class: AlmostPrimeNumbers
# Method: getNext
# Parameters: integer
# Returns: integer
# Method signature: def getNext(self, m):

#PASSED

class AlmostPrimeNumbers(object):
    def isprime(self, n):
        d = [2] + list(range(3, n, 2))
        for i in d:
            if n % i == 0:
                return bool(False)
        return bool(True)

    def getNext(self, m):

        failtest = True
        while failtest:
            m += 1
            failtest = False
            #Check all prime divisors from 2 to 10:
            for i in [2,3,5,7,9]:
                if m % i == 0:
                    failtest = True
                    break
            #Single check to make sure it's not a true prime:
            if self.isprime(m):
                failtest = True

        return int(m)




foo = AlmostPrimeNumbers()
foo.getNext(121)