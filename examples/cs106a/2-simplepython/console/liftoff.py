#!/usr/bin/env python
"""CS106A Assignment 2 Example: Lift off! (Warmup)

This program prints the calls for a spaceship that is about to launch.

It loops through the numbers from 10 down to 1, and the writes "Lift off!".

Usage::

    $ python liftoff.py
    10
    9
    8
    7
    6
    5
    4
    3
    2
    1
    Lift off!
"""

# Number which starts the countdown.
COUNTDOWN_START = 10

# Text to print at lift off.
LIFTOFF_MESSAGE = "Lift off!"

if __name__ == '__main__':
    for time_remaining in range(COUNTDOWN_START, 0, -1):
        print(time_remaining)
    print(LIFTOFF_MESSAGE)
