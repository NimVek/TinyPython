#!/usr/bin/env python3

from .basic import test

import logging
__log__ = logging.getLogger(__name__)


class Function(object):
    def __init__(self, fname, args=[], args_min=0):
        assert isinstance(fname, str)
        assert args_min in range(len(args) + 1)
        self.fname = fname
        self.args = args
        self.args_min = args_min

    def __convert(self, item):
        if isinstance(item, str):
            return '"' + item.replace('\\', '\\\\').replace('"', '\\"') + '"'
        else:
            return str(item)

    def __call__(self, *args):
        __log__.debug(self.fname)
        __log__.debug(args)
        if len(args) > len(self.args) or len(args) < self.args_min:
            if len(self.args) == self.args_min:
                raise TypeError("%s() takes %d arguments but %d were given" %
                                (self.fname, len(self.args), len(args)))
            else:
                raise TypeError(
                    "%s() takes from %d to %d arguments but %d were given" %
                    (self.fname, self.args_min, len(self.args), len(args)))
        call = "%s(%s)" % (self.fname, ','.join(
            [self.__convert(arg) for arg in args]))
        __log__.debug(call)

        result = test(call)
        __log__.debug(result)

        return result


kbhead = Function("kbhead")
kbwordleft = Function("kbwordleft", [int])
kbwordright = Function("kbwordright", [int])
gmcp = Function("gmcp", [str, str], 1)
