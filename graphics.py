from tkinter import Tk, BOTH, Canvas

class Window:

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("maze solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=0)
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False


class Point():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():

    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self._p1.x, self._p1.y, self._p2.x, self._p2.y, fill=fill_color, width=2)





