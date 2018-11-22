from .basic import grab
import enum


class Process(object):
    class Type(enum.Enum):
        REPEAT = 'REPEAT'
        QUOTE = 'QUOTE'

    def __init__(self, values):
        self.pid = int(values['PID'])


class RepeatProcess(Process):
    def __init__(self, values):
        super().__init__(values)
        self.count = -1 if values['COUNT'] == 'i' else int(values['COUNT'])
        self.command = values['COMMAND']


def ps():
    columns = {0: 5, 6: 14, 15: 16, 17: 18, 19: 27, 28: 36, 37: 42, 43: None}
    ps = grab('/ps')
    keys = [ps[0][i:columns[i]].strip() for i in sorted(columns.keys())]
    for row in ps[1:]:
        values = [row[i:columns[i]].strip() for i in sorted(columns.keys())]
        values = dict(zip(keys, values))
        if values['T'] == 'r':
            yield RepeatProcess(values)
