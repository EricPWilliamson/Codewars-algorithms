#PASSED
#  Problem Statement
# A fairground operator has designed a new game, called "Catch the Mice". This consists of a set of electronic "mice"
#  that move around on a large board. The contestant controls a square cage, which is initially suspended above the
#  board. The contestant can position the cage anywhere above the board and then drop it, the aim being to enclose some
#  of the mice in the cage. The contestant wins a prize accoring to how many mice he managed to capture. If the
#  contestant captures all of the mice, then he wins the grand prize, which is a sports car. However the fairground
#  operator is not entirely honest, and wants your help to rig the game so that it is impossible to win the grand prize.
#  He wants to make the cage sufficiently small that at no point in time are the mice close enough for it to capture
#  them all.
#
# Consider the mice as a set of points moving in an infinite 2D cartesian plane. Each mouse starts at a known position
#  at time t = 0, then moves with constant velocity in time t ≥ 0. Consider the cage as a perfect square of side
#  length L, that can be positioned anywhere in the plane with its sides parallel to the axes (i.e., the contestant can
#  move, but cannot rotate the cage). The cage can be dropped at any time t ≥ 0 and it will capture a mouse if at that
#  point in time the mouse's position is strictly contained within its boundary (mice exactly on the boundary are not
#  considered to be captured). You should calculate the maximum value of L that doesn't allow all the mice to be captured.
#
# You will be given 4 s xp, yp, xv and yv. The position of the mouse with index i is given by (xp[i], yp[i]) and its
#  velocity by (xv[i], yv[i]). The position of the mouse at time t will therefore be (xp[i] + xv[i]*t, yp[i] + yv[i]*t).
#  Return a giving the length of the side of the largest cage that cannot capture all the mice at any time t ≥ 0.
#
# Definition
# Class: CatchTheMice
# Method: largestCage
# Parameters: tuple (integer), tuple (integer), tuple (integer), tuple (integer)
# Returns: float
# Method signature: def largestCage(self, xp, yp, xv, yv):
# Limits
# Time limit (s): 840.000
# Memory limit (MB): 64
# Notes
# - Your return value must be accurate to an absolute or relative tolerance of 1e-9.
# Constraints
# - xp, yp, xv and yv will contain between 2 and 50 elements, inclusive.
# - xp, yp, xv and yv will contain the same number of elements.
# - Each element of xp, yp, xv and yv will be between -1000 and 1000, inclusive.
# - At no point in time t ≥ 0 will any two mice occupy the same point in space.
# Examples
# 0)
# {0,10}
# {0,10}
# {10,-10}
# {0,0}
# Returns: 10.0
# A cage with side length greater than 10 would be able to catch both the mice at any time before t = 1.
# 1)
# {0,10,0}
# {0,0,10}
# {1,-6,4}
# {4,5,-4}
# Returns: 3.0
# At time t = 1, the mice are at positions (1, 4), (4, 5) and (4, 6). At this point in time any cage with an edge length
#  larger than 3 would be able to catch them. This is the point in time when the mice are closest together.

class CatchTheMice(object):
    def largestCage(self, xp, yp, xv, yv):
        ###Plot the mice's paths from 0-10sec?
        #nah...
        ###List up all the times when x coords intersect:
        t_list = [0.0]
        for xp1, xv1 in zip(xp, xv):
            for xp2, xv2 in zip(xp, xv):
                #Dont bother if the velocities are the same, they'll never intersect. This also eliminates same-same comparisons
                if (xv2!=xv1):
                    new_t = (xp2-xp1) / (xv1-xv2)
                    #Add the time to our list if it's new:
                    if (not (new_t in t_list)) and (new_t > 0):
                        t_list += [float(new_t)]
        ###Also list up all the times when y coords intersect:
        for yp1, yv1 in zip(yp, yv):
            for yp2, yv2 in zip(yp, yv):
                # Dont bother if the velocities are the same, they'll never intersect. This also eliminates same-same comparisons
                if (yv2 != yv1):
                    new_t = (yp2 - yp1) / (yv1 - yv2)
                    # Add the time to our list if it's new:
                    if (not (new_t in t_list)) and (new_t>0):
                        t_list += [float(new_t)]
        ###Go through each time in t_list, and separately find the x and y distances between the 2 farthest mice:
        t_list.sort()
        delta_x_list = []
        delta_y_list = []
        max_L = []
        for t in t_list:
            #Find x distance:
            x = []
            for xp1, xv1 in zip(xp, xv):
                x += [float(xp1 + xv1*t)]
            delta_x = max(x) - min(x)
            delta_x_list += [float(delta_x)]
            #Find y distance:
            y = []
            for yp1, yv1 in zip(yp, yv):
                y += [float(yp1 + yv1*t)]
            delta_y = max(y) - min(y)
            delta_y_list += [float(delta_y)]
            #The larger of the two dimensions is going the be the maximum cage size, L
            max_L += [max([delta_x, delta_y])]

        ###Check if delta_x and delta_y cross between any of our time points:
        for i in range(len(delta_x_list)-1):
            #Use rise/run for two adjacent time points:
            dx_m = (delta_x_list[i+1]-delta_x_list[i]) / (t_list[i+1]-t_list[i])
            dy_m = (delta_y_list[i+1]-delta_y_list[i]) / (t_list[i+1]-t_list[i])

            #Solve for intersect of two lines:
            dx = delta_x_list[i]
            dy = delta_y_list[i]
            t_i = t_list[i]
            if not (dy_m == dx_m):
                new_t = ((dx - dx_m*t_i) - (dy - dy_m*t_i)) / (dy_m - dx_m)
                if (new_t>t_i) and (new_t<t_list[i+1]):
                    t_list += [new_t]

        ###Recalculate from new t_list:
        t_list.sort()
        delta_x_list = []
        delta_y_list = []
        max_L = []
        for t in t_list:
            # Find x distance:
            x = []
            for xp1, xv1 in zip(xp, xv):
                x += [float(xp1 + xv1 * t)]
            delta_x = max(x) - min(x)
            delta_x_list += [float(delta_x)]
            # Find y distance:
            y = []
            for yp1, yv1 in zip(yp, yv):
                y += [float(yp1 + yv1 * t)]
            delta_y = float(max(y) - min(y))
            delta_y_list += [delta_y]
            # The larger of the two dimensions is going the be the maximum cage size, L
            max_L += [max([delta_x, delta_y])]

        #Return the smallest cage max that we found:
        return float(min(max_L))


foo = CatchTheMice()
# Example 0)
xp = (0, 10)
yp = (0, 10)
xv = (10, -10)
yv = (0, 0)
# should* Returns: 10.0
# A cage with side length greater than 10 would be able to catch both the mice at any time before t = 1.


# Ex 1)
# xp = (0, 10, 0)
# yp = (0, 0, 10)
# xv = (1, -6, 4)
# yv = (4, 5, -4)
# should Returns: 3.0
# At time t = 1, the mice are at positions (1, 4), (4, 5) and (4, 6). At this point in time any cage with an edge length
#  larger than 3 would be able to catch them. This is the point in time when the mice are closest together.

# Ex 2)
xp = (50,10,30,15)
yp = (-10,30,20,40)
xv = (-5,-10,-15,-5)
yv = (40,-10,-1,-50)
# Returns: 40.526315789473685

#Ex 3)
xp = (0,10,10,0)
yp = (0,0,10,10)
xv = (1,0,-1,0)
yv = (0,1,0,-1)
# Returns: 10.0

# ex 4)
# xp = (13,50,100,40,-100)
# yp = (20,20,-150,-40,63)
# xv = (4,50,41,-41,-79)
# yv = (1,1,1,3,-1)
# Returns: 212.78688524590163

# ex 6)
# xp = (-49,-463,-212,-204,-557,-67,-374,-335,-590,-4)
# yp = (352,491,280,355,129,78,404,597,553,445)
# xv = (-82,57,-23,-32,89,-72,27,17,100,-94)
# yv = (-9,-58,9,-14,56,75,-32,-98,-81,-43)
# Returns: 25.467532467532468

L = foo.largestCage(xp, yp, xv, yv)

a=0
