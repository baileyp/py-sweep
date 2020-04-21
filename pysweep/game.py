from contextlib import redirect_stdout
from io import StringIO
from random import choice, randrange

EASY = 'E'
INTERMEDIATE = 'I'
HARD = 'H'
DIFFICULTIES = (EASY, INTERMEDIATE, HARD)


class Board:
    def __init__(self, difficulty):
        self._width = {EASY: 9, INTERMEDIATE: 15, HARD: 20}.get(difficulty)
        self._height = {EASY: 9, INTERMEDIATE: 9, HARD: 15}.get(difficulty)
        self._threat_counter = {EASY: 10, INTERMEDIATE: 20, HARD: 30}.get(difficulty)
        self._grid = [[self.Square() for i in range(0, self._width)] for i in range(0, self._height)]
        self._hidden_remaining = self._width * self._height - self._threat_counter

        threats = self._threat_counter
        while threats:
            while True:
                row = randrange(0, self._height)
                col = randrange(0, self._width)
                square = self._grid[row][col]
                if not square.has_threat():
                    break
            square.place_threat()
            self._set_clues_around(col, row)
            threats -= 1

    def _set_clues_around(self, col, row):
        null = self.NullSquare()
        self._fetch_square(col - 1, row - 1, null).next_to_threat()
        self._fetch_square(col - 1, row, null).next_to_threat()
        self._fetch_square(col - 1, row + 1, null).next_to_threat()
        self._fetch_square(col, row - 1, null).next_to_threat()
        self._fetch_square(col, row + 1, null).next_to_threat()
        self._fetch_square(col + 1, row - 1, null).next_to_threat()
        self._fetch_square(col + 1, row, null).next_to_threat()
        self._fetch_square(col + 1, row + 1, null).next_to_threat()

    def _fetch_square(self, col, row, default=None):
        if self.valid_row(row) and self.valid_col(col):
            return self._grid[row][col]
        return default

    def _dfs_visit(self, col, row):
        square = self._fetch_square(col, row)
        if not square or square.revealed():
            return

        square.reveal()
        self._hidden_remaining -= 1
        if square.is_empty():
            self._dfs_visit(col - 1, row - 1)
            self._dfs_visit(col - 1, row)
            self._dfs_visit(col - 1, row + 1)
            self._dfs_visit(col, row - 1)
            self._dfs_visit(col, row + 1)
            self._dfs_visit(col + 1, row - 1)
            self._dfs_visit(col + 1, row)
            self._dfs_visit(col + 1, row + 1)

    def play(self, col, row):
        try:
            self._dfs_visit(col, row)
            self._grid[row][col].play()
            if self._hidden_remaining == 0:
                raise Victory

        except ThreatFound as e:
            self.__reveal()
            raise e

    def valid_row(self, row):
        return 0 <= row < self._height

    def valid_col(self, col):
        return 0 <= col < self._width

    def __reveal(self):
        for row in self._grid:
            for square in row:
                square.reveal()

    def __str__(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            print("    ", end='')
            print(*[str(col).rjust(2, ' ') for col in range(1, self._width + 1)])
            print("   ╔", end='')
            print(*["═══"] * self._width, sep='')

            for i, row in enumerate(self._grid):
                print(str(i + 1).rjust(2, ' '), '║ ', end='')
                print(*[str(square) for square in row], sep='  ')
        return buffer.getvalue()

    class Square:
        def __init__(self):
            self._revealed = False
            self._clue = 0
            self._threat = False

        def play(self):
            if self._threat:
                raise ThreatFound
                pass
            self.reveal()

        def reveal(self):
            self._revealed = True

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

        def __str__(self):
            if self._revealed:
                if self._threat:
                    return choice(['ϧ', 'Ҩ', 'Ƨ'])
                if self._clue:
                    return str(self._clue)
                return ' '
            return 'ψ'

    class NullSquare(Square):
        def next_to_threat(self):
            pass


class ThreatFound(Exception):
    pass


class Victory(Exception):
    pass