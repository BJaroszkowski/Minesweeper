# predefined colors
GREY = (204, 204, 204)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (253, 253, 115)
GREEN = (0, 100, 0)
RED = (199, 18, 18)
LIGHT_BLUE = (0, 128, 255)
DARK_BLUE = (8, 43, 182)
BROWN = (71, 23, 23)
TEAL = (0, 192, 192)
ORANGE = (255, 165, 0)

NUM_COLS = {'0': BLACK, '1': LIGHT_BLUE, '2': GREEN, '3': RED, '4': DARK_BLUE,
            '5': BROWN, '6': TEAL, '7': ORANGE, '8': BLACK, 'F': RED}
BGCOLOR = GREY


def TILE_MID(y, x):
    return (y*TILESIZE + 11, x*TILESIZE + 4 + TOP_PANEL)


def TILE_CORNER(y, x):
    return (y*TILESIZE+1, x*TILESIZE+TOP_PANEL+1)


def TIME_POS_X(text, width):
    return int((width-5*TILESIZE)/4 + TILESIZE - 0.5*text.get_width())


def MINES_POS_X(text, width):
    return int(3*(width-TILESIZE)/4 + TILESIZE - 0.5*text.get_width())


def MENU_BTN(x, y):
    return (x in range(int(1.5*TILESIZE)) and y in range(int(TILESIZE/2)))


def MENU_TEXT_POS(text):
    return (int((1.5*TILESIZE-text.get_width())/2),
            int((TILESIZE/2 - text.get_height())/2))


def MENU_OPTION_TEXT_POS(text, row):
    return (int((5*TILESIZE-text.get_width())/2),
            int((0.5+row)*TILESIZE+(TILESIZE-text.get_height())/2))


def DIFF_CHOICE(x, y):
    return (x in range(int(5*TILESIZE)) and
            y in range(int(TILESIZE/2), int(3*TILESIZE/2+1)))


def CONFIRM_TEXT_POS(confirm_y, text):
    return int(confirm_y+5/16*TILESIZE-text.get_height()/2)


def SCORES(x, y):
    return (x in range(int(5*TILESIZE)) and
            y in range(int(3*TILESIZE/2+1), int(5*TILESIZE/2)))


def GET_TILE(y, x):
    y //= TILESIZE
    x = (x - TOP_PANEL)//TILESIZE
    return (y, x)


BOARD_SIZE = {"beginner": (382, 288), "intermediate": (
    606, 512), "expert": (606, 960)}
TOP_PANEL = 94
TILESIZE = 32
PANEL_MID = int((TOP_PANEL-TILESIZE)/2)
POPUP_WIDTH = 8 * TILESIZE - 1
POPUP_HEIGHT = 7 * TILESIZE - 1
CONFIRM_WIDTH = 2*TILESIZE
CONFIRM_HEIGHT = int(5*TILESIZE/8)
COUNTER_WIDTH = 2*TILESIZE
COUNTER_HEIGHT = TILESIZE
COUNTER_TEXT_POS_Y = PANEL_MID + 3
MENU_BTN_WIDTH = int(1.5*TILESIZE)
MENU_BTN_HEIGHT = int(0.5*TILESIZE)
MENU_WIN_POS = int(TILESIZE/2)
MENU_WIN_WIDTH = 5*TILESIZE
MENU_WIN_HEIGHT = 2*TILESIZE
MENU_OPTION_HEIGHT = TILESIZE
MENU_DIFF_POS = int(TILESIZE/2)
MENU_SCORES_POS = int(3*TILESIZE/2)
TITLE = 'MINESWEEPER'
