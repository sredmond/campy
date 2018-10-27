"""
File: sound.py
--------------
This file defines a class that represents a sound.
"""
import campy.private.platform as _platform

class Sound():
    """
    This class encapsulates a sound file.  The sound file is specified in the
    constructor and must be a file in either the current directory or a
    subdirectory named sounds.

    The following code, for example, plays the sound file ringtone.wav::

        ringtone = Sound("ringtone.wav")
        ringtone.play()

    """
    def __init__(self, filename):
        """Creates a Sound object.
        The default constructor creates an empty sound that cannot be played.
        The second form initializes the sound by reading in the contents of
        the specified file.

        @type filename: string
        @param filename: sound file
        @rtype: void
        """
        self.filename = filename
        _platform.Platform().create_sound(self, filename)


    def play(self):
        """Starts playing the sound.

        This call returns immediately without waiting for the sound to finish.
        """
        _platform.Platform().play_sound(self)

    def __del__(self):
        """Frees the Java memory associated with the sound."""
        _platform.Platform().delete_sound(self)
