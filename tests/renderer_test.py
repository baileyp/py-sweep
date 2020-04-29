from copy import deepcopy
import pytest
from unittest import mock
from pysweep import renderer as module, game


@pytest.fixture
def mock_square():
    return mock.Mock(spec=game.Board.Square)


class TestSnakeRenderer:
    def test_render_board(self, mock_square):
        mock_square_2 = deepcopy(mock_square)
        mock_grid = [[mock_square], [mock_square_2]]
        renderer = module.SnakeRenderer()
        renderer.render_board(mock_grid, 0)
        mock_square.render.assert_called_once()
        mock_square_2.render.assert_called_once()

    @pytest.mark.parametrize('square_val, expected', [
        (module.Board.Square.DEFAULT, 'ψ'),
        (module.Board.Square.REVEALED, ' '),
        (module.Board.Square.THREAT, '೬'),
        (module.Board.Square.FLAG, '⚑'),
        ('1', '1')
    ])
    def test_render_square(self, square_val, expected, mock_square):
        renderer = module.SnakeRenderer()
        mock_square.render.return_value = square_val
        assert expected in renderer.render_square(mock_square)
        mock_square.render.assert_called_once()
