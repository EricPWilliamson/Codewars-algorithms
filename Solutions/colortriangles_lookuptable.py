"""
Generates lookup table for use in colortriangles_hard_cw.py
"""
import itertools
from colortriangles_hard_cw import triangle

N = 3
A = ['RGB']*N
i = 0
for lst in itertools.product(*A):
    i += 1
    s = ''.join(lst)
    ans = triangle(s)
    print("'{}':'{}',".format(s,ans),end='')
    if i>50:
        print('')
        i = 0




