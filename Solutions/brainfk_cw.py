#PASSED
# Inspired from real-world Brainf**k, we want to create an interpreter of that language which will support the following
#  instructions (the machine memory or 'data' should behave like a potentially infinite array of bytes, initialized to 0):
#
# > increment the data pointer (to point to the next cell to the right).
#
# < decrement the data pointer (to point to the next cell to the left).
#
# + increment (increase by one, truncate overflow: 255 + 1 = 0) the byte at the data pointer.
#
# - decrement (decrease by one, treat as unsigned byte: 0 - 1 = 255 ) the byte at the data pointer.
#
# . output the byte at the data pointer.
#
# , accept one byte of input, storing its value in the byte at the data pointer.
#
# [ if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command,
#       jump it forward to the command after the matching ] command.
#
# ] if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command,
#       jump it back to the command after the matching [ command.
#
# The function will take in input...
#     * the program code, a string with the sequence of machine instructions,
#     * the program input, a string, eventually empty, that will be interpreted as an array of bytes using each character's ASCII code and will be consumed by the , instruction
#
# ... and will return ...
#     * the output of the interpreted code (always as a string), produced by the . instruction.

def march_back(c, code):
    #Work back from the "]" char to the char after the corresponding "["
    n = 1 #Number of "]" minus number of "["
    while n>0:
        c -= 1
        if code[c] == "]":
            n += 1
        if code[c] == "[":
            n -= 1
    return c+1

def march_fwd(c,code):
    #Work forward from the "[" char to the char after the corresponding "]"
    n = -1#Number of "]" minus number of "["
    while n<0:
        c += 1
        if code[c] == "]":
            n += 1
        if code[c] == "[":
            n -= 1
    return c+1

def brain_luck(code, input):
    memory = [0]*1 #Start with one "byte", we'll add more later if needed
    output = ''
    c = 0 #code pointer
    m = 0 #memory pointer
    while c<len(code):
        ###Modify memory:
        if code[c] == ">":
            # increment the data pointer (to point to the next cell to the right).
            m += 1
            #If we dont have memory for this pointer address, download more RAM
            while m+1 > len(memory):
                memory += [0]
        elif code[c] == "<":
            # decrement the data pointer (to point to the next cell to the left).
            # #!!Might drive this pointer into negative values!!
            m -= 1
        elif code[c] == "+":
            #Increment our current memory byte
            memory[m] = (memory[m]+1) % 256
        elif code[c] == "-":
            #Decrement our current memory byte
            memory[m] = (memory[m]-1) % 256
        elif code[c] == ".":
            # output the byte at the data pointer.
            output += chr(memory[m])
        elif code[c] == ",":
            #Put next byte into memory:
            memory[m] = ord(input[0])
            #The input byte is consumed:
            input = input[1:]

        ###Determine next code pointer location:
        if code[c] == "[" and memory[m] == 0:
            # [ if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command,
            #       jump it forward to the command after the matching ] command.
            c = march_fwd(c, code)
        elif code[c] == "]" and memory[m] != 0:
            # ] if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command,
            #       jump it back to the command after the matching [ command.
            c = march_back(c, code)
        else:
            c += 1

    return output

###Examples:
# Echo until byte(255) encountered
print(brain_luck(',+[-.,+]', 'Codewars' + chr(255)) == 'Codewars')

# Echo until byte(0) encountered
print(brain_luck(',[.[-],]', 'Codewars' + chr(0)) == 'Codewars')

# Two numbers multiplier
print(brain_luck(',>,<[>[->+>+<<]>>[-<<+>>]<<<-]>>.', chr(8) + chr(9)) == chr(72))







