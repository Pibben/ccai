# https://www.redblobgames.com/grids/hexagons/
import cProfile
import functools
import time

from hexagons import HexGrid, OptionalCell


class Player:
    def __init__(self, id, target_row):
        self.id = id
        self.target_row = target_row

    def __str__(self):
        return str(self.id)


class GameLogic:
    def do(self, move, grid):
        grid.move(*move[0], *move[1])

    def undo(self, move, grid):
        grid.move(*move[1], *move[0])

    def generate_all_valid_moves(self, grid, player):
        for (q, r) in grid.iterate():
            cell = grid.get_cell(q, r)
            if cell.get_value() is player:
                neighbours = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
                for n in neighbours:
                    tq, tr = q + n[0], r + n[1]  # TODO
                    dest_cell = grid.get_cell(tq, tr)
                    if dest_cell and dest_cell.is_valid() and not dest_cell.get_value():
                        yield ((q, r), (tq, tr))

    def get_score(self, grid, player):
        sum = 0

        for (q, r) in grid.iterate():
            cell_value = grid.get_cell(q, r).get_value()

            if cell_value and cell_value.id == player.id: #TODO
                #sum += abs((16 - player.target_row) - r)
                sum += grid.distance(q, r, *player.target_row)
                #print(q, r, *player.target_row, grid.distance(q, r, *player.target_row))

        return 1.0 / sum


class Heuristic:
    def __init__(self):
        pass

    def get_optimal_move(self, game_logic, grid, max_player, min_player):
        top_score = 0
        top_move = ()
        gen = game_logic.generate_all_valid_moves(grid, max_player)
        for move in gen:
            game_logic.do(move, grid)
            score = game_logic.get_score(grid, max_player)
            game_logic.undo(move, grid)

            if score > top_score:
                top_move = move
                top_score = score

        return top_move


class Minimax:
    def __init__(self):
        pass

    def get_optimal_move(self, game_logic, grid, max_player, min_player):
        def minimax(game_logic, grid, max_player, min_player, depth, maximize):

            if depth == 0:
                return game_logic.get_score(grid, max_player), (None, None)

            gen = game_logic.generate_all_valid_moves(grid, max_player if maximize else min_player)

            best_value = float('-inf') if maximize else float('inf')

            count = 0  # TODO:
            for move in gen:
                game_logic.do(move, grid)
                v, __ = minimax(game_logic, grid, max_player, min_player, depth - 1, not maximize)
                game_logic.undo(move, grid)

                if maximize:
                    if v > best_value:
                        best_value = v
                        best_move = move
                else:
                    if v < best_value:
                        best_value = v
                        best_move = move

                count += 1

            if count == 0:
                return game_logic.get_score(grid, max_player), (None, None)

            return best_value, best_move

        return minimax(game_logic, grid, max_player, min_player, 3, True)[1]


class Alphabeta:
    def __init__(self):
        pass

    def get_optimal_move(self, game_logic, grid, max_player, min_player):
        def alphabeta(game_logic, grid, max_player, min_player, depth, alpha, beta, maximize):

            if depth == 0:
                return game_logic.get_score(grid, max_player), (None, None)

            gen = game_logic.generate_all_valid_moves(grid, max_player if maximize else min_player)

            best_value = float('-inf') if maximize else float('inf')

            count = 0  # TODO:
            for move in gen:
                count += 1

                game_logic.do(move, grid)
                v, __ = alphabeta(game_logic, grid, max_player, min_player, depth - 1, alpha, beta, not maximize)
                game_logic.undo(move, grid)

                if maximize:
                    if v > best_value:
                        best_value = v
                        best_move = move
                    alpha = max(alpha, v)
                else:
                    if v < best_value:
                        best_value = v
                        best_move = move
                    beta = min(beta, v)
                if beta <= alpha:
                    break

            if count == 0:
                return game_logic.get_score(grid, max_player), (None, None)

            return best_value, best_move

        return alphabeta(game_logic, grid, max_player, min_player, 3, float('-inf'), float('inf'), True)[1]


def generate_star(hg, players):
    def set_valid(q, r):
        hg.get_cell(q, r).set_valid(True)

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
    hg = HexGrid(17, 13, OptionalCell(None, False))

    p1 = Player(1, (6 + hg.first_column(16), 16))
    p2 = Player(2, (6, 0))

    a = generate_star(hg, [p1, p2])

    print(a)

    g = GameLogic()
    opt = Alphabeta()

    for i in range(1000):
        topMove = opt.get_optimal_move(g, a, p1, p2)
        g.do(topMove, a)

        topMove = opt.get_optimal_move(g, a, p2, p1)
        g.do(topMove, a)

        if i > 1:
            print(a)
            input("->")
