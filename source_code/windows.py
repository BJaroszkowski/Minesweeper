import config as c
import pygame as pg
import pickle


class Popup:
    def __init__(self, window_height, window_width, fonts, title):
        self.window_width = window_width
        self.window_height = window_height
        self.fonts = fonts
        self.title = title
        self.win_x = int((self.window_width-c.POPUP_WIDTH)/2+1)
        self.row_x = int((self.window_width-c.POPUP_WIDTH)/2+c.TILESIZE)
        self.top_y = int((self.window_height-c.POPUP_HEIGHT)/2)

    def draw(self, window):
        # Draw main window
        pg.draw.rect(window, c.BGCOLOR, pg.Rect(
            self.win_x,
            self.top_y,
            c.POPUP_WIDTH,
            c.POPUP_HEIGHT))

        pg.draw.rect(window, c.BLACK, pg.Rect(
            self.win_x,
            self.top_y,
            c.POPUP_WIDTH+1,
            c.POPUP_HEIGHT+1),
            3)

        # Draw close button
        self.close = self.fonts['large_menu_font'].render('X', 1, c.BLACK)
        self.close_y = int((self.window_height-c.POPUP_HEIGHT)/2 + 4)
        self.close_x = int(
            (self.window_width+c.POPUP_WIDTH)/2-self.close.get_width() - 5)
        window.blit(self.close, (self.close_x, self.close_y))

        # Print out title
        text = self.fonts['large_menu_font'].render(self.title, 1, c.BLACK)
        window.blit(text,
                    ((self.window_width - text.get_width())/2,
                     self.close_y))

    def check_close(self, x, y):
        return (x in range(self.close_x - 5,
                           self.close_x+self.close.get_width()+5) and
                y in range(self.close_y-5,
                           self.close_y+self.close.get_height()+5))


class Scores(Popup):
    def draw(self, window):
        super().draw(window)
        with open('scores.p', 'rb') as f:
            scores = pickle.load(f)
        self.scores = [f'{level.title()}: ' + (f'{score}' if score else '-')
                       for level, score in scores.items()]
        # Print out scores
        for row, score in enumerate(self.scores):
            text = self.fonts['large_menu_font'].render(score, 1, c.BLACK)
            window.blit(text, (self.row_x,
                               self.top_y + (2+row)*c.TILESIZE))


class Difficulties(Popup):
    def __init__(self, window_height, window_width, fonts, title, level):
        super().__init__(window_height, window_width, fonts, title)
        self.level = level
        self.confirm_y = int(
            (self.window_height+c.POPUP_HEIGHT)/2 - c.TILESIZE)
        self.confirm_x = int((self.window_width - 2*c.TILESIZE)/2)
        self.rowend_x = int((self.window_width+c.POPUP_WIDTH)/2)

    def draw(self, window):
        super().draw(window)
        for row, lev in enumerate(['beginner', 'intermediate', 'expert']):
            text = self.fonts['large_menu_font'].render(
                lev.capitalize(), 1, c.BLACK)
            window.blit(text, (self.row_x+10,
                               self.top_y + (2+row)*c.TILESIZE))
            circle_y = self.top_y + \
                (2+row)*c.TILESIZE + int(text.get_height()/2)
            pg.draw.circle(window, c.WHITE, (self.row_x, circle_y), 5)
            if lev == self.level:
                pg.draw.circle(window, c.BLACK, (self.row_x, circle_y), 4)

        pg.draw.rect(window, c.BLACK, pg.Rect(
                     self.confirm_x,
                     self.confirm_y,
                     c.CONFIRM_WIDTH,
                     c.CONFIRM_HEIGHT), 2)

        text = self.fonts['menu_font'].render('CONFIRM', 1, c.BLACK)
        window.blit(text, ((self.window_width - text.get_width())/2,
                           c.CONFIRM_TEXT_POS(self.confirm_y, text)))

    def choose(self, x, y):
        for row, lev in enumerate(['beginner', 'intermediate', 'expert']):
            row_y = self.top_y + (2+row)*c.TILESIZE
            if (x in range(self.row_x-10, self.rowend_x) and
                    y in range(row_y, row_y + c.TILESIZE)):
                return lev

    def confirm(self, x, y):
        return (x in range(self.confirm_x, self.confirm_x+c.CONFIRM_WIDTH) and
                y in range(self.confirm_y, self.confirm_y+c.CONFIRM_HEIGHT))
