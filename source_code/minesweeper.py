# from pprint import pprint
import random
import time


class Minesweeper:

    params = {'beginner': (9, 9, 10), 'intermediate': (
        16, 16, 40), 'expert': (16, 30, 99)}

    def __init__(self, level='beginner'):
        self.height, self.width, self.mines = self.params[level]
        self._board = [['.'] * self.width for _ in range(self.height)]
        self.start_time = False
        self.final_time = False

    @property
    def mines_remaining(self):
        s = self.mines - sum(1 for row in self._board
                             for x in row if x in ('F', 'W'))
        return s if s >= 0 else 0

    @property
    def time_spent(self):
        if not self.start_time:
            return 0
        if self.final_time:
            return int(self.final_time)
        cur_time = int(time.perf_counter() - self.start_time)
        return cur_time if cur_time < 1000 else 999

    def create_board(self, x_init, y_init):
        board = [[0]*self.width for _ in range(self.height)]
        placed = 0
        while placed < self.mines:
            x, y = random.randrange(self.height), random.randrange(self.width)
            if ((x in range(x_init-1, x_init+2)
                    and y in range(y_init-1, y_init+2)) or
                    board[x][y] == 'X'):
                continue
            board[x][y] = 'X'
            for i, j in zip((-1, -1, 0, 1, 1, 1, 0, -1),
                            (0, 1, 1, 1, 0, -1, -1, -1)):
                if (x+i not in range(self.height) or
                        y+j not in range(self.width) or
                        board[x+i][y+j] == 'X' or
                        (x+i == x_init and y+j == y_init)):
                    continue
                board[x+i][y+j] += 1
            placed += 1
        return board

    def click(self, x, y):
        if self._board[x][y] != '.':
            return
        if not self.start_time:
            self.start_time = time.perf_counter()
            self.hidden_board = self.create_board(x, y)
            self.started = True
        clicked = self.hidden_board[x][y]
        if clicked == 'X':
            self.final_time = time.perf_counter() - self.start_time
            self.terminate()
            return "GAME OVER"
        elif clicked == 0:
            self.uncover_chunk(x, y)
        else:
            self._board[x][y] = self.hidden_board[x][y]
        uncovered = sum(
            1 for row in self._board for el in row if el not in ['.', 'F'])

        if uncovered == self.height*self.width-self.mines:
            self.final_time = time.perf_counter() - self.start_time
            return "VICTORY"

        # pprint([''.join([str(self._board[x][y]) for y in range(self.width)])
        #         for x in range(self.height)], width=self.width, compact=True)

    def flag_mine(self, x, y):
        if self._board[x][y] not in ('.', 'F'):
            return
        if self._board[x][y] == 'F':
            self._board[x][y] = '.'
        else:
            self._board[x][y] = 'F'

    def terminate(self):
        board = [[] for _ in range(self.height)]
        for x in range(self.height):
            for y in range(self.width):
                if self._board[x][y] == 'F' and self.hidden_board[x][y] != 'X':
                    board[x].append('W')
                elif self.hidden_board[x][y] == 'X' and \
                        self._board[x][y] != 'F':
                    board[x].append('X')
                else:
                    board[x].append(self._board[x][y])
        self._board = board

    def uncover_chunk(self, x_init, y_init):
        self._board[x_init][y_init] = 0
        stack = [(x_init, y_init)]
        visited = {(x_init, y_init)}
        while stack:
            x, y = stack.pop()
            for i, j in zip((-1, -1, 0, 1, 1, 1, 0, -1),
                            (0, 1, 1, 1, 0, -1, -1, -1)):
                if ((x+i, y+j) in visited or
                    x+i not in range(self.height) or
                    y+j not in range(self.width) or
                    self.hidden_board[x+i][y+j] == 'X' or
                        self._board[x+i][y+j] == 'F'):
                    continue
                if self.hidden_board[x+i][y+j] == 0:
                    stack.append((x+i, y+j))
                self._board[x+i][y+j] = self.hidden_board[x+i][y+j]
            visited.add((x, y))
