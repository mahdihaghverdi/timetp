from collections import defaultdict
from datetime import timedelta
from typing import NamedTuple


class Token(NamedTuple):
    token: str
    amount: int


def tokenize(string: str) -> list[Token]:
    """Tokenize and return a two tuple of the time string

    >>> tokenize('4d5w')
    [('days', 4) ,('weeks', 5)]
    """
    letters = {
        'd': 'days',
        'w': 'weeks',
        'h': 'hours',
        'm': 'minutes',
        's': 'seconds'
    }

    string = string.lower()
    tokens: list[Token] = []
    if not string:
        return tokens

    if string[0].isalpha():
        raise SyntaxError(
            f"A pair cannot start with a letter.\n"
            f"  -> {string[0]!r} needs a number behind it."
        )

    digits = ''
    i = 0
    try:
        while string[i].isdigit():
            digits += string[i]
            i += 1
        letter = string[i]
    except IndexError:
        raise SyntaxError(
            f"A pair of  a number and a letter is needed.\n"
            f"  -> {digits!r} needs a letter after it."
        ) from None

    if letter not in list('dwhms'):
        raise SyntaxError("Time convention letters should be one of d, w, h, m or s.")

    tokens.append(Token(letters[letter], int(digits)))
    string = string[i + 1:]
    return tokens + tokenize(string)


def parse(tokens: list[Token]) -> timedelta:
    """Return a `timedelta` object out of the tokens"""
    _dict = defaultdict(int)
    for type_, number in tokens:
        _dict[type_] += number

    return timedelta(**_dict)
