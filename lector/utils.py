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
