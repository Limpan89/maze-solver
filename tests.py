import unittest
from maze import Maze
from graphics import Window

class Tests(unittest.TestCase):

    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, None)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_maze_remove_walls(self):
        win = Window(800, 600)
        num_cols = 5
        num_rows = 10
        m1 = Maze(20, 20, num_rows, num_cols, 10, 10, win)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)
        self.assertEqual(m1._cells[0][0].has_top_wall, False)
        self.assertEqual(m1._cells[-1][-1].has_bottom_wall, False)

    def test_maze_solve(self):
        win = Window(800, 600)
        num_cols = 10
        num_rows = 10
        m1 = Maze(20, 20, num_rows, num_cols, 20, 20, win)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)
        self.assertTrue(m1.solve())


if __name__ == "__main__":
    unittest.main()