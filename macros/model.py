import inspect

import pprint


class MetaCommand(type):
    def __call__(cls, *args, **kwargs):
        if len(inspect.stack()) < 2:
            cmd, *tmp = args[0].split(None, 1)
            line = tmp[0] if tmp else ''
            options = getattr(cls, 'OPTIONS', None)
            tmp = cls.parse(line, None)
            if isinstance(tmp, list):
                args = tmp
            elif isinstance(tmp, dict):
                kwargs = tmp
            elif isinstance(tmp, tuple):
                args, kwargs = tmp
        return cls.call(*args, **kwargs)


class Command(metaclass=MetaCommand):
    OPTIONS = None

    def parse(line, options=None):
        if options:
            return ([line], {'options': options})
        else:
            return [line]

    def call(*args, **kwargs):
        raise NotImplementedError
