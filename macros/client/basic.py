import tf

import pprint

def evaluate(cmd: str):
    return tf.eval(
        cmd.replace('%', '%%').replace('\\', '\\\\').replace('$', '$$'))


def command(cmd: str, options={}, *args):
    result = ['/%s' % cmd]
    if not isinstance(options,dict):
      args = [ options, *args ]
      options = {}
    if options:
        for key, value in sorted(options.items()):
            if key != '-':
                key = '-%c' % key
            if isinstance(value, bool):
                if value:
                    result.append(key)
            elif isinstance(value, int):
                result.append('%s%s' % (key, value))
            elif isinstance(value, datetime.timedelta):
                result.append('%s%f' % (key, value.total_seconds()))
            else:
                result.append('%s"%s"' % (key, str(value).replace(
                    "\\", "\\\\").replace("\"", "\\\"")))
        result.append('--')
    if args:
      result.extend(args)
    return evaluate(' '.join([str(x) for x in result]))

cmd = command


def test(expression: str):
    return evaluate("/test %s" % expression)


def define(name, body=None, options=None):
    if not isinstance(name, str):
        body = name
        name = name.__name__
    if not isinstance(body, str):
        body = "/python_call %s.%s %%{0} %%{*}" % (body.__module__,
                                                   body.__name__)
    return evaluate(' '.join(['/def', name, '=', body]))


def undefine(what):
    if isinstance(what, int):
        return command('undefn', what)
    else:
        return command('undef', what)


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
    evaluate('/quote -S /%s %s`"%s"%s' % (_grab.__name__, fix, command, fix))
    undefine(macro)
    pprint.pprint(_grabbed)
    return list(_grabbed)


def debug(ghgh):
    pprint.pprint(_grabbed)


def get(name: str, convert=None, default=None):
    result = tf.getvar(name)
    if result and convert:
        try:
            result = convert(result)
        except TypeError:
            result = None
    return result


def set(name, value):
    return command('set','%s=%s' % (name, str(value)))
