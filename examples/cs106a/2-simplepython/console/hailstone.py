#!/usr/bin/env python
"""CS106A Assignment 2 Example: Hailstone

Print the hailstone sequence for a user-supplied positive integer.

The problem can be expressed as follows:

- Pick some positive integer `n`.
- If `n` is even, divide it by two.
- If `n` is odd, multiply it by three and add one.
- Continue this process until `n` is equal to one.

As an example, consider starting with the number 15:

    15 is odd, so I make 3n + 1: 46
    46 is even so I take half: 23
    23 is odd, so I make 3n + 1: 70
    70 is even so I take half: 35
    35 is odd, so I make 3n + 1: 106
    106 is even so I take half: 53
    53 is odd, so I make 3n + 1: 160
    160 is even so I take half: 80
    80 is even so I take half: 40
    40 is even so I take half: 20
    20 is even so I take half: 10
    10 is even so I take half: 5
    5 is odd, so I make 3n + 1: 16
    16 is even so I take half: 8
    8 is even so I take half: 4
    4 is even so I take half: 2
    2 is even so I take half: 1
    The process took 17 step(s) to reach 1

The numbers go up and down, but eventually - at least for all numbers that have
ever been tried — ends at 1. In some respects, this process is reminiscent of
the formation of hailstones, which get carried upward by the winds over and over
again before they finally descend to the ground. This is where the name
"hailstone sequence" comes from, although it goes by many other names as well.

The hailstone sequence comes from Chapter XII of Douglas Hofstadter's
Pulitzer-prize-winning book: "Godel, Escher, Bach," which contains many
interesting mathematical puzzles, many of which can be expressed in the form of
computer programs.

No one has yet been able to prove that this process always stops. The number of
steps in the process can certainly get very large. How many steps, for example,
does the program take when n is 27?
"""
from campy.util.simpio import get_positive_integer


def hailstone(n):
    steps = 0
    # Until n is equal to one:
    while n != 1:
        # If n is even, divide it by two.
        if n % 2 == 0:
            m = n // 2
            print('{} is even so I take half: {}'.format(n, m))
        # If n is odd, multiply it by three and add one.
        else:
            m = 3 * n + 1
            print('{} is odd, so I make 3n + 1: {}'.format(n, m))

        # Move to the next step in the hailstone sequence.
        n = m
        steps += 1
    return steps


if __name__ == '__main__':
    # Get a positive integer from the user.
    n = get_positive_integer('Enter a number: ')

    # Compute the hailstone sequence starting at that number.
    steps = hailstone(n)
    print('The process took {} step(s) to reach 1'.format(steps))
