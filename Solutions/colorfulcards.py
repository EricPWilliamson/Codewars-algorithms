# Class: ColorfulCards
# Method: theCards
# Parameters: integer, string
# Returns: tuple (integer)
# Method signature: def theCards(self, N, colors):

# "B" = non-prime
# "R" = prime

#FAILED: !!Works, but it's too slow

import re  # contains regex fcns


class ColorfulCards(object):
    def isprime(self, n):
        ##Just checks whether an integer is prime:
        d = [2] + list(range(3, n, 2))
        for i in d:
            if n % i == 0:
                return bool(False)
        return bool(True)

    def initAtts(self, N, colors):
        ## Find all the colors of the entire deck of N cards:
        self.allcolors = "BR"  # Pre-fill 1 and 2. 1 is not prime, 2 is.
        # for i in range(3, N + 1, 2): #Automatically skips even #s, marking them blue
        #     if self.isprime(i):
        #         self.allcolors += "RB"
        #     else:
        #         self.allcolors += "BB"
        for i in range(3, N + 1):
            if self.isprime(i):
                self.allcolors += "R"
            else:
                self.allcolors += "B"
        ## Form a regex search string by putting ".*" operator between each character in colors:
        self.searchstr = colors[0]
        for s in colors[1:]:
            self.searchstr += ".*" + s
        ## Just make colors a class attribute:
        self.colors = colors

    def nextseq(self, oldseq, j):
        ###Try to modify oldseq on the j-th card:
        # Remove section to be changed:
        prevnum = int(oldseq[j])
        newseq = list(oldseq[:j])
        # Search for new matches:
        for i in range(j, len(self.colors)):
            pattern = re.compile(self.searchstr[i * 3:])
            mymatch = pattern.search(self.allcolors, prevnum) #!!this search is just too slow for long sequences
            if mymatch:
                prevnum = mymatch.start() + 1
                newseq += prevnum,
        if len(newseq) >= len(self.colors):
            return list(newseq)  # Using the list function ensures that we append the VALUE, not a REFERENCE.
        else:
            return []

    def findalt(self, oldseq, j):
        ###Try to modify oldseq on the j-th card:
        # Remove section to be changed:
        prevnum = int(oldseq[j])
        # Try to find an alternate match:
        pattern = re.compile(self.searchstr[j * 3:])
        mymatch = pattern.search(self.allcolors, prevnum)#!!this search is just too slow for long sequences
        return bool(mymatch)

    def theCards(self, N, colors):
        ##Prepare attributes:
        print("Preparing attributes...")
        self.initAtts(N, colors)
        ##Find very first sequence:
        print("Finding 1st sequence...")
        firstseq = self.nextseq([0], 0)
        if firstseq:
            solution = list(firstseq)
        else:
            return ()
        ##Work back from last card, just checking if an alternate match exists:
        for k in range(len(colors) - 1, -1, -1):
            print("Finding new sequence for card #{}...".format(k))
            foundnew = self.findalt(firstseq, k)
            if foundnew:
                solution[k] = -1

        return tuple(solution)


foo = ColorfulCards()
foo.theCards(58, "RBRRBRBBRBRRBBRRBBBRRBBBRR")
# BRRBRBRB
# 12345678
# {2, 4, 5}x
# {2, 4, 7}x
# {2, 6, 7}x
# {3, 4, 5}x
# {3, 4, 7}x
# {3, 6, 7}x
# {5, 6, 7}x

# 58, RBRRBRBBRBRRBBRRBBBRRBBBRR
