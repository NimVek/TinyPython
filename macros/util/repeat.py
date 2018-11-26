from .. import client
from .. import model

from .hooks import eval_hook

import re
import pprint


class dummy(model.Command):
    """ Test if the argument is a hook"""

    @staticmethod
    def call(name):
        pprint.pprint(list(client.ps()))


client.define(dummy)


def _beat(line):
    beat = re.match('^beat_([0-9]+)$', line.strip())
    if beat:
        interval = int(beat.group(1))
        beat = beat.group(0)
        if client.get('do_beat', int) and client.get('do_%s' % beat, int):
            if client.get('do_beat', int) == 1 and client.get(
                    'do_%s' % beat, int) == 1:
                eval_hook(beat)
            pid = client.evaluate('/repeat -%d 1 /%s' % (interval, beat))
            if pid:
                client.set('beat_pid_%d' % interval, pid)
                return pid


class beat(model.Command):
    """ Test if the argument is a hook"""

    @staticmethod
    def parse(line, options=None):
        return [int(x) for x in line.split(None, 1)]

    @staticmethod
    def call(interval, status=1):
        client.define('beat_%d' % interval, _beat)
        client.set('do_beat', status)
        client.set('do_beat_%d' % interval, status)
        if next(client.ps('/beat_%d' % interval), None) == None:
          client.command('beat_%d' % interval)


client.define(beat)
