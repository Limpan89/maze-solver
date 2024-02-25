from graphics import Line, Point
import time, random

class Maze:

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        if num_rows <= 0:
            raise Exception("The number of rows must be greater then 0")
        if num_cols <= 0:
            raise Exception("The number of columns must ge greater then 0")
        if cell_size_x <= 0 or cell_size_y <= 0:
            raise Exception("The Cell Size must be greater then 0")
        if x1 < 0 or y1 < 0:
            raise Exception("The x and y values may not be a negative number")
        self._cells = []
        self._win = win
        if seed is not None:
            random.seed(seed)
        self._create_cells(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y)

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == len(self._cells) - 1 and j == len(self._cells[0]) - 1:
            return True
        for y in range(i - 1, i + 2):
            for x in range(j - 1, j + 2):
                if (y >= 0 and y < len(self._cells) and x >= 0 and x < len(self._cells[0])
                and (y - i == 0 or x - j == 0) and not self._cells[y][x].visited
                and self._cells[i][j].has_broken_walls(self._cells[y][x])):
                    self._cells[i][j].draw_move(self._cells[y][x])
                    if self._solve_r(y, x):
                        return True
                    self._cells[i][j].draw_move(self._cells[y][x], True)
        return False
                    
    def _create_cells(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y):
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                row.append(Cell(x1 + cell_size_x * j, x1 + cell_size_x * (j + 1),
                                y1 + cell_size_y * i, y1 + cell_size_y * (i + 1), self._win))
            self._cells.append(row)
        if self._win is None:
            return
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(-1, -1)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()
    
    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if ((x == 0 or y == 0) and i + y >= 0 and i + y < len(self._cells)
                        and j + x >= 0 and j + x < len(self._cells[0])
                        and not self._cells[i + y][j + x].visited):
                        to_visit.append((i + y, j + x))
            if not to_visit:
                self._draw_cell(i, j)
                return
            other = to_visit[random.randrange(len(to_visit))]
            self._cells[i][j].break_walls(self._cells[other[0]][other[1]])
            self._break_walls_r(other[0], other[1])

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False


class Cell():
    
    def __init__(self, x1, x2, y1, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self):
        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black" if self.has_left_wall else "white")
        self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black" if self.has_right_wall else "white")
        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black" if self.has_top_wall else "white")
        self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black" if self.has_bottom_wall else "white")

    def draw_move(self, to_cell, undo=False):
        p1 = Point(self._x1 + (self._x2 - self._x1) / 2, self._y1 + (self._y2 - self._y1) / 2)
        p2 = Point(to_cell._x1 + (to_cell._x2 - to_cell._x1) / 2, to_cell._y1 + (to_cell._y2 - to_cell._y1) / 2)
        self._win.draw_line(Line(p1, p2), "grey" if undo else "red")

    def has_broken_walls(self, other):
        return ((self._y2 == other._y1 and not self.has_bottom_wall and not other.has_top_wall)
                or (self._y1 == other._y2 and not self.has_top_wall and not other.has_bottom_wall)
                or (self._x2 == other._x1 and not self.has_right_wall and not other.has_left_wall)
                or (self._x1 == other._x2 and not self.has_left_wall and not other.has_right_wall))

    def break_walls(self, other):
        if self._y2 == other._y1:
            self.has_bottom_wall, other.has_top_wall = False, False
        elif self._y1 == other._y2:
            self.has_top_wall, other.has_bottom_wall = False, False
        elif self._x2 == other._x1:
            self.has_right_wall, other.has_left_wall = False, False
        elif self._x1 == other._x2:
            self.has_left_wall, other.has_right_wall = False, False
        