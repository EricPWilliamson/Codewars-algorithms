# Class: CityMap
# Method: getLegend
# Parameters: tuple (string), tuple (integer)
# Returns: string
# Method signature: def getLegend(self, cityMap, POIs):

#PASSED

class CityMap(object):
    def getLegend(self, cityMap, POIs):
        #Print cityMap for my own sanity:
        for row in cityMap:
            print(row)

        #The grid layout doesn't matter. Just put everything on one line and remove the dots:
        longRow = ""
        for row in cityMap:
            longRow += row
        longRow = longRow.replace(".", "")
        #Find which letters occur in cityMap:
        charList = ""
        cCounts = []
        while longRow:
            c = longRow[0]
            charList += str(c)
            cCounts += longRow.count(c), #Count the # of char c
            longRow = longRow.replace(c, "") #Remove char c from string



        #Match letter counts to POIs, and order them correctly:
        solution = list(charList)
        for i in range(len(cCounts)):
            iMatch = POIs.index(cCounts[i])
            solution[iMatch] = str(charList[i])



        return "".join(solution) #Join seems to be the only way to turn a list to a string...


foo = CityMap()
exMap = ("M....M", "...R.M", "R..R.R")
exPOIs = (3, 4)
result = foo.getLegend(exMap, exPOIs)
print(result)





# {"M....M", "...R.M", "R..R.R"}
# {3, 4}
# Returns: "MR"

# The city map is 3 squares high and 6 squares wide. There are 3 'M' signs and 4 'R' signs on the map.
        # The legend summary states that there are three POIs of type 0 and four POIs of type 1 on the map.
        # Obviously, the former are denoted with 'M' on the map and the latter are denoted with 'R'.
