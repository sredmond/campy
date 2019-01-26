"""Tests for the :mod:`campy.util.note` module."""
from campy.util.note import OCTAVE_MIN, OCTAVE_MAX, Note

import os
TEST_PLATFORM = 'CAMPY_TEST_PLATFORM' in os.environ


def test_pitch_contains_rest():
    assert Note.Pitch.R in Note.Pitch


def test_pitch_contains_all_pitches():
    assert Note.Pitch.A in Note.Pitch
    assert Note.Pitch.B in Note.Pitch
    assert Note.Pitch.C in Note.Pitch
    assert Note.Pitch.D in Note.Pitch
    assert Note.Pitch.E in Note.Pitch
    assert Note.Pitch.F in Note.Pitch
    assert Note.Pitch.G in Note.Pitch


def test_create_simple_note():
    note = Note(1, Note.Pitch.C, 4)
    assert note.duration == 1
    assert note.pitch == Note.Pitch.C
    assert note.octave == 4
    assert note.accidental == Note.Accidental.NATURAL
    assert note.repeat == False


def test_create_nonnatural_notes():
    note = Note(1, Note.Pitch.C, 4, Note.Accidental.SHARP)
    assert note.accidental == Note.Accidental.SHARP
    note = Note(1, Note.Pitch.C, 4, Note.Accidental.FLAT)
    assert note.accidental == Note.Accidental.FLAT


def test_create_repeating_note():
    note = Note(1, Note.Pitch.C, 4, repeat=True)
    assert note.repeat == True


def test_create_rest():
    note = Note.rest(1)
    assert note.pitch == Note.Pitch.R
    assert note.duration == 1
    assert note.is_rest()
    assert note.accidental == Note.Accidental.NATURAL
    assert note.octave == OCTAVE_MIN


def test_shorten_duration():
    note = Note(1, Note.Pitch.C, 4)
    assert note.duration == 1
    note.duration = 0.5
    assert note.duration == 0.5


def test_lengthen_duration():
    note = Note(1, Note.Pitch.C, 4)
    assert note.duration == 1
    note.duration = 2
    assert note.duration == 2


def test_change_pitch():
    note = Note(1, Note.Pitch.C, 4)
    assert note.pitch == Note.Pitch.C
    note.pitch = Note.Pitch.G
    assert note.pitch == Note.Pitch.G


def test_change_pitch_to_rest():
    note = Note(1, Note.Pitch.C, 4)
    assert note.pitch == Note.Pitch.C
    note.pitch = Note.Pitch.R
    assert note.pitch == Note.Pitch.R
    assert note.is_rest()


def test_change_rest_to_pitch():
    note = Note.rest(1)
    assert note.is_rest()
    print(note)
    print(note.octave)
    note.pitch = Note.Pitch.C
    print(note)
    assert note.pitch == Note.Pitch.C
    assert note.accidental == Note.Accidental.NATURAL
    assert note.octave == OCTAVE_MIN


def test_change_accidental():
    note = Note(1, Note.Pitch.C, 4, Note.Accidental.SHARP)
    assert note.accidental == Note.Accidental.SHARP
    note.accidental = Note.Accidental.FLAT
    assert note.accidental == Note.Accidental.FLAT


def test_change_octave():
    note = Note(1, Note.Pitch.C, 4)
    assert note.octave == 4
    note.octave = OCTAVE_MIN
    assert note.octave == OCTAVE_MIN


def test_octave_bounds_are_ordered():
    assert OCTAVE_MIN <= OCTAVE_MAX

def test_create_from_line():
    note = Note.from_line('1 C 4 NATURAL false')
    assert note.duration == 1
    assert note.pitch == Note.Pitch.C
    assert note.octave == 4
    assert note.accidental == Note.Accidental.NATURAL
    assert note.repeat == False


# TODO(sredmond): Check for invalid options, including
# negative duration, zero duration, nonnumeric duration
# unexpected pitch
# octave out of range
# unexpected accidental
# nonboolean repeat
# improperly formatted from line.
#   leading/trailing whitespace
#   more/less inner whitespace
#   weird tabs instead of spaces
#   weird boolean spellings of repeat
#   weird capitalizations of accidentals
#   bad types
#   create rest from line

if TEST_PLATFORM:
    def test_play_single_note():
        note = Note(1, Note.Pitch.C, 4, Note.Accidental.NATURAL)
        note.play()


    def test_play_all_notes():
        # Change me if you need this test to run faster or slower.:
        NOTE_DURATION = 0.05

        # Don't worry if this sounds a little strange.
        # Recall than an A9 is actually a higher pitch than a C9, since the
        # octave counts increment at C.
        for octave in range(OCTAVE_MIN, OCTAVE_MAX + 1):
            for pitch in Note.Pitch:
                for accidental in Note.Accidental:
                    note = Note(NOTE_DURATION, pitch, octave, accidental)
                    note.play()


    def test_play_tetris():
        # Change me if you need this test to run faster or slower.
        SPEEDUP_FACTOR = 8

        tetris = 'E52 B41 C51 D52 C51 B41 A42 A41 C51 E52 D51 C51 B42 B41 C51 D52 E52 C52 A42 A42 R14 D51 F51 A52 G51 F51 E53 C51 E52 D51 C51 B42 B41 C51 D52 E52 C52 A42 A42'
        for note_info in tetris.split():
            pitch, octave, duration = note_info
            pitch = Note.Pitch[pitch]
            octave = int(octave)
            duration = int(duration)
            note = Note(duration / 8, pitch, octave, Note.Accidental.NATURAL)
            note.play()


    def test_play_ode_to_joy_from_lines():
        # Change me if you need this test to run faster or slower.
        SPEEDUP_FACTOR = 8

        # The zero-second rests force the note player to stop and start a new note.
        ode_to_joy = [
            '1 E 5 NATURAL false',
            '0 R 1 NATURAL false',
            '1 E 5 NATURAL false',
            '1 F 5 NATURAL false',
            '1 G 5 NATURAL false',
            '0 R 1 NATURAL false',
            '1 G 5 NATURAL false',
            '1 F 5 NATURAL false',
            '1 E 5 NATURAL false',
            '1 D 5 NATURAL false',
            '1 C 5 NATURAL false',
            '0 R 1 NATURAL false',
            '1 C 5 NATURAL false',
            '1 D 5 NATURAL false',
            '1 E 5 NATURAL false',
            '0 R 1 NATURAL false',
            '1 E 5 NATURAL false',
            '1 D 5 NATURAL false',
            '0 R 1 NATURAL false',
            '1 D 5 NATURAL false',
        ]
        for line in ode_to_joy:
            note = Note.from_line(line)
            note.duration /= SPEEDUP_FACTOR
            note.play()
