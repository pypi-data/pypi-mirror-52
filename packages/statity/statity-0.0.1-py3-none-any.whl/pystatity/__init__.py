from functools import wraps
import inspect


class WrongParametersType(Exception):
    def __init__(self, parameter, expected_type: type, given_type: type):
        message = f"Expected type of parameter '{parameter}' is {expected_type}, but {given_type} given."
        Exception.__init__(self, message)


class WrongReturnedDataType(Exception):
    def __init__(self, expected_type: type, given_type: type):
        message = f"Expected type of returned data is {expected_type}, but {given_type} given."
        Exception.__init__(self, message)


def strict_types(func):
    """
    Decorator that check annotated types for accordance with actual params
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_args = inspect.getcallargs(func, *args, **kwargs)
        for arg, val in current_args.items():
            expected_arg_type = func.__annotations__[arg]
            if not isinstance(val, expected_arg_type):
                raise WrongParametersType(arg, expected_arg_type, type(val))
        result = func(*args, **kwargs)
        expected_result_type = func.__annotations__.get('return') or type(None)
        if not isinstance(result, expected_result_type):
            raise WrongReturnedDataType(expected_result_type, type(result))
        return result
    return wrapper
