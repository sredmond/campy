#!/usr/bin/env python3 -tt
from campy.gsounds import *
from campy.main import entrypoint

@entrypoint
def main():
    s = Sound("../res/sounds/fireball.wav")
    s.play()

if __name__ == '__main__':
    main()
