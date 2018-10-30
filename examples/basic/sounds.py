#!/usr/bin/env python3 -tt
from campy.util.sound import *
from campy.private.main import entrypoint

@entrypoint
def main():
    s = Sound("../res/sounds/fireball.wav")
    s.play()

if __name__ == '__main__':
    main()
