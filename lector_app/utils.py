"""
Various utilities
"""
import os


def mkdir(path):
    """
    Make a directory if it doesn't exist already
    :param: path of the directory to create
    :raises FileExistsError: if the specified path exists and is not a directory
    """
    if not os.path.exists(path):
        os.mkdir(path)
    elif not os.path.isdir(path):
        raise FileExistsError(path + " exists and is not a directory")


def pre_call_hook(hook: callable):
    def decorator(func: callable):
        def decorated(*args, **kwargs):
            hook(*args, **kwargs)
            return func(*args, **kwargs)

        decorated.__name__ = func.__name__
        return decorated

    return decorator


class HasHumanName:
    """Utilities for models which have a first_name and a last_name attribute"""
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
