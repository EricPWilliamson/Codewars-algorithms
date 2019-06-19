#PASSED
#  RoboScript #1 - Implement Syntax Highlighting
# Disclaimer
# The story presented in this Kata Series is purely fictional; any resemblance to actual programming languages,
#  products, organisations or people should be treated as purely coincidental.
#
# About this Kata Series
# This Kata Series is based on a fictional story about a computer scientist and engineer who owns a firm that sells a
#  toy robot called MyRobot which can interpret its own (esoteric) programming language called RoboScript. Naturally,
#  this Kata Series deals with the software side of things (I'm afraid Codewars cannot test your ability to build a physical robot!).
#
# Story
# You are a computer scientist and engineer who has recently founded a firm which sells a toy product called MyRobot
#  which can move by receiving a set of instructions by reading a file containing a script. Initially you have planned
#  the robot to be able to interpret JavaScript files for its movement instructions but you later decided that it would
#  make MyRobot too hard to operate for most customers out there who aren't even computer programmers in the first
#  place. For this reason, you have decided to invent a new (esoteric) scripting language called RoboScript which has a
#  much simpler syntax so non-computer programmers can easily learn how to write scripts in this language which would
#  enable them to properly operate MyRobot. However, you are currently at the initial stage of inventing this new
#  Esolang. The first step to popularize this (esoteric) scripting language is naturally to invent a new editor for it
#  which provides syntax highlighting for this language so your customers feel like they are writing a proper program
#  when they are writing scripts for MyRobot.
#
# Task
# Your MyRobot-specific (esoteric) scripting language called RoboScript only ever contains the following characters:
#  F, L, R, the digits 0-9 and brackets (( and ))
# Your goal is to write a function highlight which accepts 1 required argument code which is the RoboScript program
#  passed in as a string and returns the script with syntax highlighting. The following commands/characters should
#  have the following colors:
#
# F - Wrap this command around <span style="color: pink"> and </span> tags so that it is highlighted pink in our editor
# L - Wrap this command around <span style="color: red"> and </span> tags so that it is highlighted red in our editor
# R - Wrap this command around <span style="color: green"> and </span> tags so that it is highlighted green in our editor
# Digits from 0 through 9 - Wrap these around <span style="color: orange"> and </span> tags so that they are highlighted orange in our editor
# Round Brackets - Do not apply any syntax highlighting to these characters

# For example:
# highlight("F3RF5LF7"); // => "<span style=\"color: pink\">F</span><span style=\"color: orange\">3</span><span style=\"color: green\">R</span><span style=\"color: pink\">F</span><span style=\"color: orange\">5</span><span style=\"color: red\">L</span><span style=\"color: pink\">F</span><span style=\"color: orange\">7</span>"

# And for multiple characters with the same color, simply wrap them with a single <span> tag of the correct color:
# highlight("FFFR345F2LL"); // => "<span style=\"color: pink\">FFF</span><span style=\"color: green\">R</span><span style=\"color: orange\">345</span><span style=\"color: pink\">F</span><span style=\"color: orange\">2</span><span style=\"color: red\">LL</span>"

# Note that the use of <span> tags must be exactly the same format as demonstrated above. Even if your solution produces
#  the same visual result as the expected answers, if you miss a space betwen "color:" and "green", for example, you
#  will fail the tests.

def get_color(cat):
    #Generates the span style command for the color corresponding to cat.
    if cat == "number":
        return "<span style=\"color: orange\">"
    elif cat == "F":
        return "<span style=\"color: pink\">"
    elif cat == "L":
        return "<span style=\"color: red\">"
    elif cat == "R":
        return "<span style=\"color: green\">"
    else:
        return '' #!!What do brackets do?


def highlight(code):
    # Implement your syntax highlighter here
    output = ''
    prev_cat = ''
    for c in code:
        ###Determine which category the character fits:
        if c.isdigit():
            cat = "number"
        else:
            cat = c
        ###Append the output string:
        if cat == prev_cat:
            #Just add this to the current command:
            output += c
        else:
            if prev_cat in ['F','L','R','number']:
                #Close off the previous command:
                output += "</span>"
            #Start next command:
            output += get_color(cat) + c
        prev_cat = str(cat)
    #Close off the last command:
    output += "</span>"
    return output

####F3RF5LF7 translation:
# F:
# <span style="color: pink">F</span>
# 3:
# <span style="color: orange">3</span>
# R:
# <span style="color: green">R</span>
# F:
# <span style="color: pink">F</span>
# 5:
# <span style="color: orange">5</span>
# L:
# <span style="color: red">L</span>
# F:
# <span style="color: pink">F</span>
# 7:
# <span style="color: orange">7</span>

####FFFR translation:
#FFF:
# <span style="color: pink">FFF</span>
# R:
# <span style="color: green">R</span>
# 345:
# <span style="color: orange">345</span>
# F:
# <span style="color: pink">F</span>





# Test.describe("Your Syntax Highlighter")
# Test.it("should work for the examples provided in the description")
print("Code without syntax highlighting: F3RF5LF7")
print("Your code with syntax highlighting: " + highlight("F3RF5LF7"))
print('Expected syntax highlighting:       <span style="color: pink">F</span><span style="color: orange">3</span><span style="color: green">R</span><span style="color: pink">F</span><span style="color: orange">5</span><span style="color: red">L</span><span style="color: pink">F</span><span style="color: orange">7</span>')
print(highlight("F3RF5LF7") == '<span style="color: pink">F</span><span style="color: orange">3</span><span style="color: green">R</span><span style="color: pink">F</span><span style="color: orange">5</span><span style="color: red">L</span><span style="color: pink">F</span><span style="color: orange">7</span>')

print("Code without syntax highlighting: FFFR345F2LL")
print("Your code with syntax highlighting: " + highlight("FFFR345F2LL"));
print('Expected syntax highlighting:       <span style="color: pink">FFF</span><span style="color: green">R</span><span style="color: orange">345</span><span style="color: pink">F</span><span style="color: orange">2</span><span style="color: red">LL</span>')
print(highlight("FFFR345F2LL") == '<span style="color: pink">FFF</span><span style="color: green">R</span><span style="color: orange">345</span><span style="color: pink">F</span><span style="color: orange">2</span><span style="color: red">LL</span>')

###From tests:
# RRRRR(F45L3)F2
#mine: '<span style="color: green">RRRRR</span>(</span><span style="color: pink">F</span><span style="color: orange">45</span><span style="color: red">L</span><span style="color: orange">3</span>)</span><span style="color: pink">F</span><span style="color: orange">2</span>'
#ans:  '<span style="color: green">RRRRR</span>(<span style="color: pink">F</span><span style="color: orange">45</span><span style="color: red">L</span><span style="color: orange">3</span>)<span style="color: pink">F</span><span style="color: orange">2</span>'
print(highlight('RRRRR(F45L3)F2') == '<span style="color: green">RRRRR</span>(<span style="color: pink">F</span><span style="color: orange">45</span><span style="color: red">L</span><span style="color: orange">3</span>)<span style="color: pink">F</span><span style="color: orange">2</span>')

#####Smarter solution:
# import re
# def highlight(code):
#     code = re.sub(r"(F+)", '<span style="color: pink">\g<1></span>', code)
#     code = re.sub(r"(L+)", '<span style="color: red">\g<1></span>', code)
#     code = re.sub(r"(R+)", '<span style="color: green">\g<1></span>', code)
#     code = re.sub(r"(\d+)", '<span style="color: orange">\g<1></span>', code)
#     return code

