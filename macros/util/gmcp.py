import re
import json

from .. import client

import logging
__log__ = logging.getLogger(__name__)

_packages = {}
_subscriptions = {}

PACKAGE_ID = "[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)+"

_gmcp_message = re.compile("(?P<name>%s)(?P<value>.*)?" % PACKAGE_ID)


def _hook(arg):
    m = _gmcp_message.fullmatch(arg)
    if not m:
        __log__.error(arg)
        return
    receive(m.group('name'), json.loads(m.group('value')))


def receive(name, value):
    __log__.debug(name)
    __log__.debug(value)


#    m = re.fullmatch("(?P<package>.*)\.(?P<function>[^.]*)", name)
#    package = m.group("package")
#    assert package in _subscriptions, "Package not defined: %r" % package
#    for i in _subscriptions[package]:
#        i(package, m.group("function"), value)


def send(name, value):
    client.gmcp("%s %s" % (name, json.dumps(value)))


def ping():
    send("Core.Ping", 1)


#def dummy(p,f,v):
#  tf.out(str(p))
#  tf.out(str(f))
#  tf.out(str(v))


def init():
    #  reset()
    #  util.hook("GMCP",hook)
    client.evaluate(
        "/def -hGMCP gmcp-receive = /python_call %s._hook %%*" % __name__)
    add("MG.room")
    add("MG.char")
    add("comm.channel")


def add(package: str, version: int = 1):
    send("Core.Supports.Add", ["%s %d" % (package, version)])
    _packages[package] = version


def remove(package: str):
    assert package in _packages
    send("Core.Supports.Remove", ["%s %d" % (package, _packages[package])])
    _packages.remove(package)


def reset():
    send("Core.Supports.Set",
         ["%s %d" % (key, value) for key, value in _packages.items()])
