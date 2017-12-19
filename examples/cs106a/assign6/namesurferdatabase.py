import namesurferentry

class NameSurferDatabase:
    """In this case, we'll oblige the OOP design and initialize from a filename."""

    def __init__(self, filename):
        self._lookup = {}
        with open(filename) as f:
            for line in f:
                entry = namesurferentry.from_line(line)
                self._lookup[entry.name.lower()] = entry

    def __getitem__(self, name):
        return self._lookup.get(name.lower())

