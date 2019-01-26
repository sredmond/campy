"""
Exports a :class:`Note` class that can play musical notes.

A :class:`Note` has several attributes - its :class:`Pitch`

To create a note, you can
"""
import enum
import logging

import campy.private.platform as _platform

# Create a module-level logger.
logger = logging.getLogger(__name__)


# TODO: replace w/ imported error
def error(msg):
    import sys
    print(msg)
    sys.exit(1)


# Minimum legal value that an octave can have.
OCTAVE_MIN = 1


# Maximum legal value that an octave can have.
OCTAVE_MAX = 10


class Note:
    @enum.unique
    class Pitch(enum.Enum):
        R = 0  # Rest
        A = 1
        B = 2
        C = 3
        D = 4
        E = 5
        F = 6
        G = 7

    @enum.unique
    class Accidental(enum.Enum):
        SHARP = 1
        NATURAL = 0
        FLAT = -1

    def __init__(self, duration, pitch, octave, accidental=Accidental.NATURAL, repeat=False):
        self.duration = duration
        self.pitch = pitch
        self.octave = octave
        self.accidental = accidental
        self.repeat = repeat

    @classmethod
    def from_line(cls, line):
        """Constructs a new note from a line definition.

        Usage:
            note = Note.from_line('1.5 G 5 NATURAL false')
        """
        try:
            duration, pitch, octave, accidental, repeat = line.split(' ')
        except ValueError as exc:
            error(exc)

        try:
            duration = int(duration)
        except ValueError:
            error('Invalid duration numeric format.')

        try:
            pitch = Note.Pitch[pitch]
        except KeyError:
            error('Illegal pitch.')

        try:
            octave = int(octave)
        except ValueError:
            error('Illegal octave numeric format.')

        try:
            accidental = Note.Accidental[accidental]
        except KeyError:
            error('Illegal accidental.')

        repeat = repeat not in ['False', 'false']  # Compatibility with CPP-style casing

        return cls(duration, pitch, octave, accidental, repeat)

    @classmethod
    def rest(cls, duration, repeat=False):
        # TODO(sredmond): Do we ever want to allow a repeating rest? What does that even mean?
        print(duration, Note.Pitch.R, OCTAVE_MIN, Note.Accidental.NATURAL, False)
        print(cls)
        return cls(duration, Note.Pitch.R, OCTAVE_MIN, Note.Accidental.NATURAL, repeat=repeat)

    def is_rest(self):
        return self.pitch == Note.Pitch.R

    @property
    def duration(self):
        return self._duration

    @property
    def pitch(self):
        return self._pitch

    @property
    def octave(self):
        return self._octave

    @property
    def accidental(self):
        return self._accidental

    @duration.setter
    def duration(self, duration):
        if duration < 0:
            error('Illegal negative duration.')
        self._duration = duration

    @pitch.setter
    def pitch(self, pitch):
        # TODO(sredmond): Should we ever allow a rest to turn into a non-rest or vice versa?
        if pitch not in Note.Pitch:
            error('Illegal pitch.')
        self._pitch = pitch

    @octave.setter
    def octave(self, octave):
        if not OCTAVE_MIN <= octave <= OCTAVE_MAX:
            error('Illegal octave.')
        # TODO(sredmond): What the heck is this doing in here? Why would we want to increment the octave of a rest?
        # if self.is_rest():
        #     octave += 1
        self._octave = octave

    @accidental.setter
    def accidental(self, accidental):
        if accidental not in Note.Accidental:
            error('Illegal accidental value.')
        if self.is_rest():
            accidental = Note.Accidental.NATURAL
        self._accidental = accidental

    def play(self):
        logger.warning('Playing %s', self)
        _platform.Platform().note_play(self, self.repeat)

    def __str__(self):
        out = "{duration} {pitch} ".format(duration=self.duration, pitch=self.pitch.name)
        if not self.is_rest():
            out += "{octave} {accidental} ".format(octave=self.octave, accidental=self.accidental.name)
        return out


__all__ = ['OCTAVE_MIN', 'OCTAVE_MAX', 'Note']

