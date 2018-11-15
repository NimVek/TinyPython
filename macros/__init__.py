import tf
import sys

import pprint


def wrapper(args):
    macro, arg = args.split(None, 1)
    pprint.pprint((macro, args))


#sys.stdout.output = tf.out
#sys.stderr.output = tf.err

tf.eval(
    "/def -hCONNECT h_connect_hook = /python_call %s.wrapper h_connect_hook \\%%*"
    % __name__)
