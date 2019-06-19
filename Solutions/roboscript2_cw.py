#PASSED
#  RoboScript #2 - Implement the RS1 Specification
# Disclaimer
# The story presented in this Kata Series is purely fictional; any resemblance to actual programming languages, products, organisations or people should be treated as purely coincidental.
#
# About this Kata Series
# This Kata Series is based on a fictional story about a computer scientist and engineer who owns a firm that sells a toy robot called MyRobot which can interpret its own (esoteric) programming language called RoboScript. Naturally, this Kata Series deals with the software side of things (I'm afraid Codewars cannot test your ability to build a physical robot!).
#
# Story
# Now that you've built your own code editor for RoboScript with appropriate syntax highlighting to make it look like serious code, it's time to properly implement RoboScript so that our MyRobots can execute any RoboScript provided and move according to the will of our customers. Since this is the first version of RoboScript, let's call our specification RS1 (like how the newest specification for JavaScript is called ES6 :p)
#
# Task
# Write an interpreter for RS1 called execute() which accepts 1 required argument code, the RS1 program to be executed. The interpreter should return a string representation of the smallest 2D grid containing the full path that the MyRobot has walked on (explained in more detail later).
#
# Initially, the robot starts at the middle of a 1x1 grid. Everywhere the robot walks it will leave a path "*". If the robot has not been at a particular point on the grid then that point will be represented by a whitespace character " ". So if the RS1 program passed in to execute() is empty then:
#
# execute(""); // => "*"
# The robot understand 3 major commands:
#
# F - Move forward by 1 step in the direction that it is currently pointing. Initially, the robot faces to the right.
# L - Turn "left" (i.e. rotate 90 degrees anticlockwise)
# R - Turn "right" (i.e. rotate 90 degrees clockwise)
# As the robot moves forward, if there is not enough space in the grid, the grid should expand accordingly. So:
#
# execute("FFFFF"); // => "******"
# As you will notice, 5 F commands in a row should cause your interpreter to return a string containing 6 "*"s in a row. This is because initially, your robot is standing at the middle of the 1x1 grid facing right. It leaves a mark on the spot it is standing on, hence the first "*". Upon the first command, the robot moves 1 unit to the right. Since the 1x1 grid is not large enough, your interpreter should expand the grid 1 unit to the right. The robot then leaves a mark on its newly arrived destination hence the second "*". As this process is repeated 4 more times, the grid expands 4 more units to the right and the robot keeps leaving a mark on its newly arrived destination so by the time the entire program is executed, 6 "squares" have been marked "*" from left to right.
#
# Each row in your grid must be separated from the next by a CRLF (\r\n). Let's look at another example:
#
# execute("FFFFFLFFFFFLFFFFFLFFFFFL"); // => "******\r\n*    *\r\n*    *\r\n*    *\r\n*    *\r\n******"
#
# /*
#   The grid looks like this:
#   ******
#   *    *
#   *    *
#   *    *
#   *    *
#   ******
# */
# The robot moves 5 units to the right, then turns left, then moves 5 units upwards, then turns left again, then moves 5 units to the left, then turns left again and moves 5 units downwards, returning to the starting point before turning left one final time. Note that the marks do not disappear no matter how many times the robot steps on them, e.g. the starting point is still marked "*" despite the robot having stepped on it twice (initially and on the last step).
#
# Another example:
#
# execute("LFFFFFRFFFRFFFRFFFFFFF"); // => "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   "
#
# /*
#   The grid looks like this:
#       ****
#       *  *
#       *  *
#   ********
#       *
#       *
# */
# Initially the robot turns left to face upwards, then moves upwards 5 squares, then turns right and moves 3 squares, then turns right again (to face downwards) and move 3 squares, then finally turns right again and moves 7 squares.
#
# Since you've realised that it is probably quite inefficient to repeat certain commands over and over again by repeating the characters (especially the F command - what if you want to move forwards 20 steps?), you decide to allow a shorthand notation in the RS1 specification which allows your customers to postfix a non-negative integer onto a command to specify how many times an instruction is to be executed:
#
# Fn - Execute the F command n times (NOTE: n may be more than 1 digit long!)
# Ln - Execute L n times
# Rn - Execute R n times
# So the example directly above can also be written as:
#
# LF5RF3RF3RF7
# These 5 example test cases have been included for you :)

import re

def simplify_code(code):
    #Converts integers in code to repeated letters. ie 'F3' becomes 'FFF'
    cmds = list(filter(None, re.split('(\D)', code)))
    # cmds = re.split('(\D\d+)', code) #Gives things like 'F31'
    # cmds = re.split('(\d+)', code) #Gives 'FR' and '351'
    newcode = ''
    for i,s in enumerate(cmds):
        if s.isdigit():
            for x in range(int(s)-1):
                newcode += cmds[i-1]
        else:
            newcode += s
    return newcode


def step_forward(start, heading):
    #Takes one step in the direction of heading:
    if heading == 0:
        return [start[0] + 1, start[1]]
    elif heading == 90:
        return [start[0], start[1] - 1]
    elif heading == 180:
        return [start[0] - 1, start[1]]
    elif heading == 270:
        return [start[0], start[1] + 1]


def execute(code):
    # Implement your RS1 interpreter here
    ###Interpret any integers in the code, simplifying it to just letters:
    code = simplify_code(code)

    ###First list out the coordinates of each step, starting at (0,0)
    coords = [[0,0]]
    heading = 0
    for s in code:
        if s == 'F':
            coords += [step_forward(coords[-1], heading)]
        elif s == 'L':
            heading = (heading+90) % 360
        elif s == 'R':
            heading = (heading-90) % 360

    ###Then convert our coordinates to an ascii map:
    #Find the height and width needed for our map:
    xs = [c[0] for c in coords]
    min_x = min(xs)
    W = max(xs) - min_x + 1
    ys = [c[1] for c in coords]
    min_y = min(ys)
    H = max(ys) - min_y + 1
    #Initialize an empty map of " "
    rmap = [" "] * W
    for y in range(H-1):
        rmap += ["\r\n"]
        rmap += [" "] * W
    #For each coordinate, convert that point to a '*' on our map
    for c in coords:
        x = c[0] - min_x
        y = c[1] - min_y
        idx = x + (W+1)*y
        rmap[idx] = "*"
    return ''.join(rmap)

# Test.describe("Your RS1 Interpreter")
# Test.it("should work for the example tests provided in the description")
print(execute("") == "*")
print(execute("FFFFF") == "******")
print(execute("FFFFFLFFFFFLFFFFFLFFFFFL") == "******\r\n*    *\r\n*    *\r\n*    *\r\n*    *\r\n******")
print(execute("LFFFFFRFFFRFFFRFFFFFFF") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   ")
print(execute("LF5RF3RF3RF7") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   ")

# execute("LF5RF3RRF12RF7")


