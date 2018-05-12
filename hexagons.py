import copy
import math


class Storage:
    def __init__(self, rows, columns, prototype_cell):
        h = rows
        w = columns - self.first_column(rows)
        self.array = [[copy.copy(prototype_cell) for _ in range(w)] for _ in range(h)]

    def get(self, q, r):
        #print("(%d,%d) -> array[%d][%d]" % (q, r, r, q - self.first_column(r)))
        return self.array[r][q - self.first_column(r)]


class RectangleStorage(Storage):
    def __init__(self, rows, columns, prototype_cell):
        super().__init__(rows, columns, prototype_cell)
        pass

    @staticmethod
    def first_column(r):
        return -math.floor(r / 2)


class HexGrid:
    def __init__(self, rows, columns, prototype_cell):
        self.rows = rows
        self.columns = columns
        self.storage = RectangleStorage(rows, columns, prototype_cell)

    def __str__(self):
        retval = ''
        for r in range(self.rows):
            if r % 2 == 1:
                retval += ' '
            offset = self.storage.first_column(r)
            for q in range(offset, self.columns + offset):
                retval += str(self.storage.get(q, r))
                retval += ' '
            retval += '\n'
        return retval

    def get_cell(self, q, r):
        return self.storage.get(q, r)

    def first_column(self, r):
        return self.storage.first_column(r)


class OptionalCell:
    def __init__(self, default_value, valid=True):
        self.value = default_value
        self.valid = valid

    def get_value(self):
        return self.value

    def set_valid(self, value):
        self.valid = value

    def __str__(self):
        return self.value if self.valid else ' '


def generate_star():
    def set_valid(q, r):
        hg.get_cell(q, r).set_valid(True)

    hg = HexGrid(17, 13, OptionalCell('o', False))

    for r in range(9):
        q_range = range(6 - r, 7) if r < 4 else range(hg.first_column(4), 11 - r + 4)
        for q in q_range:
            set_valid(q, r)
            set_valid(q + hg.first_column(16) + r, 16 - r)

    return hg


if __name__ == '__main__':
    hg = generate_star()
    print(hg)
