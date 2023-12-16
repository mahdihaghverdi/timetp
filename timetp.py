from collections import defaultdict
from datetime import timedelta
from typing import NamedTuple, Literal

letters = {"d": "days", "w": "weeks", "h": "hours", "m": "minutes", "s": "seconds"}


class Token(NamedTuple):
    """Represent a token as a typed-namedtuple

    like: Token(token='weeks', amount=4)
    """

    token: Literal["days", "weeks", "hours", "minutes", "seconds"]
    amount: int


def tokenize(string: str) -> list[Token]:
    """Tokenize and return a list of `Token`s of the time string

    >>> tokenize('4d5w')
    [Token(token='days', amount=4), Token(token='weeks', amount=5)]
    """

    string = string.lower()
    if not string:
        return []

    tokens: list[Token] = []
    if string[0].isalpha():
        raise SyntaxError(
            f"A pair cannot start with a letter.\n"
            f"  i.e {string[0]!r} needs a number behind it."
        )

    digits = ""
    i = 0
    try:
        while string[i].isdigit():
            digits += string[i]
            i += 1
        letter = string[i]
    except IndexError:
        raise SyntaxError(
            f"A pair of a number and a letter is needed.\n"
            f"  i.e. {digits!r} needs a letter after it."
        ) from None

    if letter not in letters:
        raise SyntaxError(
            f"Time convention letters should be one of {letters.keys()!r}."
        )

    tokens.append(Token(letters[letter], int(digits)))
    string = string[i + 1 :]
    return tokens + tokenize(string)


def parse(tokens: list[Token]) -> timedelta:
    """Return a `timedelta` object out of the tokens"""
    _dict = defaultdict(int)
    for type_, number in tokens:
        _dict[type_] += number

    return timedelta(**_dict)
