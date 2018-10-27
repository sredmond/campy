"""
File: note.py
-------------
Defines a class named Note that can play musical notes.
"""
import enum as _enum

import campy.private.platform as _platform

# TODO: replace w/ imported error
def error(msg):
    import sys
    print(msg)
    sys.exit(1)


# Minimum legal value that an octave can have.
OCTAVE_MIN = 1
# Maximum legal value that an octave can have.
OCTAVE_MAX = 10

# Print message when a Note plays?
_NOTE_DEBUG = False

class Note:
    @_enum.unique
    class Pitch(_enum.Enum):
        R = 0  # Rest
        A = 1
        B = 2
        C = 3
        D = 4
        E = 5
        F = 6
        G = 7

    @_enum.unique
    class Accidental(_enum.Enum):
        SHARP = 1
        NATURAL = 0
        FLAT = -1

    def __init__(self, duration, pitch, octave, accidental, repeat=False):
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
        if pitch not in Note.Pitch:
            error('Illegal pitch.')
        self._pitch = pitch

    @octave.setter
    def octave(self, octave):
        if not OCTAVE_MIN <= octave <= OCTAVE_MAX:
            error('Illegal octave.')
        if self.is_rest():
            octave += 1
        self._octave = octave

    @accidental.setter
    def accidental(self, accidental):
        if accidental not in Note.Accidental:
            error('Illegal accidental value.')
        if self.is_rest():
            accidental = Note.Accidental.NATURAL
        self._accidental = accidental

    def play(self):
        if _NOTE_DEBUG:
            print("Playing {}".format(self))
        _platform.Platform().note_play(self, self.repeat)

    def __str__(self):
        out = "{duration} {pitch} ".format(duration=self.duration, pitch=self.pitch.name)
        if not self.is_rest():
            out += "{octave} {accidental} ".format(octave=self.octave, accidental=self.accidental.name)
        return out


def test_note():
    # for octave in range(OCTAVE_MIN, OCTAVE_MAX + 1):
    #     for pitch in Note.Pitch:
    #         for accidental in Note.Accidental:
    #             note = Note(0.05, pitch, octave, accidental, )
    #             print(note)
    #             note.play()

    tetris = 'E52 B41 C51 D52 C51 B41 A42 A41 C51 E52 D51 C51 B42 B41 C51 D52 E52 C52 A42 A42 R14 D51 F51 A52 G51 F51 E53 C51 E52 D51 C51 B42 B41 C51 D52 E52 C52 A42 A42'
    for note_info in tetris.split():
        pitch, octave, duration = note_info
        pitch = Note.Pitch[pitch]
        octave = int(octave)
        duration = int(duration)
        note = Note(duration / 8, pitch, octave, Note.Accidental.NATURAL)
        note.play()

    # ode_to_joy = [
    #     '1 E 5 NATURAL false',
    #     '1 E 5 NATURAL false',
    #     '1 F 5 NATURAL false',
    #     '1 G 5 NATURAL false',
    #     '1 G 5 NATURAL false',
    #     '1 F 5 NATURAL false',
    #     '1 E 5 NATURAL false',
    #     '1 D 5 NATURAL false',
    #     '1 C 5 NATURAL false',
    #     '1 C 5 NATURAL false',
    #     '1 D 5 NATURAL false',
    #     '1 E 5 NATURAL false',
    #     '1 E 5 NATURAL false',
    #     '1 D 5 NATURAL false',
    #     '1 D 5 NATURAL false',
    # ]
    # for line in ode_to_joy:
    #     note = Note.from_line(line)
    #     print(note)
    #     note.play()

if __name__ == '__main__':
    test_note()

