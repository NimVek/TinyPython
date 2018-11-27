from .. import client

import logging
__log__ = logging.getLogger(__name__)


def _completion(args):
   __log__.debug("Start Completion")
   buffer = client.kbhead()
   wordleft = client.kbwordleft()
   __log__.debug(buffer)
   __log__.debug(wordleft)
   prefix = buffer[wordleft - 1]
   __log__.debug(prefix)
   __log__.debug(buffer[wordleft:])
   __log__.debug(buffer[client.kbwordright(client.kbwordleft(wordleft)):wordleft])

client.evaluate('/def -b"^i" b_completion = /python_call macros.util.completion._completion %{0}')


