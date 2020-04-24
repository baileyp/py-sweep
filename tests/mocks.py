def mock_input(prompt, response):

    def mock(p):
        nonlocal prompt, response
        assert p == f"{prompt} "
        return response

    return mock
