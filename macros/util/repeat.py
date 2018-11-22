from .. import client
from .. import model

import pprint


class dummy(model.Command):
    """ Test if the argument is a hook"""

    @staticmethod
    def call(name):
        pprint.pprint(list(client.ps()))

client.define(dummy)
