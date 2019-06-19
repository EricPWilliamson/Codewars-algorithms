"""
RoboScript #5 - The Final Obstacle (Implement RSU)
Disclaimer
The story presented in this Kata Series is purely fictional; any resemblance to actual programming languages, products, organisations or people should be treated as purely coincidental.

About this Kata Series
This Kata Series is based on a fictional story about a computer scientist and engineer who owns a firm that sells a toy robot called MyRobot which can interpret its own (esoteric) programming language called RoboScript. Naturally, this Kata Series deals with the software side of things (I'm afraid Codewars cannot test your ability to build a physical robot!).

Story
Since RS3 was released into the market which introduced handy pattern definitions on top of command grouping and repetition, its popularity soared within the robotics community, insomuch that other budding robotics firms have pleaded your company to allow them to use the RoboScript programming language in their products. In order to grant them their requests and protect your company at the same time, you decided to apply for a patent which would allow other companies to utilize RoboScript in their own products with certain restrictions and only with an annual fee paid to your company. So far, so good - the patent application was successful and your firm gained an ample amount of revenue in the first year from this patent alone. However, since RoboScript is still a rather small and domain-specific programming language, the restrictions listed on the patent were rather limited. Competing firms soon found a loophole in the wording of the patent which allowed them to develop their own RoboScript-like programming language with minor modifications and improvements which allowed them to legally circumvent your patent. Soon, these robotics firms start overtaking your company in terms of popularity, profitability and size. In order to investigate the main cause of the downfall of your company, a secret survey was sent to thousands of former MyRobot (and hence "official" RoboScript) users. It was revealed in this survey that the main reason for this downfall was due to the lack of readability of RS3 code (and RoboScript code in general), especially as the program becomes very large and complex. After all, it makes perfect sense - who would even bother to try to understand and maintain the following RS3 code, let alone much larger and complex programs?
p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3qP0P1P2P3P4

In a final attempt to save your company from going bankrupt and disappearing from the world of robotics, you decide to address all of the major issues identified in the secret survey head-on by designing the fourth and final specification for the RoboScript programming language - RoboScript Ultimatum (RSU). The only thing left for you to do is to properly implement the specification by writing an RSU-compliant code executor - once that is achieved, your company will catapult back into 1st position in global robotics and perhaps even leave a mark in the history of technology ...

Task
RoboScript Ultimatum (RSU) - The Official Specification
RoboScript Ultimatum (RSU) is a superset of the RS3 specification (which itself is a superset of RS2, RS2 being a superset of RS1). However, it introduces quite a few new (and handy) features.

https://www.codewars.com/kata/5a12755832b8b956a9000133
"""

#x code can contain lots of whitespace
#x multiline commments /* lkasdfljdsf */
#x single line comments //kljsadfljdsf \n   or   //lksjdf(EOF)
#x programs can be defined within programs, affecting their scope.
#x programs can share the same id, so long as they are in different scopes
#x throw error if invalid characters or stray numbers are found in code
#x F0 L0 and R0 are allowed, but do nothing
#x  empty program definitions ( "p0q" ) and empty parenthesis "FF()23" are allowed
#x leading zeroes like F03 are NOT allowed
#x pattern definitions are not allowed inside of parentheses


import re

class RSUProgram:
    def __init__(self, source):
        """
        TODO: Configure and customize your class constructor
        """
        self.source = source


    def get_tokens(self):
        """
        TODO: Convert `source` (argument from class constructor) into
        an array of tokens as specified in the Description if `source`
        is a valid RSU program; otherwise, throw an error (ideally with
        a suitable message)
        """
        """
        The following tokens are the only valid tokens:
            Single commands: F, L and R
            Commands with repeats: Fn, Ln and Rn 
            Opening round brackets: (
            Closing round brackets, with or without a repeat prefix: ) OR )n
            Pattern definition: pn
            End of pattern definition: q
            Pattern invocation: Pn
        """
        #x Remove meaningless whitespace
        #x Remove comments
        #x comments cannot split a token: "P/* comment */3
        #x throw error if invalid characters or stray numbers are found in code
        #x throw error for numbers like 05

        code = self.source
        ###First remove comments:
        #Check for split tokens:
        if re.search("/\*[\W\w]*\*/\d+", code):
            raise Exception('Error: token split by comment.')
        #Multiline comments: "/\*[\W\w]*\*/"
        code = re.sub("/\*[\W\w]*\*/", '', code)
        # Single line comments: "//.*"
        code = re.sub("//.*", '', code)

        ###Look for bugs:
        #Check for stray numbers:
        if re.search("([^)a-zA-Z\d]|^)\d+", code):
            raise Exception('Error: number in invalid location')
        #Check for numbers with leading zeros: [0]\d+
        if re.search("\D[0]\d+", code):
            raise Exception('Error: leading zero found in code')
        #Check for illegal characters:
        if re.search("[^()FLRpPq\d\s]", code):
            raise Exception('Error: illegal character used')
        #Check for programs without ID number
        if re.search("[pP](\D|$)", code):
            raise Exception('Error: pattern lacking ID number')
        # if code[-2] == "P":
        #     raise Exception('Error: P')

        ###Identify tokens:
        tokens = re.findall("[()a-zA-Z]\d*",code)
        return tokens


    def convert_to_raw(self, tokens):

        def next_definition(parent, tokens, prog_dict):
            #Recursively goes through each scope level pulling out all pattern definitions.
            while "p" in ''.join(tokens):
                scope = 0
                for i, s in enumerate(tokens):
                    if "p" in s:
                        if scope == 0:
                            p_start = i
                        scope += 1
                    elif "q" in s:
                        scope -= 1
                        if scope == 0:
                            p_end = i
                            break
                patt = tokens[p_start + 1:p_end]
                pid = parent + tokens[p_start]
                #Look for more definitions within patt and remove those definition sequences from patt:
                prog_dict,patt = next_definition(pid, patt, prog_dict)
                #Store definition in dictionary:
                prog_dict[pid] = patt
                #Make sure the definition wasn't within brakets:
                if sum(1 for s in tokens[0:p_start] if "(" in s) != sum(1 for s in tokens[0:p_start] if ")" in s):
                    raise Exception('Error: unbalenced parenthesis.')
                if sum(1 for s in tokens[p_end + 1:] if "(" in s) != sum(1 for s in tokens[p_end + 1:] if ")" in s):
                    raise Exception('Error: unbalenced parenthesis.')
                # Remove definition from tokens:
                tokens = tokens[0:p_start] + tokens[p_end + 1:]
            return prog_dict, tokens

        """
        TODO: Process the array of tokens generated by the `getTokens`
        method (passed into this method as `tokens`) and return an (new)
        array containing only the raw commands `F`, `L` and/or `R`
        Throw a suitable error if necessary
        """
        ###Throw error if:
        # !!Unmatched bracketing and/or pattern definition sequences, e.g. (p0q or p1(q)34
        # !!Nesting pattern definitions within bracketed sequences, e.g. (p0/* ... */q).
        # !!Attempting to invoke a non-existent pattern or one that invokes a non-existing pattern definition in its pattern body, etc., in the global scope
        # !!Attempting to invoke an infinitely recursive pattern of any form

        #Make sure parenthesis counts are balanced:
        if sum(1 for s in tokens if "(" in s) != sum(1 for s in tokens if ")" in s):
            raise Exception('Error: unbalenced parenthesis.')


        ###Find all program definitions and clean them out of tokens:
        prog_dict,tokens = next_definition('', tokens, {})

        ###Look at all program calls within prog_dict, and replace them with a name that includes correct ancestry:
        for pid,patt in prog_dict.items():
            for i,s in enumerate(patt):
                if "P" in s:
                    parents = list(filter(None, re.split('(p\d+)', pid)))
                    while (''.join(parents) + s.lower()) not in prog_dict:
                        #Check if we failed to find this definition:
                        if not parents:
                            #This pattern is invalid, but we dont need to throw until the code attempts to call it
                            s = 'I' #"I" for Invalid
                            break
                        # Remove the last pn from parents.
                        parents = parents[:-1]
                    new_token = ''.join(parents) + s
                    patt[i] = new_token.upper()

        ###Replace all program calls with the defined pattern:
        recursion_count = 0
        idx = next((i for i,s in enumerate(tokens) if "P" in s), None)
        while idx is not None:
            recursion_count += 1
            if recursion_count>100:
                raise Exception('Error: program seems to be creating an infinite loop')
            pid = tokens[idx].lower()
            if pid not in prog_dict or "I" in prog_dict[pid]:
                raise Exception('Error: called nonexistant program')
            tokens = tokens[0:idx] + prog_dict[pid] + tokens[idx+1:]
            idx = next((i for i, s in enumerate(tokens) if "P" in s), None)

        ### Explode the contents of each pair of parenthesis:
        while "(" in tokens:
            # Find next "(" in cmds, then find that thing's companion ")":
            depth = 0
            for i, s in enumerate(tokens):
                if s == "(":
                    if depth == 0:
                        start_i = i
                    depth += 1
                elif ")" in s:
                    depth -= 1
                    if depth == 0:
                        end_i = i
                        break
            # Check if the companion is followed by a number:
            if s[1:].isdigit():
                n = int(s[1:])
                # Explode the contents of the parentheses:
                tokens = tokens[0:start_i] + n * tokens[start_i + 1:end_i] + tokens[end_i + 1:]
            else:
                # Just cut out these two parentheses chars:
                tokens = tokens[0:start_i] + tokens[start_i + 1:end_i] + tokens[end_i + 1:]
        ###Intepret all remaining digits and form a new code string
        rawcmds = []
        for i, s in enumerate(tokens):
            if s[1:].isdigit():
                n = int(s[1:])
                rawcmds += n*[s[0]]
                # tokens = tokens[0:i] + n*[s[0]] + tokens[i+1:]
            else:
                rawcmds += [s]
        return rawcmds


    def execute_raw(self, cmds):
        def step_forward(start, heading):
            # Takes one step in the direction of heading:
            if heading == 0:
                return [start[0] + 1, start[1]]
            elif heading == 90:
                return [start[0], start[1] - 1]
            elif heading == 180:
                return [start[0] - 1, start[1]]
            elif heading == 270:
                return [start[0], start[1] + 1]

        ###First list out the coordinates of each step, starting at (0,0)
        coords = [[0, 0]]
        heading = 0
        for s in cmds:
            if s == 'F':
                coords += [step_forward(coords[-1], heading)]
            elif s == 'L':
                heading = (heading + 90) % 360
            elif s == 'R':
                heading = (heading - 90) % 360

        ###Then convert our coordinates to an ascii map:
        # Find the height and width needed for our map:
        xs = [c[0] for c in coords]
        min_x = min(xs)
        W = max(xs) - min_x + 1
        ys = [c[1] for c in coords]
        min_y = min(ys)
        H = max(ys) - min_y + 1
        # Initialize an empty map of " "
        rmap = [" "] * W
        for y in range(H - 1):
            rmap += ["\r\n"]
            rmap += [" "] * W
        # For each coordinate, convert that point to a '*' on our map
        for c in coords:
            x = c[0] - min_x
            y = c[1] - min_y
            idx = x + (W + 1) * y
            rmap[idx] = "*"
        return ''.join(rmap)


    def execute(self):
        #Processes the source code all the way through to the output map.
        tokens = self.get_tokens()
        cmds = self.convert_to_raw(tokens)
        return self.execute_raw(cmds)



badprogram = """(
  P0

  p0
    F2 R F4 L
  q
)13"""
ans = RSUProgram(badprogram).execute()

# program1 = """this is a stray comment not escaped by a double slash or slash followed by asterisk F F F L F F F R F F F L F F F R and lowercase "flr" are not acceptable as commands"""
# program2 = """F 32R 298984"""
# my_expect_error('Your tokenizer should throw an error whenever there is whitespace before numbers (stray numbers)',
#                 lambda: RSUProgram(program0).get_tokens())
# # RSU Official Specs - Finally ... - Mini Code Example 1
# my_expect_error('Your tokenizer should throw an error when there are "stray comments"',
#                 lambda: RSUProgram(program1).get_tokens())
# # RSU Official Specs - Finally ... - Mini Code Example 2
# my_expect_error('Your tokenizer should throw an error in the presence of "stray numbers"',
#                 lambda: RSUProgram(program2).get_tokens())
#
#
# my_it('should throw an error if one or more invalid tokens are detected', test_it_tokenize_invalid)
# ans = RSUProgram(program1).execute()
# ans = RSUProgram(program2).execute()
# ans = RSUProgram("F3 FFR L3").execute()

########################## My Tests ################################
# ans = RSUProgram('').execute_raw(['F','R','F','F'])


######################## Given examples: ##############################
# RSUProgram('P0P1P2P3P4p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3q').execute()


ans = RSUProgram("""/*
    RoboScript Ultimatum (RSU)
    A simple and comprehensive code example
*/

// Define a new pattern with identifier n = 0
p0
    // The commands below causes the MyRobot to move
    // in a short snake-like path upwards if executed
    (
        F2 L // Go forwards two steps and then turn left
    )2 (
        F2 R // Go forwards two steps and then turn right
    )2
q

// Execute the snake-like pattern twice to generate
// a longer snake-like pattern
(
    P0
)2
//Yippe""").execute()
print(ans == "*  \r\n*  \r\n***\r\n  *\r\n***\r\n*  \r\n***\r\n  *\r\n***")

###Example with nested patterns:
# r = RSUProgram("""// The global scope can "see" P1 and P2
# p1
#     // P1 can see P2, P3 and P4
#     p3
#         // P3 can see P1, P2 and P4 though invoking
#         // P1 will likely result in infinite recursion
#         F L
#     q
#     p4
#         // Similar rules apply to P4 as they do in P3
#         F P3
#     q
#
#     F P4
# q
# p2
#     // P2 can "see" P1 and therefore can invoke P1 if it wishes
#     F R
# q
#
# (
#     P1 P2
# )2 // Execute both globally defined patterns twice""")
# ans = r.convert_to_raw(r.get_tokens())
# print(ans == ['F', 'F', 'F', 'L', 'F', 'F', 'F', 'R', 'F', 'F', 'F', 'L', 'F', 'F', 'F', 'R'])




# Since the output of a typical RSU program can become very large,
# test output has been minimized through the implementation of
# custom "describe"s, "it"s and assertions that only print the actual
# and expected values upon failure and do not catch any errors (some
# of which are thrown by failed assertions themselves)

import time
import json
def my_describe(msg, fn):
    print('<DESCRIBE::>%s\n' % msg)
    start = time.time()
    fn()
    print('<COMPLETEDIN::>%s\n' % (1000 * (time.time() - start)))
def my_it(msg, fn):
    print('<IT::>%s\n' % msg)
    start = time.time()
    fn()
    print('<COMPLETEDIN::>%s\n' % (1000 * (time.time() - start)))
def my_assert_similar(actual, expected):
    actual_as_json = json.dumps(actual)
    expected_as_json = json.dumps(expected)
    # Test.expect(actual_as_json == expected_as_json, 'Expected: %s, instead got: %s' % (expected_as_json, actual_as_json))
    if actual_as_json != expected_as_json: raise Exception('Assertion failed - test execution halted')
def my_assert_equals(actual, expected):
    # Test.expect(actual == expected, 'Expected: \n<pre style="font-size: 8px"><code>%s</code></pre>\nActual: \n<pre style="font-size: 8px"><code>%s</code></pre>' % (expected, actual))
    if actual != expected: raise Exception('Assertion failed - test execution halted')
def my_expect_error(msg, fn):
    error_thrown = False
    try:
        fn()
    except:
        error_thrown = True
    if not error_thrown: raise Exception('Assertion failed - test execution halted')
    # Test.expect(error_thrown, msg)



def test_describe_rsu_code_executor():
    def test_describe_the_tokenizer():
        def test_it_tokenize_valid():
            # Example RS3-compliant program from the Story
            my_assert_similar(RSUProgram('p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3qP0P1P2P3P4').get_tokens(), ['p0', 'F', 'F', 'L', 'F', 'F', 'R', '(', '(', 'F', 'F', 'F', 'R', ')2', '(', 'F', 'F', 'F', 'F', 'F', 'L', ')3', ')4', 'q', 'p1', 'F', 'R', 'q', 'p2', 'F', 'P1', 'q', 'p3', 'F', 'P2', 'q', 'p4', 'F', 'P3', 'q', 'P0', 'P1', 'P2', 'P3', 'P4'])
            # RSU Official Specs - Whitespace and Indentation Support - Example 1
            my_assert_similar(RSUProgram("""p0
    (
        F2 L
    )2 (
        F2 R
    )2
q

(
    P0
)2""").get_tokens(), ['p0', '(', 'F2', 'L', ')2', '(', 'F2', 'R', ')2', 'q', '(', 'P0', ')2'])
            # RSU Official Specs - Comment Support - Code Example
            my_assert_similar(RSUProgram("""/*
    RoboScript Ultimatum (RSU)
    A simple and comprehensive code example
*/

// Define a new pattern with identifier n = 0
p0
    // The commands below causes the MyRobot to move
    // in a short snake-like path upwards if executed
    (
        F2 L // Go forwards two steps and then turn left
    )2 (
        F2 R // Go forwards two steps and then turn right
    )2
q

// Execute the snake-like pattern twice to generate
// a longer snake-like pattern
(
    P0
)2""").get_tokens(), ['p0', '(', 'F2', 'L', ')2', '(', 'F2', 'R', ')2', 'q', '(', 'P0', ')2'])
            # RSU Official Specs - Pattern Scoping - Example 1
            my_assert_similar(RSUProgram("""// The global scope can "see" P1 and P2
p1
    // P1 can see P2, P3 and P4
    p3
        // P3 can see P1, P2 and P4 though invoking
        // P1 will likely result in infinite recursion
        F L
    q
    p4
        // Similar rules apply to P4 as they do in P3
        F P3
    q

    F P4
q
p2
    // P2 can "see" P1 and therefore can invoke P1 if it wishes
    F3 R
q

(
    P1 P2
)2 // Execute both globally defined patterns twice""").get_tokens(), ['p1', 'p3', 'F', 'L', 'q', 'p4', 'F', 'P3', 'q', 'F', 'P4', 'q', 'p2', 'F3', 'R', 'q', '(', 'P1', 'P2', ')2'])
            # RSU Official Specs - Pattern Scoping - Example 2
            my_assert_similar(RSUProgram("""p1
    p1
        F R
    q

    F2 P1 // Refers to "inner" (locally defined) P1 so no infinite recursion results
q

(
    F2 P1 // Refers to "outer" (global) P1 since the
    // global scope can't "see" local P1
)4

/*
    Equivalent to executing the following raw commands:
    F F F F F R F F F F F R F F F F F R F F F F F R
*/""").get_tokens(), ['p1', 'p1', 'F', 'R', 'q', 'F2', 'P1', 'q', '(', 'F2', 'P1', ')4'])
        my_it('should correctly tokenize valid RSU programs', test_it_tokenize_valid)

        def test_it_tokenize_invalid():
            # RSU Official Specs - Whitespace and Indentation Support - Example 2
            program0 = """p 0
    (
        F 2L
    ) 2 (
        F 2 R
    )                 2
q

(
    P    0
)2"""
            program1 = """this is a stray comment not escaped by a double slash or slash followed by asterisk F F F L F F F R F F F L F F F R and lowercase "flr" are not acceptable as commands"""
            program2 = """F 32R 298984"""
            my_expect_error('Your tokenizer should throw an error whenever there is whitespace before numbers (stray numbers)', lambda: RSUProgram(program0).get_tokens())
            # RSU Official Specs - Finally ... - Mini Code Example 1
            my_expect_error('Your tokenizer should throw an error when there are "stray comments"', lambda: RSUProgram(program1).get_tokens())
            # RSU Official Specs - Finally ... - Mini Code Example 2
            my_expect_error('Your tokenizer should throw an error in the presence of "stray numbers"', lambda: RSUProgram(program2).get_tokens())
        my_it('should throw an error if one or more invalid tokens are detected', test_it_tokenize_invalid)
    my_describe('The tokenizer', test_describe_the_tokenizer)

    def test_describe_the_compiler():
        def test_it_convert_vaild():
            # Description Example in Converter section
            r = RSUProgram('p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3qP0P1P2P3P4')
            my_assert_similar(r.convert_to_raw(r.get_tokens()), [
                'F', 'F', 'L', 'F', 'F', 'R',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'R',
                'F', 'F', 'R',
                'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'R'
            ])
            # Description Example in Converter section - Pattern Invocation before Definition
            r = RSUProgram('P0P1P2P3P4p0FFLFFR((FFFR)2(FFFFFL)3)4qp1FRqp2FP1qp3FP2qp4FP3q')
            my_assert_similar(r.convert_to_raw(r.get_tokens()), [
                'F', 'F', 'L', 'F', 'F', 'R',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'R', 'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'F', 'F', 'F', 'F', 'L',
                'F', 'R',
                'F', 'F', 'R',
                'F', 'F', 'F', 'R',
                'F', 'F', 'F', 'F', 'R'
            ])

            # A few more examples based on Description code snippets
            r = RSUProgram("""p0
    (
        F2 L
    )2 (
        F2 R
    )2
q

(
    P0
)2""")
            my_assert_similar(r.convert_to_raw(r.get_tokens()), ['F', 'F', 'L', 'F', 'F', 'L', 'F', 'F', 'R', 'F', 'F', 'R', 'F', 'F', 'L', 'F', 'F', 'L', 'F', 'F', 'R', 'F', 'F', 'R'])
            r = RSUProgram("""// The global scope can "see" P1 and P2
p1
    // P1 can see P2, P3 and P4
    p3
        // P3 can see P1, P2 and P4 though invoking
        // P1 will likely result in infinite recursion
        F L
    q
    p4
        // Similar rules apply to P4 as they do in P3
        F P3
    q

    F P4
q
p2
    // P2 can "see" P1 and therefore can invoke P1 if it wishes
    F3 R
q

(
    P1 P2
)2 // Execute both globally defined patterns twice""")
            my_assert_similar(r.convert_to_raw(r.get_tokens()), ['F', 'F', 'F', 'L', 'F', 'F', 'F', 'R', 'F', 'F', 'F', 'L', 'F', 'F', 'F', 'R'])
            r = RSUProgram("""p1
    p1
        F R
    q

    F2 P1 // Refers to "inner" (locally defined) P1 so no infinite recursion results
q

(
    F2 P1 // Refers to "outer" (global) P1 since the
    // global scope can't "see" local P1
)4

/*
    Equivalent to executing the following raw commands:
    F F F F F R F F F F F R F F F F F R F F F F F R
*/""")
            my_assert_similar(r.convert_to_raw(r.get_tokens()), ['F', 'F', 'F', 'F', 'F', 'R', 'F', 'F', 'F', 'F', 'F', 'R', 'F', 'F', 'F', 'F', 'F', 'R', 'F', 'F', 'F', 'F', 'F', 'R'])
        my_it('should correctly convert valid RSU token sequences into raw command sequences', test_it_convert_vaild)
    my_describe('The compiler', test_describe_the_compiler)
    def test_describe_the_ins_executor():
        def test_it_work_for_example():
            program = RSUProgram("""/*
    RoboScript Ultimatum (RSU)
    A simple and comprehensive code example
*/

// Define a new pattern with identifier n = 0
p0
    // The commands below causes the MyRobot to move
    // in a short snake-like path upwards if executed
    (
        F2 L // Go forwards two steps and then turn left
    )2 (
        F2 R // Go forwards two steps and then turn right
    )2
q

// Execute the snake-like pattern twice to generate
// a longer snake-like pattern
(
    P0
)2""")
            my_assert_equals(program.execute_raw(program.convert_to_raw(program.get_tokens())), "*  \r\n*  \r\n***\r\n  *\r\n***\r\n*  \r\n***\r\n  *\r\n***")
        my_it('should work for the example provided in the Description', test_it_work_for_example)
        def test_it_work_for_example_another():
            my_assert_equals(RSUProgram("""/*
    RoboScript Ultimatum (RSU)
    A simple and comprehensive code example
*/

// Define a new pattern with identifier n = 0
p0
    // The commands below causes the MyRobot to move
    // in a short snake-like path upwards if executed
    (
        F2 L // Go forwards two steps and then turn left
    )2 (
        F2 R // Go forwards two steps and then turn right
    )2
q

// Execute the snake-like pattern twice to generate
// a longer snake-like pattern
(
    P0
)2""").execute(), "*  \r\n*  \r\n***\r\n  *\r\n***\r\n*  \r\n***\r\n  *\r\n***")
        my_it('should work for the example provided in the Description', test_it_work_for_example_another)
    my_describe('The machine instructions executor', test_describe_the_ins_executor)
my_describe('Your RSU code executor (class RSUProgram)', test_describe_rsu_code_executor)
