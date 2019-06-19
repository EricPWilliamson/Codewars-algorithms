# Problem Statement
#     
# An electronic billboard is supposed to display large letters by using several lightbulbs per letter. Given a message,
#  and how each enlarged letter looks as a 5x5 arrangement of lightbulbs, return the enlarged message.
# The enlarged representation of the letters will be in a tuple (string) with each element formatted as follows
#  (quotes added for clarity):
# "<letter>:*****-*****-*****-*****-*****"
# Where <letter> is a single uppercase letter [A-Z], and each * is either the character '#' (representing a lit
#  lightbulb) or a period ('.') (representing an unlit lightbulb). Each group of 5 (delimited by a dash, '-')
#  represents a row in the 5x5 representation of the letter. So, "T:#####-..#..-..#..-..#..-..#.." means that the
#  5x5 representation of 'T' is:
# "#####"
# "..#.."
# "..#.."
# "..#.."
# "..#.."
# Return the enlarged message as a 5-element tuple (string), with each element representing one row of lightbulbs
#  (where element 0 is the top row). Leave 1 (one) column of periods ('.') between each adjacent pair of letters in the
#  enlarged message.
#     
# Class: Billboard
# Method: enlarge
# Parameters: string, tuple (string)
# Returns: tuple (string)
# Method signature: def enlarge(self, message, letters):
#
# Limits     
# Time limit (s):
# 2.000
# Memory limit (MB):
# 64
# Constraints
# -message will contain between 1 and 10 characters, inclusive.
# -each character of message will be an uppercase letter [A-Z].
# -letters will contain between 1 and 10 elements, inclusive.
# -each element of letters will be exactly 31 characters in length.
# -each element of letters will be formatted as (quotes added for clarity): "<letter>:*****-*****-*****-*****-*****", where <letter> is a single uppercase letter [A-Z] (inclusive) representing the letter being enlarged, and each * is either the character '#' or a period.
# -every letter appearing in message will have an enlarged representation in letters.
# - each letter represented in letters will be unique.

class Billboard(object):
    def enlarge(self, message, letters):
        ###Go through the message one char at at time:
        ordered_letters = []
        for c in message:
            #Find the element of letters that matches our char:
            matching_line = [s for s in letters if c in s][0]
            #Put just the pixel chars into this:
            ordered_letters += [matching_line[2:]]

        ###Go through our ordered pixel strings and reshape into the billboard image:
        image = ['', '', '', '', ''] #Image always has 5 rows
        for s in ordered_letters:
            pxls = s.split('-')
            for row in range(5):
                #Add the 5 pixels for our letter plus one '.' for spacing
                image[row] += pxls[row] + '.'

        ###Cut the extra '.' off of each row:
        for row in range(5):
            image[row] = image[row][:-1]

        return tuple(image)















foo = Billboard()

# Examples
# 0)
#
#     
message = "TOPCODER"
letters = ("T:#####-..#..-..#..-..#..-..#.."
            ,"O:#####-#...#-#...#-#...#-#####"
            ,"P:####.-#...#-####.-#....-#...."
            ,"C:.####-#....-#....-#....-.####"
            ,"D:####.-#...#-#...#-#...#-####."
            ,"E:#####-#....-####.-#....-#####"
            ,"R:####.-#...#-####.-#.#..-#..##")
# Returns:
# { "#####.#####.####...####.#####.####..#####.####.",
#   "..#...#...#.#...#.#.....#...#.#...#.#.....#...#",
#   "..#...#...#.####..#.....#...#.#...#.####..####.",
#   "..#...#...#.#.....#.....#...#.#...#.#.....#.#..",
#   "..#...#####.#......####.#####.####..#####.#..##" }
#
# 1)
#
#     
# "DOK"
# {"D:####.-#...#-#...#-#...#-####."
# ,"O:#####-#...#-#...#-#...#-#####"
# ,"K:#...#-#..#.-###..-#..#.-#...#"}
# Returns:
# { "####..#####.#...#",
#   "#...#.#...#.#..#.",
#   "#...#.#...#.###..",
#   "#...#.#...#.#..#.",
#   "####..#####.#...#" }
#
# 2)
#
#     
# "RANDOMNESS"
# {"S:##.##-#####-#.#.#-#.#.#-####."
# ,"N:#####-#####-#####-#####-#####"
# ,"R:#####-#####-##.##-#####-#####"
# ,"A:.....-.....-.....-.....-....."
# ,"D:#.#.#-.#.#.-#.#.#-.#.#.-#.#.#"
# ,"O:#####-#...#-#.#.#-#...#-#####"
# ,"E:#....-.#...-..#..-...#.-....#"
# ,"M:#....-.....-.....-.....-....."
# ,"X:#...#-.#.#.-..#..-.#.#.-#...#"}
# Returns:
# { "#####.......#####.#.#.#.#####.#.....#####.#.....##.##.##.##",
#   "#####.......#####..#.#..#...#.......#####..#....#####.#####",
#   "##.##.......#####.#.#.#.#.#.#.......#####...#...#.#.#.#.#.#",
#   "#####.......#####..#.#..#...#.......#####....#..#.#.#.#.#.#",
#   "#####.......#####.#.#.#.#####.......#####.....#.####..####." }
# Note that the letter X is defined but never used.

ans = foo.enlarge(message, letters)

print(ans)
