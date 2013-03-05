import curses

from game import Game

class CursesDisplay(object):
    def __init__(self, scr):
        self.scr = scr
        pass

    def clear(self):
        colors = [(curses.COLOR_WHITE, curses.COLOR_BLACK),
            (curses.COLOR_YELLOW, curses.COLOR_RED),
            (curses.COLOR_YELLOW, curses.COLOR_GREEN),
            (curses.COLOR_GREEN, curses.COLOR_YELLOW),
            (curses.COLOR_CYAN, curses.COLOR_BLUE),
            (curses.COLOR_BLUE, curses.COLOR_CYAN),
            (curses.COLOR_CYAN, curses.COLOR_MAGENTA) ]
        for c in range(1,7):
            f, b = colors[c]
            curses.init_pair(c, f, b)

    def update_hud(self, score, moves):
        self.scr.addstr(23, 0, "Score: %d Moves: %d" % (score, moves))

    def paint_cell(self, x, y, color, caption):
        self.scr.addch(y, x * 2, ord( caption ), curses.color_pair(color))
        self.scr.addch(y, x * 2 + 1, ' ', curses.color_pair(color))

#def set_cur_color(color):
#    f, b = colors[color]
#    curses.init_pair(7, f, b)

def loop(scr, w, h):
    display = CursesDisplay(scr)
    game = Game(w, h, display)
    game.start()

    key = scr.getch()
    while not key == ord('q'):
        if key >= ord('1') and key <= ord('6'):
            color = key - ord('0')
            cnt = game.move(color)
        elif key == ord('r'):
            game = Game(w, h, display)
            game.start()
        key = scr.getch()

curses.wrapper(loop, 10, 10)
