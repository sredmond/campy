# TODO: rewrite the functinos in this module to be more Pythonic

import enum as _enum

from campy.system.error import error

@_enum.unique
class TokenType(_enum.IntEnum):
    """The enumerated values of the <code>get_token_type</code> method."""
    SEPARATOR = 0
    WORD = 1
    NUMBER = 2
    STRING = 3
    OPERATOR = 4


class TokenScanner():
    def __init__(self, input_stream):
        self.input_stream = input_stream
        self._init_scannner()

    def set_input(self, input_stream):
        self.input_stream = input_stream

    def has_more_tokens(self):
        token = self.next_token()
        self.save_token(token)
        return token != ""

    def next_token(self):
        if self._saved_tokens:
            return self._saved_tokens.pop(0)

        while True:
            if self.ignore_whitespace:
                self._skip_spaces()
            ch = self.input_stream.read(1)

            if ch == '/' and self._ignore_comments:
                ch = self.input_stream.read(1)
                if ch == '/':
                    while True:
                        ch = self.input_stream.read(1)
                        if ch in ('', '\r', '\n'):
                            break
                    continue
                elif ch == '*':
                    prev = ''
                    while True:
                        ch = self.input_stream.read(1)
                        if not ch or (prev == '*' and ch == '/'):
                            break
                        prev = ch
                    continue
                if ch:
                    self.unget_char(ch)
                ch = '/'
            if not ch:
                return ''
            if ch in ('"', "'") and self._scan_strings:
                self.unget_char(ch)
                return self._scan_string()
            if ch.isdigit() and self._scan_numbers:
                self.unget_char(ch)
                return self._scan_number()
            if self.is_word_character(ch):
                self.unget_char(ch)
                return self._scan_word()
            op = ch
            while self._is_operator_prefix(op):
                ch = self.input_stream.read(1)
                if not ch:
                    break
                op += ch
            while len(op) > 1 and not self._is_operator(op):
                self.unget_char(op[-1])
                op = op[:-1]
            return op


    def save_token(self, token):
        self._saved_tokens.append(token)

    def get_position(self):
        pass

    def ignore_whitespace(self):
        pass

    def ignore_comments(self, python_style=True, c_style=False):
        pass

    def scan_numbers(self):
        pass

    def scan_strings(self):
        pass

    def add_word_characters(self, characters):
        self._word_characters += characters

    def is_word_character(self, ch):
        return ch.isalnum() or ch in self._word_characters

    def add_operator(self, op):
        self._operators.append(op)

    def verify_token(self, expected):
        token = self.next_token()
        if token != expected:
            # TODO: error w/ buffer
            error('Found "{}" when expecting "{}"'.format(token, expected))


    def get_token_type(self, token):
        if not token:
            error('Empty token: TODO(EOF)?')

        ch = token[0]
        if ch.isspace():
            return TokenType.SEPARATOR
        elif ch == '"' or (ch == "'" and len(token) > 1):
            return TokenType.STRING
        elif ch.isdigit():
            return TokenType.NUMBER
        elif self.is_word_character(ch):
            return TokenType.WORD
        else:
            return TokenType.OPERATOR

    def get_char(self):
        return self.input_stream.read(1)

    def unget_char(self, ch):
        # TODO: char must match current location
        current = self.input_stream.tell()
        if current > 0:
            self.input_stream.seek(current - 1)

    def get_string_value(self, token):
        out = ''
        start = 0
        finish = len(token)
        if finish > 1 and (token[0] == '"' or token[0] == "'"):
            start = 1
            finish -= 1

        for i in range(start, finish):
            ch = token[i]
            if ch == '\\':
                i += 1
                ch = token[i]
                if ch.isdigit() or ch == 'x':
                    base = 8
                    if ch == 'x':
                        base = 16
                        i += 1
                    result = 0
                    digit = 0
                    while i < finish:
                        ch = token[i]
                        if ch.isdigit():
                            digit = ord(ch) - ord(0)
                        elif ch.isalpha():
                            digit = ord(ch.upper()) - ord('A') + 10
                        else:
                            digit = base
                        if digit >= base:
                            break
                        result = base * result + digit
                        i += 1
                    ch = chr(result)
                    i -= 1
                else:
                    if ch == 'a': ch = '\a'
                    elif ch == 'b': ch = '\b'
                    elif ch == 'f': ch = '\f'
                    elif ch == 'n': ch = '\n'
                    elif ch == 'r': ch = '\r'
                    elif ch == 't': ch = '\t'
                    elif ch == 'v': ch = '\v'
                    # TODO: other delims?
            out += ch
        return out


    # Private
    def _init_scannner(self):
        self._buffer = None
        self._isp = None
        self._string_input = False
        self._ignore_whitespace = False
        self._ignore_comments = False
        self._scan_numbers = False
        self._scan_strings = False
        self._word_characters = []
        self._saved_tokens = []
        self._operators = []

    def _skip_spaces(self):
        while True:
            ch = self.input_stream.read(1)
            if not ch:
                return
            if not ch.isspace():
                self.unget_char(ch)
                return

    def _scan_word(self):
        token = ''
        while True:
            ch = self.input_stream.read(1)
            if not ch:
                break
            if not self.is_word_character(ch):
                self.unget_char(ch)
                break
            token += ch
        return token

    def _scan_number(self):
        token = ''
        state = _NumberScannerState.INITIAL_STATE
        while state != _NumberScannerState.FINAL_STATE:
            ch = self.input_stream.read(1)
            if state == _NumberScannerState.INITIAL_STATE:
                if not ch.isdigit():
                    error('internal error: illegal call')
                state = _NumberScannerState.BEFORE_DECIMAL_POINT
            elif state == _NumberScannerState.BEFORE_DECIMAL_POINT:
                if ch == '.':
                    state = _NumberScannerState.AFTER_DECIMAL_POINT
                elif ch in ('e', 'E'):
                    state = _NumberScannerState.STARTING_EXPONENT
                elif not ch.isdigit():
                    if ch:
                        self.unget_char(ch)
                    state = _NumberScannerState.FINAL_STATE
            elif state == _NumberScannerState.AFTER_DECIMAL_POINT:
                if ch in ('e', 'E'):
                    state = _NumberScannerState.STARTING_EXPONENT
                elif not ch.isdigit():
                    if ch:
                        self.unget_char(ch)
                    state = _NumberScannerState.FINAL_STATE
            elif state == _NumberScannerState.STARTING_EXPONENT:
                if ch in ('-', '+'):
                    state = _NumberScannerState.FOUND_EXPONENT_SIGN
                elif ch.isdigit():
                    state = _NumberScannerState.SCANNING_EXPONENT
                else:
                    if ch:
                        self.input_stream.unget_char(ch)
                    self.input_stream.unget_char(ch)
                    state = _NumberScannerState.FINAL_STATE
            elif state == _NumberScannerState.FOUND_EXPONENT_SIGN:
                if ch.isdigit():
                    state = _NumberScannerState.SCANNING_EXPONENT
                else:
                    if ch:
                        self.input_stream.unget_char(ch)
                    self.input_stream.unget_char(ch)
                    self.input_stream.unget_char(ch)
                    state = _NumberScannerState.FINAL_STATE
            elif case == _NumberScannerState.SCANNING_EXPONENT:
                if not ch.isdigit():
                    if ch:
                        self.input_stream.unget_char(ch)
                    state = _NumberScannerState.FINAL_STATE
            else:
                state = _NumberScannerState.FINAL_STATE
            if state != _NumberScannerState.FINAL_STATE:
                token += ch
        return token

    def _scan_string(self):
        token = ''
        delim = self.input_stream.read(1)
        token += delim
        escape = False
        while True:
            ch = self.input_stream.read(1)
            if not ch:
                error('found unterminated string') # TODO: fn name
            if ch == delim and not escape:
                break
            escape = ch == '\\' and not escape
            token += ch
        return token

    def _is_operator(self, op):
        return op in self._operators

    def _is_operator_prefix(self, op):
        return any(operator.startswith(op) for operator in self._operators)

@_enum.unique
class _NumberScannerState(_enum.IntEnum):
    INITIAL_STATE = 0
    BEFORE_DECIMAL_POINT = 1
    AFTER_DECIMAL_POINT = 2
    STARTING_EXPONENT = 3
    FOUND_EXPONENT_SIGN = 4
    SCANNING_EXPONENT = 5
    FINAL_STATE = 6
