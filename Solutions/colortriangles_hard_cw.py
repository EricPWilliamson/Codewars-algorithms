"""
https://www.codewars.com/kata/insane-coloured-triangles/train/python
"""

lookup_dict = {'RRR':'R','RRG':'G','RRB':'B','RGR':'B','RGG':'R','RGB':'G','RBR':'G','RBG':'B',
               'RBB':'R','GRR':'G','GRG':'B','GRB':'R','GGR':'R','GGG':'G','GGB':'B','GBR':'B',
               'GBG':'R','GBB':'G','BRR':'B','BRG':'R','BRB':'G','BGR':'G','BGG':'B','BGB':'R',
               'BBR':'R','BBG':'G','BBB':'B'}

def triangle(row):
    #First use lookup table for faster processing:
    lookN = len(next(iter(lookup_dict)))
    while len(row)>=lookN:
        row = ''.join([lookup_dict[row[i:i+lookN]] for i in range(len(row)-lookN+1)])

    #Finish up the last few lines linearly:
    C = set('RGB')
    while len(row)>1:
        row = ''.join([c1 if c1==c2 else (C-{c1,c2}).pop() for c1,c2 in zip(row,row[1:])])
    return row

#########################################################
from my_tester import MyTest
test = MyTest()

def _test(cases):
    for _in, _out in cases:
        test.assert_equals(triangle(_in), _out)

test.describe('Insane Coloured Triangles')
basic_cases = [
    ['B', 'B'],
    ['GB', 'R'],
    ['RRR', 'R'],
    ['RGBG', 'B'],
    ['RBRGBRB', 'G'],
    ['RBRGBRBGGRRRBGBBBGG', 'G']
]
# test.it('Basic Tests')
_test(basic_cases)

my_cases = [
    'RGBRGGG',
    'RBGRRBG',
    'RRGGRGG'
]
for case in my_cases:
    print(case,': ', triangle(case))

"""
Efficiency testing:
Without any lookup table, 2000 takes 0.68s
With lenth 3 lookup table, 2000 takes 0.30s
With length 4... 0.20s
With length 7... 0.11s
With length 10... 0.14s
"""
###Efficiency testing:
from timeit import default_timer as timer
import random

for z in range(4):
    N = 2000
    case = ''.join(random.choice(['R','G','B']) for _ in range(N))

    t1 = timer()
    x = triangle(case)
    t2 = timer()
    print("Run time: {:.2f}s".format(t2-t1))

