"""
https://www.codewars.com/kata/coloured-triangles/train/python
"""

def change(s):
    if s[0]==s[1]:
        return s[0]
    else:
        return ({'R','G','B'}-{s[0],s[1]}).pop()

def triangle(row):
    """Main fcn"""
    while len(row)>1:
        newrow = ''.join([change(row[i:i+2]) for i in range(len(row)-1)])
        row = newrow
    return row

from my_tester import MyTest
test = MyTest()
test.assert_equals(triangle('GB'), 'R')
test.assert_equals(triangle('RRR'), 'R')
test.assert_equals(triangle('RGBG'), 'B')
test.assert_equals(triangle('RBRGBRB'), 'G')
test.assert_equals(triangle('RBRGBRBGGRRRBGBBBGG'), 'G')
test.assert_equals(triangle('B'), 'B')
