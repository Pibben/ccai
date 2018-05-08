import copy
import math

def width2(line):
    if line < 4:
        return line+1
    elif line < 9:
        return 13 - (line - 4)
    else:
        return width(16-line)

def width(line):
    if line < 9:
        return line + 1
    else:
        return width(16-line)


class BoardState:
    def __init__(self):
        self.state = []
        for x in range(17):
            self.state.append([0]*width(x))

    def reset(self):
        for x in range(4):
            self.state[x] = [1]*width(x)

        for x in range(13,17):
            self.state[x] = [2]*width(x)

    def pprint(self):
        for x in range(16, -1, -1):
            print("{: ^50s}".format(" ".join([str(i) for i in self.state[x]])))
        print("")

class Move:
    pass


class Player:
    def __init__(self, id, target_row):
        self.id = id
        self.target_row = target_row

class GameLogic:
    def decodeTarget(self, row, i, dir, steps):

        narrowingFwd = (width(row) - width(row + 1) + 1) // 2
        narrowingBwd = (width(row) - width(row - 1) + 1) // 2

        if dir == 'r':
            retval = (row, i + 1)
        elif dir == 'l':
            retval = (row, i - 1)
        elif dir == 'lf':
            retval = (row + 1, i - narrowingFwd)
        elif dir == 'rf':
            retval = (row + 1, i - narrowingFwd + 1)
        elif dir == 'lb':
            retval = (row - 1, i - narrowingBwd)
        elif dir == 'rb':
            retval = (row - 1, i - narrowingBwd + 1)
        else:
            print("ERROR!")
            retval = ()

        if steps == 1:
            return retval
        else:
            return self.decodeTarget(*retval, dir, 1)

    def evolve(self, move, state):
        ((frow, fi), (trow, ti)) = move
        player_id = state.state[frow][fi]
        state.state[frow][fi] = 0
        state.state[trow][ti] = player_id

    def isMoveWithinBoard(self, move):
        (row, i, dir, steps) = move

        #print(row, i, dir)

        if row == 0 and dir in ['rb', 'lb']:
            return False

        if row == 16 and dir in ['rf', 'lf']:
            return False

        narrowingFwd = (width(row) - width(row+1) + 1) // 2
        narrowingBwd = (width(row) - width(row-1) + 1) // 2

        if dir == 'l':
            if i == 0:
                return False
        elif dir == 'lf':
            if i < narrowingFwd or i > width(row) - narrowingFwd:
                return False
        elif dir == 'rf':
            if i < narrowingFwd - 1 or i > width(row) - narrowingFwd - 1:
                return False
        elif dir == 'r':
            if i == width(row) - 1:
                return False
        elif dir == 'lb':
            if i < narrowingBwd or i > width(row) - narrowingBwd:
                return False
        elif dir == 'rb':
            if i < narrowingBwd - 1 or i > width(row) - narrowingBwd - 1:
                return False

        return True

    def isValidMove(self, move, state, player):
        if not self.isMoveWithinBoard(move):
            return False

        (row, i, dir, steps) = move

        (trow, ti) = self.decodeTarget(row, i, dir, 1)

        if state[trow][ti] != 0:
            if steps == 1:
                return False
            else:
                return self.isValidMove((trow, ti, dir, 1), state, player)
        else:
            if steps == 2:
                return False

        return True

    def generateAllValidMoves(self, state, player):
        state = state.state
        for row in range(17):
            for i in range(len(state[row])):
                if state[row][i] == player.id:
                    for dir in ['l', 'lf', 'rf', 'r', 'rb', 'lb']:
                        if self.isValidMove((row, i, dir, 1), state, player):
                            (trow, ti) = self.decodeTarget(row, i, dir, 1)
                            yield ((row, i), (trow, ti))

                        (prow, pi) = (row, i)

                        while(self.isValidMove((prow, pi, dir, 2), state, player)):
                            (trow, ti) = self.decodeTarget(prow, pi, dir, 2)
                            yield ((prow, pi), (trow, ti))
                            (prow, pi) = (trow, ti)

    def getScore(self, state, player):
        state = state.state
        sum = 0
        for row in range(17):
            for i in range(len(state[row])):
                if state[row][i] == player.id:
                    sum += abs((16 - player.target_row) - row)

        return sum

    def getOptimalMove(self, state, player):
        topScore = 0
        topMove = ()
        gen = g.generateAllValidMoves(state, player)
        for move in gen:
            ap = copy.deepcopy(state)
            g.evolve(move, ap)
            score = g.getScore(ap, player)

            if score > topScore:
                topMove = move
                topScore = score

        return topMove


if __name__ == '__main__':
    a = BoardState()
    a.reset()

    a.pprint()

    g = GameLogic()

    p1 = Player(1, 16)
    p2 = Player(2, 0)

    for i in range(10):
        topMove = g.getOptimalMove(a, p1)
        g.evolve(topMove, a)

        topMove = g.getOptimalMove(a, p2)
        g.evolve(topMove, a)

        a.pprint()
        print(g.getScore(a, p1))
        input("->")
