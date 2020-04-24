import pytest
from pysweep import game as module
from tests.stubs import FunctionInvoked, Square


class TestGame:
    def test_play_reveal_on_blank_square(self):
        board, square = make_board(module.EASY)

        def reveal():
            raise FunctionInvoked
        square.reveal = reveal

        with pytest.raises(FunctionInvoked):
            board.play(module.REVEAL, 0, 0)

    def test_play_reveal_on_flagged_square(self):
        board, square = make_board(module.EASY, f=True)

        with pytest.raises(module.CannotReveal):
            board.play(module.REVEAL, 0, 0)

    def test_play_reveal_on_threat_square(self):
        board, square = make_board(module.EASY, t=True)

        with pytest.raises(module.ThreatFound):
            board.play(module.REVEAL, 0, 0)

    def test_play_flag_on_blank_square(self):
        board, square = make_board(module.EASY)

        old_threat_count = board._threat_counter
        board.play(module.FLAG, 0, 0)
        assert board._threat_counter == old_threat_count - 1

    def test_play_flag_on_flagged_square(self):
        board, square = make_board(module.EASY, f=True)

        old_threat_count = board._threat_counter
        board.play(module.FLAG, 0, 0)
        assert board._threat_counter == old_threat_count + 1

    def test_play_flag_on_revealed_square(self):
        board, square = make_board(module.EASY, r=True)

        with pytest.raises(module.CannotFlag):
            board.play(module.FLAG, 0, 0)

    def test_valid_row(self):
        board = module.Board(module.INTERMEDIATE)
        for row in range(0, board._height):
            assert board.valid_row(row)

        for col in range(0, board._width):
            assert board.valid_col(col)

        assert not board.valid_row(-1)
        assert not board.valid_col(-1)
        assert not board.valid_row(board._height)
        assert not board.valid_col(board._width)


def make_board(difficulty, row=0, col=0, **kwargs):
    board = module.Board(difficulty)

    square_to_play = Square(**kwargs)
    board._grid[row][col] = square_to_play

    return board, square_to_play
