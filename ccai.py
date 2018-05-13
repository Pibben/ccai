# https://www.redblobgames.com/grids/hexagons/

import copy

from hexagons import HexGrid, OptionalCell


def width2(line):
    if line < 4:
        return line + 1
    elif line < 9:
        return 13 - (line - 4)
    else:
        return width(16 - line)


def width(line):
    if line < 9:
        return line + 1
    else:
        return width(16 - line)


class Move:
    pass


class Player:
    def __init__(self, id, target_row):
        self.id = id
        self.target_row = target_row

    def __str__(self):
        return str(self.id)


class GameLogic:
    def evolve(self, move, grid):
        grid.move(*move[0], *move[1])

    def generate_all_valid_moves(self, grid, player):
        for (q, r) in grid.iterate():
            cell = grid.get_cell(q, r)
            if cell.get_value() is player:
                neighbours = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
                for n in neighbours:
                    tq, tr = q + n[0], r + n[1] #TODO
                    dest_cell = grid.get_cell(tq, tr)
                    if dest_cell and dest_cell.is_valid() and not dest_cell.get_value():
                        yield ((q, r), (tq, tr))

    def get_score(self, grid, player):
        sum = 0

        for (q, r) in grid.iterate():
            cell = grid.get_cell(q, r)
            if cell.get_value() and cell.get_value().id == player.id: #TODO
                sum += abs((16 - player.target_row) - r)

        return sum

    def get_optimal_move(self, grid, player):
        top_score = 0
        top_move = ()
        gen = g.generate_all_valid_moves(grid, player)
        for move in gen:
            ap = copy.deepcopy(grid)
            g.evolve(move, ap)
            score = g.get_score(ap, player)
            print(move, score)

            if score > top_score:
                top_move = move
                top_score = score

        return top_move


def generate_star(players):
    def set_valid(q, r):
        hg.get_cell(q, r).set_valid(True)

    hg = HexGrid(17, 13, OptionalCell(None, False))

    for r in range(9):
        q_range = range(6 - r, 7) if r < 4 else range(hg.first_column(4), 11 - r + 4)
        for q in q_range:
            set_valid(q, r)
            set_valid(q + hg.first_column(16) + r, 16 - r)
            if r < 4:
                hg.get_cell(q, r).set_value(players[0])
                hg.get_cell(q + hg.first_column(16) + r, 16 - r).set_value(players[1])
    return hg


if __name__ == '__main__':
    p1 = Player(1, 16)
    p2 = Player(2, 0)

    a = generate_star([p1, p2])

    print(a)

    g = GameLogic()

    for i in range(10):
        topMove = g.get_optimal_move(a, p1)
        print(topMove)
        g.evolve(topMove, a)

        topMove = g.get_optimal_move(a, p2)
        g.evolve(topMove, a)

        print(a)
        print(g.get_score(a, p1))
        input("->")
