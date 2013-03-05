import curses
import random

class Game(object):
    def __init__(self, w, h, display):
        self.display = display
        self.field = []
        self.score = 0
        self.moves = 0
        self.point_per_cell = 50
        for i in range(0, w + 2):
            row = []
            self.field.append(row)
            for j in range(0, h + 2):
                if i == 0 or i == w + 1:
                    row.append(0)
                elif j == 0 or j == h + 1:
                    row.append(0)
                else:
                    row.append(random.randrange(1, 7))

    def start(self):
        self.display.clear()
        initial_color = self.field[1][1]
        self.field[1][1] = 7
        res = self._find_cells_to_color(initial_color)
        if res > 0:
            for x, y in res:
                self.field[y][x] = 7
        self._update_field()
        self.display.update_hud(self.score, self.moves)

    def _find_cells_to_color(self, color):
        res = []
        cells = []
        def find_colored(x, y, color):
            if color == 7:
                cells.append( (x, y) )
        self._for_each_cell(False, find_colored)
        while len(cells) > 0:
            x, y = cells[0]
            if self.field[y][x] == color:
                res.append( (x, y) )
            for nx, ny in self._find_neighs(x, y):
                if (self.field[ny][nx] == color) and (not (nx, ny) in res):
                    cells.append( (nx, ny) )
            cells = cells[1:]
        return res

    def move(self, color):
        res = self._find_cells_to_color(color)
        if len(res) > 0:
            for x, y in res:
                self.field[y][x] = 7
            self.score = self.score + self.point_per_cell * len(res)
            self.point_per_cell = self.point_per_cell - 1
            self.moves = self.moves + 1
            self._update_field()
            self.display.update_hud(self.score, self.moves)
        return len(res)

    def finished(self):
        pass

    def _find_neighs(self, x, y):
        return [ (x + 1, y), (x-1, y), (x, y+1), (x, y-1) ]

    def _for_each_cell(self, skip_border, func):
        y_start = 0
        y_end = len(self.field)
        x_start = 0
        x_end = len(self.field[0])
        if skip_border:
            y_start = 1
            x_start = 1
            x_end = x_end - 1
            y_end = y_end - 1
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                func(x, y, self.field[y][x])

    def _update_field(self):
        sym_map = [ ' ', '1', '2', '3', '4', '5', '6', ' ' ]
        def _update_cell(x, y, color):
            ch = ' '
            for nx, ny in self._find_neighs(x, y):
                if color == 0:
                    continue
                if self.field[ny][nx] == 7:
                    ch = sym_map[color]
                    break
            self.display.paint_cell(x, y, color, ch)
        self._for_each_cell(False, _update_cell)
        pass


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
