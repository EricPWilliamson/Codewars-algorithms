#PASSED
# Problem Statement
#  Little Lisa has been invited to a holiday party with her friends. So that everyone receives a
# gift, the host of the party has decided to give presents through a "Yankee swap".
#
# In this version of a Yankee swap (which may differ from the version that you are used to), each person begins
# holding a present; the first person (indexed from 1) holds present 'A', the second person holds present 'B',
# etc. Each guest in turn (starting with guest 1 and ending with guest N) decides whether or not he wants to swap
# presents. If he decides to swap, he chooses a person to swap with, and the chosen person cannot reject the swap.
# When every person has had a turn, the Yankee swap is over, and each person leaves with the gift they are holding.
#
# For example, one way that the party (with 3 people) could proceed is as follows:
#
# "ABC" --&gt Person 1 swaps with person 2 --&gt "BAC"
# "BAC" --&gt Person 2 does not swap       --&gt "BAC"
# "BAC" --&gt Person 3 swaps with person 2 --&gt "BCA"
# In the above example, person 1 leaves with present B, person 2 leaves with present C, and person 3 leaves with present A.
#
# The guests at the party have given you their preferences, where the i-th element corresponds to the preference list
#  of the i-th guest. If a guest ends up with the gift in the j-th position of his preference list, he will have an
# unhappiness of j.
#
# Each guest knows the preferences of all other guests. Each guest will act optimally to minimize
# his own unhappiness, and knows all other guests will do the same. If there are multiple ways for a guest to
# minimize his own unhappiness, he will choose not to swap at all if possible; if there are still multiple ways,
# he will choose to swap with the guest with the lowest index.
#
# Return a String, the i-th character of which corresponds to the turn of the i-th person. If the i-th person did not
#  swap in his turn, the i-th character of the result must be equal to '-'. If he did swap with the k-th person,
# the i-th character of the result must be equal to the k-th lowercase letter (so, 'a' corresponds to swapping with
# the first person, 'b' to the second and so on).
#
# Definition
# Class: YankeeSwap
# Method: sequenceOfSwaps
# Parameters: tuple (string)
# Returns: string
# Method signature: def sequenceOfSwaps(self, preferences):
# Limits
# Time limit (s): 840.000
# Memory limit (MB): 64
# Constraints
# - preferences will contain N elements, where N is between 1 and 20 inclusive.
# - Each element of preferences will be a permutation of the first N uppercase letters of the alphabet.

class YankeeSwap(object):
    def nextSwap(self, i, state, objectives, actions):
        N = len(objectives)

        #Find where your goal gift is located:
        goal_idx = state.index(objectives[i])

        ###if you already have your goal, dont do anything:
        if state[i] == objectives[i]:
            # do nothin:
            newstate = list(state)
            newactions = str(actions) + '-'
            # run later steps:
            if i+1<N:
                newstate, newactions = self.nextSwap(i+1, newstate, objectives, newactions)
            return newstate, newactions

        if i < N-1:
            ###try doing nothing and see if you get your goal
            #can only work if you are holding something that someone still wants:
            if state[i] in objectives[i:]:
                # do nothin:
                hyp_state = list(state)
                hyp_actions = str(actions) + '-'
                # run later steps:
                if i + 1 < N:
                    hyp_state, hyp_actions = self.nextSwap(i+1, hyp_state, objectives, hyp_actions)

                # check final state to see if you got your goal:
                if hyp_state[i] == objectives[i]:
                    # finalize
                    return hyp_state, hyp_actions

            ###Then try grabbing each gift from lower people and see if any give you your goal:
            # take a gift from a lower person, starting with 0, ending at the person holding your goal.
            for victim in range(goal_idx):
                # Only take from people holding something that someone still wants:
                if (state[victim] in objectives[i:]):
                    #swap with victim:
                    test_state = list(state)
                    test_state[victim] = state[i]
                    test_state[i] = state[victim]
                    hyp_state = list(test_state)
                    hyp_actions = str(actions) + chr(victim + 97)#ASCII char 97 is 'a'
                    # run later steps:
                    if i + 1 < N:
                        hyp_state, hyp_actions = self.nextSwap(i+1, hyp_state, objectives, hyp_actions)
                    # check final state to see if you got your goal
                    if hyp_state[i] == objectives[i]:
                        # finalize:
                        return hyp_state, hyp_actions
        ### If those things havent worked, just grab your goal:
        newstate = list(state)
        newstate[goal_idx] = state[i]
        newstate[i] = state[goal_idx]
        newactions = str(actions) + chr(goal_idx + 97) #ASCII char 97 is 'a'
        # run later steps:
        if i + 1 < N:
            newstate, newactions = self.nextSwap(i+1, newstate, objectives, newactions)
        return newstate, newactions




    def sequenceOfSwaps(self, preferences):
        N = len(preferences)

        ###We start by trying to figure out which gift each person will try to end up with:
        objectives = [] #Lists take-home gift, starting with last person
        for p in reversed(preferences):
            for c in p:
                if not (c in objectives):
                    goal = c
                    break
            objectives += [goal]
        #Flip objectives:
        objectives.reverse()

        ###Try to find best moves:
        #Initialize the state to "ABCD...":
        state = [chr(i+65) for i in range(N)] #ASCII char 65 is 'A'

        #Run this recurseive function that will find the optimal set of moves:
        state, actions = self.nextSwap(0, state, objectives, '')
        # print(state)
        return actions



foo = YankeeSwap()

# Examples
# 0)
preferences = ("BAC", "ACB", "BCA")
# Returns: "-aa"
# This swap will proceed as follows:
# 1) Guest 1 keeps his present. ABC
# 2) Guest 2 swaps with Guest 1. BAC
# 3) Guest 3 swaps with Guest 1. CAB
# 1)
# {"ABC", "BCA", "CAB"}
# Returns: "---"
# In this scenario, everyone keeps their own gift.
# 2)
# preferences = ("AECDBF", "BAEDCF", "DEBACF", "BEDCAF", "CEABDF", "CBDEAF")
# objectives = ["F",          "A",       "D",     "B",      "E",     "C"]
# {"AECDBF", "BAEDCF", "DEBACF", "BEDCAF", "CEABDF", "CBDEAF"}
# Returns: "-aac-a"
#1- -A-BCDEF knows hes fucked, so doesnt try
#2- B-A-CDEF knows he cant keep B, takes 2nd choice
#3- CA-B-DEF knows that #4 will now give him D?
#4- CAD-B-EF takes 1st choice
#5- CADB-E-F knows he cant keep C, so takes 2nd choice
#6- FADBE-C- takes 1st choice
# 3)
preferences = ("FDBHMAIELGKNJC", "KGMDJBAFLECNHI", "FKLJCADBEHNGIM", "JMHNICABFKEGDL", "IKFCDNJBLEGAMH", "FDNLJGCKHMBIEA", "MBKJAHDNIGECLF", "KNADLFGBJIMHCE", "AIFMGEBDHKJNCL", "MCDALIJGNKBFHE", "AJHMDLEIFKNCGB", "IJLKBCMDGNHFEA", "EAKFLJBDGMHCIN", "JEMANBDFGICHKL")
#                       1              2                 3                   4               5                   6                7                   8               9                  10                11                12                13               14
# Returns: "--acacbdcahcja"
#           12345678901234
#1 -A-BCDEFGHIJKLMN
#2 A-B-CDEFGHIJKLMN
#3 CB-A-DEFGHIJKLMN
#4 CBD-A-EFGHIJKLMN
#5 ABDA-C-FGHIJKLMN
#6 ABFAC-D-GHIJKLMN

ans = foo.sequenceOfSwaps(preferences)
print(ans)
