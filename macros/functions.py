#!/usr/bin/env python3

import pprint

def getopts(args, opts):
  flags = {}
  i, length = 0, len(opts)
  while i < length:
    if i < length - 1 and opts[i+1] in ':#@':
      flags[opts[i]] = opts[i+1]
      i += 2
    else:
      flags[opts[i]] = ' '
      i += 1

  pprint.pprint(flags)

  outdict = {}
  inword = False
  while True:
    if not inword:
      args = args.lstrip()
      if not len(args) or args[0] != '-':
        break
      else:
        args = args[1:]
        if args[0] == '-':
          args = args[1:]
          if len(args) and not args[0].isspace():
            raise "Invalid option syntax: --%c" % args[0]
        if not len(args) or args[0].isspace():
          args = args.lstrip()
          break
    elif args[0] == '=':
      break

    op, args = args[0], args[1:]
    pprint.pprint((op, args))

    if op not in flags:
      pprint.pprint( "Invalid option: %c" % op)
      raise "Invalid option: %c" % op

    pprint.pprint((op, flags[op] in ':#'))
    if flags[op] in ':#':
      value = ''
      if args[0] in '"\'`':
        quote = args[0]
        args = args[1:]
        value = ''
        while args[0] != quote:
          value += args[0]
          if args[0] == '\\':
            if len(args) > 1:
              value += args[1]
              args = args[2:]
            else:
              raise "Unmached quote"
          else:
            args = args[1:]
        args = args[1:]
#        raise "Unsupported"
      else:
        while len(args) and not args[0].isspace():
          value += args[0]
          args = args[1:]
      if flags[op] == '#':
         #expression?
        value = int(value)
    elif flags[op] == '@':
      raise "Unsupported"
    else:
      value = True

    pprint.pprint(args)

    outdict[op] = value

    inword = len(args) and not args[0].isspace()
    pprint.pprint(inword)

    pprint.pprint((outdict,args))
  pprint.pprint(("ENDE",outdict,args))


getopts(" -f -p12332 -rghghg -- ende", "fp#r:")
getopts(" -f -p12332 -rghghg = ende", "fp#r:")
getopts(" -fp12332 -rghghg=ende", "fp#r:")
getopts(" -r'ggg'=ende", "fp#r:")
getopts("-a -b -n5 -s\"can't stop\" -- whiz = bang biff","abn#s:")
getopts("-a -b -n5 -s'can\\'t stop' whiz = bang biff","abn#s:")
getopts("-n5 -ba -s`can't stop` whiz = bang biff","abn#s:")
getopts("-as\"can't stop\" -bn5 whiz = bang biff","abn#s:")

