def read(prompt, cast=str, on_value_error=None):
    try:
        return cast(input(str(prompt).strip() + ' ').strip())
    except ValueError as e:
        if on_value_error is not None:
            return on_value_error
        raise e


def read_until(callback, validator, failure):
    while True:
        user_input = callback()
        if validator(user_input):
            break
        if callable(failure):
            failure()
        else:
            out(failure)
    return user_input


def out(message, renderer=print, **kwargs):
    renderer(message)
