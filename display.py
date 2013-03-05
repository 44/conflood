import curses

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

    def loop(self, control):
        while True:
            proceed = True
            key = self.scr.getch()
            if  key == ord('q'):
                proceed = control.quit()
            elif key == ord('r'):
                proceed = control.reset()
            elif key >= ord('1') and key <= ord('6'):
                proceed = control.move( key - ord('0') )
            if not proceed:
                return

