EASY = 'E'
INTERMEDIATE = 'I'
HARD = 'H'
DIFFICULTIES = (EASY, INTERMEDIATE, HARD)

class Board:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.width = {EASY: 9, INTERMEDIATE: 15, HARD: 20}.get(difficulty)
        self.height = {EASY: 9, INTERMEDIATE: 9, HARD: 15}.get(difficulty)
        self.bombs = {EASY: 10, INTERMEDIATE: 20, HARD: 30}.get(difficulty)
        # self.grid = [[self.Square()]*self.width]*self.height
        self.grid = [[self.Square() for i in range(0, self.width)] for i in range(0, self.height)]

        # Set bombs
        # TODO

        # Set clues
        # TODO

    def play(self, col, row):
        # TODO Probably DFS to reveal region
        self.grid[row][col].reveal()

    def valid_row(self, row):
        try:
            return 0 < int(row) <= self.height
        finally:
            pass
        return False

    def valid_col(self, col):
        try:
            return 0 < int(col) <= self.width
        finally:
            pass
        return False

    def render(self):
        print("    ", end='')
        print(*[str(col).rjust(2, ' ') for col in range(1, self.width + 1)])
        print("   ╔", end='')
        print(*["═══"]*self.width, sep='')

        for i, row in enumerate(self.grid):
            print(str(i+1).rjust(2, ' '), '║ ', end='')
            print(*[square.value() for square in row], sep='  ')

    class Square:
        def __init__(self):
            self.revealed = False
            self.val = 0
            self.bomb = False

        def reveal(self):
            self.revealed = True
            if (self.bomb):
                # TODO Raise GameOver
                pass

        def make_bomb(self):
            self.bomb = True

        def value(self):
            if self.bomb:
                return "*"
            if self.val:
                return str(self.val)
            if self.revealed:
                return ' '
            return '?'
