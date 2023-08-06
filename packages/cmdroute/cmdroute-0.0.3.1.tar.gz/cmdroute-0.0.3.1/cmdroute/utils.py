import sys
import inspect
from .cmdroute import entrypoint, dispacth


def all(name):
    functions = inspect.getmembers(
        sys.modules[name], inspect.isfunction
    )
    for k, l in functions:
        if l.__name__ != "all":
            entrypoint()(l)

    dispacth()
