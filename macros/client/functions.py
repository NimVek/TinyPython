#!/usr/bin/env python3

from .basic import test

def kbhead():
  return test("kbhead()")

def kbwordleft(i:int = None):
  if i != None:
    return test("kbwordleft(%d)" % i)
  return test("kbwordleft()")

def kbwordright( i:int = None):
  if i != None:
    return test("kbwordright(%d)" % i)
  return test("kbwordright()")