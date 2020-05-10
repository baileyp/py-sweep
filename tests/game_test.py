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

        cols = set(range(0, spec.cols))
        rows = set(range(0, spec.rows))

        # Happy Path
        for col in cols:
            for row in rows:
                assert (col, row) in board

        # Out of Bounds ints
        assert (-1, 0) not in board
        assert (0, -1) not in board
        assert (spec.cols, 0) not in board
        assert (0, spec.rows) not in board

        # Full Rows and Cols
        for col in cols:
            assert (col, rows) in board
        for row in rows:
            assert (cols, row) in board
        assert (cols, rows) in board

        # Out of Bounds sets
        assert (cols | {-1}, 0) not in board
        assert (0, rows | {-1}) not in board
        assert (cols | {spec.cols}, 0) not in board
        assert (0, rows | {spec.rows}) not in board

    @pytest.mark.parametrize('command, expected', [
        ('4 7', (module.REVEAL, '4', '7')),
        ('r 4 7', (module.REVEAL, '4', '7')),
        ('f 3 1', (module.FLAG, '3', '1')),
    ])
    def test_parse_command(self, monkeypatch, command, expected):
        monkeypatch.setattr('pysweep.game.Board.parse_coord', lambda c: c)

        assert module.Board.parse_command(command) == expected

    def test_parse_command_quit_raises_exception(self):
        with pytest.raises(module.QuitGame):
            module.Board.parse_command(module.QUIT)

    def test_parse_command_too_many_values_raises_exception(self, monkeypatch):
        monkeypatch.setattr('pysweep.game.Board.parse_coord', lambda c: c)
        with pytest.raises(ValueError):
            assert module.Board.parse_command('r 1 2 3')

    @pytest.mark.parametrize('coord, expected', [
        ('1', {0}),
        ('4-7', {3, 4, 5, 6}),
        ('7-4', {3, 4, 5, 6}),
        ('8,12,1', {0, 7, 11}),
    ])
    def test_parse_coord(self, coord, expected):
        assert module.Board.parse_coord(coord) == expected

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
