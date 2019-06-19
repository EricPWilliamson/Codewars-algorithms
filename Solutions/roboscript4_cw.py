#PASSED
# RoboScript #4 - RS3 Patterns to the Rescue
# Disclaimer
# The story presented in this Kata Series is purely fictional; any resemblance to actual programming languages, products, organisations or people should be treated as purely coincidental.
#
# About this Kata Series
# This Kata Series is based on a fictional story about a computer scientist and engineer who owns a firm that sells a toy robot called MyRobot which can interpret its own (esoteric) programming language called RoboScript. Naturally, this Kata Series deals with the software side of things (I'm afraid Codewars cannot test your ability to build a physical robot!).
#
# Story
# Ever since you released RS2 to the market, there have been much fewer complaints from RoboScript developers about the inefficiency of the language and the popularity of your programming language has continuously soared. It has even gained so much attention that Zachary Mikowski, the CEO of the world-famous Doodle search engine, has contacted you to try out your product! Initially, when you explain the RoboScript (RS2) syntax to him, he looks satisfied, but then he soon finds a major loophole in the efficiency of the RS2 language and brings forth the following program:
#
# (F2LF2R)2FRF4L(F2LF2R)2(FRFL)4(F2LF2R)2
# As you can see from the program above, the movement sequence (F2LF2R)2 has to be rewritten every time and no amount of RS2 syntax can simplify it because the movement sequences in between are different each time (FRF4L and (FRFL)4). If only RoboScript had a movement sequence reuse feature that makes writing programs like these less repetitive ...
#
# Task
# Define and implement the RS3 specification whose syntax is a superset of RS2 (and RS1) syntax. Your interpreter should be named execute() and accept exactly 1 argument $code, the RoboScript code to be executed.
#
# Patterns - The New Feature
# To solve the problem outlined in the Story above, you have decided to introduce a new syntax feature to RS3 called the "pattern". The "pattern" as defined in RS3 behaves rather like a primitive version of functions/methods in other programming languages - it allows the programmer to define and name (to a certain extent) a certain sequence of movements which can be easily referenced and reused later instead of rewriting the whole thing.
#
# The basic syntax for defining a pattern is as follows:
#
# p(n)<CODE_HERE>q
# Where:
#
# p is a "keyword" that declares the beginning of a pattern definition (much like the function keyword in JavaScript or the def keyword in Python)
# (n) is any non-negative integer (without the round brackets) which acts as a unique identifier for the pattern (much like a function/method name)
# <CODE_HERE> is any valid RoboScript code (without the angled brackets)
# q is a "keyword" that marks the end of a pattern definition (like the end keyword in Ruby)
# For example, if I want to define (F2LF2R)2 as a pattern and reuse it later in my code:
#
# p0(F2LF2R)2q
# It can also be rewritten as below since (n) only serves as an identifier and its value doesn't matter:
#
# p312(F2LF2R)2q
# Like function/method definitions in other languages, merely defining a pattern (or patterns) in RS3 should cause no side effects, so:
#
# execute('p0(F2LF2R)2q'); // => '*'
# execute('p312(F2LF2R)2q'); // => '*'
# To invoke a pattern (i.e. make the MyRobot move according to the movement sequences defined inside the pattern), a capital P followed by the pattern identifier (n) is used:
#
# P0
# (or P312, depending on which example you are using)
#
# So:
#
# execute('p0(F2LF2R)2qP0'); // => "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "
# execute('p312(F2LF2R)2qP312'); // => "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "
# Additional Rules for parsing RS3
# It doesn't matter whether the invocation of the pattern or the pattern definition comes first - pattern definitions should always be parsed first, so:
#
# execute('P0p0(F2LF2R)2q'); // => "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "
# execute('P312p312(F2LF2R)2q'); // => "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "
# Of course, RoboScript code can occur anywhere before and/or after a pattern definition/invocation, so:
#
# execute('F3P0Lp0(F2LF2R)2qF2'); // => "       *\r\n       *\r\n       *\r\n       *\r\n     ***\r\n     *  \r\n******  "
# Much like a function/definition can be invoked multiple times in other languages, a pattern should also be able to be invoked multiple times in RS3. So:
#
# execute('(P0)2p0F2LF2RqP0'); // => "      *\r\n      *\r\n    ***\r\n    *  \r\n  ***  \r\n  *    \r\n***    "
# If a pattern is invoked which does not exist, your interpreter should throw. This could be anything and will not be tested, but ideally it should provide a useful message which describes the error in detail. In PHP this must be an instance of ParseError.
#
# execute('p0(F2LF2R)2qP1'); // throws ParseError
# execute('P0p312(F2LF2R)2q'); // throws ParseError
# execute('P312'); // throws ParseError
# Much like any good programming language will allow you to define an unlimited number of functions/methods, your RS3 interpreter should also allow the user to define a virtually unlimited number of patterns. A pattern definition should be able to invoke other patterns if required. If the same pattern (i.e. both containing the same identifier (n)) is defined more than once, your interpreter should throw (again, anything). In PHP this error must again be an instance of ParseError.
#
# execute('P1P2p1F2Lqp2F2RqP2P1'); // => "  ***\r\n  * *\r\n*** *"
# execute('p1F2Lqp2F2Rqp3P1(P2)2P1q(P3)3'); // => "  *** *** ***\r\n  * * * * * *\r\n*** *** *** *"
# execute('p1F2Lqp1(F3LF4R)5qp2F2Rqp3P1(P2)2P1q(P3)3'); // throws ParseError
# Furthermore, your interpreter should be able to detect (potentially) infinite recursion, including mutual recursion. Instead of just getting stuck in an infinite loop and timing out, your interpreter should throw (yes, anything again) when the "stack" (or just the total number of pattern invocations) exceeds a particular very high (but sensible) threshold. In PHP, the thrown error once again must be an instance of ParseError.
#
# execute('p1F2RP1F2LqP1'); // throws ParseError
# execute('p1F2LP2qp2F2RP1qP1'); // throws ParseError
# For the sake of simplicity, you may assume that all programs passed into your interpreter contains valid syntax and that pattern definitions will never be empty. Furthermore, nesting pattern definitions is not allowed either (it is considered a syntax error) so your interpreter will not need to account for these.

# x Programs can be defined like this: p0(F2LF2R)2q
# x Programs can be called at any point in code like this P0
# x Throw if same program number defined more than once
# x Throw if undefined program is called
# x Throw if patterns are invoked repeatedly a large number of times (infinite loop)

import re

def replace_calls(code, prog_dict):
    #Finds any program calls within code, and replaces them with the defined program.
    recursion_count = 0
    match = re.search("P\d*", code)
    while match:
        #Make sure recursion is not getting out of control:
        recursion_count += 1
        if recursion_count > 100:
            raise ValueError('Error: Input code is generating an infinite loop.')
        #Check the pid:
        pid = match.group()[1:]
        if pid not in prog_dict:
            raise ValueError('Error: Code attempted to call an undefined program.')
        #Replace the program call in code with actual commands:
        code = code[0:match.start()] + prog_dict[pid] + code[match.end():]
        #Find next program call:
        match = re.search("P\d*", code)
    return code


def extract_progs(code):
    #Handles all program definitions and program calls within code.

    ###Process all the program definitions found in code
    prog_dict = {}
    for match in re.finditer("p[^q]*q", code):
        prog = match.group()
        #Get program's id number:
        pid = re.search("\d+",prog).group()
        #Throw error if id number was already used:
        if pid in prog_dict:
            raise ValueError('Error: Same program ID defined more than once.')
        #Store the content of prog in our dict, trimming off the 'p(n)' and 'q'
        prog_dict[pid] = prog[1+len(pid) : -1]
    #Remove program definitions from code:
    lst = list(filter(None, re.split("p[^q]*q", code)))
    newcode = ''.join(lst)

    ###Replace program calls with program contents:
    newcode = replace_calls(newcode,prog_dict)
    return newcode


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
    ### Find all program definitions within code. Remove them from code, but save the definitions in prog_dict
    code= extract_progs(code)
    ###

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


# Test.describe('Your RS3 Interpreter')
def assert_path_equals(actual, expected):
    if actual != expected:
        print("You returned:")
        print(actual)
        print("Expected path of MyRobot:")
        print(expected)
    print(actual == expected)
def expect_error(why, code):
    # expect_error(why, lambda: execute(code))
    pass

tests = [
    ('should work for RS2-compliant programs', [
        lambda: assert_path_equals(execute('(F2LF2R)2FRF4L(F2LF2R)2(FRFL)4(F2LF2R)2'), "    **   **      *\r\n    **   ***     *\r\n  **** *** **  ***\r\n  *  * *    ** *  \r\n***  ***     ***  ")
    ]),
    ('should properly parse a pattern definition and not cause any side effects', [
        lambda: assert_path_equals(execute('p0(F2LF2R)2q'), '*'),
        lambda: assert_path_equals(execute('p312(F2LF2R)2q'), '*')
    ]),
    ('should execute a given pattern when it is invoked', [
        lambda: assert_path_equals(execute('p0(F2LF2R)2qP0'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "),
        lambda: assert_path_equals(execute('p312(F2LF2R)2qP312'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  ")
    ]),
    ('should always parse pattern definitions first before attempting to invoke them', [
        lambda: assert_path_equals(execute('P0p0(F2LF2R)2q'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "),
        lambda: assert_path_equals(execute('P312p312(F2LF2R)2q'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  ")
    ]),
    ('should allow other forms of RoboScript code alongside pattern definitions and invocations', [
        lambda: assert_path_equals(execute('F3P0Lp0(F2LF2R)2qF2'), "       *\r\n       *\r\n       *\r\n       *\r\n     ***\r\n     *  \r\n******  ")
    ]),
    ('should allow a pattern to be invoked multiple times', [
        lambda: assert_path_equals(execute('(P0)2p0F2LF2RqP0'), "      *\r\n      *\r\n    ***\r\n    *  \r\n  ***  \r\n  *    \r\n***    ")
    ]),
    ('should throw an error when a non-existing pattern is invoked', [
        lambda: expect_error('Your interpreter should throw an error because pattern "P1" does not exist', 'p0(F2LF2R)2qP1'),
        lambda: expect_error('Your interpreter should throw an error because pattern "P0" does not exist', 'P0p312(F2LF2R)2q'),
        lambda: expect_error('Your interpreter should throw an error because pattern "P312" does not exist', 'P312')
    ]),
    ('should properly parse multiple pattern definitions', [
        lambda: assert_path_equals(execute('P1P2p1F2Lqp2F2RqP2P1'), "  ***\r\n  * *\r\n*** *"),
        lambda: assert_path_equals(execute('p1F2Lqp2F2Rqp3P1(P2)2P1q(P3)3'), "  *** *** ***\r\n  * * * * * *\r\n*** *** *** *")
    ]),
    ('should throw an error when a pattern is defined more than once', [
        lambda: expect_error('Your interpreter should throw an error since pattern "P1" is defined twice', 'p1F2Lqp1(F3LF4R)5qp2F2Rqp3P1(P2)2P1q(P3)3')
    ]),
    ('should throw an error when any form of infinite recursion is detected', [
        lambda: expect_error('should throw an error when any form of infinite recursion is detected', 'p1F2RP1F2LqP1'),
        lambda: expect_error('Your interpreter should throw an error since pattern "P1" invokes "P2" which then again invokes "P1", creating an infinite cycle', 'p1F2LP2qp2F2RP1qP1')
    ])
]

for scenario in tests:
    message, assertions = scenario
    print(message)
    for assertion in assertions:
        assertion()
