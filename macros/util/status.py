from .. import client

import re

import logging
__log__ = logging.getLogger(__name__)


def _config_status_static(line):
    reg = re.compile("(?P<padding>_*)(?P<string>[^_]*)")
    fields = []
    while line:
      test=reg.search(line)
      if not test:
        break
      if test.group('padding'):
        fields.append(":%d" % len(test.group('padding')))
      if test.group('string'):
        fields.append('"%s"' % test.group('string'))
      line = line[test.span()[1]:]
      __log__.debug(line)
    __log__.debug(fields)
    return fields

def config_status(line):
    line = line[14:]
    reg = re.compile("{(?P<variable>[^:}]+)(:(?P<length>[0-9]+))?}")
    fields = []
    while line:
      test=reg.search(line)
      if not test:
        break
      __log__.debug(test)
      prefix = line[:test.span()[0]]
      __log__.debug(prefix)
      fields.extend(_config_status_static(prefix))
      __log__.debug(test.group('variable'))
      __log__.debug(test.group('length'))
      if test.group('length'):
        fields.append("%s:%s" % (test.group('variable'), test.group('length')))
      else:
        fields.append(test.group('variable'))
      line = line[test.span()[1]:]
      __log__.debug(line)
    fields.extend(_config_status_static(line))
    client.evaluate("/status_add -A -c %s" % fields[0])
    for i in fields[1:]:
      __log__.debug(i)
      r = client.evaluate("/status_add -A -s0 %s" % i)
      __log__.debug(r)
    __log__.debug(fields)


client.define(config_status)