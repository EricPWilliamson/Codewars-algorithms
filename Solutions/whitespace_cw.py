"""
Whitespace
Whitespace is an esoteric programming language that uses only three characters:

[space] or " " (ASCII 32)
[tab] or "\t" (ASCII 9)
[line-feed] or "\n" (ASCII 10)
All other characters may be used for comments. The interpreter ignores them.

Whitespace is an imperative, stack-based programming language, including features such as subroutines.


"""

from timeit import default_timer as timer

class ReadCode:
    def __init__(self, code, inp):
        self.code = code
        self.inp = inp
        self.cursor = 0
        self.inp_cursor = 0
        self.stack = []
        self.heap = {}
        self.labels = {}
        self.jump_back = 0
        self.log = '-START-'
        self.output = ''
        self.scan_only = False
        self.fix_labels = False
        self.terminate = False

    def eat_char(self):
        c = self.code[self.cursor]
        self.cursor += 1
        return c

    def push(self,n):
        if not self.scan_only:
            self.stack = [n] + self.stack

    def pop_stack(self):
        if self.scan_only:
            return 1
        else:
            if len(self.stack)==0:
                raise Exception('Attempted to pop from empty stack.')
            out = self.stack[0]
            self.stack = self.stack[1:]#!!not sure
            return out

    def eat_inp_char(self):
        if self.scan_only:
            return '0'
        else:
            if self.inp_cursor >= len(self.inp):
                raise Exception('Inp has run out.')
            c = self.inp[self.inp_cursor]
            self.inp_cursor += 1
            return c

    def read_imp(self):
        ###Find next IMP:
        c = self.eat_char()
        if c=='s':
            self.log += '\n>[{}]stack manipulation:'.format(self.cursor)
            self.stack_man()
        elif c=='n':
            self.log += '\n>[{}]flow control:'.format(self.cursor)
            self.flow_control()
        elif c=='t':
            c = self.eat_char()
            if c=='s':
                self.log += '\n>[{}]arithmatic:'.format(self.cursor)
                self.arithmatic()
            elif c=='n':
                self.log += '\n>[{}]input output:'.format(self.cursor)
                self.input_output()
            elif c=='t':
                self.log += '\n>[{}]heap access:'.format(self.cursor)
                self.heap_access()

    def parse_binary(self):
        ###List out binary digits until we hit [terminal]
        bit_str = ''
        while True:
            c = self.eat_char()
            if c=='n':
                #terminal char
                break
            elif c=='t':
                #binary '1'
                bit_str += '1'
            elif c=='s':
                #binary '0'
                bit_str += '0'
        ###Finish up:
        if len(bit_str)>0:
            return int(bit_str,2)
        else:
            return 0

    def read_number(self):
        """
        Parsing Numbers
        -Numbers begin with a [sign] symbol. The sign symbol is either [tab] -> negative, or [space] -> positive.
        -Numbers end with a [terminal] symbol: [line-feed].
        -Between the sign symbol and the terminal symbol are binary digits [space] -> binary-0, or [tab] -> binary-1.
        -A number expression [sign][terminal] will be treated as zero.
        -The expression of just [terminal] should throw an error. (The Haskell implementation is inconsistent about this.)
        """
        ###First get [sign]:
        c = self.eat_char()
        if c=='t':
            sign = -1
        elif c=='s':
            sign = 1
        elif c=='n':
            raise Exception('Number input lacks valid [sign].')
        ###Then read the binary integer:
        num = self.parse_binary() * sign
        self.log += str(num)
        return num

    def read_label(self):
        """
        Parsing Labels
        -Labels begin with any number of [tab] and [space] characters.
        -Labels end with a terminal symbol: [line-feed].
        -Unlike with numbers, the expression of just [terminal] is valid.
        -Labels must be unique.
        -A label may be declared either before or after a command that refers to it.
        """
        # label = str(self.parse_binary())#!!BAD
        label = ''
        while True:
            c = self.eat_char()
            if c=='n':
                #terminal char
                break
            else:
                label += c

        self.log += "'" + label + "'"
        return label

    def jump_to(self,label):
        if not self.scan_only:
            if label not in self.labels:
                print('Reading ahead for labels...')
                self.scan_only = True
            else:
                self.cursor = self.labels[label]

    def stack_man(self):
        """
        IMP [space] - Stack Manipulation
        [space] (number): Push n onto the stack.
        [tab][space] (number): Duplicate the nth value from the top of the stack.
        [tab][line-feed] (number): Discard the top n values below the top of the stack from the stack. (For n<0 or n>=stack.length, remove everything but the top value.)
        [line-feed][space]: Duplicate the top value on the stack.
        [line-feed][tab]: Swap the top two value on the stack.
        [line-feed][line-feed]: Discard the top value on the stack.
        """
        c = self.eat_char()
        if c == 's':
            #Push n onto the stack.
            self.log += ' Push '
            n = self.read_number()
            self.push(n)
        elif c == 't':
            c = self.eat_char()
            if c == 's':
                #Duplicate the nth value from the top of the stack
                self.log += ' Duplicate '
                n = self.read_number()
                if not self.scan_only:
                    if n>=len(self.stack) or n<0:
                        raise Exception('Non existant stack address.')
                    self.push(self.stack[n])
            elif c == 'n':
                #Discard the top n values below the top of the stack from the stack. (For n<0 or n>=stack.length, remove everything but the top value.)
                self.log += ' Discard '
                n = self.read_number()
                if not self.scan_only:
                    if n < 0 or n >= (len(self.stack)-1):
                        self.stack = [self.stack[0]]
                    else:
                        self.stack = [self.stack[0]] + self.stack[n+1:] #!!not sure
            else:
                raise Exception('Invalid command')
        elif c == 'n':
            c = self.eat_char()
            if c=='s':
                #Duplicate the top value on the stack.
                self.log += ' Duplicate top '
                if not self.scan_only:
                    self.push(self.stack[0])
            elif c=='t':
                #Swap the top two value on the stack.
                self.log += ' Swap top '
                if not self.scan_only:
                    self.stack = [self.stack[1]] + [self.stack[0]] + self.stack[2:] #!!not sure
            elif c=='n':
                #Discard the top value on the stack.
                self.log += ' Discard top '
                if not self.scan_only:
                    if len(self.stack) == 0:
                        raise Exception('Stack is already empty.')
                    self.stack = self.stack[1:] #!!not sure

    def flow_control(self):
        """
        IMP [line-feed] - Flow Control
        [space][space] (label): Mark a location in the program with label n.
        [space][tab] (label): Call a subroutine with the location specified by label n.
        [space][line-feed] (label): Jump unconditionally to the position specified by label n.
        [tab][space] (label): Pop a value off the stack and jump to the label specified by n if the value is zero.
        [tab][tab] (label): Pop a value off the stack and jump to the label specified by n if the value is less than zero.
        [tab][line-feed]: Exit a subroutine and return control to the location from which the subroutine was called.
        [line-feed][line-feed]: Exit the program.
        """
        c1 = self.eat_char()
        c2 = self.eat_char()
        cmd = c1+c2
        if cmd=='ss':
            #Mark a location in the program with label n
            self.log += ' Mark label '
            label = self.read_label()
            if not self.fix_labels:
                if label in self.labels:
                    raise Exception('Same label used twice.')
                self.labels[label] = self.cursor #!!correct cursor postion?
        elif cmd=='st':
            #Call a subroutine with the location specified by label n.
            self.log += ' Call subroutine '
            label = self.read_label()
            self.jump_back = self.cursor
            self.jump_to(label)
        elif cmd=='sn':
            #Jump unconditionally to the position specified by label n.
            self.log += ' Jump to label '
            label = self.read_label()
            self.jump_to(label)
        elif cmd=='ts':
            #Pop a value off the stack and jump to the label specified by n if the value is zero.
            self.log += ' If zero jump to label '
            label = self.read_label()
            if self.pop_stack() == 0:
                self.jump_to(label)
        elif cmd=='tt':
            #Pop a value off the stack and jump to the label specified by n if the value is less than zero.
            self.log += ' If neg jump to label '
            label = self.read_label()
            if self.pop_stack() < 0:
                self.jump_to(label)
        elif cmd=='tn':
            #Exit a subroutine and return control to the location from which the subroutine was called.
            self.log += ' Exit subroutine '
            if not self.scan_only:
                if self.jump_back==0:
                    raise Exception('Attempted to exit subroutine before entering one')
                self.cursor = self.jump_back
                self.jump_back = 0
        elif cmd=='nn':
            #Exit the program.
            self.log += ' Exit program '
            self.terminate = True
        else:
            raise Exception('Invalid command')

    def arithmatic(self):
        """
        IMP [tab][space] - Arithmetic
        [space][space]: Pop a and b, then push b+a.
        [space][tab]: Pop a and b, then push b-a.
        [space][line-feed]: Pop a and b, then push b*a.
        [tab][space]: Pop a and b, then push b/a*. If a is zero, throw an error.
        *Note that the result is defined as the floor of the quotient.
        [tab][tab]: Pop a and b, then push b%a*. If a is zero, throw an error.
        *Note that the result is defined as the remainder after division and sign (+/-) of the divisor (a).
        """
        c1 = self.eat_char()
        c2 = self.eat_char()
        cmd = c1+c2
        a = self.pop_stack()
        b = self.pop_stack()
        if cmd=='ss':
            self.log += ' Calc b+a'
            self.push(b+a)
        elif cmd=='st':
            self.log += ' Calc b-a'
            self.push(b-a)
        elif cmd=='sn':
            self.log += ' Calc b*a'
            self.push(b*a)
        elif cmd=='ts':
            self.log += ' Calc b//a'
            self.push(b//a)
        elif cmd=='tt':
            self.log += ' Calc b%a'
            self.push(b%a)
        else:
            raise Exception('Invalid command')

    def input_output(self):
        """
        IMP [tab][line-feed] - Input/Output
        [space][space]: Pop a value off the stack and output it as a character.
        [space][tab]: Pop a value off the stack and output it as a number.
        [tab][space]: Read a character from input, a, Pop a value off the stack, b, then store the ASCII value of a at heap address b.
        [tab][tab]: Read a number from input, a, Pop a value off the stack, b, then store a at heap address b.

        !!An error should be thrown if the input ends before parsing is complete.
        """
        c = self.eat_char()
        if c=='s':
            c = self.eat_char()
            if c=='s':
                #Pop a value off the stack and output it as a character.
                self.log += ' Pop char '
                n = self.pop_stack()
                self.output += chr(n)
            elif c=='t':
                #Pop a value off the stack and output it as a number.
                self.log += ' Pop num '
                n = self.pop_stack()
                self.output += str(n)
            else:
                raise Exception('Invalid command')
        elif c=='t':
            c = self.eat_char()
            if c=='s':
                #Read a character from input, 'a', Pop a value off the stack, 'b', then store the ASCII value of 'a' at heap address 'b'.
                self.log += ' Input char '
                a = self.eat_inp_char()
                self.log += a
                b = self.pop_stack()
                self.heap[str(b)] = ord(a)

            elif c=='t':
                #Read a number from input, 'a', Pop a value off the stack, 'b', then store 'a' at heap address 'b'.
                self.log += ' Input num '
                num_str = self.eat_inp_char()
                while self.inp[self.inp_cursor] in '+-0123456789':
                    num_str += self.eat_inp_char()
                a = int(num_str)
                self.log += str(a)
                b = self.pop_stack()
                self.heap[str(b)] = a
            else:
                raise Exception('Invalid command')
        else:
            raise Exception('Invalid command')

    def heap_access(self):
        """
        IMP [tab][tab] - Heap Access
        [space]: Pop a and b, then store a at heap address b.
        [tab]: Pop a and then push the value at heap address a onto the stack.
        """
        c = self.eat_char()
        if c=='s':
            #Pop a and b, then store a at heap address b.
            self.log += ' Store '
            a = self.pop_stack()
            b = self.pop_stack()
            self.log += str(a) + ' at ' + str(b)
            self.heap[str(b)] = a
        elif c=='t':
            #Pop a and then push the value at heap address a onto the stack.
            self.log += ' Retrieve from heap at '
            a = self.pop_stack()
            self.log += str(a)
            if not self.scan_only:
                self.stack = [self.heap[str(a)]] + self.stack
        else:
            raise Exception('Invalid command')

    def execute(self):
        ###First just try to run the code normally
        while not self.terminate and not self.scan_only:
            self.read_imp()

        ###If we catch a label error, we will have to scan the code first:
        if self.scan_only:
            ###Now reinitialize and scan the code:
            self.cursor = 0
            self.inp_cursor = 0
            self.stack = []
            self.heap = {}
            self.log = '-START-'
            self.output = ''
            self.labels = {}
            self.terminate = False
            while self.cursor < len(self.code):
                self.read_imp()
            ###Reinitialize again and run code:
            self.cursor = 0
            self.inp_cursor = 0
            self.stack = []
            self.heap = {}
            self.log = '-START-'
            self.output = ''
            self.scan_only = False
            self.fix_labels = True
            self.terminate = False
            while not self.terminate and not self.scan_only:
                self.read_imp()

        if not self.terminate:
            raise Exception('Code could not be completed')

        self.log += '\n-END-'
        print(self.log)
        return self.output


def unbleach(n):
    n = ''.join(c for c in n if c in ' \t\n') #Removes any extraneous characters.
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')

def whitespace(code, inp=''):
    t1 = timer()
    print('')
    print('input string:')
    print([inp])
    print("Input code:")
    print([code])
    code = unbleach(code)
    print([code])
    output = ReadCode(code,inp).execute()
    print([output])
    t2 = timer()
    print("Runtime: {:.1f}ms".format((t2-t1)*1000))
    return output


########################################################
class MyTest:
    def describe(self, s):
        print('==================')
        print(s)

    def assert_equals(self, output, answer):
        print("++++", output == answer)
        if output != answer:
            print("Incorrect output:")
            print([output])
            print("Desired output:")
            print([answer])

Test = MyTest()

#PASSED
# Test.describe("Testing push, output of numbers 0 through 3")
# output1 = "   \t\n\t\n \t\n\n\n"
# output2 = "   \t \n\t\n \t\n\n\n"
# output3 = "   \t\t\n\t\n \t\n\n\n"
# output0 = "    \n\t\n \t\n\n\n"
# Test.assert_equals(whitespace(output1), "1")
# Test.assert_equals(whitespace(output2), "2")
# Test.assert_equals(whitespace(output3), "3")
# Test.assert_equals(whitespace(output0), "0")
#
# #PASSED
# Test.describe("Testing ouput of numbers -1 through -3")
# outputNegative1 = "  \t\t\n\t\n \t\n\n\n"
# outputNegative2 = "  \t\t \n\t\n \t\n\n\n"
# outputNegative3 = "  \t\t\t\n\t\n \t\n\n\n"
# Test.assert_equals(whitespace(outputNegative1), "-1")
# Test.assert_equals(whitespace(outputNegative2), "-2")
# Test.assert_equals(whitespace(outputNegative3), "-3")
#
# #PASSED
# Test.describe("Testing output of letters A through C")
# outputA = "   \t     \t\n\t\n  \n\n\n"
# outputB = "   \t    \t \n\t\n  \n\n\n"
# outputC = "   \t    \t\t\n\t\n  \n\n\n"
# Test.assert_equals(whitespace(outputA), "A")
# Test.assert_equals(whitespace(outputB), "B")
# Test.assert_equals(whitespace(outputC), "C")

################## Extra Tests #####################
# Test.describe("Testing input functionality")
# whitespace('   \t\n\t\n\t\t   \t \n\t\n\t\t   \t\t\n\t\n\t\t   \t\t\n\t\t\t   \t \n\t\t\t   \t\n\t\t\t\t\n \t\t\n \t\t\n \t\n\n\n',
#            '1\n2\n3\n') #should equal ?

# whitespace('   \t\n\t\n\t    \t \n\t\n\t    \t\t\n\t\n\t    \t  \n\t\n\t    \t \t\n\t\n\t    \t \t\n\t\t\t   \t  \n\t\t\t   \t\t\n\t\t\t   \t \n\t\t\t   \t\n\t\t\t\t\n  \t\n  \t\n  \t\n  \t\n  \n\n\n',
#            '12345')

# Test.describe('Testing jump fuctionality')
# whitespace('   \n   \t\n   \t \n   \t\t\n\n  \n\t\n \t \n \n\t  \n\n \n\n\n   \n\n\n\n')

#Should throw error:
whitespace('\n\n   \t\n\n\n\n')


# Test.describe('Testing subroutine functionality')
# whitespace('   \t\n\n \t \n   \t \n\n \t \n   \t\t\n\n \t \n\n\n\n\n   \n\t\n \t\n\t\n') #='2'



