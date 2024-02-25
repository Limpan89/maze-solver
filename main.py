from graphics import Window
from maze import Maze

def main():
    win = Window(800, 600)
    m = Maze(10, 10, 10, 10, 40, 40, win)
    m.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()