#!/usr/bin/env python3 -tt
from spgl.gsounds import *
from spgl.main import entrypoint

@entrypoint
def main():
    s = Sound("../res/sounds/fireball.wav")
    s.play()

if __name__ == '__main__':
    main()
