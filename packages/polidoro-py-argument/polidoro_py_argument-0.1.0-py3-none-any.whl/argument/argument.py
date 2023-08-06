import inspect

from argument.custom_action import CustomAction


class Argument(object):
    """
    Decorator to create a command line argument
    """
    arguments = []

    def __init__(self, method, **kwargs):
        self.method = method

        self.args = tuple(['--' + method.__name__])

        self.kwargs = kwargs
        self.kwargs['action'] = CustomAction
        self.kwargs['method'] = method
        self.kwargs.setdefault('nargs', len(inspect.signature(method).parameters))

        self.arguments.append(self)

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)
