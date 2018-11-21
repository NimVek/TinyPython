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
def _grab (line):
  global _grabbed
  _grabbed.append(line.split('>',1)[1].rsplit('<',1)[0])

def grab( command):
  global _grabbed
  _grabbed = []
  macro = define(_grab, options = { 'i' : True, 'q': True })
  fix = "<%s:%d>" % (_grab.__name__, macro)
  eval('/quote -S /%s %s`"%s"%s' % ( _grab.__name__, fix, command, fix) )
  undefine(macro)
  pprint.pprint(_grabbed)
  return list(_grabbed)

import enum
class Process(object):
  class Type(enum.Enum):
   REPEAT = 'REPEAT'
   QUOTE = 'QUOTE'

  def __init__(self,values):
    self.pid = int(values['PID']
#    self.next = line[6:14]
#    self.type = Process.Type.REPEAT if line[15:16] == 'r' else Process.Type.QUOTE
#    pprint.pprint(self.type)

class RepeatProcess(Process):
  def __init__(self, values):
    super().__init__(values)
    self.count = -1 if values['COUNT'] == 'i' else int(values['COUNT'])

def ps(dummy):
  columns = { 0:5, 6:14, 15:16, 17: 18, 19:27, 28:36, 37:42, 43:None }
  ps = grab('/ps')
  keys = [ ps[0][i:columns[i]].strip() for i in sorted(columns.keys()) ]
  pprint.pprint(keys)
  for row in ps[1:]:
    values = [ row[i:columns[i]].strip() for i in sorted(columns.keys()) ]
    values = dict(zip(keys, values))
    pprint.pprint(values)
    r = Process(row)
    pprint.pprint(r)

def debug(ghgh):
  pprint.pprint(_grabbed)
