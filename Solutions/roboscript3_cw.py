#PASSED
#  RoboScript #3 - Implement the RS2 Specification
# Disclaimer
# The story presented in this Kata Series is purely fictional; any resemblance to actual programming languages, products, organisations or people should be treated as purely coincidental.
#
# About this Kata Series
# This Kata Series is based on a fictional story about a computer scientist and engineer who owns a firm that sells a toy robot called MyRobot which can interpret its own (esoteric) programming language called RoboScript. Naturally, this Kata Series deals with the software side of things (I'm afraid Codewars cannot test your ability to build a physical robot!).
#
# Story
# Last time, you implemented the RS1 specification which allowed your customers to write more concise scripts for their robots by allowing them to simplify consecutive repeated commands by postfixing a non-negative integer onto the selected command. For example, if your customers wanted to make their robot move 20 steps to the right, instead of typing FFFFFFFFFFFFFFFFFFFF, they could simply type F20 which made their scripts more concise. However, you later realised that this simplification wasn't enough. What if a set of commands/moves were to be repeated? The code would still appear cumbersome. Take the program that makes the robot move in a snake-like manner, for example. The shortened code for it was F4LF4RF4RF4LF4LF4RF4RF4LF4LF4RF4RF4 which still contained a lot of repeated commands.
#
# Task
# Your task is to allow your customers to further shorten their scripts and make them even more concise by implementing the newest specification of RoboScript (at the time of writing) that is RS2. RS2 syntax is a superset of RS1 syntax which means that all valid RS1 code from the previous Kata of this Series should still work with your RS2 interpreter. The only main addition in RS2 is that the customer should be able to group certain sets of commands using round brackets. For example, the last example used in the previous Kata in this Series:
#
# LF5RF3RF3RF7
# ... can be expressed in RS2 as:
#
# LF5(RF3)(RF3R)F7
# Or ...
#
# (L(F5(RF3))(((R(F3R)F7))))
# Simply put, your interpreter should be able to deal with nested brackets of any level.
#
# And of course, brackets are useless if you cannot use them to repeat a sequence of movements! Similar to how individual commands can be postfixed by a non-negative integer to specify how many times to repeat that command, a sequence of commands grouped by round brackets () should also be repeated n times provided a non-negative integer is postfixed onto the brackets, like such:
#
# (SEQUENCE_OF_COMMANDS)n
# ... is equivalent to ...
#
# SEQUENCE_OF_COMMANDS...SEQUENCE_OF_COMMANDS (repeatedly executed "n" times)
# For example, this RS1 program:
#
# F4LF4RF4RF4LF4LF4RF4RF4LF4LF4RF4RF4
# ... can be rewritten in RS2 as:
#
# F4L(F4RF4RF4LF4L)2F4RF4RF4
# Or:
#
# F4L((F4R)2(F4L)2)2(F4R)2F4
# All 4 example tests have been included for you. Good luck :D

import re

def simplify_code(code):
    #Inteprets all integers and parentheses in code. Returns a code string that only contains R, L, F

    ###Separate the code string into a list containing single characters and integer numbers (still as str type):
    cmds = list(filter(None, re.split('(\D)', code)))
    ### Explode the contents of each pair of parenthesis:
    while "(" in cmds:
        #Find next "(" in cmds, then find that thing's companion ")":
        depth = 0
        for i,s in enumerate(cmds):
            if s == "(":
                if depth == 0:
                    start_i = i
                depth += 1
            elif s == ")":
                depth -= 1
                if depth == 0:
                    end_i = i
                    break
        # Check if the companion is followed by a number:
        if end_i+1 < len(cmds) and cmds[end_i + 1].isdigit():
            n = int(cmds[end_i + 1])
            # Explode the contents of the parentheses:
            cmds = cmds[0:start_i] + n * cmds[start_i + 1:end_i] + cmds[end_i + 2:]
        else:
            #Just cut out these two parentheses chars:
            cmds = cmds[0:start_i] + cmds[start_i+1:end_i] + cmds[end_i+1:]
    ###Intepret all remaining digits and form a new code string
    newcode = ''
    for i,s in enumerate(cmds):
        if s.isdigit():
            for x in range(int(s)-1):
                newcode += cmds[i-1]
            if int(s) == 0:
                newcode = newcode[:-1]
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



# Test.describe("Your RS2 Interpreter")
# Test.it("should work for the example tests provided in the description")
print(execute("LF5(RF3)(RF3R)F7") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   ")
print(execute("(L(F5(RF3))(((R(F3R)F7))))") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   ")
print(execute("F4L(F4RF4RF4LF4L)2F4RF4RF4") == "    *****   *****   *****\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n*****   *****   *****   *")
print(execute("F4L((F4R)2(F4L)2)2(F4R)2F4") == "    *****   *****   *****\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n*****   *****   *****   *")

### Tricky tests:
execute("FFF0F0LFL0FF((F5R0R)2(F3R)2)0RFR0FFF0FF0F0F0")

