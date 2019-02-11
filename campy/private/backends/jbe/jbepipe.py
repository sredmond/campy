"""Manage initialization of and communications to and from the Java backend.

The Java backend should live in a JAR file adjacent to this module.

The backend is initialized lazily, only created once someone tries to write
to or read from the pipe. This means that the first call to the pipe will be
slow, as it must take time to spawn the Java process.
"""
# TODO(sredmond): Consider updating the subprocess calls to use Python 3.5+
import logging
import pathlib
import queue  # TODO(sredmond): Double-check that this doesn't have to be multiprocessing.queue
import shlex
import subprocess
import sys
import threading

from campy.system import error

# Module-level logger.
logger = logging.getLogger(__name__)


# The backend JAR should live adjacent to this file.
SPL_JAR_LOCATION = pathlib.Path(__file__).parent / 'spl.jar'


# Use `shlex` to parse shell text. These args, when passed to `Popen`, launch the Java backend.
LAUNCH_SPL_ARGS = shlex.split('java -jar {}'.format(SPL_JAR_LOCATION))


def debug_print(line):
    # if DEBUG_PIPE:
    # options['file'] = sys.stderr
    # options['flush'] = True

    logger.info(line)
    # print(*values, **options)


def append_output_to_queue(out, queue):
    for line in iter(out.readline, b''):
        logger.info('Adding output to queue: %r', line)
        queue.put(line)
    out.close()


class JavaBackendPipe:
    """A JavaBackendPipe connects to a single instance of a running JAR file.

    A JavaBackendPipe knows how to write strings to the backend and how to read
    responses from the backend.

    In order to avoid side-effects on import, the JAR is not run until a read or
    write is requested.

    Implementation note: A JavaBackendPipe starts a thread to consume the output
    from the Java backend, so that the internal OS pipe is unlikely to fill up.
    When the JavaBackendPipe is deleted, the thread is joined as well.
    """

    def __init__(self):
        self._pipe = None

    @property
    def pipe(self):
        # TODO(sredmond): Adding a level of indirection here (self.pipe calls a
        # function) seems like it could slow down the frequent operation of
        # using this pipe. Perhaps consider a different way to make pipe lazily-
        # initialized.
        if not self._pipe:
            # TODO(sredmond): Double check that these are the correct kwargs.
            # TODO(sredmond): Crash if the SPL can't be found or if this process exits
            # early.
            self._pipe = subprocess.Popen(LAUNCH_SPL_ARGS,
                                           shell=False,
                                           stdin=subprocess.PIPE, \
                                           stdout=subprocess.PIPE, \
                                           stderr=sys.stdout, \
                                           universal_newlines=True)

            self.line_queue = queue.Queue()
            self.watchdog = threading.Thread(target=append_output_to_queue,
                                             args=(self._pipe.stdout, self.line_queue))
            self.watchdog.daemon = True # thread dies with the program
            self.watchdog.start()

        return self._pipe

    def write(self, line):
        line += '\n'  # TODO(sredmond): Do we only need to add a newline when
        # there isn't already one, or always?
        # TODO(sredmond): Consider self.pipe.communicate(input=line, timeout=1)[0]
        logger.info('Writing line: %r', line)
        debug_print(line)
        self.pipe.stdin.write(line)
        self.pipe.stdin.flush()

    def read(self):
        logger.info('Queue size: %d', self.line_queue.qsize())
        return self.line_queue.get()
        # Alternatively, return self.pipe.stdout.readline()

    def get_status(self):
        result = self.get_result()
        if result != 'ok':
            error(result)

    # TODO: check for whitespace returned at start or finish
    def get_result(self, consume_acks=True, stop_on_event=False, caller=''):
        while True:
            debug_print('get_result(): calling read()...')
            line = self.read()
            debug_print(line)

            is_result = line.startswith('result:')
            is_result_long = line.startswith('result_long:')
            is_event = line.startswith('event:')
            is_ack = line.startswith('result:___jbe___ack___')
            has_acm_exception = 'acm.util.ErrorException' in line
            has_exception = 'xception' in line
            has_error = 'Unexpected error' in line

            if is_result_long:
                # Read a long result (sent across multiple lines)
                result = ''
                next_line = self.read()
                while next_line != 'result_long:end':
                    if not line.startswith('result:___jbe___ack___'):
                        result += line
                        debug_print('getResult(): appended line (length so far: {})'.format(len(result)))
                    next_line = self.read()
                debug_print('getResult(): returning long strings "{}...{}" (length {})'.format(result[:10], result[-10:], len(result)))
                return result
            elif ((is_result or is_event) and has_acm_exception) or (not is_result and not is_event and (has_exception or has_error)):
                # Read an error message from the back-end
                if is_result:
                    line = line[7:]  # Prune 'result:'
                elif is_event:
                    line = line[6:]  # Prune 'event:'
                result = 'ERROR emitted from Stanford Java back-end process\n{}'.format(line)
                error(result)

            elif is_result:
                # Read a regular result
                if not is_ack or not consume_acks:
                    result = line[7:]  # Prune 'result:'
                    debug_print('getResult(): returning regular result (length {}) {}'.format(len(result), repr(result)))
                    return result.strip()
                else:
                    # Just an acknowledgement of some previous event: not a real result.
                    debug_print('getResult(): saw ACK (length {}) "{}"'.format(len(line), line))
            elif is_event:
                # Read a Java-originated event; enqueue it to process here.
                event = self.parseEvent(line[6:].strip())
                Platform.EVENT_QUEUE.append(event)
                if stop_on_event or (event.event_class == gevents.EventClassType.WINDOW_EVENT and event.event_type == gevents.EventType.CONSOLE_CLOSED and caller == 'get_line_console'):
                    return ''
            else:
                if '\tat ' in line or '   at ' in line:
                    # a line from a back-end Java exception stack trace;
                    # shouldn't really be happening, but back end isn't perfect.
                    # echo it here to STDERR so Python user can see it to help diagnose the issue
                    debug_print(line)

    def __del__(self):
        self._pipe.terminate()
        # TODO(sredmond): Do we want to join threads now or at program exit?
        # pass

