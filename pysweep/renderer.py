from contextlib import redirect_stdout
from io import StringIO
from pysweep.game import Board


class SnakeRenderer:
    def __init__(self, with_chrome=True):
        self._with_chrome = with_chrome

    def render_board(self, grid, counter):
        width = len(grid[0])
        buffer = StringIO()
        with redirect_stdout(buffer):
            cols = ["     "] + [str(col).rjust(2, ' ') for col in range(1, width + 1)]
            horiz_border = "═══" * width

            if self._with_chrome:
                print(*cols)
                print("    ╔═", horiz_border, "═╗", sep='')

            for i, row in enumerate(grid):
                line = [self.render_square(square) for square in row]
                if self._with_chrome:
                    line.insert(0, '║')
                    line.insert(0, str(i + 1).rjust(2, ' '))
                    line.append('║')
                    line.append(str(i + 1).ljust(2, ' '))
                print(*line, sep='  ')

            if self._with_chrome:
                print("    ╚═", horiz_border, "═╝", sep='')
                print(*cols)

            print("Snakes Remaining:", counter, sep="\t")
        return buffer.getvalue()

    @staticmethod
    def render_square(square):
        val = square.render()
        if val == Board.Square.DEFAULT:
            return 'ψ'
        if val == Board.Square.REVEALED:
            return ' '
        if val == Board.Square.THREAT:
            return '೬'
        if val == Board.Square.FLAG:
            return '⚑'
        return val
