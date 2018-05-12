from unittest import TestCase

from hexagons import RectangleStorage


class TestRectangleStorage(TestCase):
    def test___init__(self):
        class TestCell:
            pass

        rs = RectangleStorage(7, 7, TestCell())
        self.assertEqual(len(rs.array), 7)
        self.assertEqual(len(rs.array[0]), 10)
