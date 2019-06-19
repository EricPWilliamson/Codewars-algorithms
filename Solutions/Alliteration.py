
#PASSED

class Alliteration(object):
    def picture(self, wordtup):
        result = 0

        prevletter = ""
        onarun = False
        for s in wordtup:
            newletter = s[0].lower()
            if newletter == prevletter:
                if not onarun:
                    result += 1
                onarun = True
            else:
                onarun = False

            prevletter = newletter

        return int(result)

foo = Alliteration()
foo.picture(("He", "has", "four", "fanatic", "fantastic", "fans"))

