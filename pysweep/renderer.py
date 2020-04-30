from contextlib import redirect_stdout
from io import StringIO

from pysweep.colors import SnakeColors
from pysweep.game import Board


class SnakeRenderer:
    def __init__(self, with_chrome=True, colors=SnakeColors):
        self._with_chrome = with_chrome
        self._colors = colors

    def render_board(self, grid, counter, time=(0, 0, 0)):
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

            hours, minutes, seconds = [self._colors.TIMER + str(p).zfill(2) + self._colors.END for p in time]
            print(f"Snakes Remaining: {self._colors.THREAT_COUNTER}{counter}{self._colors.END}")
            print(f"Time Elapsed: {hours}:{minutes}:{seconds}")
        return buffer.getvalue()

    def render_square(self, square):
        val = square.render()
        if val == Board.Square.DEFAULT:
            return f'{self._colors.GRASS}ψ{self._colors.END}'
        if val == Board.Square.REVEALED:
            return ' '
        if val == Board.Square.THREAT:
            return f'{self._colors.THREAT}೬{self._colors.END}'
        if val == Board.Square.FLAG:
            return f'{self._colors.FLAG}⚑{self._colors.END}'
        return f"{self._colors.CLUE}{val}{self._colors.END}"
