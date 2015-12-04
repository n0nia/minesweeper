import random


class Game(object):
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[False for y in xrange(height)] for x in xrange(width)]
        self.exposed = [[False for y in xrange(height)] for x in xrange(width)]
        self.counts = [[0 for y in xrange(height)] for x in xrange(width)]

        self._place_mines()
        self._init_counts()

    def select(self, x, y):
        if self.exposed[x][y]:
            return None
        if self.board[x][y]:
            return Result(True)
        return Result(False, self._update_board(x, y))

    def get_state(self):
        state = [[None for y in xrange(self.height)] for x in xrange(self.width)]
        for x in xrange(self.width):
            for y in xrange(self.height):
                if self.exposed[x][y]:
                    state[x][y] = self.counts[x][y]
        return state

    def _place_mines(self):
        for i in xrange(self.num_mines):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.board[x][y] = True

    def _init_counts(self):
        """Calculates how many neighboring squares have minds for all squares"""
        for x in xrange(self.width):
            for y in xrange(self.height):
                for x_offset in [-1, 0, 1]:
                    for y_offset in [-1, 0, 1]:
                        if x_offset != 0 or y_offset != 0:
                            self.counts[x][y] += self._is_mine(x + x_offset, y + y_offset)

    def _is_mine(self, x, y):
        """Returns 1 if mine and 0 otherwise"""
        if x < 0 or x == self.width:
            return 0
        if y < 0 or y == self.height:
            return 0
        return int(self.board[x][y])

    def _update_board(self, x, y):
        """Finds all the squares to expose based on a selection"""
        self.exposed[x][y] = True
        if self.counts[x][y] != 0:
            return Result(False, [Position(x, y, self.counts[x][y])])

        # ToDo
        squares = []
        stack = [(x, y)]
        while stack.count() > 0:
            (x, y) = stack.pop()
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    if x_offset != 0 or y_offset != 0:
                        new_x = x + x_offset
                        new_y = y + y_offset
                        if self.counts[new_x][new_y] == 0:
                            stack.append((new_x, new_y))
        return squares


class Position(object):
    def __init__(self, x, y, neighbors):
        self.x = x
        self.y = y
        self.neighbors = neighbors


class Result(object):
    def __init__(self, explosion, new_squares=[]):
        self.explosion = explosion
        self.new_squares = new_squares
