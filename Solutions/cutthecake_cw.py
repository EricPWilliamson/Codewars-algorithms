# Task
# We have a rectangular cake with some raisins on it:
#
# cake =
#   ........
#   ..o.....
#   ...o....
#   ........
# // o is the raisins
# We need to cut the cake evenly into n small rectangular pieces, so that each small cake has 1 raisin. n is not an argument, it is the number of raisins contained inside the cake:
#
# cake =
#   ........
#   ..o.....
#   ...o....
#   ........
#
# result should be an array:
#   [
#      ........
#      ..o.....
#   ,
#      ...o....
#      ........
#   ]
# // In order to clearly show, we omit the quotes and "\n"
# If there is no solution, return an empty array []
#
# Note
# The number of raisins is always more than 1 and less than 10.
# If there are multiple solutions, select the one with the largest width of the first element of the array. (See also the examples below.)
# Evenly cut into n pieces, meaning the same area. But their shapes can be different. (See also the examples below.)
# In the result array, the order is from top to bottom and from left to right (according to the location of the upper left corner).
# Each piece of cake should be rectangular.

import numpy as np

def list_dims(cutA, W, H):
    #Takes an area and finds all the integer length rectangles that can make it. Also makes sure those dimensions dont exceed the overall WxH
    out = []
    maxw = min(cutA,W)
    for w in range(1,maxw+1):
        #First make sure we can complete the rectangle with another integer:
        if cutA % w == 0:
            h = cutA//w
            #Now make sure h isnt too big:
            if h <= H:
                #add the dimensions to our answer
                out += [[w,h]]
    return out


def check_raisins(start, end, raisins):
    #Tests if the piece defined by start and end has exactly one raisin
    counter = 0
    for r in raisins:
        if start[0] <= r[0] <= end[0] and start[1] <= r[1] <= end[1]:
            counter += 1
    return counter == 1


def update_map(start, end, cutmap):
    #Replaces a region of our map with 1s, to show the region has been cut off
    newmap = np.array(cutmap)
    newmap[start[1]:end[1]+1, start[0]:end[0]+1] = 1
    return newmap


def search_map(cutmap):
    #Finds the upper-most, left-most cell that has not yet been cut off
    i = np.where(cutmap==0)
    return [i[1][0], i[0][0]]


def check_map(start, end, cutmap):
    #Tests whether the end point is still on the map. Also checks whether all points from start:end are 0s.
    on_map = (end[0] < cutmap.shape[1]) and (end[1] < cutmap.shape[0])
    no_ones = not 1 in cutmap[start[1]:end[1] + 1, start[0]:end[0] + 1]
    return (on_map and no_ones)


def cut_piece(corners, cutmap, piece_dims, raisins):
    #Recursively finds valid pieces to cut away from the cake. Recursion continues until the first valid solution is
    # produced, or until all possibilities have been exhausted.
    start = search_map(cutmap)
    for S in reversed(piece_dims): #We perfer the largest width piece, so reverse piece_dims
        #Find the opposite corner's coordinates:
        x = start[0] + S[0] - 1
        y = start[1] + S[1] - 1
        end = [x, y]

        # Make sure we have space for this piece:
        cutmap_ok = check_map(start, end, cutmap)
        # Test whether there is exactly one raisin in this piece:
        raisin_ok = check_raisins(start, end, raisins)

        #If this piece is valid...
        if cutmap_ok and raisin_ok:
            new_cutmap = update_map(start,end,cutmap)
            new_corners = corners + [[start,end]]
            if 0 in new_cutmap:
                # ...and we still need more, proceed to next cut:
                final_corners = cut_piece(new_corners, new_cutmap, piece_dims, raisins)
                if final_corners: #If this piece isnt a dead-end, we will get back a solution
                    return final_corners
            else:
                # ...and we now have the required # of pieces, then finish up:
                return new_corners
        #If invalid, then try next piece size.
    #If none of the piece sizes worked, we must send a signal that this is a dead-end
    return []


def cut(cake):
    ###Get the basic dimensions of this cake:
    n = cake.count('o')
    W = cake.find('\n')
    H = cake.count('\n')+1
    A = W*H
    cutA = A/n
    if cutA%1 != 0:
        print("Cannot create integer area pieces")
        return []
    else:
        cutA = int(cutA)

    ###Find all the ways one piece can be made with the right area:
    piece_dims = list_dims(cutA, W, H)
    if not piece_dims:
        print("Cannot create int x int pieces")
        return []

    ###Initialize a map which allows us to track which cells have been cut off from the cake:
    cutmap = np.zeros((H,W))

    ###Find the coordinates of each raisin:
    simp_str = cake.replace('\n','')
    raisins = []
    idx = -1
    for x in range(n):
        idx = simp_str.find('o', idx+1)
        raisins += [[idx % W, idx // W]]

    ###Look for a valid solution:
    corners = cut_piece([], cutmap, piece_dims, raisins)

    ###Use the solution to generate the answer in the desired format:
    #make cake a numpy array of chars:
    cake_array = np.array(list(simp_str)).reshape(H,W)
    #Take each piece from cake_array:
    ans = []
    for X in corners:
        start = X[0]
        end = X[1]
        piece_array = cake_array[start[1]:end[1]+1, start[0]:end[0]+1]
        #Convert piece_array into desired string format:
        a = [s.astype('|S1').tostring().decode('utf-8') + '\n' for s in piece_array]
        b = ''.join(a)
        ans += [b[:-1]]
    return ans

#####PROVIDED:
def fmt(pieces):
    return '[\n%s\n]'%("\n,\n".join(pieces))

def test_assert(actual, expected):
    errmsg = 'Test Failed\nExpected:\n%s\nActual:\n%s\n'%(fmt(expected), fmt(actual))
    # Test.assert_equals(actual, expected, errmsg)
    if actual != expected:
        pass
        print(errmsg)
    else:
        print("PASS\n")
    return []

###These are the dimensions of our tests:
# L:    8   H:    4   A:   32   n:    2
# L:    8   H:    4   A:   32   n:    4
# L:    8   H:    6   A:   48   n:    4
# L:    8   H:    4   A:   32   n:    4
# L:    8   H:    4   A:   32   n:    8
# L:   16   H:   16   A:  256   n:    8

# Test.describe('Basic Tests')
# Test.it('Should work for basic tests')

cake = '''
........
..o.....
...o....
........
'''.strip()
result = [
"""
........
..o.....
""".strip(),
"""
...o....
........
""".strip()
]
test_assert(cut(cake), result)#PASS

cake = '''
.o......
......o.
....o...
..o.....
'''.strip()
result = [
".o......",
"......o.",
"....o...",
"..o....."
]
test_assert(cut(cake), result)#PASS

cake = '''
.o.o....
........
....o...
........
.....o..
........
'''.strip()
result = [
"""
.o
..
..
..
..
..
""".strip(),
"""
.o....
......
""".strip(),
"""
..o...
......
""".strip(),
"""
...o..
......
""".strip()
]
test_assert(cut(cake), result)#PASS

cake = '''
.o.o....
.o.o....
........
........
'''.strip()
result = []
test_assert(cut(cake), result)#PASS

cake = '''
.o....o.
.o....o.
........
o..oo..o
'''.strip()
result = [
"""
.o..
""".strip(),
"""
..o.
""".strip(),
"""
.o..
""".strip(),
"""
..o.
""".strip(),
"""
..
o.
""".strip(),
"""
..
.o
""".strip(),
"""
..
o.
""".strip(),
"""
..
.o
""".strip()
]
test_assert(cut(cake), result)#PASS

# A complex example ;-)
cake = '''
................
.....o..........
................
...............o
................
................
................
.....o..o.....o.
................
................
...o............
................
................
...............o
................
.o..............
'''.strip()
result = [
"""
................
.....o..........

""".strip(),
"""
................
...............o
""".strip(),
"""
........
........
........
.....o..
""".strip(),
"""
....
....
....
o...
....
....
....
....
""".strip(),
"""
....
....
....
..o.
....
....
....
.... 
""".strip(),
"""
........
........
...o....
........
""".strip(),
"""
................
...............o 
""".strip(),
"""
................
.o..............
""".strip()
]
test_assert(cut(cake), result)#PASS
