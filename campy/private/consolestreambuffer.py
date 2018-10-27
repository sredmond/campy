"""
File: consolestreambuf.py
-------------------------
This file defines the <code>ConsoleStreamBuffer</code> class, which
represents a stream buffer that reads/writes to the Stanford graphical console
using a process pipe to a Java back-end process.
"""
import io as _io
import campy.private.platform as _platform

class ConsoleStreamBuffer:
    def input(self, prompt=''):
        _platform.Platform().put_console(prompt)
        result = _platform.Platform().get_line_console()
        if result.endswith('\n'):
            result = result[:-1]
        return result

    def print(self, *objects, sep='', end='\n', flush=False, stderr=False):
        buffer = _io.StringIO()
        __builtins__.print(*objects, sep=sep, end=end, file=buffer, flush=True)
        data = buffer.getvalue()
        _platform.Platform().put_console(data, stderr=stderr)


def test_consolestreambuffer():
    console = ConsoleStreamBuffer()
    console.print('Hello there! I echo text.\n')
    name = console.input('What is your name? ')
    console.print('Hello, {}'.format(name))
    while True:
        to_say = console.input('What should I say (hit ENTER to exit)? ')
        if not to_say: break
        console.print(to_say)

    console.print(5, 6, 7, sep='/', end=' :)', stderr=True)

if __name__ == '__main__':
    test_consolestreambuffer()
