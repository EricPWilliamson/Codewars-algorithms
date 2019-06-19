"""
A. Fingerprints
time limit per test:1 second
memory limit per test:256 megabytes
input:standard input
output:standard output

You are locked in a room with a door that has a keypad with 10 keys corresponding to digits from 0 to 9. To escape from
 the room, you need to enter a correct code. You also have a sequence of digits.

Some keys on the keypad have fingerprints. You believe the correct code is the longest not necessarily contiguous
 subsequence of the sequence you have that only contains digits with fingerprints on the corresponding keys. Find such code.

Input
The first line contains two integers n and m(1≤n,m≤10) representing the number of digits in the sequence you have and
 the number of keys on the keypad that have fingerprints.

The next line contains n distinct space-separated integers representing the sequence

The next line contains m distinct space-separated integers representing the fingerprints

Output
In a single line print a space-separated sequence of integers representing the code. If the resulting sequence is empty,
 both printing nothing and printing a single line break is acceptable.

My Summary: The meaning of the above is as follows. Take integers from the sequence array that match integers found within
  the fingerprints array. Output those matches in the same order as they occurred within the sequence array.
"""

def fingerprint_code(len_list, sequence, fingerprints):
    print(len_list)
    print(type(len_list))
    print(sequence)
    print(type(sequence))
    print(fingerprints)
    print(type(fingerprints))


    return None

fingerprint_code([1,2], '123', '12')

