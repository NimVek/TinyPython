from .. import client
from .. import model

import pprint


def _hook_id(hook):
    return "hook_" + hook


class is_hook(model.Command):
    """ Test if the argument is a hook"""

    @staticmethod
    def call(name):
        return client.test('ismacro("%s")' % _hook_id(name))


class remove_hook(model.Command):
    """ Test if the argument is a hook"""

    @staticmethod
    def call(name):
        if is_hook(name):
            client.undefine(_hook_id(hook))
        return True


class __HookModifyCommand(model.Command):
    @staticmethod
    def parse(line, options=None):
        hook, command = line.split(None, 1)
        return line.split(None, 1)


class add_to_hook(__HookModifyCommand):
    @staticmethod
    def call(hook, command):
        commands = set(command.split('%;'))
        if is_hook(hook):
            commands |= set(client.test('${%s}' % _hook_id(hook)).split("%;"))
        client.define(_hook_id(hook), '%;'.join(commands))
        return True


class remove_from_hook(__HookModifyCommand):
    @staticmethod
    def call(hook, command):
        if is_hook(hook):
            commands = set(client.test(
                '${%s}' % _hook_id(hook)).split("%;")) - set(
                    command.split("%;"))
            if commands:
                client.define(_hook_id(hook), '%;'.join(commands))
            else:
                remove_hook(hook)


class evaluate_hook(__HookModifyCommand):
    @staticmethod
    def call(hook, command):
        if is_hook(hook):
            #          pprint.pprint('/%s %s' % (_hook_id(hook), command))
            client.eval('/%s %s' % (_hook_id(hook), command))


client.define(is_hook)
client.define(remove_hook)
client.define(add_to_hook)
client.define(remove_from_hook)
client.define(evaluate_hook)
