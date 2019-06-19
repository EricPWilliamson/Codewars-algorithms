"""
https://www.codewars.com/kata/find-the-cheapest-path
"""
from timeit import default_timer as timer

def plot_paths(possibilities, height, width):
    import matplotlib.pyplot as plt
    from math import floor

    fig,ax = plt.subplots(1,len(possibilities), subplot_kw=dict(aspect='equal'))
    for i in range(len(possibilities)):
        ax[i].scatter([floor(j/width) for j in range(height*width)], [j for j in range(width)]*height)
        ax[i].plot(*zip(*possibilities[i]))

def get_adjacents(cell):
    x = cell[0]
    y = cell[1]
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

def direct_path(start, finish):
    #Make a simple direct path from start to finish, just to get a base cost set down
    dx = finish[0]-start[0]
    dy = finish[1]-start[1]
    path = [start]
    if dx<0:
        for x in range(-1,dx-1,-1):
            path += [(start[0]+x,start[1])]
    else:
        for x in range(1,dx+1):
            path += [(start[0]+x, start[1])]
    if dy<0:
        for y in range(-1,dy-1,-1):
            path += [(finish[0],start[1]+y)]
    else:
        for y in range(1,dy+1):
            path += [(finish[0], start[1]+y)]
    return path

def next_possibilities_simple(path, height, width, finish, costs, t):
    #Create all possible paths by only moving towards the finish point
    x = path[-1][0]
    y = path[-1][1]
    adjacencies = []
    if finish[0] > x:
        adjacencies += [(x+1,y)]
    elif finish[0] < x:
        adjacencies += [(x-1,y)]
    if finish[1] > y:
        adjacencies += [(x,y+1)]
    elif finish[1] < y:
        adjacencies += [(x,y-1)]

    if finish in adjacencies:
        possibilities = [path + [finish]]
    else:
        possibilities = []
        for next in adjacencies:
            #Only use this cell if it leads towards the finsih:
            if 0<=next[0]<height and 0<=next[1]<width:
                #Also make sure we havent already used that cell:
                if next not in path:
                    #Also, check that we arent doubling back to a cell we could have reached earlier:
                    if not any(cell in get_adjacents(next) for cell in path[0:-1]):
                        #Finally, check that the cost hasnt already exceeded the cheapest known path:
                        if costs==[] or calc_cost(t, path+[next]) < min(costs):
                            possibilities += [path + [next]]
    return possibilities

def next_possibilities(path, height, width, finish, costs, t):
    #Create all possibilites, including those with circuitous routes.
    adjacencies = get_adjacents(path[-1])
    if finish in adjacencies:
        possibilities = [path + [finish]]
    else:
        possibilities = []
        for next in adjacencies:
            #Make sure we only use a step if its still on the map
            if 0<=next[0]<height and 0<=next[1]<width:
                #Also make sure we havent already used that cell:
                if next not in path:
                    #Also, check that we arent doubling back to a cell we could have reached earlier:
                    if not any(cell in get_adjacents(next) for cell in path[0:-1]):
                        #Finally, check that the cost hasnt already exceeded the cheapest known path:
                        if costs==[] or calc_cost(t, path+[next]) < min(costs):
                            possibilities += [path + [next]]
    return possibilities

def calc_cost(t, path):
    #Calcuates the total cost of a path:
    cost = 0
    for point in path:
        cost += t[point[0]][point[1]]
    return cost

def get_directions(path):
    #Converts a path (sequence of coords) into up/down/right/left directions
    directions = []
    for i in range(len(path)-1):
        if path[i][0] == path[i+1][0] - 1:
            directions += ['down']
        elif path[i][0] == path[i+1][0] + 1:
            directions += ['up']
        elif path[i][1]==path[i+1][1]-1:
            directions += ['right']
        elif path[i][1]==path[i+1][1]+1:
            directions += ['left']
    return directions

def cheapest_path(t, start, finish):
    #Special case for no path:
    if start==finish:
        return []

    #Find the best path using a simple, direct approach:
    costs = []
    height = len(t)
    width = len(t[0])
    path = [start]
    possibilities = [direct_path(start,finish)]
    possibilities += next_possibilities_simple(path, height, width, finish,costs, t)
    while not all(path[-1]==finish for path in possibilities):
        print(len(possibilities))
        new_possibilities = []
        for path in possibilities:
            if path[-1] == finish:
                #If the path is complete just keep it in circulation
                new_possibilities += [path]
                costs += [calc_cost(t,path)]
            else:
                #If its not complete, add another step to it
                new_possibilities += next_possibilities_simple(path,height,width,finish,costs, t)
        possibilities = new_possibilities
    costs = []
    for path in possibilities:
        costs += [calc_cost(t,path)]
    mincost,idx = min((cost,idx) for (idx,cost) in enumerate(costs))

    #Find every path from start to finish that doesnt double back on itself:
    costs = [mincost]
    height = len(t)
    width = len(t[0])
    path = [start]
    possibilities = next_possibilities(path, height, width, finish,costs, t)
    while not all(path[-1]==finish for path in possibilities):
        print(len(possibilities))
        new_possibilities = []
        for path in possibilities:
            if path[-1] == finish:
                #If the path is complete just keep it in circulation
                new_possibilities += [path]
                costs += [calc_cost(t,path)]
            else:
                #If its not complete, add another step to it
                new_possibilities += next_possibilities(path,height,width,finish,costs, t)
        possibilities = new_possibilities

    # plot_paths(possibilities,height,width)

    #ReCalculate the cost of each possible path:
    costs = []
    for path in possibilities:
        costs += [calc_cost(t, path)]

    #Find the cheapest path, and convert it into directions:
    mincost,idx = min((cost,idx) for (idx,cost) in enumerate(costs))
    directions = get_directions(possibilities[idx])
    return directions


#########################################################
from my_tester import MyTest
Test = MyTest()

Test.it("Hopefuly, you're already where you need to be")
Test.assert_equals(cheapest_path([[1]], (0,0), (0,0)), [])

Test.it("But what if you actually needed to move?")
Test.assert_equals(cheapest_path([[1,9,1],[2,9,1],[2,1,1]], (0,0), (0,2)), ["down", "down", "right", "right", "up", "up"])

Test.it("And is your solution doing it right at all?")
Test.assert_equals(cheapest_path([[1,4,1],[1,9,1],[1,1,1]], (0,0), (0,2)), ["right", "right"])

cheapest_path([[55, 28, 44, 90, 31, 29, 18, 16, 11, 26, 17, 59, 17, 62, 21, 44, 19, 53, 39, 16, 85, 40, 4, 78, 62, 92, 55, 40, 2, 15, 42], [48, 14, 78, 27, 17, 52, 59, 9, 75, 79, 50, 94, 33, 92, 14, 45, 14, 56, 65, 86, 56, 7, 95, 79, 18, 35, 11, 10, 52, 48, 37], [50, 31, 47, 41, 88, 7, 15, 76, 92, 88, 75, 50, 48, 99, 85, 61, 49, 49, 80, 54, 51, 41, 40, 100, 66, 81, 89, 44, 83, 83, 14], [35, 64, 68, 71, 30, 59, 20, 46, 100, 65, 60, 47, 30, 84, 13, 7, 14, 75, 11, 73, 81, 17, 28, 50, 56, 63, 37, 28, 39, 23, 35], [11, 40, 94, 36, 96, 37, 54, 61, 54, 16, 100, 67, 33, 40, 65, 33, 1, 10, 55, 79, 94, 95, 50, 1, 65, 86, 12, 64, 11, 29, 95], [6, 79, 49, 37, 68, 39, 77, 14, 40, 43, 10, 39, 6, 98, 16, 31, 31, 74, 28, 14, 93, 89, 20, 49, 60, 23, 75, 1, 34, 41, 90], [60, 89, 94, 97, 87, 38, 19, 86, 75, 30, 85, 73, 65, 54, 84, 98, 12, 23, 24, 49, 8, 7, 93, 57, 75, 24, 7, 88, 75, 2, 22], [83, 8, 23, 83, 25, 88, 2, 58, 40, 29, 60, 77, 98, 28, 30, 57, 57, 13, 80, 74, 52, 36, 7, 5, 95, 26, 50, 96, 6, 40, 31], [74, 15, 87, 32, 1, 79, 78, 77, 33, 34, 61, 86, 95, 22, 10, 7, 86, 15, 34, 47, 10, 43, 35, 46, 44, 55, 51, 47, 67, 20, 72], [34, 94, 17, 44, 34, 76, 54, 71, 23, 86, 11, 22, 53, 92, 53, 23, 75, 20, 32, 11, 79, 42, 1, 31, 59, 78, 25, 13, 27, 2, 64], [27, 54, 43, 32, 84, 28, 7, 17, 38, 60, 79, 80, 68, 86, 47, 26, 34, 4, 45, 24, 71, 8, 82, 26, 44, 23, 17, 61, 95, 34, 6], [28, 61, 95, 27, 93, 69, 6, 33, 19, 51, 96, 55, 40, 65, 25, 79, 20, 12, 48, 31, 91, 100, 56, 56, 81, 52, 100, 95, 79, 19, 21], [39, 72, 90, 80, 44, 20, 28, 100, 61, 22, 86, 99, 90, 42, 61, 63, 47, 77, 78, 18, 95, 13, 64, 66, 71, 99, 76, 72, 95, 33, 95], [8, 27, 7, 69, 80, 46, 47, 99, 80, 75, 71, 7, 11, 32, 5, 66, 86, 44, 42, 28, 21, 23, 73, 74, 99, 74, 41, 70, 46, 57, 8], [17, 28, 96, 51, 100, 14, 45, 3, 74, 7, 34, 50, 75, 40, 48, 42, 72, 72, 50, 81, 42, 30, 53, 94, 49, 27, 8, 85, 38, 9, 84], [9, 46, 77, 70, 19, 55, 7, 3, 44, 65, 47, 51, 93, 97, 80, 97, 25, 42, 59, 18, 6, 12, 30, 76, 27, 18, 50, 72, 48, 67, 57], [28, 1, 100, 49, 40, 26, 79, 21, 15, 53, 1, 28, 96, 56, 75, 9, 83, 97, 95, 48, 35, 46, 54, 7, 36, 46, 74, 21, 32, 93, 43], [40, 19, 17, 24, 9, 83, 91, 35, 57, 72, 67, 76, 85, 54, 20, 21, 43, 24, 50, 67, 58, 11, 62, 77, 5, 38, 96, 33, 76, 32, 80], [35, 27, 74, 92, 29, 21, 33, 60, 17, 37, 39, 43, 54, 58, 59, 5, 95, 27, 12, 65, 6, 87, 46, 1, 37, 11, 88, 76, 27, 62, 66], [45, 8, 2, 42, 25, 9, 73, 26, 44, 88, 38, 68, 81, 84, 13, 4, 88, 74, 68, 39, 11, 22, 1, 42, 100, 30, 40, 60, 55, 63, 47], [79, 96, 35, 25, 9, 35, 64, 39, 57, 21, 46, 36, 57, 54, 83, 74, 12, 43, 16, 74, 26, 91, 31, 2, 36, 61, 98, 10, 43, 64, 54], [64, 40, 94, 18, 85, 73, 90, 10, 62, 22, 81, 36, 17, 13, 63, 39, 4, 5, 72, 63, 48, 86, 14, 67, 33, 68, 87, 82, 98, 11, 62], [61, 62, 5, 24, 23, 84, 31, 59, 9, 38, 53, 70, 22, 85, 54, 92, 8, 62, 57, 4, 64, 87, 92, 62, 3, 14, 72, 11, 12, 32, 25], [72, 83, 78, 68, 56, 65, 83, 88, 46, 82, 41, 81, 74, 24, 52, 28, 69, 7, 73, 3, 57, 83, 67, 59, 2, 73, 29, 38, 100, 61, 73], [59, 6, 45, 13, 82, 10, 82, 13, 61, 70, 72, 43, 62, 90, 6, 68, 76, 17, 11, 93, 39, 62, 83, 29, 6, 99, 46, 89, 15, 8, 78], [94, 55, 71, 75, 13, 50, 41, 68, 42, 88, 95, 47, 91, 3, 100, 66, 37, 13, 56, 25, 83, 52, 98, 5, 20, 10, 11, 38, 8, 72, 91], [11, 60, 3, 16, 4, 22, 69, 82, 53, 52, 73, 45, 5, 75, 64, 46, 88, 85, 18, 76, 44, 12, 42, 84, 13, 53, 74, 13, 99, 11, 19], [98, 27, 39, 98, 19, 44, 79, 25, 79, 4, 6, 80, 31, 94, 90, 58, 74, 98, 14, 94, 45, 82, 86, 90, 61, 86, 60, 18, 75, 16, 46], [8, 50, 87, 51, 76, 19, 15, 16, 42, 21, 23, 36, 90, 88, 58, 27, 21, 90, 73, 73, 10, 23, 40, 14, 61, 9, 77, 45, 9, 40, 37], [23, 4, 1, 98, 64, 69, 39, 20, 90, 71, 57, 38, 39, 42, 72, 93, 17, 3, 33, 43, 1, 18, 7, 14, 93, 74, 38, 92, 35, 15, 68], [88, 90, 36, 97, 72, 58, 56, 71, 59, 27, 91, 90, 69, 33, 48, 44, 72, 33, 65, 69, 19, 1, 17, 87, 6, 38, 26, 74, 31, 23, 48], [33, 12, 57, 26, 61, 44, 41, 31, 100, 9, 69, 70, 98, 49, 29, 9, 27, 85, 95, 54, 98, 99, 32, 51, 73, 23, 41, 49, 87, 1, 71], [88, 39, 88, 20, 66, 7, 75, 60, 90, 35, 77, 94, 22, 68, 1, 51, 54, 2, 70, 7, 61, 61, 97, 97, 28, 8, 75, 50, 58, 78, 97], [24, 98, 90, 98, 20, 76, 19, 25, 52, 79, 31, 46, 72, 22, 74, 22, 84, 23, 9, 12, 26, 61, 67, 40, 62, 36, 33, 98, 85, 41, 58], [22, 11, 66, 28, 30, 31, 32, 86, 48, 23, 35, 93, 3, 60, 16, 15, 27, 99, 100, 82, 7, 74, 98, 90, 38, 57, 92, 4, 5, 71, 39], [81, 39, 78, 4, 52, 50, 3, 80, 46, 99, 80, 27, 20, 21, 4, 80, 58, 45, 46, 2, 46, 82, 8, 32, 4, 11, 31, 78, 90, 50, 88], [53, 90, 22, 40, 3, 91, 46, 22, 89, 16, 4, 95, 84, 12, 15, 6, 3, 69, 38, 40, 88, 22, 35, 46, 2, 63, 97, 40, 14, 36, 91], [91, 21, 77, 34, 70, 18, 79, 96, 58, 37, 27, 87, 74, 66, 23, 60, 36, 46, 89, 100, 77, 26, 83, 92, 35, 9, 6, 80, 31, 1, 82], [98, 33, 30, 82, 63, 20, 62, 88, 89, 77, 49, 89, 49, 49, 84, 48, 16, 44, 85, 52, 38, 63, 84, 19, 69, 27, 28, 58, 78, 43, 3], [95, 43, 94, 44, 13, 25, 23, 78, 97, 99, 41, 69, 23, 90, 42, 66, 22, 90, 60, 31, 14, 79, 19, 60, 86, 75, 35, 70, 7, 47, 41], [16, 79, 64, 60, 92, 15, 94, 10, 45, 88, 71, 74, 70, 95, 89, 77, 65, 35, 70, 47, 84, 18, 88, 1, 56, 36, 50, 38, 38, 9, 28], [33, 87, 56, 56, 3, 63, 72, 65, 89, 7, 75, 41, 85, 87, 62, 86, 84, 22, 35, 29, 49, 15, 21, 7, 92, 73, 38, 16, 91, 32, 41], [78, 88, 10, 83, 43, 58, 18, 53, 84, 23, 95, 75, 34, 53, 73, 59, 21, 5, 73, 23, 39, 96, 39, 68, 54, 7, 95, 88, 26, 56, 36]],
              (35, 6),
              (21,16))
