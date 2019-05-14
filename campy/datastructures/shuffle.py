"""Shuffle an immutable collection and return a copy of the collection."""
import random as _random

def shuffle(collection, random=None):
    """Randomly shuffle a collection.

    Note that this function has different behavior depending on what the input is.

    If collection represents an infinite iterable, this will loop indefinitely.
    """
    elements = list(collection)  # Consume
    _random.shuffle(elements, random=random)
    if isinstance(collection, str):
        return ''.join(elements)
    return collection.__class__(elements)

__all__ = ['shuffle']
