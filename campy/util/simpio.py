#!/usr/bin/env python3 -tt
"""
File: simpio.h
--------------
This file exports a set of functions that simplify input/output
operations in Python and provide some error-checking on console input.

Modified from Marty Stepp's CPP libraries.

@author sredmond
"""

GETINTEGER_DEFAULT_PROMPT = "Enter an integer: ";
GETINTEGER_DEFAULT_REPROMPT = "Illegal integer format. Try again.";
GETREAL_DEFAULT_PROMPT = "Enter a number: ";
GETREAL_DEFAULT_REPROMPT = "Illegal numeric format. Try again.";
GETPOSITIVEREAL_DEFAULT_PROMPT = "Enter a positive number: "
GETPOSITIVEREAL_DEFAULT_REPROMPT = "Illegal numeric format. Try again. "
GETYESORNO_DEFAULT_PROMPT = "Yes or No? ";
GETYESORNO_DEFAULT_REPROMPT = "Please type a word that starts with 'Y' or 'N': ";
DEFAULT_PROMPT = "> "
DEFAULT_REPROMPT = "Invalid input. Please try again. "


def get_integer(prompt=GETINTEGER_DEFAULT_PROMPT, reprompt=GETINTEGER_DEFAULT_REPROMPT):
    return get_fn_cond(
        lambda line: int(line.strip()),
        lambda _: True,
        prompt, reprompt
    )


def get_real(prompt=GETREAL_DEFAULT_PROMPT, reprompt=GETREAL_DEFAULT_REPROMPT):
    return get_fn_cond(
        lambda line: float(line.strip()),
        lambda _: True,
        prompt, reprompt
    )


def get_positive_real(prompt=GETPOSITIVEREAL_DEFAULT_PROMPT, reprompt=GETPOSITIVEREAL_DEFAULT_REPROMPT):
    return get_fn_cond(
        lambda line: float(line.strip()),
        lambda val: val > 0,
        prompt, reprompt
    )


def get_yes_or_no(prompt=GETYESORNO_DEFAULT_PROMPT, reprompt=GETYESORNO_DEFAULT_REPROMPT, default=None):
    result = get_fn_cond(
        lambda line: line[0].upper() if line else default,
        lambda val: val in ['Y', 'N'],
        prompt, reprompt
    )
    return result == 'Y'


def get_fn_cond(fn, pred, prompt=DEFAULT_PROMPT, reprompt=DEFAULT_REPROMPT):
    prompt = append_space(prompt)
    while True:
        line = input(prompt)
        try:
            out = fn(line)
        except Exception:
            pass
        else:
            if pred(out):
                return out
        if reprompt:
            print(append_space(reprompt))


def get_line(prompt=None):
    return input(append_space(prompt))


def append_space(prompt):
    """Adds a space to the end of the given string if none is present."""
    if not prompt.endswith(' '):
        return prompt + ' '
    return prompt
