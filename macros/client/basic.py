import tf

import pprint


def eval(cmd: str):
    pprint.pprint(cmd)
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

_grabbed = []


def _grab(line):
    global _grabbed
    _grabbed.append(line.split('>', 1)[1].rsplit('<', 1)[0])


def grab(command):
    global _grabbed
    _grabbed = []
    macro = define(_grab, options={'i': True, 'q': True})
    fix = "<%s:%d>" % (_grab.__name__, macro)
    eval('/quote -S /%s %s`"%s"%s' % (_grab.__name__, fix, command, fix))
    undefine(macro)
    pprint.pprint(_grabbed)
    return list(_grabbed)


def debug(ghgh):
    pprint.pprint(_grabbed)
