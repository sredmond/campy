#!/usr/bin/env python3
"""
Reads commands from stdin, pipes them straight to the backend

Usage for file: cat foo.txt | python run_commands_from_file.py
"""
if __name__ == '__main__':
    import spgl.private.platform as _platform
    import sys

    while True:
        line = sys.stdin.readline()
        _platform.Platform().put_pipe(line)
