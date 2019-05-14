#!/usr/bin/env python3 -tt
"""
File: random.h
--------------
This file exports functions for generating pseudorandom numbers.
In most cases, the builtin random library should be used, but this
class offers some nice conveniences.

Note: the methods are named in consistency with the random module
"""
import random as _random
from collections import deque as _deque

"""TODO: singleton?"""
class RandomGenerator(_random.Random):
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    """ NOTE: a student shouldn't ever instantiate a RandomGenerator"""
    """ Rather, they should access one using getInstance """
    def __init__(self):
        self._fixed_bools = _deque()
        self._fixed_ints = _deque()
        self._fixed_reals = _deque()

    def randbool(self):
        return randchance(0.5)

    def randint(self, low, high):
        if self._fixed_ints:
            return self._fixed_ints.pop()
        return super().randint(low, high)

    def randchance(self, p):
        if self._fixed_bools:
            return self._fixed_bools.pop()
        return self.random() < p

    def randreal(self, low=0, high=1):
        if self._fixed_reals:
            return self._fixed_reals.pop()
        return low + (high - low) * self.random()

    def _feed_bool(self, value):
        self._fixed_bools.appendleft(value)

    def _feed_int(self, value):
        self._fixed_ints.appendleft(value)

    def _feed_real(self, value):
        self._fixed_reals.appendleft(value)

RandomGenerator._instance = RandomGenerator()
