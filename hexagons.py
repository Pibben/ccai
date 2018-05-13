import copy
import math


class Storage:
    def __init__(self, rows, columns, prototype_cell):
        h = rows
        w = columns - self.first_column(rows)
        self.array = [[copy.copy(prototype_cell) for _ in range(w)] for _ in range(h)]

    def get(self, q, r):
        try:
            return self.array[r][q - self.first_column(r)]
        except IndexError:
            return None

    def set(self, q, r, cell):
        self.array[r][q - self.first_column(r)] = cell


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

    def iterate(self):
        for r in range(self.rows):
            offset = self.first_column(r)
            for q in range(offset, self.columns + offset):
                yield q, r

    def move(self, from_q, from_r, to_q, to_r):
        src_cell = self.storage.get(from_q, from_r)
        dst_cell = self.storage.get(to_q, to_r)
        dst_cell.set_value(src_cell.get_value())
        src_cell.set_value(None)


class OptionalCell:
    def __init__(self, default_value, valid=True):
        self.value = default_value
        self.valid = valid
        self.default_value = default_value

    def reset(self):
        self.value = self.default_value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_valid(self, value):
        self.valid = value

    def is_valid(self):
        return self.valid

    def __str__(self):
        if self.valid:
            if self.value:
                return str(self.value)
            else:
                return 'o'
        else:
            return ' '


if __name__ == '__main__':
    hg = generate_star()
    print(hg)
    for c in hg.iterate():
        print(c)
