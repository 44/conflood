import curses

from game import Game
from display import CursesDisplay

#def set_cur_color(color):
#    f, b = colors[color]
#    curses.init_pair(7, f, b)

class Control(object):
    def __init__(self, w, h, display):
        self.w = w
        self.h = h
        self.display = display
        self.reset()
        pass
    def move(self, color):
        self.game.move(color)
        return True
    def reset(self):
        self.game = Game(self.w, self.h, self.display)
        self.game.start()
        return True
    def quit(self):
        return False

def loop(scr, w, h):
    display = CursesDisplay(scr)
    control = Control(w, h, display)
    display.loop(control)

curses.wrapper(loop, 5, 5)
