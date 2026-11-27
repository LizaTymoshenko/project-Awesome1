from functools import wraps

COMMAND_ERROR_MESSAGE = "Something went wrong while processing the command."


def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError) as error:
            return str(error)
        except Exception:
            return COMMAND_ERROR_MESSAGE

    return wrapper
