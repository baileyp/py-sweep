import pytest
from pysweep import console as module


class TestConsole:

    def test_read_happy_path(self, monkeypatch):
        user_input = "Input"
        prompt = "Prompt"

        monkeypatch.setattr('builtins.input', mock_input(prompt, user_input))
        assert user_input == module.read(prompt)

        monkeypatch.setattr('builtins.input', mock_input(prompt, f"\t{user_input}  "))
        assert user_input == module.read(prompt)

    def test_read_with_builtin_cast(self, monkeypatch):
        user_input = "7"
        prompt = "Prompt"
        monkeypatch.setattr('builtins.input', mock_input(prompt, user_input))
        assert int(user_input) == module.read("Prompt", int)

    def test_read_with_cast(self, monkeypatch):
        user_input = "Input"
        prompt = "Prompt"
        casted = "Casted"

        def cast(i):
            nonlocal casted, user_input
            assert i == user_input
            return casted

        monkeypatch.setattr('builtins.input', mock_input(prompt, user_input))
        assert casted == module.read(prompt, cast)

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
        user_input = "Input"
        failure = "Fail"
        responses = [False, True]
        cursor = -1

        def out(message):
            nonlocal failure
            assert failure == message

        def validator(*args):
            nonlocal cursor, user_input, responses
            cursor += 1
            assert args == tuple(user_input)
            return responses[cursor]

        monkeypatch.setattr(module, "out", out)

        module.read_until(lambda: user_input, validator, failure)

    def test_read_until_callable_failure(self):
        user_input = "Input"
        responses = [False, True]
        cursor = -1

        def failure():
            raise FunctionInvoked

        def validator(*args):
            nonlocal cursor, user_input, responses
            cursor += 1
            assert args == tuple(user_input)
            return responses[cursor]

        with pytest.raises(FunctionInvoked):
            module.read_until(lambda: user_input, validator, failure)

    def test_out(self, monkeypatch):
        message = "message"

        def mock_print(m):
            nonlocal message
            assert m == message
            raise FunctionInvoked

        monkeypatch.setattr("builtins.print", mock_print)

        with pytest.raises(FunctionInvoked):
            module.out(message, mock_print)


def mock_input(prompt, response):

    def mock(p):
        nonlocal prompt, response
        assert p == f"{prompt} "
        return response

    return mock


class FunctionInvoked(BaseException):
    pass
