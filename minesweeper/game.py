from contextlib import redirect_stdout
from io import StringIO
from random import randrange

EASY = 'E'
INTERMEDIATE = 'I'
HARD = 'H'
DIFFICULTIES = (EASY, INTERMEDIATE, HARD)


class Board:
    def __init__(self, difficulty):
        self._width = {EASY: 9, INTERMEDIATE: 15, HARD: 20}.get(difficulty)
        self._height = {EASY: 9, INTERMEDIATE: 9, HARD: 15}.get(difficulty)
        self._grid = [[self.Square() for i in range(0, self._width)] for i in range(0, self._height)]

        # Set bombs
        bombs = {EASY: 10, INTERMEDIATE: 20, HARD: 30}.get(difficulty)
        while bombs:
            while True:
                row = randrange(0, self._height)
                col = randrange(0, self._width)
                square = self._grid[row][col]
                if not square.has_bomb():
                    break
            square.plant_bomb()
            self._set_clues_around(col, row)
            bombs -= 1

    def _set_clues_around(self, col, row):
        null = self.NullSquare()
        self._fetch_square(col - 1, row - 1, null).next_to_bomb()
        self._fetch_square(col - 1, row, null).next_to_bomb()
        self._fetch_square(col - 1, row + 1, null).next_to_bomb()
        self._fetch_square(col, row - 1, null).next_to_bomb()
        self._fetch_square(col, row + 1, null).next_to_bomb()
        self._fetch_square(col + 1, row - 1, null).next_to_bomb()
        self._fetch_square(col + 1, row, null).next_to_bomb()
        self._fetch_square(col + 1, row + 1, null).next_to_bomb()

    def _fetch_square(self, col, row, default=None):
        if self.valid_row(row) and self.valid_col(col):
            return self._grid[row][col]
        return default

    def play(self, col, row):
        # TODO Probably DFS to reveal region
        try:
            self._grid[row][col].play()
        except BombFound as e:
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
            self._bomb = False

        def play(self):
            if (self._bomb):
                raise BombFound
                pass
            self.reveal()

        def reveal(self, ignore_bombs=False):
            self._revealed = True

        def plant_bomb(self):
            self._bomb = True

        def has_bomb(self):
            return self._bomb

        def next_to_bomb(self):
            self._clue += 1

        def __str__(self):
            if self._revealed:
                if self._clue:
                    return str(self._clue)
                if self._bomb:
                    return '*'
                return ' '
            return '?'

    class NullSquare(Square):
        def next_to_bomb(self):
            pass

class BombFound(Exception):
    pass