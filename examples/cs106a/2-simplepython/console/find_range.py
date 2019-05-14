#!/usr/bin/env python
"""CS106A Assignment 2 Example: Find Range

Prompt a user repeatedly for integers until a sentinel is entered, then report
the smallest and largest values entered.

It is an error for the user to immediately enter the sentinel value without
first entering at least one value.

Sample Usage::
$ python find_range.py
This program finds the largest and smallest numbers.
? 5
? -1
? 7
? 0
Smallest: -1
Largest: 7
"""
from campy.util.simpio import get_integer


# Value representing positive infinity.
POSITIVE_INFINITY = float('inf')

# Value representing negative infinity.
NEGATIVE_INFINITY = float('-inf')

# Input that terminates the program.
SENTINEL = 0


def main():
    print("This program finds the largest and smallest numbers.")
    smallest, largest = POSITIVE_INFINITY, NEGATIVE_INFINITY

    # Loop until the user enters the SENTINEL value.
    while True:
        n = get_integer('?')
        if n == SENTINEL:
            break

        # Possibly update the running lowest or highest values.
        if n < smallest:
            smallest = n
        if n > largest:
            largest = n

    # The smallest and largest values will be set to their defaults values only
    # if the user has entered no non-sentinel values.
    if smallest == POSITIVE_INFINITY or largest == NEGATIVE_INFINITY:
        print('You must enter at least one value before the sentinel!')
    else:
        print('Smallest:', smallest)
        print('Largest:', largest)


if __name__ == '__main__':
    main()
