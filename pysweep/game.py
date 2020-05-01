from random import randrange, choice

from pysweep.timer import Timer

FLAG = 'F'
REVEAL = 'R'
QUIT = 'Q'
ACTIONS = (FLAG, REVEAL)

class Board:
    def __init__(self, spec, renderer):
        self._width = spec.cols
        self._height = spec.rows
        self._threat_counter = spec.threats
        self._grid = [[self.Square() for _ in range(0, self._width)] for _ in range(0, self._height)]
        self._hidden_remaining = self._width * self._height - self._threat_counter
        self._renderer = renderer
        self._timer = Timer()
        self._timer.start()

        threats = self._threat_counter
        while threats:
            while True:
                row = randrange(0, self._height)
                col = randrange(0, self._width)
                square = self._fetch_square(col, row)
                if not square.has_threat():
                    break
            square.place_threat()
            self._set_clues_around(col, row)
            threats -= 1

    def __iter__(self):
        for row in self._grid:
            for square in row:
                yield square

    def __contains__(self, item):
        col, row = item
        return 0 <= row < self._height and 0 <= col < self._width

    def _set_clues_around(self, col, row):
        null = self.NullSquare()
        for col, row in self.neighbors_of(col, row):
            self._fetch_square(col, row, null).next_to_threat()

    def _fetch_square(self, col, row, default=None):
        if (col, row) in self:
            return self._grid[row][col]
        return default

    def _dfs_visit(self, col, row):
        square = self._fetch_square(col, row)
        if not square or square.revealed():
            return

        square.reveal()
        self._hidden_remaining -= 1
        if square.is_empty():
            if square.is_flagged():
                square.flag()
                self._threat_counter += 1
            for col, row in self.neighbors_of(col, row):
                self._dfs_visit(col, row)

    @staticmethod
    def neighbors_of(col, row):
        for n_col in range(col - 1, col + 2):
            for n_row in range(row - 1, row + 2):
                if col != n_col or row != n_row:
                    yield n_col, n_row

    def _reveal(self):
        for square in self:
            square.reveal()

    def play(self, action, col, row):
        square = self._fetch_square(col, row)
        if action == FLAG:
            if square.revealed():
                raise CannotFlag
            if square.flag():
                self._threat_counter -= 1
            else:
                self._threat_counter += 1
            return
        try:
            if square.is_flagged():
                raise CannotReveal
            if square.has_threat():
                raise ThreatFound
            self._dfs_visit(col, row)
            if self._hidden_remaining == 0:
                raise Victory

        except (ThreatFound, Victory) as e:
            self._reveal()
            raise e

    def render(self):
        return self._renderer.render_board(self._grid, self._threat_counter, self._timer.get_elapsed())

    class Square:
        DEFAULT = 'd'
        FLAG = 'f'
        THREAT = 't'
        REVEALED = 'r'

        def __init__(self):
            self._revealed = False
            self._flagged = False
            self._clue = 0
            self._threat = False

        def reveal(self):
            self._revealed = True

        def flag(self):
            self._flagged = not self._flagged
            return self._flagged

        def is_flagged(self):
            return self._flagged

        def revealed(self):
            return self._revealed

        def place_threat(self):
            self._threat = True

        def has_threat(self):
            return self._threat

        def next_to_threat(self):
            self._clue += 1

        def is_empty(self):
            return not self.has_threat() and self._clue == 0

        def render(self):
            if self._flagged:
                return self.FLAG
            if self._revealed:
                if self._threat:
                    return self.THREAT
                if self._clue:
                    return str(self._clue)
                return self.REVEALED
            return self.DEFAULT

    class NullSquare(Square):
        def next_to_threat(self):
            pass


class Spec:
    MINI = 'M'
    EASY = 'E'
    INTERMEDIATE = 'I'
    HARD = 'H'
    DIFFICULTIES = (MINI, EASY, INTERMEDIATE, HARD)

    def __init__(self, difficulty):
        if not self.valid(difficulty):
            raise ValueError("Invalid difficulty")

        self.cols = {
            self.MINI: 3,
            self.EASY: choice(range(8, 11)),
            self.INTERMEDIATE: choice(range(15, 17)),
            self.HARD: 30
        }.get(difficulty)

        self.rows = {
            self.MINI: 3,
            self.EASY: self.cols,
            self.INTERMEDIATE: choice(range(13, 17)),
            self.HARD: 16
        }.get(difficulty)

        self.threats = {self.MINI: 1, self.EASY: 10, self.INTERMEDIATE: 40, self.HARD: 99}.get(difficulty)

    @staticmethod
    def valid(difficulty):
        return difficulty in Spec.DIFFICULTIES


class ThreatFound(Exception):
    pass


class CannotReveal(Exception):
    pass


class CannotFlag(Exception):
    pass


class QuitGame(Exception):
    pass


class Victory(Exception):
    pass
