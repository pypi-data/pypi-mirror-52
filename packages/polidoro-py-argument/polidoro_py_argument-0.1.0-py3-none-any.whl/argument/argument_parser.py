import argparse

from argument.argument import Argument


class ArgumentParser(argparse.ArgumentParser):
    """
    An argparse.ArgumentParser wrapper to create the arguments and run the methods
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('argument_default', argparse.SUPPRESS)

        super(ArgumentParser, self).__init__(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        for arg in Argument.arguments:
            self.add_argument(*arg.args, **arg.kwargs)

        namespace = super(ArgumentParser, self).parse_args(*args, **kwargs)
        namespace_dict = vars(namespace)
        method = namespace_dict.pop('method', None)
        if method is not None:
            method(**namespace_dict)
            exit(0)

        return namespace
