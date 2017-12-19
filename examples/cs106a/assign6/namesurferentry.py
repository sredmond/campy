import collections

NameSurferEntry = collections.namedtuple('NameSurferEntry', ['name', 'ranks'])
# TODO(sredmond): Is it worth writing a __str__ method?


def from_line(line):
    name, *ranks = line.split(' ')
    return NameSurferEntry(name, [int(r) for r in ranks])
