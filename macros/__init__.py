import tf
import sys
import re

#from . import base

from . import client
from . import util
from . import model

import pprint


def wrapper(args):
    macro, arg = args.split(None, 1)
    pprint.pprint((macro, args))


if tf.getvar('TFHELP', 'unset') != 'unset':
    sys.stdout.output = tf.out
    sys.stderr.output = tf.err

tf.eval(
    "/def -hCONNECT h_connect_hook = /python_call %s.wrapper h_connect_hook \\%%*"
    % __name__)


class reload(model.Command):
    """ Test if the argument is a hook"""

    @staticmethod
    def parse(line, options=None):
        return []

    @staticmethod
    def call():
        regex = re.compile('^macros(\.|$)')
        modules = sys.modules.keys()
        for i in sorted(filter(regex.search, modules), reverse=True):
            client.evaluate("/python_load %s" % i)


client.define(reload)
