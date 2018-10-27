#!/usr/bin/env python3 -tt
"""
File: main.py
-------------
Exports a decorator to wrap a student's main function, providing
better error handling in some cases.
"""
from functools import wraps as _wraps

class DuplicateMainException(Exception):
    """Custom exception for duplicate entry points."""
    pass

def entrypoint(main):
    if entrypoint._EXISTS:
        raise DuplicateMainException("You can have at most one entry point in your code!")
    entrypoint._EXISTS = True
    @_wraps(main)
    def wrapper():
        try:
            main()
        except Exception as e:
            print("Error: {}".format(e))
            raise
    return wrapper

entrypoint._EXISTS = False
