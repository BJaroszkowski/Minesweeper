import config as c
from windows import Scores, Difficulties
from util import resource_path
import minesweeper
import pygame as pg
import sys
import pickle
import os


class Game:
    def __init__(self, level):
        self.level = level
        pg.init()
        self.height, self.width = c.BOARD_SIZE[self.level]
        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(c.TITLE)
        icon = pg.image.load(resource_path('icon.png'))
        pg.display.set_icon(icon)
        pg.font.init()
        self.fonts = {
            'grid_font': pg.font.Font(resource_path('FreeSansBold.ttf'), 20),
            'panel_font': pg.font.SysFont("lucidaconsole", 30),
            'menu_font':  pg.font.SysFont("dejavuserif", 10),
            'large_menu_font': pg.font.SysFont("dejavuserif", 20)
        }
        self.ms = minesweeper.Minesweeper(level=self.level)
        self.flag = pg.image.load(resource_path('flag.bmp'))
        self.tp_btn_pos = int((self.width-c.TILESIZE)/2)
        self.tp_bt_col = c.YELLOW
        self.timer_pos = int((self.width-5*c.TILESIZE)/4)
        self.mine_pos = int(3*(self.width-c.TILESIZE)/4)
        self.scores = Scores(self.height, self.width,
                             self.fonts, "HIGH SCORES")
        self.diff_choice = Difficulties(self.height, self.width, self.fonts,
                                        "SET DIFFICULTY", self.level)
        self.down = False
        self.show_scores = False
        self.show_diff_choice = False
        self.reset = False
        self.menu = False
        self.on = True

    def run(self):
        while True:
            self.events()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.down_b = event.button
                self.btn_down()
            if event.type == pg.MOUSEBUTTONUP:
                b = event.button
                if b == 1:
                    self.down = False
                # middle mouse button does nothing
                if b == 2:
                    continue
                y, x = pg.mouse.get_pos()
                # If popups are open serve them
                if self.show_scores:
                    self.serve_scores(y, x)
                    continue
                if self.show_diff_choice:
                    self.serve_diff_choice(y, x)
                    continue
                # restart the game by clicking the top button
                if (x in range(c.PANEL_MID, c.PANEL_MID+c.TILESIZE) and
                    y in range(self.tp_btn_pos, self.tp_btn_pos+c.TILESIZE) and
                        self.reset and b == 1):
                    self.restart(self.level)
                    continue
                # choose options from menu if it is open
                if self.menu:
                    self.serve_menu(y, x)
                    continue
                # at this point if menus are on or panel is clicked, do
                # nothing
                if x <= c.TOP_PANEL or not self.on:
                    continue
                # click on the board: reveal or set flag
                y, x = c.GET_TILE(y, x)
                if (y == self.down_tile_y and x == self.down_tile_x
                        and b == self.down_b):
                    if b == 1:
                        self.l_click(x, y)
                    if b == 3:
                        self.ms.flag_mine(x, y)

    def quit(self):
        with open('settings.p', 'wb') as f:
            pickle.dump({"level": self.level}, f)
        pg.quit()
        sys.exit()

    def btn_down(self):
        if self.down_b == 1:
            self.down = True
        self.down_y, self.down_x = pg.mouse.get_pos()
        if self.show_scores or self.show_diff_choice:
            return
        if (self.down_x in range(c.PANEL_MID,
                                 c.PANEL_MID+c.TILESIZE) and
                self.down_y in range(self.tp_btn_pos,
                                     self.tp_btn_pos+c.TILESIZE)):
            self.reset = True
        if c.MENU_BTN(self.down_y, self.down_x):
            self.menu = True
        self.down_tile_y, self.down_tile_x = c.GET_TILE(
            self.down_y, self.down_x)

    def serve_scores(self, y, x):
        if (self.scores.check_close(self.down_y, self.down_x) and
                self.scores.check_close(y, x)):
            self.show_scores = False
            self.on = True

    def serve_diff_choice(self, y, x):
        if (self.diff_choice.check_close(self.down_y, self.down_x)
                and self.diff_choice.check_close(y, x)):
            self.show_diff_choice = False
            self.on = True
            return
        if (self.diff_choice.confirm(self.down_y, self.down_x)
                and self.diff_choice.confirm(y, x)):
            if self.diff_choice.level == self.level:
                self.show_diff_choice = False
                self.on = True
                return
            else:
                self.restart(self.diff_choice.level)
        down_return = self.diff_choice.choose(
            self.down_y, self.down_x)
        up_return = self.diff_choice.choose(y, x)
        if up_return and up_return == down_return:
            self.diff_choice.level = up_return

    def serve_menu(self, y, x):
        if c.DIFF_CHOICE(y, x) and c.DIFF_CHOICE(self.down_y, self.down_x):
            self.menu = False
            self.on = False
            self.show_diff_choice = True
        if c.SCORES(y, x) and c.SCORES(self.down_y, self.down_x):
            self.menu = False
            self.on = False
            self.show_scores = True

    def restart(self, level):
        self.__init__(level)

    def _reset_scores(self):
        empty = {"beginner": "", "intermediate": "", "expert": ""}
        with open('scores.p', 'wb') as f:
            pickle.dump(empty, f)

    def l_click(self, x, y):
        ret = self.ms.click(x, y)
        if ret == "VICTORY":
            self.on = False
            self.tp_bt_col = c.GREEN
            self.update_high_scores()
        if ret == "GAME OVER":
            self.x_miss, self.y_miss = x, y
            self.on = False
            self.tp_bt_col = c.RED

    def update_high_scores(self):
        with open('scores.p', 'rb') as f:
            scores = pickle.load(f)
        score = int(self.ms.final_time)
        high_score = scores[self.level]
        if not high_score or high_score > score:
            scores[self.level] = score
            with open('scores.p', 'wb') as f:
                pickle.dump(scores, f)

    def draw(self):
        self.window.fill(c.BGCOLOR)
        self.draw_grid()
        self.draw_panel()
        self.draw_nums()
        if self.ms.final_time:
            self.draw_mines()
        if self.menu:
            self.draw_menu()
        if self.show_scores:
            self.scores.draw(self.window)
        if self.show_diff_choice:
            self.diff_choice.draw(self.window)
        pg.display.update()

    def draw_nums(self):
        for x in range(self.ms.height):
            for y in range(self.ms.width):
                val = str(self.ms._board[x][y])
                if val.isdigit():
                    text = self.fonts['grid_font'].render(
                        val, 1, c.NUM_COLS[val])
                    self.window.blit(text, c.TILE_MID(y, x))
                if val == 'F':
                    self.window.blit(self.flag, c.TILE_CORNER(y, x))

    def draw_mines(self):
        for x in range(self.ms.height):
            for y in range(self.ms.width):
                if self.ms._board[x][y] == 'X':
                    color = c.RED if x == self.x_miss \
                        and y == self.y_miss else c.BLACK
                    text = self.fonts['grid_font'].render('X', 1, color)
                    self.window.blit(text, c.TILE_MID(y, x))
                if self.ms._board[x][y] == 'W':
                    text = self.fonts['grid_font'].render('X', 1, c.GREEN)
                    self.window.blit(text, c.TILE_MID(y, x))

    def draw_grid(self):
        for x in range(0, self.width, c.TILESIZE):
            pg.draw.line(self.window, c.BLACK,
                         (x, c.TOP_PANEL), (x, self.height))

        for y in range(c.TOP_PANEL, self.height, c.TILESIZE):
            pg.draw.line(self.window, c.BLACK, (0, y), (self.width, y))

        y, x = pg.mouse.get_pos()
        if x <= c.TOP_PANEL or not self.on:
            return
        y, x = c.GET_TILE(y, x)
        coords = c.TILE_CORNER(y, x)
        if (self.down and y == self.down_tile_y and x == self.down_tile_x
                and self.ms._board[x][y] == '.'):
            pg.draw.rect(self.window, c.WHITE,
                         pg.Rect(coords[0], coords[1],
                                 c.TILESIZE-1, c.TILESIZE-1))

    def draw_panel(self):
        # Reset button
        pg.draw.rect(self.window, self.tp_bt_col, pg.Rect(
            self.tp_btn_pos, c.PANEL_MID, c.TILESIZE, c.TILESIZE))

        # Timer
        pg.draw.rect(self.window, c.BLACK, pg.Rect(
            self.timer_pos, c.PANEL_MID, c.COUNTER_WIDTH, c.COUNTER_HEIGHT))
        text = self.fonts['panel_font'].render(
            f'{self.ms.time_spent}', 1, c.RED)
        self.window.blit(text, (c.TIME_POS_X(text, self.width),
                                c.COUNTER_TEXT_POS_Y))
        # Mine counter
        pg.draw.rect(self.window, c.BLACK, pg.Rect(
            self.mine_pos, c.PANEL_MID, c.COUNTER_WIDTH, c.COUNTER_HEIGHT))
        text = self.fonts['panel_font'].render(
            f'{self.ms.mines_remaining}', 1, c.RED)
        self.window.blit(text, (c.MINES_POS_X(text, self.width),
                                c.COUNTER_TEXT_POS_Y))

        # Menu button
        pg.draw.rect(self.window, c.BLACK, pg.Rect(
            0, 0, c.MENU_BTN_WIDTH, c.MENU_BTN_HEIGHT), 1)
        text = self.fonts['menu_font'].render('MENU', 1, c.BLACK)
        self.window.blit(text, c.MENU_TEXT_POS(text))

    def draw_menu(self):
        x, y = pg.mouse.get_pos()
        if not (c.MENU_BTN(x, y) or c.DIFF_CHOICE(x, y) or c.SCORES(x, y)):
            self.menu = False
            return
        pg.draw.rect(self.window, c.WHITE, pg.Rect(
            0, c.MENU_WIN_POS, c.MENU_WIN_WIDTH, c.MENU_WIN_HEIGHT))
        if c.DIFF_CHOICE(x, y):
            pg.draw.rect(self.window, c.TEAL, pg.Rect(
                0, c.MENU_DIFF_POS, c.MENU_WIN_WIDTH, c.MENU_OPTION_HEIGHT))
        if c.SCORES(x, y):
            pg.draw.rect(self.window, c.TEAL, pg.Rect(
                0, c.MENU_SCORES_POS, c.MENU_WIN_WIDTH, c.MENU_OPTION_HEIGHT))
        pg.draw.line(self.window, c.BLACK,
                     (0, c.MENU_SCORES_POS),
                     (c.MENU_WIN_WIDTH, c.MENU_SCORES_POS))
        text1 = self.fonts['menu_font'].render(
            'CHOOSE DIFICULTY LEVEL', 1, c.BLACK)
        text2 = self.fonts['menu_font'].render(
            'SHOW HIGH SCORES', 1, c.BLACK)
        self.window.blit(text1, c.MENU_OPTION_TEXT_POS(text1, row=0))
        self.window.blit(text2, c.MENU_OPTION_TEXT_POS(text2, row=1))


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))

    if not os.path.exists('settings.p'):
        with open('settings.p', 'wb') as f:
            pickle.dump({"level": 'beginner'}, f)

    if not os.path.exists('scores.p'):
        with open('scores.p', 'wb') as f:
            pickle.dump({"beginner": "", "intermediate": "", "expert": ""}, f)

    with open('settings.p', 'rb') as f:
        settings = pickle.load(f)

    g = Game(settings["level"])
    g.run()
