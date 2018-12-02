from .. import client

import logging
__log__ = logging.getLogger(__name__)


def common_prefix(words):
    first = min(words)
    last = max(words)
    for i, char in enumerate(first):
        if last[i] != char:
            return first[:i]


_last_complete = None


def _complete(prefix: str, candidates):
    global _last_complete
    candidates = [str(i).strip() for i in candidates]
    candidates = [i for i in candidates if i.startswith(prefix)]
    candidates = sorted(set(candidates))
    if not candidates:
        client.evaluate("/beep 1")
    elif len(candidates) == 1:
        client.evaluate('/@test input("%s")' % candidates[0][len(prefix):])
        client.evaluate("/@test input(' ')")
    else:
        client.evaluate("/beep 1")
        client.evaluate(
            '/@test input("%s")' % common_prefix(candidates)[len(prefix):])
        if _last_complete == candidates:
            client.evaluate("/echo %s" % ' '.join(candidates))
        _last_complete = candidates


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
    if prefix == "/":
        possi = client.grab("/@list -s -i - %s*" % start)
        possi = [p.split(':', 1)[1].strip() for p in possi]
        __log__.debug(possi)
        _complete(start, possi)


client.define(completion)
#client.define('key_tab','/if (moresize()) ${key_tab}%; /else /completion%; /endif')
#client.evaluate('/edit key_tab=/if (moresize()) ${key_tab}%; /else /completion%; /endif')
client.evaluate(
    '/edit key_tab=/if (moresize()) /dokey page%; /else /completion%; /endif')
