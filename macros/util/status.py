from .. import client
from .. import model

import re

import logging
__log__ = logging.getLogger(__name__)


def _config_status_static(line):
    reg = re.compile("(?P<padding>_*)(?P<string>[^_]*)")
    fields = []
    while line:
        test = reg.search(line)
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


class status_config(model.Command):
    @staticmethod
    def call(line):
        reg = re.compile("{(?P<variable>[^:}]+)(:(?P<length>[0-9]+))?}")
        fields = []
        while line:
            test = reg.search(line)
            if not test:
                break
            __log__.debug(test)
            prefix = line[:test.span()[0]]
            __log__.debug(prefix)
            fields.extend(_config_status_static(prefix))
            __log__.debug(test.group('variable'))
            __log__.debug(test.group('length'))
            if test.group('length'):
                fields.append(
                    "%s:%s" % (test.group('variable'), test.group('length')))
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


client.define(status_config)


class status_value(model.Command):
    @staticmethod
    def call(var):
        __log__.debug("Inside")
        value = client.get(var, None)
        if client.isvar("status_func_%s" % var):
            value = client.evaluate("/eval /test %%{status_func_%s}" % var)
        attribute = 'n'
        if client.isvar("status_attr_%s" % var):
            attribute = client.evaluate("/eval /test %%{status_attr_%s}" % var)
        client.evaluate("/echo -a%s %s" % (str(attribute), str(value)))


def tumbel(line):
    value = client.get("uhu")
    if value < 50:
        client.evaluate("/echo Cgreen")
    else:
        client.evaluate("/echo Cred")


client.define(status_value)
#/set status_attr_uhu=$(/python 'Cblue')
#/set status_func_uhu=1+4
#/set status_var_uhu=$(/status_value uhu)
