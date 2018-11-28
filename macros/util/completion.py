from .. import client

import logging
__log__ = logging.getLogger(__name__)


def completion(args):
   __log__.debug("Start Completion")
   buffer = client.kbhead()
   start = client.kbwordleft()
   __log__.debug(buffer)
   __log__.debug(start)
   prefix = buffer[start - 1] if start > 0 else None
   start = buffer[start:]
   __log__.debug(prefix)
   __log__.debug(start)

client.define(completion)
#client.define('key_tab','/if (moresize()) ${key_tab}%; /else /completion%; /endif')
#client.evaluate('/edit key_tab=/if (moresize()) ${key_tab}%; /else /completion%; /endif')
client.evaluate('/edit key_tab=/if (moresize()) /dokey page%; /else /completion%; /endif')
#client.evaluate('/def -b"^i" b_completion = /python_call macros.util.completion._completion %{0}')


