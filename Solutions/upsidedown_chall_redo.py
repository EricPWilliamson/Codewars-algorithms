#PASSED
#Rewriting upsidedownnums_challenge_cw.py because original got too cludgey



def near_min(n_s, i, co_str):
    #Desc
    counter = 0
    L = len(n_s) - 2*i
    if (len(n_s)-1)/2 == i:#special case: center digit from odd length n_s. Also accounts for single digit limits
        V = [0, 1, 8]
        W = [0, 1, 8]
    elif i==0:
        V = [1, 6, 8, 9]
        W = [1, 9, 8, 6]
    else:
        V = [0, 1, 6, 8, 9]
        W = [0, 1, 9, 8, 6]

    for v,w in zip(V,W):
        if v > int(n_s[i]):
            #We can use all subcombinations:
            if L == 1: #Special case
                counter += 1
            if L % 2 == 1:  # odd num of digits
                counter += int(3 * 5 ** ((L - 3) / 2))
            else:  # even num of digits
                counter += int(5 ** ((L - 2) / 2))
        elif v == int(n_s[i]):
            #Maybe we can use the subcombinations, but we need to look deeper:
            new_cs = str(w) + co_str
            if L == 1:
                if int(new_cs) >= int(n_s[i:]):
                    counter += 1
            elif L == 2:
                new_cs = str(v) + str(w) + co_str
                if int(new_cs) >= int(n_s[i:]):
                    counter += 1
            else:
                counter += near_min(n_s, i+1, new_cs)

    return counter


def near_max(n_s, i, co_str):
    #Desc
    counter = 0
    L = len(n_s) - 2*i
    if (len(n_s)-1)/2 == i:#special case: center digit from odd length n_s. Also accounts for single digit limits
        V = [0, 1, 8]
        W = [0, 1, 8]
    elif i==0:
        V = [1, 6, 8, 9]
        W = [1, 9, 8, 6]
    else:
        V = [0, 1, 6, 8, 9]
        W = [0, 1, 9, 8, 6]

    for v,w in zip(V,W):
        if v < int(n_s[i]):
            #We can use all subcombinations:
            if L == 1: #Special case
                counter += 1
            if L % 2 == 1:  # odd num of digits
                counter += int(3 * 5 ** ((L - 3) / 2))
            else:  # even num of digits
                counter += int(5 ** ((L - 2) / 2))
        elif v == int(n_s[i]):
            #Maybe we can use the subcombinations, but we need to look deeper:
            if L == 1:
                new_cs = str(v) + co_str
                if int(new_cs) <= int(n_s[i:]):
                    counter += 1
            elif L == 2:
                new_cs = str(v) + str(w) + co_str
                if int(new_cs) <= int(n_s[i:]):
                    counter += 1
            else:
                new_cs = str(w) + co_str
                counter += near_max(n_s, i+1, new_cs)

    return counter


def upsidedown(a_s, b_s):
    counter = 0

    #Deal with the smallest digit size:
    counter += near_min(a_s,0, '')

    #Middle: we can use always use all digits in len(a_s)+1 and len(b_s)-1:
    for d in range(len(a_s)+1, len(b_s)):
        if d==1: #special case for 1 digit nums
            counter += 3
        elif (d % 2)==1: #odd num digits
            counter += int( 3 * 4 * 5**((d-3)/2) )
        else: #even num digits
            counter += int( 4 * 5**((d-2)/2) )

    #Deal with the last digit size:
    counter += near_max(b_s, 0, '')

    return counter

# test.describe('Example Tests')
print(upsidedown('0','10')==3)
print(upsidedown('6','25')==2)
print(upsidedown('10','100')==4) #Smallest 2 digit # to smallest 3 digit #. So all 2 digit #s are counted
print(upsidedown('100','1000')==12) #All 3 digit #s are counted
print(upsidedown('100000','12345678900000000')==718650) #All 6 digit #s, through 16 digit #s counted. About 400,000 17 digit #s counted.

#My own tests:
print(upsidedown('100','1001')==13)
print(upsidedown('100','1002')==13)

######################### Tricky CW tests: #########################################

print(upsidedown('9090908074312','617239057843276275839275848') - 2919867187)
#New min fcn puts us under by 312
#Orig min fcn puts us over by 1
# print('6172390578432')
# print('7')
# print('6275839275848')
# 909090
# 8
# 074312

# print(upsidedown('534','101')) #WTF!!
# # 534
# # 101
# # Should equal -2

print(upsidedown('26008611','668618434') - 952)
# 26008611
# 668618434
# 0.02ms
# 953 should equal 952

print(upsidedown('819','5505608') - 259)
# 819
# 5505608
# 0.01ms
# 258 should equal 259

print(upsidedown('908','12005') - 28)
# 908
# 12005
# 0.01ms
# 26 should equal 28

print(upsidedown('173','3625316') - 265)
# 173
# 3625316
# 0.01ms
# 264 should equal 265


