"""
https://www.codewars.com/kata/mine-sweeper/train/python
"""

import numpy as np

# np.set_printoptions(linewidth=1000)

def list_neighbors(r0, c0, mat):
    neighbors = []
    rows = []
    cols = []
    for r in range(r0-1,r0+2):
        for c in range(c0-1,c0+2):
            if 0<=r<mat.shape[0] and 0<=c<mat.shape[1] and not (r==r0 and c==c0):
                neighbors += [mat[r,c]]
                rows += [r]
                cols += [c]
    return neighbors, rows, cols

def simple_solver(matmap,n,safemode):
    #Make deductions without guess and check until we get stuck.
    h = matmap.shape[0]
    w = matmap.shape[1]
    made_progress = True
    count = 0
    while made_progress:
        made_progress = False
        for r0 in range(h):
            for c0 in range(w):
                #only proceed to check clues:
                if matmap[r0,c0].isdigit():
                    clue = int(matmap[r0,c0])
                    neighbors,rows,cols = list_neighbors(r0,c0,matmap)
                    q_cells = sum(1 for cell in neighbors if cell=='?')
                    x_cells = sum(1 for cell in neighbors if cell=='x')
                    #Make sure we still need to solve cells here:
                    if q_cells>0:
                        #Check to see if we have only just enough '?' cells:
                        if clue-x_cells==q_cells:
                            #Replace the '?'s with 'x's
                            for i,cell in enumerate(neighbors):
                                if cell=='?':
                                    matmap[rows[i],cols[i]] = 'x'
                                    #Check that we didnt just exceed n:
                                    if (matmap == 'x').sum() > n:
                                        # print('Exceeded n limit')
                                        return matmap,count,False
                                    made_progress = True
                                    count += 1
                        #Check to see if we already have enough 'x' cells:
                        elif clue==x_cells:
                            #Open the '?'s:
                            for i,cell in enumerate(neighbors):
                                if cell=='?':
                                    if safemode:
                                        matmap[rows[i],cols[i]] = 'o'
                                    else:
                                        matmap[rows[i],cols[i]] = open(rows[i],cols[i])
                                    made_progress = True
                                    count += 1
                    #Check to make sure we havent created an invalid situation:
                    if clue-x_cells > q_cells:
                        #We cant produce enough 'x's for this clue anymore...
                        return matmap, count, False
                    if clue < x_cells:
                        #We have too many 'x's for this clue
                        return matmap, count, False

    ###Finally, check on the mine count:
    mine_count = (matmap == 'x').sum()
    q_count = (matmap == '?').sum()
    if mine_count + q_count < n:
        # print('Too few mines for n.')
        return matmap,count,False
    elif mine_count + q_count == n:
        #All the '?'s must be mines:
        matmap[matmap=='?'] = 'x'
    elif mine_count == n:
        #All the '?'s must be clear:
        if safemode:
            matmap[matmap=='?'] = 'o'
        else:
            for r0 in range(h):
                for c0 in range(w):
                    if matmap[r0,c0]=='?':
                        matmap[r0,c0] = open(r0,c0)

    ###Make sure all clues can still be met:
    for r0 in range(h):
        for c0 in range(w):
            #only proceed to check clues:
            if matmap[r0,c0].isdigit():
                clue = int(matmap[r0,c0])
                neighbors,rows,cols = list_neighbors(r0,c0,matmap)
                q_cells = sum(1 for cell in neighbors if cell=='?')
                x_cells = sum(1 for cell in neighbors if cell=='x')
                #Check to make sure we havent created an invalid situation:
                if clue-x_cells>q_cells:
                    #We cant produce enough 'x's for this clue anymore...
                    return matmap,count,False
                if clue<x_cells:
                    #We have too many 'x's for this clue
                    return matmap,count,False

    return matmap, count, True

def try_bifurcations(matmap,n):
    ###Create a bifurcation by guessing, and check for its validity:
    print('Bifurcating...')
    print('{} mines remaining.'.format(n - (matmap=='x').sum()))
    h = matmap.shape[0]
    w = matmap.shape[1]
    #Find '?'s with at least one clue adjacent:
    q_choices = []
    for r0 in range(h):
        for c0 in range(w):
            #is it a '?' cell:
            if matmap[r0,c0]=='?':
                #Count how many clues are affected by it:
                neighbors,rows,cols = list_neighbors(r0,c0,matmap)
                c_cells = sum(1 for cell in neighbors if cell.isdigit())
                if c_cells>0:
                    q_choices += [[c_cells,r0,c0]]

    #Sort choices by the number of adjacent clues (more clues should be more likely to reach an invalid solution)
    if len(q_choices)<1:
        print('No viable bifurcation points.')
        return None
    else:
        q_choices = np.array(q_choices)
        q_choices = q_choices[q_choices[:,0].argsort()[::-1]]

    #Try each choice until we gain a cell:
    for best_cell in q_choices:
        #Try setting the chosen cell to 'x' and see what happens:
        hyp_map = np.copy(matmap)
        hyp_map[best_cell[1],best_cell[2]] = 'x'
        hyp_map,count,is_valid = simple_solver(hyp_map,n,True)
        if not is_valid:
            #Since we created in invalid solution, we have proven that this cell can't be an 'x'
            matmap[best_cell[1],best_cell[2]] = open(best_cell[1],best_cell[2])
            print(best_cell,'o')
            return matmap
        else:
            #We didnt learn anything, so instead try setting the cell to 'o' (representing non-mine):
            hyp_map = np.copy(matmap)
            hyp_map[best_cell[1],best_cell[2]] = 'o'
            hyp_map,count,is_valid = simple_solver(hyp_map,n,True)
            if not is_valid:
                #Since the 'o' created in invalid solution, we know 'x' is the correct assignment:
                matmap[best_cell[1],best_cell[2]] = 'x'
                print(best_cell,'x')
                return matmap
            else:
                print(best_cell,'?')

    #That didnt tell us anything, so now try 2 layer bifurcation:
    print('Two layer bifurcations')
    sol_list = []
    for best_cell in q_choices:
        #Try setting the chosen cell to 'x' and solve until we get stuck:
        hyp_map = np.copy(matmap)
        hyp_map[best_cell[1],best_cell[2]] = 'x'
        hyp_map,count,_ = simple_solver(hyp_map,n,True)
        #Now make a secondary bifurcation: (all possible solutions must be invalid for us to draw a conclusion)
        if '?' in hyp_map:
            valid_sol,new_sol_list = secondary_bifurcation(hyp_map,n)
            if not valid_sol:
                #All possible follow up bifurcations are invalid, so this choice must be invalid
                matmap[best_cell[1],best_cell[2]] = open(best_cell[1],best_cell[2])
                print(best_cell,'o')
                return matmap
            else:
                #We can still check to see if our valid solutions agree on certain cells:
                # print('xxx')
                # print(hyp_map)
                sol_list += new_sol_list
        else:
            #This is a complete solution, so add it to sol_list:
            sol_list += [hyp_map]

        #Try that again with a guess of 'o':
        hyp_map = np.copy(matmap)
        hyp_map[best_cell[1],best_cell[2]] = 'o'
        hyp_map,count,_ = simple_solver(hyp_map,n,True)
        #Now make a secondary bifurcation: (all possible solutions must be invalid for us to draw a conclusion)
        if '?' in hyp_map:
            valid_sol,new_sol_list = secondary_bifurcation(hyp_map,n)
            if not valid_sol:
                #All possible follow up bifurcations are invalid, so this choice must be invalid
                matmap[best_cell[1],best_cell[2]] = 'x'
                print(best_cell,'x')
                return matmap
            else:
                # print('ooo')
                # print(hyp_map)
                sol_list += new_sol_list
        else:
            #This is a complete solution, so add it to sol_list:
            sol_list += [hyp_map]

    ###Last ditch effort--Compare the solutions in sol_list to see if they converge anywhere:
    matmap = check_consensus(matmap,sol_list)
    return matmap

def secondary_bifurcation(matmap,n):
    ###Create a bifurcation by guessing, and check for its validity:
    # print('secondary bifurcation...')
    # print('{} mines remaining.'.format(n - (matmap=='x').sum()))
    # print(matmap)
    # print('')


    h = matmap.shape[0]
    w = matmap.shape[1]
    #Find '?'s with at least one clue adjacent:
    q_choices = []
    for r0 in range(h):
        for c0 in range(w):
            #is it a '?' cell:
            if matmap[r0,c0]=='?':
                #Count how many clues are affected by it:
                neighbors,rows,cols = list_neighbors(r0,c0,matmap)
                c_cells = sum(1 for cell in neighbors if cell.isdigit())
                if c_cells>0:
                    q_choices += [[c_cells,r0,c0]]

    #Sort choices by the number of adjacent clues (more clues should be more likely to reach an invalid solution)
    if len(q_choices)<1:
        print('No viable bifurcation points.')
        # print("Mines placed: {}".format((matmap == 'x').sum()))
        # print(matmap)
        return True, [matmap]
    else:
        q_choices = np.array(q_choices)
        q_choices = q_choices[q_choices[:,0].argsort()[::-1]]

    ###Try each choice until we are out of options:
    #Check if we can still add mines:
    if (matmap == 'x').sum()==n:
        guesses = ['o']
    else:
        guesses = ['x','o']
    #Try each possible guess in every possible cell:
    sol_list = []
    are_any_valid = False
    for best_cell in q_choices:
        for guess in guesses:
            #Try setting the chosen cell to 'x' or 'o' and see what happens:
            hyp_map = np.copy(matmap)
            hyp_map[best_cell[1],best_cell[2]] = guess
            hyp_map,count,is_valid = simple_solver(hyp_map,n,True)

            if not is_valid:
                #This choice can be eliminated:
                # print('check other choices--pass')
                pass
            elif '?' not in hyp_map:
                #The puzzle has reached a complete solution:
                # print('Cant eliminate this--quit')
                # print(hyp_map)
                sol_list += [hyp_map]
                are_any_valid = True
                # return True, hyp_map
            else:
                #The option looks passible, but we need to dig further...
                print('dig deeper on this option--recurse')
                valid_sol, new_sol_list = secondary_bifurcation(hyp_map,n)
                if valid_sol:
                    sol_list += new_sol_list
                    are_any_valid = True
                    # return True, hyp_map
                else:
                    pass
    return are_any_valid, sol_list

def check_consensus(matmap,sol_list):
    ###Compare the solutions in sol_list to see if they converge anywhere:
    h = matmap.shape[0]
    w = matmap.shape[1]
    sol_list = np.stack(sol_list)
    #Check each '?' cell for concensus in valid solutions:
    success = False
    for r in range(h):
        for c in range(w):
            #is it a '?' cell:
            if matmap[r,c]=='?':
                #List out the possible solutions from our sol_list:
                possibilities = np.unique(sol_list[:,r,c])
                if len(possibilities)==1:
                    #There is only one possibility so it must be right:
                    if possibilities[0]=='x':
                        matmap[r,c] = 'x'
                        print("Concensus at {},{}: 'x'".format(r,c))
                        success = True
                    elif possibilities[0]=='o':
                        matmap[r,c] = open(r,c)
                        print("Concensus at {},{}: 'o'".format(r,c))
                        success = True
                    elif possibilities[0]=='?':
                        pass
                    else:
                        raise Exception('Weird possibility occurred!')
    if success:
        return matmap
    else:
        return None

def solve_mine(map, n):
    # print([map])
    # print([n])

    ###Convert map string to 2d matrix:
    matmap = np.array([s.split(' ') for s in map.split('\n')])
    h = matmap.shape[0]
    w = matmap.shape[1]

    ###Handle special cases:
    if n==0:
        matmap[:] = '0'
    elif n==matmap.size:
        matmap[:] = 'x'
    if '0' not in matmap and '?' in matmap:
        return '?'

    ###Begin solving:
    if '?' in matmap:
        ###Check for clues that have only one possible solution on the board until we get stuck:
        matmap,count,_ = simple_solver(matmap,n,False)
        print("Cells solved: ", count)

    ###Create a bifurcation by guessing, and check for its validity:
    while '?' in matmap:
        matmap = try_bifurcations(matmap,n)
        if matmap is None:
            print('Bifurcation method failed')
            return '?'
        #Now that we have a new cell completed, continue solving:
        matmap,count,_ = simple_solver(matmap,n,False)
        print("Cells solved: ",count)


    ###Finish up:
    if '?' not in matmap:
        print('solved')
    else:
        print('WAIT! Not done yet!')

    #Make sure the n clue given works with our solution: (!!Can also identify invalid bifurcations)
    x_count = (matmap == 'x').sum()
    if x_count != n:
        print('Solution doesnt match n.')
        return '?'

    #Convert the matrix back into string format:
    ans = ''
    for r in range(h):
        for c in range(w):
            ans += matmap[r,c]
            ans += ' '
        ans = ans[:-1] + '\n'
    ans = ans[:-1] #cut last '\n' char
    return ans


# # Test.describe("Basic Tests")
# # Test.it("It should works for basic tests")
# gamemap = """
# ? ? ? ? ? ?
# ? ? ? ? ? ?
# ? ? ? 0 ? ?
# ? ? ? ? ? ?
# ? ? ? ? ? ?
# 0 0 0 ? ? ?
# """.strip()
# result = """
# 1 x 1 1 x 1
# 2 2 2 1 2 2
# 2 x 2 0 1 x
# 2 x 2 1 2 2
# 1 1 1 1 x 1
# 0 0 0 1 1 1
# """.strip()
# # game.read(gamemap, result)
# # makeAssertion(solve_mine(gamemap, game.count), result)

# gamemap = """
# 0 ? ?
# 0 ? ?
# """.strip()
# result = """
# 0 1 x
# 0 1 1
# """.strip()
# # game.read(gamemap, result)
# # makeAssertion(solve_mine(gamemap, game.count), "?")


# gamemap = """
# ? ? ? ? 0 0 0
# ? ? ? ? 0 ? ?
# ? ? ? 0 0 ? ?
# ? ? ? 0 0 ? ?
# 0 ? ? ? 0 0 0
# 0 ? ? ? 0 0 0
# 0 ? ? ? 0 ? ?
# 0 0 0 0 0 ? ?
# 0 0 0 0 0 ? ?
# """.strip()
# result = """
# 1 x x 1 0 0 0
# 2 3 3 1 0 1 1
# 1 x 1 0 0 1 x
# 1 1 1 0 0 1 1
# 0 1 1 1 0 0 0
# 0 1 x 1 0 0 0
# 0 1 1 1 0 1 1
# 0 0 0 0 0 1 x
# 0 0 0 0 0 1 1
# """.strip()
# game.read(gamemap, result)
# makeAssertion(solve_mine(gamemap, game.count), result)

# gamemap = """
# ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
# ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
# ? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
# 0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
# 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
# 0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
# 0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
# 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
# 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
# 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
# 0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
# 0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
# 0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
# 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
# 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# """.strip()
# result = """
# 1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
# x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
# 1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
# 0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
# 0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
# 0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
# 0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
# 0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
# 0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
# 0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
# 0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
# 0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
# 0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
# 0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
# 0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
# 0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
# 0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
# 0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
# 0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
# 0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
# 0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
# """.strip()
# # game.read(gamemap, result)
# # makeAssertion(solve_mine(gamemap, game.count), "?")

# gamemap = """
# 0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
# 0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
# 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
# 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
# ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
# ? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
# ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
# ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
# ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
# """.strip()
# result = """
# 0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
# 0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
# 0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
# 0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
# 1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
# x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
# 2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
# 1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
# 1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
# """.strip()
# game.read(gamemap, result)
# makeAssertion(solve_mine(gamemap, game.count), "?")

######## Tricky Tests ############
gamemap = """
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 ? ? ? ? ? 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 x 2 1 1 0 0 1 1 1
0 0 1 2 2 1 1 1 1 0 0 0 1 x 1 0 1 2 3 x 1 0 0 1 x 1
0 0 1 x x 1 1 x 1 0 0 0 1 2 2 1 0 1 x 3 2 1 0 1 1 1
0 0 1 2 2 1 1 1 1 0 0 0 0 1 x 1 0 1 1 2 x 1 0 0 0 0
""".strip()



########### Unalterable: ###################################
def open(r,c):
    s = result.split('\n')
    w = (len(s[0])+1)//2
    cell = result[2*c+(w*2)*r]
    if cell == 'x':
        raise Exception('STEPPED ON A MINE')
    else:
        return int(cell)
################################################################

n_mines = sum(1 for char in result if char=='x')
solution = solve_mine(gamemap,n_mines)
print(solution)
print(solution==result)

