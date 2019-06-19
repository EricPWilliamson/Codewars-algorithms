# Class: AirlinerSeats
# Method: mostAisleSeats
# Parameters: integer, integer
# Returns: tuple (string)
# Method signature: def mostAisleSeats(self, width, seats):

#PASSED

class AirlinerSeats(object):
    def mostAisleSeats(self, width, seats):
        #Aisle spots are normally the limiting reagent. One aisle can create two aisle seats max.
        nAisles = width - seats
        maxASeats = nAisles * 2
        if maxASeats > seats:
            print("Extra aisles available...")
            #Extra aisles should go at beginning of string, because that is lexographically smaller:
            sol = ""
            while maxASeats > seats:
                sol += "."
                nAisles -= 1
                maxASeats = nAisles * 2

            if maxASeats == seats:
                sol += "S."
                nAisles -= 1
                seats -= 1
            #Use aisles optimally until they run out:
            while nAisles > 0:
                sol += "SS."
                seats -= 2
                nAisles -= 1
            #Add final aisle and seat to end:
            sol += "S"
            seats -= 1
        elif maxASeats == seats:
            print("Just the right # of aisles...")
            #Lexographical order won't matter, since there is only one optimal solution.
            #This is always the optimal start:
            sol = "S"
            seats -= 1
            #Use aisles optimally until they run out:
            while nAisles > 1:
                sol += ".SS"
                seats -= 2
                nAisles -= 1
            #Add final aisle and seat to end:
            sol += ".S"
            seats -= 1
            nAisles -= 1

        else:
            print("Aisles limited...")
            #Aisles should be used as early in the string as possible, because that is lexographically smaller.
            #This is always the optimal start:
            sol = "S"
            seats -= 1
            #Use aisles optimally until they run out:
            while nAisles > 0:
                sol += ".SS"
                seats -= 2
                nAisles -= 1
            #Add remaining seats to end:
            while seats > 0:
                sol += "S"
                seats -= 1

        #For long solutions, split sol into smaller strings:
        if len(sol) < 51:
            ans = (sol),
        elif len(sol) < 101:
            ans = (sol[0:50], sol[50:])
        else:
            ans = (sol[0:50], sol[-50:])

        return ans




foo = AirlinerSeats()
# 0)x
# foo.mostAisleSeats(6, 3)
# 6
# 3
# Returns: {"..SS.S" }
# All three seats can be made aisle seats and this is the lexicographically smallest such arrangement.
# 1)x
# foo.mostAisleSeats(6, 4)
# 6
# 4
# Returns: {"S.SS.S" }
# This is the only arrangement where all four seats are aisle seats.
# 2)x
foo.mostAisleSeats(12, 10)
# 12
# 10
# Returns: {"S.SS.SSSSSSS" }
# The picture in the problem statement shows another arrangement with the maximum number of aisle seats, but this one is lexicographically smaller.