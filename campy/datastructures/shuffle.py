"""Shuffle an immutable collection and return a copy of the collection."""
import random

def shuffle(collection, random=None):
    """Return a randomly shuffled copy of a collection.

    Note that this function's behavior depends on the type of its input.

    If collection represents an infinite iterable, this will loop indefinitely.
    """
    elements = list(collection)  # Consume all elements.
    random.shuffle(elements, random=random)
    if isinstance(collection, str):
        return ''.join(elements)
    return collection.__class__(elements)

__all__ = ['shuffle']
