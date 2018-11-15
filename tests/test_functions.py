#!/usr/bin/env python3

from nose.tools import *
from macros.functions import *


def test_getopts():
    expected = ({
        'a': True,
        'b': True,
        'n': 5,
        's': "can't stop"
    }, "whiz = bang biff")
    assert_equals(
        getopts("-a -b -n5 -s\"can't stop\" -- whiz = bang biff", "abn#s:"),
        expected)
    #  assert_equals(getopts("-a -b -n5 -s'can\\'t stop' whiz = bang biff","abn#s:"), expected)
    assert_equals(
        getopts("-n5 -ba -s`can't stop` whiz = bang biff", "abn#s:"), expected)
    assert_equals(
        getopts("-as\"can't stop\" -bn5 whiz = bang biff", "abn#s:"), expected)

    assert_equals(getopts('-t"foo"=bar', "t:"), ({'t': 'foo'}, "=bar"))
