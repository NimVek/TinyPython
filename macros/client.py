import tf

import pprint


def eval(cmd: str):
    return tf.eval(
        cmd.replace('%', '%%').replace('\\', '\\\\').replace('$', '$$'))


def test(expression: str):
    return eval("/test %s" % expression)


def define(name, body=None, options=None):
    if not isinstance(name, str):
        body = name
        name = name.__name__
    if not isinstance(body, str):
        body = "/python_call %s.%s %%{*}" % (body.__module__, body.__name__)
    return eval(' '.join(['/def', name, '=', body]))


def undefine(what):
    if isinstance(what, int):
        return eval('/undefn %d' % what)
    else:
        return eval('/undef %s' % what)


undef = undefine
