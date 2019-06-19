# Class: TVTower
# Method: minRadius
# Parameters: tuple (integer), tuple (integer)
# Returns: float
# Method signature: def minRadius(self, x, y):

#PASSED !Seems like it could fail under more rigorous test conditions...

import tensorflow as tf

class TVTower(object):
    def minRadius(self, x, y):
        #Look at town locations:
        N = len(x)
        if N == 1:
            return 0.0

        #Find optimal tower coords:
        #First make a best guess:
        xTower = (max(x)+min(x))/2.0 #IMPORTANT--Some compilers will make result an int if I use "2" instead of "2.0"
        yTower = (max(y)+min(y))/2.0
        #Calculate distance to each town:
        dist = [0.0] * N
        for i in range(N):
            dist[i] = ( (x[i]-xTower)**2 + (y[i] - yTower)**2 )**0.5

        #Find which two towns still have the longest distance:
        l = [i[0] for i in sorted(enumerate(dist), key=lambda x:x[1])] #USEFUL--Finds indexes of sorted list

        ##Recalculate tower coords from 2 worst towns until optimum is found
        while dist[l[-2]] != dist[l[-1]]: #!Seems dangerous to compare floats in this way
            #Recalculate tower coords from those 2 towns:
            xTower = (x[ l[-2] ] + x[ l[-1] ]) / 2.0 #IMPORTANT--Some compilers will make result an int if I use "2" instead of "2.0"
            yTower = (y[l[-2]] + y[l[-1]]) / 2.0
            #Recalculate distance to each town:
            dist = [0.0] * N
            for i in range(N):
                dist[i] = ( (x[i]-xTower)**2 + (y[i] - yTower)**2 )**0.5
            # Find which two towns still have the longest distance:
            l = [i[0] for i in sorted(enumerate(dist), key=lambda x: x[1])]  # USEFUL--Finds indexes of sorted list

        #Radius must match the longest distance:
        minRad = dist[l[-1]]
        return minRad


foo = TVTower()

# 0)
foo.minRadius((1, 0, -1, 0), (0, 1, 0, -1))
# {1, 0, -1, 0}
# {0, 1, 0, -1}
# Returns: 1.0
# By symmetry we should locate the tower at the origin, which is in the center of the diamond formed by these 4 towns.
# 1)
# {3}
# {299}
# Returns: 0.0
# Locate the tower right in the town.
# 2)
# foo.minRadius((5, 3, -4, 2), (0, 4, 3, 2))
# {5, 3, -4, 2}
# {0, 4, 3, 2}
# Returns: 4.743416490252569