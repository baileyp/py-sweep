import pytest
from unittest import mock
from pysweep import console as module


class TestConsole:

    def test_read_happy_path(self, monkeypatch):
        user_input = "Input"
        prompt = "Prompt"

        with mock.patch('builtins.input', return_value=user_input) as patched_input:
            monkeypatch.setattr('builtins.input', patched_input)
            assert patched_input.called_once_with(f"{prompt} ")
            assert module.read(prompt) == user_input

        with mock.patch('builtins.input', return_value=f"\t{user_input}  ") as patched_input:
            monkeypatch.setattr('builtins.input', patched_input)
            assert patched_input.called_once_with(f"{prompt} ")
            assert module.read(prompt) == user_input

    def test_read_with_builtin_cast(self, monkeypatch):
        user_input = "7"
        prompt = "Prompt"

        with mock.patch('builtins.input', return_value=user_input) as patched_input:
            monkeypatch.setattr('builtins.input', patched_input)
            assert patched_input.called_once_with(f"{prompt} ")
            assert module.read(prompt, int) == int(user_input)

    def test_read_with_cast(self, monkeypatch):
        user_input = "Input"
        prompt = "Prompt"
        casted = "Casted"

        cast = mock.Mock(return_value=casted)

        with mock.patch('builtins.input', return_value=user_input) as patched_input:
            monkeypatch.setattr('builtins.input', patched_input)
            assert module.read(prompt, cast) == casted
            assert patched_input.called_once_with(f"{prompt} ")
            assert cast.called_once_with(user_input)

    def test_read_cast_throws_value_error(self, monkeypatch):
        with pytest.raises(ValueError):
            monkeypatch.setattr('builtins.input', lambda _: "7 7")
            assert module.read("Prompt", int) is None

    def test_read_custom_value_error_response(self, monkeypatch):
        custom_response = "Custom Return"
        monkeypatch.setattr('builtins.input', lambda _: "7 7")
        assert custom_response == module.read("Prompt", int, custom_response)

    def test_read_until_happy_path(self):
        assert "Input" == module.read_until(lambda: "Input", lambda *_: True, "Fail")

    def test_read_until_validator_fails(self, monkeypatch):
        user_input = ['First', 'Second']
        failure = "Fail"

        callback = mock.Mock(side_effect=user_input)
        out = mock.Mock(return_value=None)
        validator = mock.Mock(side_effect=[False, True])
        monkeypatch.setattr(module, "out", out)

        assert module.read_until(callback, validator, failure) == user_input[1]

        out.assert_called_once_with(failure)
        validator.assert_has_calls([mock.call(_) for _ in user_input])
        assert callback.call_count == 2

    def test_read_until_callable_failure(self):
        user_input = ['First', 'Second']

        callback = mock.Mock(side_effect=user_input)
        failure = mock.Mock(return_value=None)

        validator = mock.Mock(side_effect=[False, True])

        module.read_until(callback, validator, failure)
        validator.assert_has_calls([mock.call(_) for _ in user_input])
        assert failure.called_once()

    def test_out(self):
        message = "message"

        renderer = mock.Mock(return_value=None)
        module.out(message, renderer)

        renderer.assert_called_once_with(message)
