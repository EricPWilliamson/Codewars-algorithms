"""
https://www.codewars.com/kata/55d18ceefdc5aba4290000e5/train/python
"""

import itertools

def add_roll(outcomes,faces):
    new_outcomes = []
    for outcome in outcomes:
        for face in faces:
            new_outcomes += [outcome+face]
    return new_outcomes

def roll_dice_old(rolls, sides, threshold):
    faces = [i+1 for i in range(sides)]
    outcomes = [0]

    for _ in range(rolls):
        outcomes = add_roll(outcomes,faces)

    passing_outcomes = sum(1 for i in outcomes if i>=threshold)
    return passing_outcomes/len(outcomes)

def count_combos(rolls,faces,outcome):
    #Finds how many ways the specified outcome can be achieved.
    C = [i for i in itertools.combinations(faces,rolls)]

    for face in faces:
        if outcome-face >= rolls-1:
            if rolls==1 and outcome==face:

            count_combos(rolls-1,faces,outcome)

    return 1


def roll_dice(rolls, sides, threshold):
    faces = [i+1 for i in range(sides)]
    outcomes = [i for i in range(rolls,rolls*sides+1)]
    n_chances = 0
    for outcome in outcomes:
        if outcome >= threshold:
            n_chances += count_combos(rolls,faces,outcome)

    for _ in range(rolls):
        outcomes = add_roll(outcomes,faces)

    passing_outcomes = sum(1 for i in outcomes if i>=threshold)
    return passing_outcomes/len(outcomes)


from my_tester import MyTest
test = MyTest()

test.describe('Basic test cases')
test_data_set = [
  [ 3,  6,  4, 3.0/6 ],
  [ 1, 20, 20, 1.0/20 ],
  [ 2,  4,  2, 1.0 ],
  [ 2,  4,  9, 0.0 ],
  [ 2,  6,  3, 35.0/36 ]
]
for row in test_data_set:
    [rolls, sides, threshold, expected] = row
    test.it("P({}d{} >= {}) = {}".format(*row))
    actual = roll_dice(rolls, sides, threshold)
    test.expect(abs(actual - expected) < 1e-4, actual)
