import math
import numpy as np

class Storage:
    def __init__(self, rows, columns, default_value):
        h = rows
        w = columns - self.first_column(rows)
        self.array = np.ones((h, w)) * default_value

    def get(self, q, r):
        try:
            return self.array[r][q - self.first_column(r)]
        except IndexError:
            return None

    def set(self, q, r, cell):
        self.array[r][q - self.first_column(r)] = cell

    def run(self, func):
        return func(self.array)

class RectangleStorage(Storage):
    def __init__(self, rows, columns, default_value):
        super().__init__(rows, columns, default_value)
        pass

    @staticmethod
    def first_column(r):
        return -math.floor(r / 2)


class HexGrid:
    def __init__(self, rows, columns, default_value):
        self.rows = rows
        self.columns = columns
        self.storage = RectangleStorage(rows, columns, default_value)

    def __str__(self):
        retval = ''
        for r in range(self.rows):
            if r % 2 == 1:
                retval += ' '
            offset = self.storage.first_column(r)
            for q in range(offset, self.columns + offset):
                value = self.storage.get(q, r)
                if value == 0:
                    retval += 'o'
                elif value > 0:
                    retval += str(int(value))
                else:
                    retval += ' '
                retval += ' '
            retval += '\n'
        return retval

    def get_cell(self, q, r):
        return self.storage.get(q, r)

    def set_cell(self, q, r, value):
        self.storage.set(q, r, value)

    def first_column(self, r):
        return self.storage.first_column(r)

    def iterate(self):
        for r in range(self.rows):
            offset = self.first_column(r)
            for q in range(offset, self.columns + offset):
                yield q, r

    def move(self, from_q, from_r, to_q, to_r):
        src_cell = self.storage.get(from_q, from_r)
        self.storage.set(to_q, to_r, src_cell)
        self.storage.set(from_q, from_r, 0)

    def run(self, func):
        return self.storage.run(func)

    @staticmethod
    def distance(a_q, a_r, b_q, b_r):
        return (abs(a_q - b_q)
                + abs(a_q + a_r - b_q - b_r)
                + abs(a_r - b_r)) / 2


if __name__ == '__main__':
    hg = generate_star()
    print(hg)
    for c in hg.iterate():
        print(c)
