import curses
import random

sym_map = [ ' ', '1', '2', '3', '4', '5', '6', ' ' ]
colors = [(curses.COLOR_WHITE, curses.COLOR_BLACK),
    (curses.COLOR_YELLOW, curses.COLOR_RED),
    (curses.COLOR_YELLOW, curses.COLOR_GREEN),
    (curses.COLOR_GREEN, curses.COLOR_YELLOW),
    (curses.COLOR_CYAN, curses.COLOR_BLUE),
    (curses.COLOR_BLUE, curses.COLOR_CYAN),
    (curses.COLOR_CYAN, curses.COLOR_MAGENTA) ]

def generate_field(w, h):
    result = []
    for i in range(0, w+2):
        row = []
        result.append(row)
        for j in range(0, h+2):
            if i == 0 or i == w + 1:
                row.append(0)
            elif j == 0 or j == h + 1:
                row.append(0)
            else:
                row.append(random.randrange(1, 7))
    return result

def scan(fld, skip_border, func):
    y_start = 0
    y_end = len(fld)
    x_start = 0
    x_end = len(fld[0])
    if skip_border:
        y_start = 1
        x_start = 1
        x_end = x_end - 1
        y_end = y_end - 1

    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            func(x, y, fld[y][x])

def paint_elem(scr, fld, x, y, elem):
    neighs = [ (x + 1, y), (x-1, y), (x, y+1), (x, y-1) ]
    ch = ' '
    for nx, ny in neighs:
        if elem == 0:
            continue
        if fld[ny][nx] == 7:
            has_flood_neigh = True
            ch = sym_map[elem]
            break
    scr.addch(y, x * 2, ord( ch ), curses.color_pair(elem))
    scr.addch(y, x * 2 + 1, ' ', curses.color_pair(elem))

def paint_field(scr, fld):
    import functools
    scan(fld, False, functools.partial(paint_elem, scr, fld))
    scr.refresh()

def find_by_color(result, color, x, y, elem):
    if (color == elem):
        result.append( (x, y) )

def flood(fld, color):
    import functools
    res = []
    scan(fld, True, functools.partial(find_by_color, res, 7))
    while len(res) > 0:
        x, y = res[0]
        fld[y][x] = 7
        neighs = [ (x+1, y), (x-1, y), (x, y+1), (x, y-1) ]
        for nx, ny in neighs:
            if fld[ny][nx] == color:
                res.append( (nx, ny) )
        res = res[1:]

def init_colors(scr):
    for c in range(1,7):
        f, b = colors[c]
        curses.init_pair(c, f, b)

def set_cur_color(color):
    f, b = colors[color]
    curses.init_pair(7, f, b)

def loop(scr, w, h):
    init_colors(scr)
    field = generate_field(w,h)
    initial_color = field[1][1]
    field[1][1] = 7
    flood(field, initial_color)
    set_cur_color(initial_color)
    paint_field(scr, field)
    key = scr.getch()
    while not key == ord('q'):
        if key >= ord('1') and key <= ord('6'):
            color = key - ord('0')
            flood(field, color)
            set_cur_color(color)
            paint_field(scr, field)
        key = scr.getch()

curses.wrapper(loop, 13, 13)
