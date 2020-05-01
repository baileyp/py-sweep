from random import choice, randint

import pytest
from unittest import mock
from pysweep import game as module
from pysweep.renderer import SnakeRenderer


@pytest.fixture
def square():
    mock_square = mock.Mock(spec=module.Board.Square)
    mock_square.is_flagged.return_value = False
    mock_square.has_threat.return_value = False
    mock_square.revealed.return_value = False
    mock_square.flag.return_value = True
    return mock_square


@pytest.fixture
def flagged_square(square):
    square.is_flagged.return_value = True
    square.flag.return_value = False
    return square


@pytest.fixture
def threat_square(square):
    square.has_threat.return_value = True
    return square


@pytest.fixture
def revealed_square(square):
    square.revealed.return_value = True
    return square


@pytest.fixture
def spec():
    mock_speck = mock.Mock(spec=module.Spec)
    mock_speck.cols = 10
    mock_speck.rows = 10
    mock_speck.threats = 10
    return mock_speck


@pytest.fixture
def renderer():
    return mock.Mock(spec=SnakeRenderer)


@pytest.fixture
def board(spec, renderer):
    board = Board(spec, renderer)

    return board


class TestGame:
    def test___contains__(self, spec, renderer):
        spec.rows = 4
        spec.cols = 7
        board = Board(spec, renderer)

        for col in range(0, spec.cols):
            for row in range(0, spec.rows):
                assert (col, row) in board

        assert (-1, 0) not in board
        assert (0, -1) not in board
        assert (spec.cols, 0) not in board
        assert (0, spec.rows) not in board

    def test_play_reveal_on_blank_square(self, board, square):
        board.set_square_at(0, 0, square)

        with mock.patch.object(board, '_dfs_visit') as mock_dfs_visit:
            board.play(module.REVEAL, 0, 0)
            mock_dfs_visit.assert_called_once()

    def test_play_reveal_on_flagged_square(self, board, flagged_square):
        board.set_square_at(1, 2, flagged_square)

        with pytest.raises(module.CannotReveal):
            board.play(module.REVEAL, 1, 2)

    def test_play_reveal_on_threat_square(self, board, threat_square):
        board.set_square_at(3, 4, threat_square)

        with mock.patch.object(board, '_reveal') as mock_reveal, \
                pytest.raises(module.ThreatFound):
            board.play(module.REVEAL, 3, 4)
            mock_reveal.assert_called_once()

    def test_play_flag_on_blank_square(self, board, square):
        board.set_square_at(0, 0, square)

        old_threat_count = board._threat_counter
        board.play(module.FLAG, 0, 0)
        assert board._threat_counter == old_threat_count - 1

    def test_play_flag_on_flagged_square(self, board, flagged_square):
        board.set_square_at(2, 1, flagged_square)

        old_threat_count = board._threat_counter
        board.play(module.FLAG, 2, 1)
        assert board._threat_counter == old_threat_count + 1

    def test_play_flag_on_revealed_square(self, board, revealed_square):
        board.set_square_at(5, 7, revealed_square)

        with pytest.raises(module.CannotFlag):
            board.play(module.FLAG, 5, 7)

    def test_render(self, monkeypatch, spec, renderer):
        board = Board(spec, renderer)
        with mock.patch.object(board, '_timer') as mock_timer:
            mock_timer.get_elapsed.return_value = 'time'

            board.render()

            renderer.render_board.assert_called_once_with(board._grid, board._threat_counter, 'time')

    def test_neighbors_of(self):
        col = choice(range(-10, 10))
        row = choice(range(-10, 10))
        expected = [
            (col - 1, row - 1),
            (col - 1, row),
            (col - 1, row + 1),
            (col, row - 1),
            (col, row + 1),
            (col + 1, row - 1),
            (col + 1, row),
            (col + 1, row + 1),
        ]
        assert list(module.Board.neighbors_of(col, row)) == expected


class Board(module.Board):
    """
    This is a special, "testable" version of the Board class
    """
    def set_square_at(self, col, row, square):
        self._grid[row][col] = square
