#PASSED
#  Problem Statement
# Your chess club is playing a match against an opposing chess club. Each club enters N players into the match, and each player plays one game against a player from the other team. Each game that is won is worth 2 points, and each game that is drawn is worth 1 point. Your goal is to score as many points as possible.
#
# Your secret agents have determined the skill of every member of the opposing team, and of course you know the skill of every member of your own team. You can use this information to decide which opposing player will play against each of your players in order to maximize your score. Assume that the player with the higher skill in a game will always win, and if the players have the same skill then they will draw.
#
# You will be given s us and them, indicating the skills of your players and of the opposing players, respectively. Return the maximum number of points that your team can score.
#
# Definition
# Class: ChessMatchup
# Method: maximumScore
# Parameters: tuple (integer), tuple (integer)
# Returns: integer
# Method signature: def maximumScore(self, us, them):
# Limits
# Time limit (s): 840.000
# Memory limit (MB): 64
# Constraints
# - us and them will each contain between 1 and 50 elements, inclusive.
# - us and them will contain the same number of elements.
# - Each element of us and them will be between 1 and 1000, inclusive.


class ChessMatchup(object):
    def maximumScore(self, us, them):
        #Sort skill vals:
        us = list(us)
        them = list(them)
        us.sort()
        them.sort()

        #Starting with the lowest from us, try to eliminate an opponent:
        score = 0
        remaining = list(them)
        for me in us:
            #try to win the matchup:
            ret = [i for i in range(len(remaining)) if remaining[i] < me]
            if ret:
                score += 2
                del remaining[max(ret)]
            else:
                #Try to just tie:
                ret = [i for i in range(len(remaining)) if remaining[i] == me]
                if ret:
                    score += 1
                    del remaining[max(ret)]

        # Try also going from highest to lowest:
        altscore = 0
        remaining = list(them)
        for me in reversed(us):
            # try to win the matchup:
            ret = [i for i in range(len(remaining)) if remaining[i] < me]
            if ret:
                altscore += 2
                del remaining[max(ret)]
            else:
                # Try to just tie:
                ret = [i for i in range(len(remaining)) if remaining[i] == me]
                if ret:
                    altscore += 1
                    del remaining[max(ret)]
        if altscore > score:
            score = altscore

        return score















foo = ChessMatchup()
# Examples
# 0)
# {5, 8}
# {7, 3}
us = (5, 8)
them = (7, 3)
# Returns: 4
# By playing 5 against 3 and 8 against 7, you can win both games.
# 1)
# {7, 3}
# {5, 8}
# Returns: 2
# This is the reverse of the previous case. By playing 7 against 5 and 3 against 8, you can win one game.
# 2)
us = (10, 5, 1)
them = (10, 5, 1)
# Returns: 4
# If you play matching pairs you will draw all three games for 3 points. However, playing 10-5, 5-1 and 1-10 gives you two wins and a loss, for 4 points.
# 3)
# us = (1, 10, 7, 4)
# them = (15, 3, 8, 7)
# Returns: 5

result = foo.maximumScore(us, them)

print('done')
